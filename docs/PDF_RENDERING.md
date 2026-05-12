# PDF_RENDERING.md

本文件定义 Legal-Assistant_agent 的按需 PDF 渲染和版式质量规则。PDF 不是默认输出；只有用户明确要求 PDF、可下载 PDF 报告或阶段交付 PDF 时，才进入本文件的渲染流程。PDF 不能只是把 Markdown 原文塞进页面；必须先把 Markdown 结构渲染成可读版式，再导出 PDF。

## 1. 目标

PDF 报告应当像一份法律备忘录或事项报告：

- 有封面、标题层级、目录、页眉页脚和页码。
- 表格必须是真正的表格，不得显示 Markdown 管道符。
- 引用、提示、核心判断等内容应使用区块、边框或浅色底展示。
- 争议焦点关系、证据链、流程图应以表格、图片、SVG 或可读文本结构呈现。
- 中文字体必须可读，不能乱码、缺字、挤压或项目符号异常。

## 2. 渲染流程

用户已明确要求 PDF 时，生成 PDF 前必须按以下流程处理：

```text
Markdown 报告
→ 语义结构检查
→ 转换为 DOCX、XeLaTeX、PDF-native 文档对象，或由无浏览器 HTML-to-PDF 引擎处理的 styled HTML
→ 使用 CSS/文档样式渲染表格、标题、提示框、页眉页脚
→ 导出 PDF
→ 质量检查
```

允许使用宿主环境可用的文档 / PDF 工具，例如 Pandoc、XeLaTeX、文档工具、DOCX-to-PDF、WeasyPrint、wkhtmltopdf、ReportLab、PDFKit、根目录可选渲染器或其他可靠渲染能力。工具选择由运行环境决定。PDF 生成默认不得依赖外部浏览器、Chrome headless、Chromium、Edge、Playwright 浏览器或浏览器打印。

### 2A. 工具探测与降级顺序

用户已请求 PDF 后，应先探测当前环境实际可用的渲染能力，不要假设某个工具存在：

1. 优先使用宿主提供的文档 / PDF 运行时、Pandoc、XeLaTeX、WeasyPrint、wkhtmltopdf、DOCX-to-PDF、ReportLab、PDFKit 或其他可渲染表格和中文字体的非浏览器工具。
2. 如果默认 Python/Node 环境缺少依赖，但宿主提供 bundled runtime，可以优先使用 bundled runtime 中已有的 PDF/文档库。
3. 若使用代码生成 PDF，必须使用支持 CJK 字体的字体文件，并把 Markdown 表格转换为真实表格。
4. 若 Mermaid、flowchart 或其他图形无法渲染为图片，应在 PDF 版删除源码并改写为关系表、编号链条或说明文字。
5. 如果没有任何可靠渲染能力，标记 `PDF status: blocked`，交付 Markdown，并说明下一步需要的转换工具。

如果用户未请求 PDF，`PDF status` 应写为 `not requested`，`PDF Gate` 写为 `skipped / not requested`，不得标记 blocked。

不得为了生成文件而把 Markdown 纯文本直接写入 PDF；这类文件视为 PDF gate 未通过。

### 2B. 推荐执行路径

本仓库保持纯文档工作流，根目录渲染器仅作为可选辅助工具。运行环境具备相应工具时，优先按以下顺序选择一种路径；只要任一步无法确认质量，就标记 `PDF status: blocked`，不要生成伪成功文件。

#### 路径 A：Markdown → DOCX → PDF

适合需要稳定分页、中文字体、后续人工编辑或正式交付的场景。推荐作为首选。

```sh
pandoc "<报告.md>" \
  --from gfm \
  --to docx \
  --reference-doc "<参考样式.docx>" \
  --output "<报告.docx>"
```

再用宿主文档工具或 DOCX-to-PDF 引擎导出 PDF。导出后必须检查表格、标题、中文字体和页码；不能因为 DOCX 生成成功就认为 PDF gate 通过。

#### 路径 B：Markdown → XeLaTeX PDF

适合法律研究报告、公式较多、表格不太宽的文档。对复杂 CSS、提示卡片和流程图支持较弱。

```sh
pandoc "<报告.md>" \
  --from gfm \
  --pdf-engine=xelatex \
  -V CJKmainfont="PingFang SC" \
  -V mainfont="Inter" \
  -V geometry:margin=22mm \
  --toc \
  --output "<报告.pdf>"
```

