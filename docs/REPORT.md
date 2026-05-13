# REPORT.md

本文件定义 Legal-Assistant_agent 的报告规则。报告只在用户要求报告文件、阶段交付或归档时生成；普通分析默认只给会话结论。

## 1. 触发条件

生成或更新 Markdown 报告的条件：

- 用户明确要求“报告、总结文件、Markdown 文件、阶段交付、归档”。
- 已有 `matter.md` 或目标交付文件，需要整理成可交付报告。
- Deep Case 已完成阶段性案件分析，需要对外呈现。

用户只说“分析一下”时，不自动生成报告文件。PDF 只在用户明确要求 PDF、可下载 PDF 或阶段交付 PDF 时触发。

## 2. 输入文件

按存在情况读取，不因缺少某个内部文件而强制生成：

```text
matter.md
sources.md
timeline.md
evidence.md
case_dashboard.md
consultation_note.md
case_package.md
pleading_framework.md
hearing_playbook.md
review_delta.md
drafts.md
hearing.md
negotiation.md
contract.md
clause_review.md
term_sheet.md
contract_draft.md
```

`plan.md`、`case.md`、`skill_outputs.md` 仅在它们已经存在或用户要求审计轨迹时读取。报告不得为了补齐这些文件而额外生成。

## 3. 写作原则

- 结论先行，依据紧随，限制明确，动作落地。
- 区分事实、证据、推断、法律评价和策略建议。
- 每个关键判断都说明材料依据、来源状态、适用条件、对方可能反驳和当前不确定性。
- 不把用户陈述写成已证明事实。
- 不把法律来源堆成链接清单；只保留能服务本事项的规则和适用边界。
- 金额区间、结果倾向和谈判锚点必须绑定计算口径、证据状态和替代情形。

## 4. 推荐结构

```markdown
# <本地化主题>报告

## 1. 执行摘要

## 2. 事项范围与材料限制

## 3. 关键事实或合同结构

## 4. 核心争议焦点或条款风险

## 5. 证据与来源状态

## 6. 法律分析或规则适用边界

## 7. 风险评估

## 8. 行动建议

## 9. 待补材料
```

合同审查、合同起草、法律研究、文书草稿可按目标交付物调整章节，不必套用案件报告结构。

## 5. Deep Case 报告增强

Deep Case 的报告不是 `matter.md` 的短摘要。只要事项文件夹中已存在案件工作台或深度文件，报告必须把可用内容吸收到实体分析中：

| 已有材料 | 报告中的去向 |
|---|---|
| `case_dashboard.md` / `consultation_note.md` | 案件地图、请求与抗辩、程序阶段、材料限制 |
| `timeline.md` / `evidence.md` | 关键时间线、证明对象、证据强弱和缺口 |
| `sources.md` | 已核验规则、适用边界和引用风险 |
| `case_package.md` / `pleading_framework.md` | 要件、证明责任、请求或抗辩结构 |
| `hearing_playbook.md` | 质证、发问、裁判关注点和庭审行动 |
| `review_delta.md` | 新材料改变了什么、未改变什么 |

Deep Case 报告至少要呈现：

- 争议焦点之间的关系，而不是只列点。
- 用户主张、对方可能抗辩和裁判者关注点。
- 事实链、证据链、规则链、策略链如何互相支撑或互相削弱。
- 最大风险、关键证据缺口、下一步优先动作。

报告可以压缩重复内容，但不得遗漏会改变结论的前序发现。已有文件缺失时，不为补齐形式而造文件；在“事项范围与材料限制”中说明缺口和影响。

## 6. 状态标记

| 状态 | 使用条件 |
|---|---|
| ready | 本轮报告目标已完成，仍保留一般法律不确定性 |
| draft | 已形成阶段性报告，但事实、证据或来源有关键限制 |
| blocked | 缺少必要信息、来源、权限或工具，无法可靠完成报告 |
| ready_except_pdf | 用户已请求 PDF，Markdown 内容 ready，但 PDF 生成或质量检查失败 |

Source blocked 时，报告通常为 `draft` 或 `blocked`。只有 PDF 是唯一阻塞项时，才使用 `ready_except_pdf`。

## 7. PDF 按需交付

PDF 只在用户明确要求 PDF、可下载 PDF 报告或阶段交付 PDF 时生成。未请求 PDF 时，不执行 PDF 检查，也不把 PDF 缺失标记为失败。

触发后必须保持输出能力：

1. 先确认 Markdown 报告或目标交付文件是本轮最新版本。
2. 优先使用当前环境可用的可靠路径：DOCX-to-PDF、Pandoc + XeLaTeX、WeasyPrint、wkhtmltopdf、ReportLab/PDFKit、宿主文档工具或根目录 `tools/render_report_pdf.py`。
3. PDF 必须同源于 Markdown，不得沿用旧 PDF。
4. Markdown 表格必须渲染为真实表格；宽表可拆成窄表或卡片式表格。
5. Mermaid、flowchart、HTML、LaTeX 或代码块不能以源码残留在 PDF 正文中；无法渲染时改写为关系表、编号链条或普通文本。
6. 中文必须可读，不能乱码、缺字、严重挤压或项目符号异常。
7. 默认不使用 Chrome headless、Chromium、Edge、Playwright、Puppeteer、Selenium 或系统浏览器打印；只有用户明确允许浏览器渲染时，才可作为 fallback。

推荐版式保持克制、清晰、现代：A4、明确标题层级、页码、可读表格、核心判断/最大风险/待补材料/引用风险区块；可优先复用 `assets/legal-report.css` 和 `assets/legal-report-style-reference.png`。

PDF 基础检查：

| 检查项 | 通过标准 |
|---|---|
| 文件存在 | PDF 文件真实存在且非空 |
| 中文可读 | 中文、英文、数字正常显示 |
| 表格渲染 | Markdown 表格已变成真实表格或卡片 |
| 源码残留 | 无 Markdown/HTML/Mermaid/LaTeX 源码残留 |
| 内容同源 | PDF 与 Markdown 报告内容一致 |

检查不通过时，不得声称 PDF 已完成。若 Markdown 内容已 ready，但 PDF 工具缺失或质量检查失败，标记为 `ready_except_pdf`；若同时存在事实、证据或来源阻塞，标记为 `draft` 或 `blocked`。
