# CAPABILITIES.md

本文件定义 Legal-Assistant_agent 的能力覆盖矩阵、角色分工、工具要求和执行 gate。它用于回答三个问题：

```text
这是什么法律工作场景
→ 必须由哪些角色和 skill 覆盖
→ 哪些 gate 没过就不能交付完整报告
```

纠纷、仲裁、诉讼、听证和复盘事项的案件工作台输出另见 `CASE_WORKBENCH.md`；本文件负责决定何时触发、哪些角色和 gate 必须覆盖。合同审查、合同起草和纯法律研究通常不进入案件工作台，除非同时存在明确争议、对方主张、程序节点或听证准备。

## 1. 角色抽象

| 角色 | 责任 | 典型产物 |
|---|---|---|
| Intake Guard | 隐私、法域、边界、高风险行为和缺口识别 | 范围记录、风险提示 |
| Matter Architect | 事项类型路由、事项文件夹、计划和长期记忆 | `plan.md`、`case.md` |
| Case Navigator | 一页式案件驾驶舱、胜败关键、争点树、可信度和咨询入口 | `case_dashboard.md`、`consultation_note.md` |
| Evidence Manager | 时间线、证据台账、证明对象、三性风险 | `timeline.md`、`evidence.md` |
| Issue Analyst | 争点树、推断链、请求权基础、证明责任、抗辩入口和法条适用边界 | `analysis.md` |
| Legal Researcher | 官方/权威来源、法规案例、引用风险 | `sources.md` |
| Red Team | 对方视角、证据攻击、反请求和谈判压价 | `analysis.md`、`advice.md` |
| Adjudicator | 法官、仲裁员、调解员或审稿律师视角 | `analysis.md`、`advice.md` |
| Strategist | 谈判、投诉、仲裁、诉讼、执行和行动路径 | `advice.md`、`plan.md` |
| Drafter | 文书、函件、合同、条款和提纲 | `drafts.md`、`contract_draft.md` |
| Final Editor / QA | 串联所有产物，检查完整性，默认输出会话汇总结论；按用户要求生成专业报告和 PDF | 专业报告 `.md`，按需 `.pdf` |

## 2. 能力覆盖矩阵

| 事项类型 | 触发信号 | 必跑角色 | 必跑 skill | 可选 skill | 必备文件 | 工具要求 | 最终报告重点 |
|---|---|---|---|---|---|---|---|
| 纠纷/案件分析 | 维权、赔偿、仲裁、诉讼、投诉、对方主张、风险评估 | Intake, Matter, Case Navigator, Evidence, Issue, Research, Red Team, Adjudicator, Strategist, Editor | 01,02,03,04,08,09,10,11,17 | 05,06,07,12,13,14 | `plan.md`, `case.md`, `skill_outputs.md`, `case_dashboard.md`, `consultation_note.md`, `timeline.md`, `evidence.md`, `sources.md`, `analysis.md`, `advice.md`, `case_package.md`, 专业报告 | 涉及法律依据时必须检索官方/权威来源 | 案件驾驶舱、争点树、推断链、证明责任、证据链、来源、对方视角、裁判视角、策略 |
| 合同审查 | 审合同、能不能签、条款风险、补充协议风险 | Intake, Matter, Research, Contract Reviewer, Strategist, Editor | 01,10,15,11,17 | 12,14 | `plan.md`, `case.md`, `skill_outputs.md`, `contract.md`, `clause_review.md`, `sources.md`, `advice.md`, 专业报告 | 涉及强制性规定、行业监管、管辖时检索 | 条款摘要、风险分级、缺失条款、修改建议、谈判优先级 |
| 合同起草 | 写合同、拟协议、补充协议、和解协议、条款清单 | Intake, Matter, Research, Deal Architect, Drafter, Editor | 01,10,16,17 | 11,12,14 | `plan.md`, `case.md`, `skill_outputs.md`, `term_sheet.md`, `contract_draft.md`, `sources.md`, `advice.md` | 涉及监管、格式条款、行业规则时检索 | 交易结构、条款框架、合同草案、可谈判条款、签署清单 |
| 法律研究 | 查法律、找案例、政策依据、规则适用、引用来源 | Intake, Matter, Research, Issue, Editor | 01,10,17 | 04,09,11 | `plan.md`, `case.md`, `skill_outputs.md`, `sources.md`, `analysis.md`, 研究报告 | 必须检索官方/权威来源；未联网则只能输出待核验研究框架 | 法律问题、来源表、规则摘要、适用条件、引用风险 |
| 文书草拟 | 写函、投诉、起诉状框架、答辩、沟通话术、证据目录 | Intake, Matter, Drafter, Strategist, Editor | 01,12,11,17 | 03,04,07,10,13,14 | `plan.md`, `case.md`, `skill_outputs.md`, `drafts.md`, `advice.md`, 必要时 `sources.md` | 文书引用法律或官方口径时检索 | 用途、对象、事实依据、请求、措辞风险、使用前核验 |
| 谈判/和解 | 怎么谈、报价、底线、让步、对方压价、和解协议 | Intake, Matter, Evidence, Red Team, Strategist, Drafter, Editor | 01,03,08,11,12,17 | 04,07,09,10,14 | `plan.md`, `case.md`, `skill_outputs.md`, `evidence.md`, `advice.md`, `drafts.md` | 需要法律筹码时检索 | 筹码、底线、让步顺序、交换条件、话术和禁忌 |
| 庭审/听证准备 | 开庭、仲裁庭、调解、质证、法官追问、听证 | Intake, Matter, Evidence, Issue, Red Team, Adjudicator, Drafter, Editor | 01,03,04,08,09,13,17 | 05,07,10,11,14 | `plan.md`, `case.md`, `skill_outputs.md`, `timeline.md`, `evidence.md`, `hearing.md`, `hearing_playbook.md`, `drafts.md` | 涉及法律依据和裁判规则时检索 | 庭审主线、证据使用、质证意见、发问清单、追问回答 |
| 复盘更新 | 新证据、新报价、新程序节点、新合同版本、用户目标变化 | Review Loop, Matter, Relevant Role, Editor | 14,17 | 按变化重跑相关 skill | `plan.md`, `case.md`, `skill_outputs.md`, `review_delta.md`, 受影响主题文件, 更新后报告 | 若新信息影响法律依据，重新检索 | 新旧变化、判断变化、风险变化、下一步 |