若中文字体不可用、宽表溢出或提示区块丢失，改用路径 A 或标记 blocked。

#### 路径 C：Markdown → styled HTML → WeasyPrint / wkhtmltopdf

适合需要 CSS 视觉系统但不能使用外部浏览器的环境。WeasyPrint 和 wkhtmltopdf 属于无浏览器 HTML-to-PDF 引擎；不得替换为 Chrome、Chromium、Edge、Playwright 或浏览器打印。

默认样式以根目录 `assets/legal-report.css` 为准，并以 `assets/legal-report-style-reference.png` 作为视觉参考。该 CSS 定义现代白底卡片、蓝/紫/青强调色、双语标题、编号胶囊、浅色数据表、指标卡、时间线/证据/行动模块和可打印 A4 间距。渲染时应优先引用或内联根目录样式，不要每次把样式和脚本复制到 `work/` 事项文件夹。

```sh
pandoc "<报告.md>" --from gfm --to html5 --standalone --toc --css "<报告样式.css>" --output "<报告.html>"
weasyprint "<报告.html>" "<报告.pdf>"
```

或：

```sh
wkhtmltopdf --enable-local-file-access "<报告.html>" "<报告.pdf>"
```

使用该路径时尤其要检查中文字体、表格分页、CSS 支持程度和图形嵌入。

#### 路径 D：Markdown → PDF-native 文档对象 → PDF

适合宿主没有 Pandoc、LaTeX 或 DOCX-to-PDF，但有可用 PDF 生成库的环境，例如 ReportLab、PDFKit、pdfmake、Prawn 或宿主文档运行时。

本仓库提供一个可选的根目录渲染器，适合“输入目录 = 输出目录”的事项文件夹用法：

```sh
python tools/render_report_pdf.py "work/<date>_<事项名>"
```

默认自动查找该目录下的 Markdown 报告，并在同一目录生成 PDF 报告。若报告文件名特殊，可指定：

```sh
python tools/render_report_pdf.py "work/<date>_<事项名>" --report "<报告.md>"
```

该路径依赖 `reportlab`。若系统默认 Python 缺少依赖，应使用宿主或 Codex 提供的文档/PDF bundled Python 运行时，或在执行脚本的 Python 环境中安装 `reportlab`。

该脚本属于可选辅助工具，不应复制到事项文件夹；事项文件夹只保留报告 Markdown、PDF、工作底稿和必要附件。

要求：

- 先解析 Markdown 结构，不得把 Markdown 原文逐行写入 PDF。
- 标题、段落、表格、引用块、列表和公式必须转换为 PDF-native 对象。
- Markdown 表格必须转换为真实表格或卡片式表格。
- Mermaid/flowchart 必须转换为图片、关系表或编号链条。
- 中文字体必须明确注册或使用宿主可用 CJK 字体。

若只能做到“把 Markdown 文本塞进 PDF”，必须标记 blocked。

#### 禁用路径：外部浏览器 PDF

默认禁止使用以下方式生成 PDF：

- Chrome headless / Chromium / Edge headless。
- Playwright、Puppeteer 或 Selenium 启动的浏览器。
- 系统浏览器打印、浏览器“另存为 PDF”。
- 任何需要额外下载浏览器二进制的路径。

只有用户明确要求或允许使用浏览器渲染时，才可把浏览器作为 fallback；仍必须通过 PDF Gate 质量检查。

### 2C. 阻塞判定

用户已请求 PDF 后，以下情况应立即停止 PDF 交付并写入 `plan.md`：

| 阻塞原因 | PDF status | Report status 影响 | 下一步 |
|---|---|---|---|
| 缺少可用渲染工具 | blocked | 若其他 gate 通过，可为 `complete_except_pdf` | 安装或启用 Pandoc、XeLaTeX、WeasyPrint、DOCX-to-PDF、ReportLab/PDFKit 等非浏览器工具 |
| 可生成文件但中文乱码或字体缺失 | blocked | 若其他 gate 通过，可为 `complete_except_pdf` | 指定 CJK 字体或改用 DOCX、XeLaTeX、WeasyPrint、PDF-native 路径 |
| 表格、Mermaid、LaTeX 或 HTML 源码残留 | blocked | 若其他 gate 通过，可为 `complete_except_pdf` | 改写为真实表格、图片、关系表或计算表后重渲染 |
| Markdown 已更新但 PDF 未重渲染 | blocked | 不得沿用旧 PDF 状态 | 用同一 Markdown 重新生成 PDF |
| Source Gate 或 Evidence Gate 同时 blocked | blocked | 报告通常为 `draft` 或 `incomplete`，不是 `complete_except_pdf` | 先完成来源/证据核验或明确阶段性限制 |

