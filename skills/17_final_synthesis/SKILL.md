---
name: final_synthesis
description: 在复杂法律事项、案件分析、合同审查、合同起草或法律研究需要阶段性收口、专业报告、PDF 交付或会话实质汇总时使用。
---

# Skill：最终汇总与专业报告交付

## 事项记忆要求

- 执行本技能后，必须按根目录 `SKILLS.md` 的映射更新事项文件夹中的主题文件，并追加或更新 `skill_outputs.md`。
- `skill_outputs.md` 至少记录：skill 名称、触发原因、读取文件、更新文件、关键发现、待补问题、来源使用、对应最终报告章节。
- 如果本技能没有实际执行，不能在最终报告中声称已执行；如果执行但信息不足，仍要记录缺口、影响和下一步。

## 目标

1. 把事项文件夹中的分散工作文件汇总为一份专业报告，而不是几段概述。
2. 逐项吸收 `skill_outputs.md` 中已沉淀的关键发现，确保事实、证据、来源、分析和建议进入报告；不要把 skill 执行表直接展示给阅读对象。
3. 在会话界面展示实质性汇总内容：核心结论、争点关系、证据缺口、来源核验、最大风险和下一步。
4. 按 `LEGAL_REASONING.md` 检查争点树、推断链和法条适用边界是否进入报告。
5. 输出本地化命名的专业报告 `.md`，再按 `PDF_RENDERING.md` 渲染为可读 PDF。
6. 对 PDF 做基本质量检查；若不合格，明确标记 blocked。

## 输入

- 事项文件夹路径，必须是 `work/<date>_<本地化事项名>/`。
- 用户主语言和目标读者。
- 已存在的工作文件。
- `CAPABILITIES.md` 中的事项类型、必跑 skill、条件必跑 skill、gate 和报告状态规则。
- `CASE_WORKBENCH.md` 中的案件驾驶舱、咨询纪要、案件包、文书框架、庭审手册和增量复盘规则。
- `LEGAL_REASONING.md` 中的争点挖掘和法条适用边界规则。
- `PDF_RENDERING.md` 中的 PDF 渲染和质量检查规则。
- `plan.md` 中的 PDCA 阶段、Check 结果和 Act 动作。
- `skill_outputs.md` 中的执行索引。
- `sources.md` 中的来源记录。
- 宿主环境是否具备可靠 PDF 导出能力。

## 必读文件

按存在情况逐项读取：

```text
CAPABILITIES.md
CASE_WORKBENCH.md
LEGAL_REASONING.md
PDF_RENDERING.md
plan.md
case.md
skill_outputs.md
case_dashboard.md
consultation_note.md
case_package.md
pleading_framework.md
hearing_playbook.md
review_delta.md
timeline.md
evidence.md
sources.md
analysis.md
advice.md
drafts.md
hearing.md
negotiation.md
contract.md
clause_review.md
term_sheet.md
contract_draft.md
```

缺失文件不阻塞汇总，但必须在报告附录说明“未见/待补/不适用”。

## 命名

- 中文复杂纠纷：`<法律问题主题>专业报告.md` 和 `<法律问题主题>专业报告.pdf`。
- 中文合同审查：`<合同主题>合同审查专业报告.md` 和 `<合同主题>合同审查专业报告.pdf`。
- 中文合同起草：`<合同主题>合同草案.md` 和 `<合同主题>合同草案.pdf`。
- 中文法律研究：`<主题>法律研究报告.md` 和 `<主题>法律研究报告.pdf`。
- 英文事项使用英文对应名称。
- 事项文件夹必须直接位于 `work/` 下。

## 汇总工作流

### 0. 复用与复核

如果事项文件夹和专业报告已经存在，先执行复用复核：

1. 读取既有 `plan.md`、`case.md`、`skill_outputs.md`、`sources.md`、`analysis.md`、`advice.md` 和旧报告。
2. 判断本轮输入是否属于同一事项；如复用，在 `plan.md` 写明 `Reuse check: reused existing folder` 和复用理由。
3. 把新事实写入 `case.md` 的 `Update Log`；如没有原始证据，保持“用户陈述/待证明事实”。
4. 若涉及最新法律、政策、期限、来源或 PDF 状态，重新核验并更新 `sources.md`、`plan.md` 和报告质量检查。
5. 更新 Markdown 后必须重新生成同名 PDF；无法生成合格 PDF 时，标记 blocked，不得继续把旧 PDF 当作本轮交付成果。

### 1. 文件覆盖表

建立工作文件覆盖表：

| 工作文件 | 是否存在 | 是否读取 | 用途 | 对结论影响 | 纳入报告章节 |
|---|---|---|---|---|---|

