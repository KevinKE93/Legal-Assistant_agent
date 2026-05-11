# PDF_RENDERING.md

本文件定义 Legal-Assistant_agent 的 PDF 渲染和版式质量规则。PDF 不能只是把 Markdown 原文塞进页面；必须先把 Markdown 结构渲染成可读版式，再导出 PDF。

## 1. 目标

最终 PDF 应当像一份专业法律备忘录或事项报告：

- 有封面、标题层级、目录、页眉页脚和页码。
- 表格必须是真正的表格，不得显示 Markdown 管道符。
- 引用、提示、核心判断等内容应使用区块、边框或浅色底展示。
- 争点关系、证据链、流程图应以表格、图片、SVG 或可读文本结构呈现。
- 中文字体必须可读，不能乱码、缺字、挤压或项目符号异常。

## 2. 渲染流程

生成 PDF 前必须按以下流程处理：

```text
Markdown 报告
→ 语义结构检查
→ 转换为 styled HTML、DOCX 或宿主支持的富文本格式
→ 使用 CSS/文档样式渲染表格、标题、提示框、页眉页脚
→ 导出 PDF
→ 质量检查
```

允许使用宿主环境可用的外部工具，例如浏览器打印、Pandoc、文档工具、HTML-to-PDF、DOCX-to-PDF 或其他可靠渲染能力。本仓库不内置脚本；工具选择由运行环境决定。

### 2A. 工具探测与降级顺序

生成 PDF 前，应先探测当前环境实际可用的渲染能力，不要假设某个工具存在：

1. 优先使用宿主提供的文档/PDF运行时、浏览器打印、Pandoc、WeasyPrint、wkhtmltopdf、DOCX-to-PDF 或其他可渲染表格和中文字体的工具。
2. 如果默认 Python/Node 环境缺少依赖，但宿主提供 bundled runtime，可以优先使用 bundled runtime 中已有的 PDF/文档库。
3. 若使用代码生成 PDF，必须使用支持 CJK 字体的字体文件，并把 Markdown 表格转换为真实表格。
4. 若 Mermaid、flowchart 或其他图形无法渲染为图片，应在 PDF 版删除源码并改写为关系表、编号链条或说明文字。
5. 如果没有任何可靠渲染能力，标记 `PDF status: blocked`，交付 Markdown，并说明下一步需要的转换工具。

不得为了生成文件而把 Markdown 纯文本直接写入 PDF；这类文件视为 PDF gate 未通过。

### 2B. 推荐执行路径

本仓库保持纯文档工作流，不内置渲染脚本。运行环境具备相应工具时，优先按以下顺序选择一种路径；只要任一步无法确认质量，就标记 `PDF status: blocked`，不要生成伪成功文件。

#### 路径 A：Markdown → styled HTML → 浏览器 PDF

适合需要保留 CSS 视觉系统、提示区块、宽表、流程图图片和中文字体的报告。推荐作为首选。

```sh
pandoc "<报告.md>" \
  --from gfm \
  --to html5 \
  --standalone \
  --toc \
  --metadata title="<报告标题>" \
  --css "<报告样式.css>" \
  --output "<报告.html>"
```

随后使用支持打印 CSS 的浏览器导出 PDF，例如 Chrome、Edge、Chromium、Playwright 或宿主浏览器打印能力。导出时应开启背景图形、A4 纸张、默认或自定义页边距，并确认中文字体可用。

如使用 headless Chromium，命令形态通常类似：

```sh
chromium --headless --disable-gpu \
  --print-to-pdf="<报告.pdf>" \
  "file:///<报告.html>"
```

实际浏览器命令因系统而异。若找不到浏览器可执行文件，不要改用纯文本 PDF；改为 blocked。

#### 路径 B：Markdown → DOCX → PDF

适合宿主具备可靠文档工具、需要更强分页控制或后续人工编辑的场景。

```sh
pandoc "<报告.md>" \
  --from gfm \
  --to docx \
  --reference-doc "<参考样式.docx>" \
  --output "<报告.docx>"
```

再用宿主文档工具导出 PDF。导出后必须检查表格、标题、中文字体和页码；不能因为 DOCX 生成成功就认为 PDF gate 通过。