`complete_except_pdf` 只能用于“用户已请求 PDF，且内容、来源、证据、报告和会话 gate 均通过，唯独 PDF 渲染环境或质量检查失败”的情况。未请求 PDF 时不使用 `complete_except_pdf`。

## 3. 禁止的 PDF 交付

用户已请求 PDF 时，以下情况必须标记为 `PDF status: blocked`，不能声称 PDF 已完成：

- PDF 中出现 Markdown 表格管道符：`|---|---|`。
- Mermaid、flowchart、HTML 或 Markdown 代码块以原始文本形式出现在正文。
- 标题、表格、列表没有被渲染成版式结构。
- 中文乱码、缺字、字体过小、行距过密或表格严重溢出。
- 页眉页脚、页码、目录或章节层级明显错乱。
- PDF 内容与 Markdown 报告不一致。

## 4. 推荐版式

### 页面

- A4 纵向。
- 正文页边距约 18-24mm。
- 中文字体优先使用 PingFang SC、Source Han Sans SC、Noto Sans CJK SC、Microsoft YaHei、Heiti SC 或宿主可用的现代无衬线中文字体；避免使用传统衬线中文字体作为默认正文或标题字体。
- 正文字号建议 10.5-12pt，行距 1.45-1.7。
- 页脚保留页码，长报告可加简短页眉。

### 封面

封面应包含：

- 报告标题。
- 副标题或用途说明。
- 生成日期。
- 事项类型。
- 重要提示。
- “核心判断”摘要框。

### 表格

- 表头使用浅蓝或浅青底色、深色文字和加粗；若工具限制，也必须使用清晰表头底色和边界线。
- 单元格允许自动换行。
- 宽表可拆分为多张窄表，或改成卡片式列表。
- 金额区间、风险判断、时间线、证据链、争议焦点矩阵应优先表格化。

### 区块

可使用以下区块：

- 核心判断。
- 最大风险。
- 待补材料。
- 引用风险。
- 下一步行动。

### 4A. 视觉系统

PDF 视觉系统以 `assets/legal-report-style-reference.png` 和 `assets/legal-report.css` 为 canonical 样式：可信、清晰、高效、数据驱动、一致规范。整体应像面向律师、当事人和决策层的现代法律分析产品报告，而不是普通 Markdown 打印稿或传统备忘录。允许使用克制的徽标、编号、卡片、指标和浅色抽象背景；不得使用夸张法律锤/天平、深色整页正文或高饱和大面积渐变。

设计基调：

| 项目 | 建议 |
|---|---|
| Ink / 主文字 | `#101936` 深蓝黑，用于标题、正文和关键判断 |
| Primary / 主强调 | `#1677FF` 明亮蓝，用于编号胶囊、章节强调、链接和主线 |
| Purple / 辅助强调 | `#635BFF` 蓝紫色，用于封面视觉、目录编号和模块渐变 |
| Cyan / 数据强调 | `#14B8A6` 青绿色，用于证据强度、数据驱动、已核验状态 |
| Steel / 次级文字 | `#64748B` 灰蓝，用于页码、元信息、图例和弱提示 |
| Page / 页面底 | `#F6FAFF` 极浅蓝白，用于页面背景 |
| Card / 卡片底 | `#FFFFFF` 用于章节、摘要、数据、证据、行动模块 |
| Border / 分割线 | `#DDE8F7` 浅蓝灰，用于表格、卡片、页眉页脚分割 |
| Warning / 风险强调 | `#F59E0B` 琥珀色，仅用于风险、待核验、重要提示 |
| 标题字体 | 中文优先现代黑体，例如 `PingFang SC`、`Source Han Sans SC`、`Noto Sans CJK SC` |
| 正文字体 | 中文优先 `PingFang SC`、`Source Han Sans SC`、`Noto Sans CJK SC`、`Microsoft YaHei`、`Heiti SC`；英文可用 `Inter` |

版式组件：

