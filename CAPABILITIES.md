# CAPABILITIES.md

本文件定义 Legal-Assistant_agent 的能力覆盖矩阵、角色分工、工具要求和执行 gate。它用于回答三个问题：

```text
这是什么法律工作场景
→ 必须由哪些角色和 skill 覆盖
→ 哪些 gate 没过就不能交付完整报告
```

## 1. 角色抽象

| 角色 | 责任 | 典型产物 |
|---|---|---|
| Intake Guard | 隐私、法域、边界、高风险行为和缺口识别 | 范围记录、风险提示 |
| Matter Architect | 事项类型路由、事项文件夹、计划和长期记忆 | `plan.md`、`case.md` |
| Evidence Manager | 时间线、证据台账、证明对象、三性风险 | `timeline.md`、`evidence.md` |
| Issue Analyst | 争点、请求权基础、证明责任、抗辩入口 | `analysis.md` |
| Legal Researcher | 官方/权威来源、法规案例、引用风险 | `sources.md` |
| Red Team | 对方视角、证据攻击、反请求和谈判压价 | `analysis.md`、`advice.md` |
| Adjudicator | 法官、仲裁员、调解员或审稿律师视角 | `analysis.md`、`advice.md` |
| Strategist | 谈判、投诉、仲裁、诉讼、执行和行动路径 | `advice.md`、`plan.md` |
| Drafter | 文书、函件、合同、条款和提纲 | `drafts.md`、`contract_draft.md` |
| Final Editor / QA | 串联所有产物，检查完整性，生成专业报告和 PDF | 专业报告 `.md/.pdf` |

## 2. 能力覆盖矩阵

| 事项类型 | 触发信号 | 必跑角色 | 必跑 skill | 可选 skill | 必备文件 | 工具要求 | 最终报告重点 |
|---|---|---|---|---|---|---|---|
| 纠纷/案件分析 | 维权、赔偿、仲裁、诉讼、投诉、对方主张、风险评估 | Intake, Matter, Evidence, Issue, Research, Red Team, Adjudicator, Strategist, Editor | 01,02,03,04,08,09,10,11,17 | 05,06,07,12,13,14 | `plan.md`, `case.md`, `skill_outputs.md`, `timeline.md`, `evidence.md`, `sources.md`, `analysis.md`, `advice.md`, 专业报告 | 涉及法律依据时必须检索官方/权威来源 | 争点、证明责任、证据链、来源、对方视角、裁判视角、策略 |
| 合同审查 | 审合同、能不能签、条款风险、补充协议风险 | Intake, Matter, Research, Contract Reviewer, Strategist, Editor | 01,10,15,11,17 | 12,14 | `plan.md`, `case.md`, `skill_outputs.md`, `contract.md`, `clause_review.md`, `sources.md`, `advice.md`, 专业报告 | 涉及强制性规定、行业监管、管辖时检索 | 条款摘要、风险分级、缺失条款、修改建议、谈判优先级 |
| 合同起草 | 写合同、拟协议、补充协议、和解协议、条款清单 | Intake, Matter, Research, Deal Architect, Drafter, Editor | 01,10,16,17 | 11,12,14 | `plan.md`, `case.md`, `skill_outputs.md`, `term_sheet.md`, `contract_draft.md`, `sources.md`, `advice.md` | 涉及监管、格式条款、行业规则时检索 | 交易结构、条款框架、合同草案、可谈判条款、签署清单 |
| 法律研究 | 查法律、找案例、政策依据、规则适用、引用来源 | Intake, Matter, Research, Issue, Editor | 01,10,17 | 04,09,11 | `plan.md`, `case.md`, `skill_outputs.md`, `sources.md`, `analysis.md`, 研究报告 | 必须检索官方/权威来源；未联网则只能输出待核验研究框架 | 法律问题、来源表、规则摘要、适用条件、引用风险 |
| 文书草拟 | 写函、投诉、起诉状框架、答辩、沟通话术、证据目录 | Intake, Matter, Drafter, Strategist, Editor | 01,12,11,17 | 03,04,07,10,13,14 | `plan.md`, `case.md`, `skill_outputs.md`, `drafts.md`, `advice.md`, 必要时 `sources.md` | 文书引用法律或官方口径时检索 | 用途、对象、事实依据、请求、措辞风险、使用前核验 |
| 谈判/和解 | 怎么谈、报价、底线、让步、对方压价、和解协议 | Intake, Matter, Evidence, Red Team, Strategist, Drafter, Editor | 01,03,08,11,12,17 | 04,07,09,10,14 | `plan.md`, `case.md`, `skill_outputs.md`, `evidence.md`, `advice.md`, `drafts.md` | 需要法律筹码时检索 | 筹码、底线、让步顺序、交换条件、话术和禁忌 |
| 庭审/听证准备 | 开庭、仲裁庭、调解、质证、法官追问、听证 | Intake, Matter, Evidence, Issue, Red Team, Adjudicator, Drafter, Editor | 01,03,04,08,09,13,17 | 05,07,10,11,14 | `plan.md`, `case.md`, `skill_outputs.md`, `timeline.md`, `evidence.md`, `hearing.md`, `drafts.md` | 涉及法律依据和裁判规则时检索 | 庭审主线、证据使用、质证意见、发问清单、追问回答 |
| 复盘更新 | 新证据、新报价、新程序节点、新合同版本、用户目标变化 | Review Loop, Matter, Relevant Role, Editor | 14,17 | 按变化重跑相关 skill | `plan.md`, `case.md`, `skill_outputs.md`, 受影响主题文件, 更新后报告 | 若新信息影响法律依据，重新检索 | 新旧变化、判断变化、风险变化、下一步 |