### 2. 内部完整性检查

读取 `CAPABILITIES.md`、`plan.md` 和 `skill_outputs.md`，在内部建立完整性检查表。该表用于判断报告状态和补证动作，默认不进入专业报告正文。

| 项目 | 内容 | 状态 | 影响 |
|---|---|---|---|
| 主事项类型 |  |  |  |
| 必跑 skill |  |  |  |
| 条件必跑 skill |  |  |  |
| 可选 skill |  |  |  |
| Gate 状态 |  |  |  |
| PDCA 阶段 | Plan / Do / Check / Act |  |  |
| 报告状态 | complete / complete_except_pdf / draft / incomplete |  |  |

并在内部建立 skill 覆盖表：

| Skill | Required / Conditional / Optional | Status | 关键发现 | 待补问题 | 对应报告章节 | 是否已纳入 |
|---|---|---|---|---|---|---|

每个已执行 skill 的关键发现至少进入一个实体章节或子章节，但不要以内部产物索引、覆盖表或“某内部阶段未执行”等形式面向读者展示。必跑或条件必跑 skill 未 `done` 的，报告状态不能标记为 complete；若该缺口影响实质分析，应标记为 draft 或 incomplete。complete_except_pdf 只适用于内容、来源、证据、报告和会话 gate 全部通过、仅 PDF Gate 阻塞的情况；Source Gate blocked 时不得标记为 complete_except_pdf。

如果内部检查发现缺口，只在专业报告中转化为读者可理解的可靠性限制，例如：

- 尚未核验原始合同文本。
- 未取得银行流水，金额判断仅为框架性分析。
- 未完成类案检索，裁判倾向仅作一般规则判断。
- 未取得送达凭证，程序期限判断存在不确定性。

### 3. 来源核验表

读取 `sources.md`，输出：

- 来源总数。
- 官方/权威来源数量。
- 未核验来源数量。
- 核心可用规则。
- 引用风险。

如果 `sources.md` 缺失或为空，但报告涉及法律依据，必须标记来源缺口，不能声称已核验。

### 4. 交叉核对

检查：

- `case.md` 的关键事实是否被 `evidence.md` 支撑。
- `analysis.md` 的结论是否被 `sources.md` 或待核验规则支撑。
- `advice.md` 的行动建议是否匹配证据强度和程序阶段。
- `skill_outputs.md` 的关键发现是否全部转化为报告中的事实、证据、争点、来源、风险或行动建议。
- `case_dashboard.md` 的胜败关键、争点树和可信度是否进入报告的事项地图或执行摘要。
- `consultation_note.md` 的用户可理解判断、限制、补证材料和禁忌动作是否进入会话展示或报告摘要。
- `case_package.md`、`pleading_framework.md`、`hearing_playbook.md` 或 `review_delta.md` 如已存在，是否被吸收为案件包、文书、庭审或复盘章节。
- `CAPABILITIES.md` 要求的必跑和条件必跑 skill 是否全部执行或说明阻塞/跳过原因。
- gate 状态是否支持当前报告状态。
- PDCA 是否完成本轮 Plan、Do、Check，并产生明确 Act。
- 复杂争议是否包含母命题、条件命题、反制命题、推断链条和法条适用边界。
- 是否存在前后矛盾、金额矛盾、程序矛盾、i18n 命名错误或 PDF 交付风险。

### 5. 重写专业报告

按 `REPORT.md` 的专业报告结构生成，不在本 skill 内复制完整模板。根据事项类型组织为法律备忘录、案件分析报告、合同审查报告、合同草案或法律研究报告。报告必须呈现事实、证据、争点、法律依据、适用边界、风险和行动建议；案件工作台文件应转化为读者可用的事项地图、咨询摘要、案件包、文书或庭审章节；内部 skill 索引、gate 表、PDCA 表和执行日志不得作为报告章节输出。

合同审查、合同起草和法律研究按 `REPORT.md` 的类型调整章节；仍必须保留来源、待补信息、可靠性限制和质量检查。

### 6. 输出 Markdown

写入事项文件夹中的本地化专业报告文件。报告不得只是复制 `analysis.md`；必须串联 `case.md`、`case_dashboard.md`、`consultation_note.md`、`case_package.md`、`timeline.md`、`evidence.md`、`sources.md`、`advice.md` 和 `skill_outputs.md`。某些工作台文件不存在时，要说明是“不适用、未生成、待补材料后生成”，不能暗示已经覆盖。

### 7. 渲染 PDF