| 组件 | 视觉要求 | 内容要求 |
|---|---|---|
| 封面 | 白底主卡片，左侧报告标题与元信息，右侧蓝紫视觉面板；使用品牌徽标、双语副标题和模块化信息区 | 必须能一眼识别报告主题、状态、日期、版本和限制 |
| 目录 | `01/02/03` 编号胶囊 + 章节卡片 + 页码/序号 | 长报告必须生成可扫描目录页，避免普通长列表 |
| 执行摘要 | 使用卡片、编号结论、关键指标和风险概览，而不是纯段落 | 每条结论绑定依据、证据状态、风险和下一步 |
| 事实与证据 | 使用时间线、证据清单、强度条或状态字段 | 证据强弱和缺口必须可视化或表格化 |
| 争议焦点矩阵 | 浅蓝表头、浅色交替行、固定列宽、可重复表头 | 超过 6 列优先拆分或降级为卡片式窄表 |
| 法律依据与论证 | 法律依据、论证路径、适用边界分区展示 | 不把法条和结论挤成单段 |
| 行动清单 | 表格 + 进度/状态 + 风险提示 + 附件/材料模块 | 行动必须有目的、责任方、触发条件或产物 |
| 交付检查 | 使用小型清单或状态表 | 明确 PDF 可读、表格已渲染、来源列明、风险披露 |

排版原则：

- 一页只承担一个主要任务：封面、目录、摘要、表格、争议焦点关系、附录不要挤在一起。
- 标题层级最多使用 3 级；第 4 级以后改用加粗短句或表格字段。
- 正文段落控制在 3-6 行，长段落拆成小标题、表格或清单。
- 表格不追求“一张表装下所有问题”；超过 6 列的宽表优先拆分。
- 关键判断、最大风险、待补材料和引用风险必须用醒目的提示区块，不埋在正文中。
- 页眉页脚保持轻量：页眉放报告类型或章节提示，页脚放页码、保密/草稿提示或事项简称。
- 双语不是逐句翻译全文，而是关键标题、封面、指标标签、交付检查等高层导航保持中英并列。

### 4B. 推荐 CSS 样式

使用 styled HTML、Pandoc、WeasyPrint、wkhtmltopdf 或其他无浏览器 HTML-to-PDF 路径渲染时，可按以下样式实现。不同工具语法可调整，但视觉目标应保持一致。

```css
@page {
  size: A4;
  margin: 20mm 18mm 22mm 18mm;
  @bottom-center {
    content: counter(page);
    color: #7a8796;
    font-size: 9pt;
  }
}

:root {
  --paper: #ffffff;
  --page-bg: #f6faff;
  --ink: #101936;
  --muted: #64748b;
  --line: #dde8f7;
  --soft: #f1f7ff;
  --brand: #1677ff;
  --purple: #635bff;
  --cyan: #14b8a6;
  --risk: #f59e0b;
  --ok: #10b981;
  --danger: #a33a35;
}

body {
  margin: 0;
  background: var(--page-bg);
  color: var(--ink);
  font-family: "Inter", "PingFang SC", "Source Han Sans SC", "Noto Sans CJK SC", "Microsoft YaHei", "Heiti SC", sans-serif;
  font-size: 11pt;
  line-height: 1.62;
}

.page, main {
  background: var(--paper);
}

h1, h2, h3 {
  color: var(--ink);
  break-after: avoid;
  page-break-after: avoid;
}

h1 {
  font-family: "Inter", "PingFang SC", "Source Han Sans SC", "Noto Sans CJK SC", sans-serif;
  font-size: 26pt;
  line-height: 1.18;
  margin: 0 0 16pt;
  letter-spacing: 0;
}

h2 {
  font-size: 15pt;
  margin: 22pt 0 10pt;
  padding: 8pt 10pt;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--paper);
}

h2::before {
  content: "";
  display: inline-block;
  width: 18pt;
  height: 18pt;
  margin-right: 7pt;
  vertical-align: middle;
  border-radius: 6px;
  background: linear-gradient(135deg, var(--brand), var(--purple));
}

h3 {
  font-size: 12.5pt;
  margin: 14pt 0 6pt;
}

p {
  margin: 0 0 8pt;
}

a {
  color: var(--brand);
  text-decoration: none;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 10pt 0 14pt;
  font-size: 9.5pt;
  table-layout: fixed;
  break-inside: auto;
}

thead {
  display: table-header-group;
}

th {
  background: var(--soft);
  color: var(--ink);
  font-weight: 700;
}

th, td {
  border: 1px solid var(--line);
  padding: 7pt 8pt;
  vertical-align: top;
  word-break: break-word;
}

tr {
  break-inside: avoid;
}

blockquote,
.callout {
  margin: 12pt 0;
  padding: 10pt 12pt;
  border: 1px solid var(--line);
  border-left: 4px solid var(--brand);
  background: var(--paper);
  border-radius: 8px;
}

.callout.core {
  border-left-color: var(--brand);
}

.callout.risk {
  border-left-color: var(--risk);
  background: #fff8eb;
}

.callout.source {
  border-left-color: var(--cyan);
  background: #ecfeff;
}

.callout.danger {
  border-left-color: var(--danger);
  background: #fff3f3;
}

code, pre {
  font-family: "SFMono-Regular", "Menlo", "Consolas", monospace;
}

pre {
  white-space: pre-wrap;
  background: #f3f6fa;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 10pt;
}

.report-cover {
  min-height: 252mm;
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 12mm;
  border: 1px solid var(--line);
  background: var(--paper);
  border-radius: 8px;
  padding: 22mm 18mm;
  break-after: page;
}

.report-cover__body {
  padding: 0;
}

.report-cover__visual {
  border-radius: 8px;
  background: linear-gradient(135deg, var(--brand), var(--purple));
  min-height: 110mm;
}

.cover-meta,
.metric-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8pt;
}

.metric-grid {
  grid-template-columns: repeat(4, 1fr);
}

.metric-card {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #ffffff;
  padding: 8pt 9pt;
}

.toc a {
  color: var(--ink);
}
```