编号对应 `skills/` 目录：01 privacy, 02 intake, 03 timeline/evidence, 04 elements/burden, 05 contradiction, 06 causation, 07 admission questions, 08 opponent, 09 judge, 10 research, 11 strategy, 12 drafting, 13 hearing, 14 review, 15 contract review, 16 contract drafting, 17 final synthesis。

## 3. 路由规则

1. 先判断主场景。如果用户请求同时包含多个场景，以最能决定交付物的场景为主场景，并把其他场景列为子任务。
2. 读取本矩阵，列出必跑 skill、可选 skill、必备文件和工具要求。
3. 创建或复用事项文件夹后，在 `plan.md` 记录事项类型、必跑 skill、可选 skill、gate 状态和下一步。
4. 在 `skill_outputs.md` 记录每个必跑 skill 的执行状态：`done / skipped / blocked / pending`。
5. 进入 `final_synthesis` 前，必须完成 gate 检查。

## 4. 跳过规则

必跑 skill 不能静默跳过。若跳过，必须在 `skill_outputs.md` 和最终报告“能力覆盖与执行完整性”章节说明：

| 状态 | 含义 | 是否可交付完整报告 |
|---|---|---|
| done | 已执行并写入主题文件 | 可以 |
| pending | 计划执行但尚未完成 | 不可以，除非报告标记为阶段性草稿 |
| blocked | 因缺材料、缺工具、无法联网或用户未授权而阻塞 | 可以交付阶段性报告，但必须标记不完整 |
| skipped | 经过判断不适用 | 可以，但必须写明理由 |

可选 skill 可以跳过，但如果跳过会影响结论深度，必须写入 `plan.md` 的 Next Actions。

## 5. Gate 机制

| Gate | 通过条件 | 未通过处理 |
|---|---|---|
| Routing Gate | 已识别事项类型，并按本文件列出必跑/可选 skill | 不进入最终报告 |
| Folder Gate | 已创建或复用 `work/<date>_<本地化事项名>/` | 不进入多文件交付 |
| Skill Gate | 必跑 skill 已 `done`；确实不适用或无法执行的 skill 已标记 `skipped/blocked` 并说明影响 | `blocked/pending` 时报告标记为 incomplete 或 draft；`skipped` 时必须说明不适用理由 |
| Source Gate | 涉及法律依据时，`sources.md` 已记录来源、待核验状态或未检索原因 | 不得声称已核验 |
| Evidence Gate | 关键结论绑定事实依据、证据状态、证明责任和不确定性 | 降级为待核验分析 |
| Report Gate | 专业报告覆盖已执行 skill 和所有必备文件 | 不可只输出摘要 |
| Conversation Gate | 会话回复展示核心结论、关系、缺口、来源、风险、下一步和路径 | 不可只列路径 |
| PDF Gate | PDF 真实存在且可读；否则 `PDF status: blocked` | 不得声称 PDF 完成 |

## 6. 工具选择

| 工具类型 | 使用条件 | 记录要求 |
|---|---|---|
| 浏览器/搜索引擎 | 需要最新法规、政策、案例、网页核验 | 写入 `sources.md` 和 `skill_outputs.md` |
| 官方法规库/法院/政府网站 | 涉及法律依据或程序规则 | 标记官方性、访问日期、引用风险 |
| 权威数据库 | 官方来源不可得或需要案例补充 | 标记数据库性质和可引用限制 |
| 文件读写 | 复杂事项、合同、文书或报告交付 | 写入事项文件夹 |
| PDF 导出工具 | 用户要求报告 PDF 或阶段交付 | 质量检查写入报告和 `plan.md` |

## 7. 报告完整性标记

专业报告必须标记执行状态：

| 状态 | 使用条件 |
|---|---|
| complete | 必跑 skill、来源、证据、报告和 PDF gate 均通过 |
| complete_except_pdf | 除 PDF 外均通过，PDF 因环境能力 blocked |
| draft | 事实、证据或来源仍有关键缺口，但已形成阶段性报告 |
| incomplete | 必跑 skill 或关键 gate 未完成，不能作为完整分析交付 |

状态必须出现在 `plan.md`、专业报告“能力覆盖与执行完整性”章节和会话最终回复中。
