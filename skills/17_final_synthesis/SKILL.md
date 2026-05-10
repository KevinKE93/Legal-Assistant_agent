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
2. 逐项覆盖 `skill_outputs.md` 中已执行的 skill，确保每个 skill 产物进入报告章节或附录。
3. 在会话界面展示实质性汇总内容：核心结论、争点关系、证据缺口、来源核验、最大风险和下一步。
4. 按 `LEGAL_REASONING.md` 检查争点树、推断链和法条适用边界是否进入报告。
5. 输出本地化命名的专业报告 `.md`，再按 `PDF_RENDERING.md` 渲染为可读 PDF。
6. 对 PDF 做基本质量检查；若不合格，明确标记 blocked。

## 输入

- 事项文件夹路径，必须是 `work/<date>_<本地化事项名>/`。
- 用户主语言和目标读者。
- 已存在的工作文件。
- `CAPABILITIES.md` 中的事项类型、必跑 skill、条件必跑 skill、gate 和报告状态规则。
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
LEGAL_REASONING.md
PDF_RENDERING.md
plan.md
case.md
skill_outputs.md
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

### 2. 能力覆盖与 Skill 覆盖表

读取 `CAPABILITIES.md`、`plan.md` 和 `skill_outputs.md`，建立能力覆盖表：

| 项目 | 内容 | 状态 | 影响 |
|---|---|---|---|
| 主事项类型 |  |  |  |
| 必跑 skill |  |  |  |
| 条件必跑 skill |  |  |  |
| 可选 skill |  |  |  |
| Gate 状态 |  |  |  |
| PDCA 阶段 | Plan / Do / Check / Act |  |  |
| 报告状态 | complete / complete_except_pdf / draft / incomplete |  |  |

并建立 skill 覆盖表：

| Skill | Required / Conditional / Optional | Status | 关键发现 | 待补问题 | 对应报告章节 | 是否已纳入 |
|---|---|---|---|---|---|---|

每个已执行 skill 至少进入一个章节或子章节。不能只列路径。
必跑或条件必跑 skill 未 `done` 的，报告状态不能标记为 complete；若该缺口影响实质分析，应标记为 draft 或 incomplete。complete_except_pdf 只适用于内容 gate 全部通过、仅 PDF gate 阻塞的情况。

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
- `skill_outputs.md` 的关键发现是否全部进入报告。
- `CAPABILITIES.md` 要求的必跑和条件必跑 skill 是否全部执行或说明阻塞/跳过原因。
- gate 状态是否支持当前报告状态。
- PDCA 是否完成本轮 Plan、Do、Check，并产生明确 Act。
- 复杂争议是否包含母命题、条件命题、反制命题、推断链条和法条适用边界。
- 是否存在前后矛盾、金额矛盾、程序矛盾、i18n 命名错误或 PDF 交付风险。

### 5. 重写专业报告

按 `REPORT.md` 的结构生成。复杂纠纷默认包含：

1. 封面信息和重要提示。
2. 目录。
3. 执行摘要。
4. 报告范围、假设与材料清单。
5. Skill 产物索引。
6. 能力覆盖与执行完整性，包含 PDCA 执行轨迹。
7. 事项地图与程序状态。
8. 关键事实时间线。
9. 核心争议焦点矩阵。
10. 争议焦点关系图或关系链。
11. 争点深挖与推断链。
12. 请求权基础与证明责任。
13. 证据链与缺口。
14. 法律依据与参考来源。
15. 法条适用边界。
16. 对方视角与反制。
17. 裁判者/审稿者视角。
18. 金额、胜率和风险区间。
19. 策略路径与行动清单。
20. 禁忌动作与表达风险。
21. 待补信息。
22. 附录：工作文件覆盖表、Skill 覆盖表。

合同审查、合同起草和法律研究按 `REPORT.md` 调整章节，但仍必须保留 skill 索引、来源、待补信息和质量检查。

### 6. 输出 Markdown

写入事项文件夹中的本地化专业报告文件。报告不得只是复制 `analysis.md`；必须串联 `case.md`、`timeline.md`、`evidence.md`、`sources.md`、`advice.md` 和 `skill_outputs.md`。

### 7. 渲染 PDF

先将 Markdown 报告转换为 styled HTML、DOCX 或宿主支持的富文本版式，再导出同名 PDF。优先使用支持 CJK 字体、表格、页眉页脚和分页的渲染能力；其次使用浏览器打印或可靠文档工具。

开始渲染前先探测工具：宿主文档/PDF运行时、浏览器打印、Pandoc、WeasyPrint、wkhtmltopdf、DOCX-to-PDF、bundled Python/Node 依赖等。不要假设默认命令或默认 Python 环境有依赖；若 bundled runtime 有可用库，可优先使用。

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
- 使用的工作文件：
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

### 执行完整性
- 报告状态：
- 未完成 gate：
- PDCA 阶段：
- 需要 Act 的事项：
- 已执行 skill：
- 未执行/阻塞 skill 对结论的影响：

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
- 不遗漏 `CAPABILITIES.md` 的必跑、条件必跑 skill 和 gate 检查。
- 不遗漏 PDCA 阶段、Check 结果和 Act 动作。
- 不遗漏已执行 skill 的关键发现。
- 不把待证明事实写成已证明事实。
- 不把工作底稿直接复制为最终报告。
- 中文输入不得输出英文目录名或英文总结文件名。
- 引用来源必须进入 `sources.md` 和报告参考文献表。
- PDF 路径必须真实存在且质量合格；否则明确说明未生成及原因。
- PDF 不得包含未渲染 Markdown 表格、Mermaid 源码或代码块。