### 4C. Markdown 到版式的转换规则

Markdown 源文档应当是语义清晰的报告，不是渲染后的视觉稿。渲染时按以下规则转换：

| Markdown 内容 | PDF 中应呈现为 | 禁止 |
|---|---|---|
| `#` 一级标题 | 封面标题或章节首页标题 | 每页重复超大标题 |
| `##` 二级标题 | 主要章节标题 | 标题与正文挤在一起 |
| 表格 | 真实表格，浅蓝/浅青表头或清晰表头底色，单元格自动换行 | 显示 `|---|---|` |
| 引用块 | 提示区块或判断框 | 与普通正文无区分 |
| 代码块 | 仅用于真实代码或命令；报告正文不应出现 Mermaid 源码 | 把流程图源码放进 PDF |
| 长列表 | 分组列表、步骤表或行动清单 | 连续 20 行项目符号 |
| 争议焦点关系 | 流程图、关系表或编号链条 | 未渲染的 Mermaid 文本 |
| 执行摘要 | 结论卡片、关键指标、风险提示区块 | 只有长段落 |
| 来源列表 | 参考文献表、脚注或来源卡片 | 只写“已检索”不列来源 |
| 证据链 | 时间线、证据矩阵或节点链路图 | 证据与证明对象分离 |
| 金额计算 | 计算表、公式块、假设说明 | 只有最终金额没有计算过程 |
| 行动清单 | 优先级表、责任方、触发条件和产物 | 泛泛建议 |
| 图片或附件 | 图注、来源、说明和引用风险 | 无来源图片 |

其他类型内容按相同原则处理：先判断内容在法律报告中的功能，再选择最易读的版式。若无法可靠渲染，优先改写成表格、编号链条或短段落，不保留源码。

### 4D. LaTeX 公式与计算式

报告可能出现赔偿金额、利息、违约金、加班费、股权比例、折现、概率或税费等计算式。若 Markdown 中包含 LaTeX 公式，应按以下规则处理：

| 公式来源 | PDF 中应呈现为 | 禁止 |
|---|---|---|
| 行内公式 `$...$` 或 `\\(...\\)` | 行内数学公式，字号与正文协调 | 原样显示 `$`、反斜杠或未闭合公式 |
| 块级公式 `$$...$$` 或 `\\[...\\]` | 独立公式块，可编号，可附文字解释 | 公式挤在正文中或换行错乱 |
| 金额/补偿计算 | “假设 + 公式 + 计算表 + 小结”组合 | 只有公式没有变量解释 |
| 多步骤计算 | 分步表格，每一步列变量、来源、计算和风险 | 一个长公式承担全部逻辑 |

渲染要求：