编号对应 `skills/` 目录：01 privacy, 02 intake, 03 timeline/evidence, 04 elements/burden, 05 contradiction, 06 causation, 07 admission questions, 08 opponent, 09 judge, 10 research, 11 strategy, 12 drafting, 13 hearing, 14 review, 15 contract review, 16 contract drafting, 17 final synthesis。

## 3. 路由规则

1. 先判断主场景。如果用户请求同时包含多个场景，以最能决定交付物的场景为主场景，并把其他场景列为子任务。
2. 读取本矩阵，列出必跑 skill、可选 skill、必备文件和工具要求，并判断是否出现条件必跑触发。
3. 如果可选 skill 的触发条件已经出现，将其提升为 `conditional_required`。例如：报告、文书、谈判策略或合同意见引用法律依据时，`case_reference_research` 必须执行或标记 blocked。
4. 创建或复用事项文件夹后，在 `plan.md` 记录事项类型、必跑 skill、条件必跑 skill、可选 skill、gate 状态和下一步。
5. 在 `skill_outputs.md` 记录每个必跑和条件必跑 skill 的执行状态：`done / skipped / blocked / pending`。
6. 进入 `final_synthesis` 前，必须完成 gate 检查。

## 4. 跳过规则

必跑和条件必跑 skill 不能静默跳过。若跳过，必须在 `skill_outputs.md` 说明；若该缺口影响读者判断，在最终报告“分析范围与可靠性说明”中转化为材料限制、来源限制或结论限制，不直接展示 skill 名称或执行表：

| 状态 | 含义 | 是否可交付完整报告 |
|---|---|---|
| done | 已执行并写入主题文件 | 可以 |
| pending | 计划执行但尚未完成 | 不可以，除非报告标记为阶段性草稿 |
| blocked | 因缺材料、缺工具、无法联网或用户未授权而阻塞 | 可以交付阶段性报告，但必须标记不完整 |
| skipped | 经过判断不适用 | 可以，但必须写明理由 |

可选 skill 可以跳过，但如果跳过会影响结论深度，必须写入 `plan.md` 的 Next Actions。

`conditional_required` 适用于原本可选、但因用户目标或报告内容而变成必须执行的 skill。常见触发：

- 事项文件夹中缺少可用 `case.md`，或用户事实、角色、目标、程序阶段尚未结构化时，`case_intake_issue_map` 必须执行或标记 blocked。
- 任何报告、文书、合同意见或谈判策略引用法律规则、案例、政策或网页。
- 用户要求“查法条、找案例、引用来源、最新规定、官方依据”。
- 新证据或新程序节点改变既有法律依据，需要重新核验。
- 合同审查/起草涉及强制性规定、行业监管、格式条款、管辖或消费者/劳动/数据合规等不可只凭经验判断的事项。

## 5. Gate 机制