#### 路径 C：Markdown → XeLaTeX PDF

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

#### 路径 D：Markdown → HTML → WeasyPrint / wkhtmltopdf

适合服务器环境或无图形浏览器环境。

```sh
pandoc "<报告.md>" --from gfm --to html5 --standalone --toc --css "<报告样式.css>" --output "<报告.html>"
weasyprint "<报告.html>" "<报告.pdf>"
```

或：

```sh
wkhtmltopdf --enable-local-file-access "<报告.html>" "<报告.pdf>"
```

使用该路径时尤其要检查中文字体、表格分页、CSS 支持程度和图形嵌入。

### 2C. 阻塞判定

以下情况应立即停止 PDF 交付并写入 `plan.md`：

| 阻塞原因 | PDF status | Report status 影响 | 下一步 |
|---|---|---|---|
| 缺少可用渲染工具 | blocked | 若其他 gate 通过，可为 `complete_except_pdf` | 安装或启用浏览器、Pandoc、WeasyPrint、DOCX-to-PDF 等工具 |
| 可生成文件但中文乱码或字体缺失 | blocked | 若其他 gate 通过，可为 `complete_except_pdf` | 指定 CJK 字体或改用浏览器/DOCX 路径 |
| 表格、Mermaid、LaTeX 或 HTML 源码残留 | blocked | 若其他 gate 通过，可为 `complete_except_pdf` | 改写为真实表格、图片、关系表或计算表后重渲染 |
| Markdown 已更新但 PDF 未重渲染 | blocked | 不得沿用旧 PDF 状态 | 用同一 Markdown 重新生成 PDF |
| Source Gate 或 Evidence Gate 同时 blocked | blocked | 报告通常为 `draft` 或 `incomplete`，不是 `complete_except_pdf` | 先完成来源/证据核验或明确阶段性限制 |

`complete_except_pdf` 只能用于“内容、来源、证据、报告和会话 gate 均通过，唯独 PDF 渲染环境或质量检查失败”的情况。

## 3. 禁止的 PDF 交付

以下情况必须标记为 `PDF status: blocked`，不能声称 PDF 已完成：

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

- 表头使用浅色底和加粗。
- 单元格允许自动换行。
- 宽表可拆分为多张窄表，或改成卡片式列表。
- 金额、概率、时间线、证据链、争点矩阵应优先表格化。

### 区块

可使用以下区块：

- 核心判断。
- 最大风险。
- 待补材料。
- 引用风险。
- 下一步行动。

### 4A. 视觉系统

推荐使用克制、清晰、专业的法律备忘录风格，不使用夸张装饰、法律锤/天平等陈词滥调图形，也不使用深色背景或高饱和渐变。

设计基调：

| 项目 | 建议 |
|---|---|
| 纸张背景 | `#F8FAFC` 页面底，正文卡片/纸张使用 `#FFFFFF` |
| 主文字 | `#102033` 深蓝黑 |
| 次级文字 | `#53657A` 灰蓝 |
| 边框 | `#D8E0EA` 浅灰蓝 |
| 表头底色 | `#EEF4FA` |
| 主强调色 | `#1E4A8A` 稳重蓝 |
| 风险强调 | `#B7791F` 琥珀色，仅用于风险、待核验、注意事项 |
| 已核验强调 | `#2F7D57` 绿色，仅用于已核验来源或完成状态 |
| 字体 | 中文优先 `PingFang SC`、`Source Han Sans SC`、`Noto Sans CJK SC`、`Microsoft YaHei`、`Heiti SC` 等现代无衬线字体；标题和正文保持同一字体体系 |

排版原则：

- 一页只承担一个主要任务：封面、目录、摘要、表格、争点关系、附录不要挤在一起。
- 标题层级最多使用 3 级；第 4 级以后改用加粗短句或表格字段。
- 正文段落控制在 3-6 行，长段落拆成小标题、表格或清单。
- 表格不追求“一张表装下所有问题”；超过 6 列的宽表优先拆分。
- 关键判断、最大风险、待补材料和引用风险必须用醒目的提示区块，不埋在正文中。