- 优先使用 KaTeX、MathJax、Pandoc math、LaTeX-to-SVG/PNG 或宿主支持的数学公式渲染能力。
- 公式字体应与正文协调，变量、数字和中文说明都必须可读。
- 每个公式必须解释变量含义、数据来源、证据状态和不确定性。
- 公式不能替代证明责任分析；金额计算仍需绑定事实依据和证据状态。
- 若当前环境无法渲染 LaTeX，必须改写为普通文本公式或计算表，并在 PDF 中删除原始 LaTeX 源码。

公式 CSS 建议：

```css
.equation,
.math-block {
  margin: 12pt 0;
  padding: 10pt 12pt;
  background: #f8fafc;
  border: 1px solid var(--line);
  border-radius: 6px;
  overflow-wrap: anywhere;
}

.calculation-table td,
.calculation-table th {
  text-align: left;
}

.calculation-note {
  color: var(--muted);
  font-size: 9.5pt;
}
```

## 5. 图形和流程图

如果报告包含 Mermaid、流程图或关系图：

- 优先渲染为 SVG/PNG 后嵌入 PDF。
- 无法渲染时，改写为“争议焦点关系表”或编号链条。
- 不得把 Mermaid 源码直接放入 PDF 正文。

推荐 Mermaid 视觉配置：

```yaml
theme: base
themeVariables:
  fontFamily: "PingFang SC, Source Han Sans SC, Noto Sans CJK SC, Inter, sans-serif"
  primaryColor: "#F1F7FF"
  primaryTextColor: "#101936"
  primaryBorderColor: "#1677FF"
  lineColor: "#64748B"
  secondaryColor: "#F4F2FF"
  secondaryTextColor: "#101936"
  secondaryBorderColor: "#635BFF"
  tertiaryColor: "#ECFEFF"
  tertiaryTextColor: "#101936"
  tertiaryBorderColor: "#14B8A6"
  noteBkgColor: "#FFF7E6"
  noteTextColor: "#101936"
```

流程图规范：

- 节点文字使用短句，不超过 18 个中文字符或 8 个英文单词。
- 同一图只表达一种关系：争议焦点依赖、程序路径、证据链或策略分支，不混在一张图里。
- 使用颜色表达状态：蓝色为中性主线，琥珀色为风险/待核验，绿色为已核验或已完成。
- 宽图应横向排布并在 PDF 中独立成页；窄图可嵌入正文。
- 如果生成 SVG/PNG 后文字过小、截断或乱码，必须改成关系表。

## 6. 质量检查

PDF 生成后至少检查：

| 检查项 | 通过条件 |
|---|---|
| 文件存在 | PDF 路径真实存在且大小非空 |
| 中文可读 | 中文、英文、数字正常显示 |
| 表格渲染 | Markdown 表格已变成真实表格 |
| 代码残留 | 无未渲染 Mermaid、HTML、Markdown 代码 |
| 公式渲染 | LaTeX 公式已渲染，或已改写为普通文本公式/计算表 |
| 页面结构 | 封面、目录、正文、附录层级清晰 |
| 长表处理 | 宽表没有严重截断或溢出 |
| 内容一致 | PDF 与 Markdown 报告同源 |

若任一关键项不通过，在 `plan.md` 或内部交付记录以及会话回复中说明 PDF blocked，并交付 Markdown 作为主文件。若用户未请求 PDF，不执行本检查，状态写为 `not requested`。

### 6A. 可执行检查建议

环境允许时，至少执行以下检查中的若干项，并把结果写入报告质量检查表或 `plan.md`：

- `file <报告.pdf>` 或等价方式确认文件确为 PDF。
- 检查 PDF 文件大小非空，页数合理。
- 使用文本抽取工具或人工检查确认中文可读。
- 搜索抽取文本中是否残留 `|---`、`---|`、代码围栏、`flowchart`、`mermaid`、`<table>`、`<html>`、未渲染 `$...$`、`\\(...\\)`、`\\[...\\]` 等源码痕迹。
- 对宽表格，必要时拆表、压缩列、改成卡片式列表或放入附录。
- 记录 PDF 报告与 Markdown 报告的生成时间或同源状态，避免旧 PDF 报告搭配新 Markdown 报告。

## 7. 最低交付要求

用户已请求 PDF 时，会话回复不能只说“PDF 已生成”。必须说明：

- Markdown 报告路径。
- PDF 路径或 blocked 原因。
- PDF 是否经过基础可读性检查。
- 如果 blocked，下一步应使用哪类渲染工具转换。

用户未请求 PDF 时，会话回复应以实质汇总结论为主，并提示：“如需 PDF 报告，可以继续提出。”