| Gate | 通过条件 | 未通过处理 |
|---|---|---|
| Routing Gate | 已识别事项类型，并按本文件列出必跑/条件必跑/可选 skill | 不进入最终报告 |
| Folder Gate | 已创建或复用 `work/<date>_<本地化事项名>/` | 不进入多文件交付 |
| Workbench Gate | 纠纷/案件/庭审/复盘事项已按 `CASE_WORKBENCH.md` 生成或更新必要工作台文件；合同审查、合同起草、纯法律研究等不适用事项已标记 `skipped/not applicable` 并说明理由 | 适用但未完成时，不进入深度案件包或最终报告降级为阶段性草稿 |
| Skill Gate | 必跑和条件必跑 skill 已 `done`；确实不适用或无法执行的 skill 已标记 `skipped/blocked` 并说明影响 | `blocked/pending` 时报告标记为 incomplete 或 draft；`skipped` 时必须说明不适用理由 |
| Source Gate | 涉及法律依据时，`case_reference_research` 已执行并写入来源；若无法检索，已标记 blocked 并在 `sources.md` 记录未核验原因和影响 | 不得声称已核验；Source Gate blocked 时报告通常只能是 draft 或 incomplete，不能标记为 complete_except_pdf |
| Evidence Gate | 关键结论绑定事实依据、证据状态、证明责任和不确定性 | 降级为待核验分析 |
| Reasoning Gate | 复杂争议已形成争点树、推断链和法条适用边界 | 不得交付完整争议分析 |
| Report Gate | 专业报告覆盖已完成阶段的关键发现和所有必备事实、证据、来源、分析与建议；内部 skill 覆盖写入 `skill_outputs.md`，不作为读者正文 | 不可只输出摘要 |
| Conversation Gate | 会话回复展示核心结论、关系、缺口、来源、风险、下一步和路径 | 不可只列路径 |
| PDF Gate | 未请求 PDF 时为 `skipped/not requested`；已请求 PDF 时，PDF 真实存在、可读，且表格/图形/区块已按 `PDF_RENDERING.md` 渲染 | 已请求但未通过时，不得声称 PDF 完成；未请求时不阻塞报告 |

## 6. 工具选择

| 工具类型 | 使用条件 | 记录要求 |
|---|---|---|
| 浏览器/搜索引擎 | 需要最新法规、政策、案例、网页核验 | 写入 `sources.md` 和 `skill_outputs.md` |
| 官方法规库/法院/政府网站 | 涉及法律依据或程序规则 | 标记官方性、访问日期、引用风险 |
| 权威数据库 | 官方来源不可得或需要案例补充 | 标记数据库性质和可引用限制 |
| 文件读写 | 复杂事项、合同、文书或报告交付 | 写入事项文件夹 |
| PDF 渲染工具 | 用户明确要求报告 PDF、可下载 PDF、正式报告 PDF 或阶段交付 PDF | 按 `PDF_RENDERING.md` 渲染，质量检查写入报告和 `plan.md` |

## 7. 报告完整性标记

专业报告必须标记执行状态：

| 状态 | 使用条件 |
|---|---|
| complete | 必跑和条件必跑 skill、来源、证据、报告和会话展示 gate 均通过；PDF 未请求时不影响 complete，已请求时 PDF gate 也必须通过 |
| complete_except_pdf | 用户已请求 PDF，且除 PDF Gate 外，Routing、Folder、Workbench、Skill、Source、Evidence、Reasoning、Report 和 Conversation gate 均已通过；PDF 因环境能力或质量检查 blocked |
| draft | 事实、证据或来源仍有关键缺口，但已形成阶段性报告；Source Gate blocked 通常属于此类 |
| incomplete | 必跑或条件必跑 skill、关键 gate 未完成，不能作为完整分析交付 |

状态必须出现在 `plan.md`；专业报告和会话最终回复只展示“报告状态、材料限制、来源状态、证据状态和下一步”，不展示内部 skill/gate 表。

### 7A. Gate 状态示例

合同审查场景的 Workbench Gate 示例：

```text
Workbench Gate: skipped / not applicable
Reason: 本事项为合同签署前审查，无既有争议、对方抗辩、程序节点或听证准备；按合同审查路径输出 contract.md、clause_review.md、advice.md 和合同审查专业报告。
Impact: 不影响完整报告；若后续出现违约争议或谈判冲突，再触发 CASE_WORKBENCH.md。
```

Source Gate blocked 场景的报告状态示例：

```text
Source Gate: blocked
Reason: 本轮未联网或无法访问官方/权威来源；法律规则仅作待核验分析假设。
Report status: draft
Why not complete_except_pdf: 阻塞点不是 PDF，而是法律来源尚未核验。
```

用户已请求 PDF，且 PDF Gate blocked 但其他 gate 均通过的示例：

```text
PDF Gate: blocked
Reason: Markdown 已生成，但 Pandoc、XeLaTeX、WeasyPrint、DOCX-to-PDF、ReportLab/PDFKit 或宿主文档工具不可用，无法生成合格 PDF。
Report status: complete_except_pdf
Condition: 用户已明确要求 PDF，且 Source、Evidence、Reasoning、Report、Conversation gate 均已通过。
```

## 8. PDCA 传递规则

每个复杂事项都按 PDCA 传递：

| 阶段 | 在本项目中的含义 | 必须更新 |
|---|---|---|
| Plan | 事项路由、目标、必跑/条件必跑 skill、gate、文件清单和待补信息 | `plan.md` |
| Do | 执行各阶段 skill，写入主题文件和 `skill_outputs.md` | 主题文件、`skill_outputs.md` |
| Check | 检查证据、来源、skill 覆盖、报告覆盖和会话展示 gate；仅在用户请求 PDF 时检查 PDF gate | `plan.md`、专业报告 |
| Act | 基于检查结果生成下一步、补证任务、重跑 skill 或复盘更新 | `plan.md`、`case.md`、相关主题文件 |

`plan.md` 必须说明当前处于哪个 PDCA 阶段，以及哪些 Check 结果触发了 Act；专业报告只展示报告状态、可靠性限制和下一步行动。