先将 Markdown 报告转换为 DOCX、XeLaTeX、PDF-native 文档对象，或由无浏览器 HTML-to-PDF 引擎处理的 styled HTML，再导出同名 PDF。优先使用支持 CJK 字体、表格、页眉页脚和分页的非浏览器渲染能力。

开始渲染前先探测工具，并按 `PDF_RENDERING.md` 的推荐执行路径选择：Markdown → DOCX → PDF；Markdown → XeLaTeX PDF；Markdown → styled HTML → WeasyPrint/wkhtmltopdf；Markdown → PDF-native 文档对象 → PDF。不要假设默认命令或默认 Python/Node 环境有依赖；若 bundled runtime 有可用库，可优先使用。

默认禁止使用 Chrome headless、Chromium、Edge、Playwright、Puppeteer、Selenium 或系统浏览器打印生成 PDF。只有用户明确允许浏览器渲染时，才可作为 fallback；仍必须通过 PDF Gate 质量检查。

渲染要求：

- Markdown 表格必须变成真实表格。
- Mermaid、flowchart 或关系图必须渲染成图形，或改写成关系表。
- 核心判断、最大风险、待补材料和引用风险应使用区块样式。
- PDF 中不得出现 Markdown 管道符、未渲染代码块、Mermaid 源码或 HTML 残留。
- 如果 Mermaid/flowchart 不能渲染为图片，PDF 版必须改写为关系表、编号链条或说明文字，不能保留源码。

不得假称已生成 PDF。若当前环境无法导出合格 PDF：

- 在 `plan.md` 标记 `PDF status: blocked`。
- 在 `plan.md` 或内部交付记录写明阻塞原因。
- 在会话中说明 Markdown 已生成、PDF 待转换。
- 如果同时存在 Source Gate、Evidence Gate 或必跑 skill blocked，报告状态应为 `draft` 或 `incomplete`；只有 PDF 是唯一阻塞项时，才可标记 `complete_except_pdf`。

### 8. PDF 质量检查

合格 PDF 必须满足：

- 文件存在且大小非空。
- 中文、英文、数字、表格基本可读。
- 表格已渲染，不出现 `|---|---|` 等 Markdown 原文。
- 不出现 Mermaid 源码、HTML 残留、明显乱码、缺字、项目符号异常、标题挤压或目录错乱。
- 内容与 Markdown 一致。
- 更新 Markdown 后重渲染 PDF，保证同源；旧 PDF 不得标记为本轮 ready。

如果发现乱码或明显排版问题，不能把 PDF 标记为完成。

### 9. 对话界面展示

最终回复必须用用户语言展示，并从事项文件夹和最终报告中提取实质内容。不能只列路径或只写“已生成报告”。

```markdown
## 最终汇总

### 核心结论
1.
2.
3.

### 本轮依据
- 已核验/读取的关键材料：
- 案件驾驶舱/咨询纪要要点：
- 用户新增信息：
- 尚未读取/缺失的材料：

### 争议焦点关系
- 母命题：
- 条件命题：
- 反制命题：
- 关键依赖关系：

### 关键证据缺口
- 对结论影响最大的证据：
- 当前只能作为用户陈述的事实：
- 需要对方、平台、法院/仲裁机构或行政机关调取的材料：

### 来源核验
- 来源数量：
- 来源类型：
- 核心可用规则：
- 未核验/引用风险：

### 分析范围与可靠性
- 报告状态：
- 已核验材料：
- 尚未核验/缺失材料：
- 对结论的影响：
- 需要更新报告的触发事项：

### 最大风险
- 法律风险：
- 证据风险：
- 程序风险：
- 金额/谈判风险：

### 下一步三项动作
1.
2.
3.

### 已生成文件
- Markdown:
- PDF:
```

## 质量检查

- 不遗漏 `skill_outputs.md`。
- 不遗漏内部 `CAPABILITIES.md` 必跑、条件必跑 skill 和 gate 检查，但这些内容默认只写入 `plan.md` 和 `skill_outputs.md`。
- 不遗漏 PDCA 阶段、Check 结果和 Act 动作；会话和报告中转化为“当前报告状态、限制和下一步”。
- 不遗漏已执行 skill 的关键发现，但要转化为读者关心的事实、争点、证据、来源、风险或行动建议。
- 不把待证明事实写成已证明事实。
- 不把工作底稿直接复制为最终报告。
- 中文输入不得输出英文目录名或英文总结文件名。
- 引用来源必须进入 `sources.md` 和报告参考文献表。
- PDF 路径必须真实存在且质量合格；否则明确说明未生成及原因。
- PDF 不得包含未渲染 Markdown 表格、Mermaid 源码或代码块。