### 4B. 推荐 CSS 样式

使用 HTML/浏览器/Pandoc/WeasyPrint 等路径渲染时，可按以下样式实现。不同工具语法可调整，但视觉目标应保持一致。

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
  --page-bg: #f8fafc;
  --ink: #102033;
  --muted: #53657a;
  --line: #d8e0ea;
  --soft: #eef4fa;
  --brand: #1e4a8a;
  --risk: #b7791f;
  --ok: #2f7d57;
  --danger: #9f2d2d;
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
  font-size: 25pt;
  line-height: 1.18;
  margin: 0 0 16pt;
  letter-spacing: 0;
}

h2 {
  font-size: 16pt;
  margin: 22pt 0 9pt;
  padding-bottom: 5pt;
  border-bottom: 1px solid var(--line);
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
  border-left: 4px solid var(--brand);
  background: #f5f8fc;
  border-radius: 6px;
}

.callout.core {
  border-left-color: var(--brand);
}

.callout.risk {
  border-left-color: var(--risk);
  background: #fff8eb;
}

.callout.source {
  border-left-color: var(--ok);
  background: #f1f8f4;
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

.cover {
  min-height: 230mm;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.cover-meta {
  color: var(--muted);
  font-size: 10pt;
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
| 表格 | 真实表格，表头浅色底，单元格自动换行 | 显示 `|---|---|` |
| 引用块 | 提示区块或判断框 | 与普通正文无区分 |
| 代码块 | 仅用于真实代码或命令；报告正文不应出现 Mermaid 源码 | 把流程图源码放进 PDF |
| 长列表 | 分组列表、步骤表或行动清单 | 连续 20 行项目符号 |
| 争点关系 | 流程图、关系表或编号链条 | 未渲染的 Mermaid 文本 |
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
- 无法渲染时，改写为“争点关系表”或编号链条。
- 不得把 Mermaid 源码直接放入 PDF 正文。

推荐 Mermaid 视觉配置：

```yaml
theme: base
themeVariables:
  fontFamily: "PingFang SC, Source Han Sans SC, Noto Sans CJK SC, Inter, sans-serif"
  primaryColor: "#EEF4FA"
  primaryTextColor: "#102033"
  primaryBorderColor: "#1E4A8A"
  lineColor: "#587FA6"
  secondaryColor: "#FFF8EB"
  secondaryTextColor: "#102033"
  secondaryBorderColor: "#B7791F"
  tertiaryColor: "#F1F8F4"
  tertiaryTextColor: "#102033"
  tertiaryBorderColor: "#2F7D57"
  noteBkgColor: "#FFF8EB"
  noteTextColor: "#102033"
```

流程图规范：

- 节点文字使用短句，不超过 18 个中文字符或 8 个英文单词。
- 同一图只表达一种关系：争点依赖、程序路径、证据链或策略分支，不混在一张图里。
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

若任一关键项不通过，在 `plan.md` 或内部交付记录以及会话回复中说明 PDF blocked，并交付 Markdown 作为主文件。

### 6A. 可执行检查建议

环境允许时，至少执行以下检查中的若干项，并把结果写入报告质量检查表或 `plan.md`：

- `file <报告.pdf>` 或等价方式确认文件确为 PDF。
- 检查 PDF 文件大小非空，页数合理。
- 使用文本抽取工具或人工检查确认中文可读。
- 搜索抽取文本中是否残留 `|---`、`---|`、代码围栏、`flowchart`、`mermaid`、`<table>`、`<html>`、未渲染 `$...$`、`\\(...\\)`、`\\[...\\]` 等源码痕迹。
- 对宽表格，必要时拆表、压缩列、改成卡片式列表或放入附录。
- 记录 PDF 与 Markdown 的生成时间或同源状态，避免旧 PDF 搭配新 Markdown。

## 7. 最低交付要求

最终回复不能只说“PDF 已生成”。必须说明：

- Markdown 报告路径。
- PDF 路径或 blocked 原因。
- PDF 是否经过基础可读性检查。
- 如果 blocked，下一步应使用哪类渲染工具转换。
