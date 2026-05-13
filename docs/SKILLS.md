# SKILLS.md

本文件是 Legal-Assistant_agent 的能力路由与分析镜头接口。它回答三个问题：

```text
这是什么场景
→ 需要哪些分析镜头
→ 最小产物是什么
```

这里的 `skill` 是分析镜头，不是必须串行执行的流程节点。默认不维护 `skill_outputs.md`；镜头结果应直接合并进会话回复、`matter.md` 或目标交付文件。

## 1. 分析镜头总览

| 镜头 | 对应 skill | 解决的问题 |
|---|---|---|
| Privacy / Scope | 01 `privacy_scope_guard` | 隐私、法域、安全边界、高风险行为 |
| Intake | 02 `case_intake_issue_map` | 事实、角色、目标、争议焦点初筛 |
| Evidence | 03 `timeline_evidence_ledger` | 时间线、证据、证明对象、证据缺口 |
| Burden | 04 `elements_burden_matrix` | 请求权基础、证明责任、抗辩结构 |
| Contradiction | 05 `contradiction_analysis` | 陈述、证据、时间线和行为逻辑矛盾 |
| Causation | 06 `causation_chain` | 行为、损害、金额、替代原因和扩大损失 |
| Questions | 07 `admission_question_design` | 合法追问、确认事实、发问路径 |
| Opponent | 08 `opponent_perspective` | 对方抗辩、证据攻击、谈判筹码 |
| Judge | 09 `judge_perspective` | 裁判者或审稿者视角 |
| Research | 10 `case_reference_research` | 法律、案例、政策、官方来源 |
| Strategy | 11 `strategy_risk_action` | 谈判、投诉、仲裁、诉讼、行动路径 |
| Drafting | 12 `document_drafting` | 函件、投诉、诉状框架、沟通口径 |
| Hearing | 13 `hearing_prep` | 调解、仲裁、庭审、听证准备 |
| Review | 14 `review_learning_loop` | 新证据、新报价、新程序、新版本复盘 |
| Contract Review | 15 `contract_review` | 合同条款风险、缺失条款、修改建议 |
| Contract Drafting | 16 `contract_drafting` | 合同、补充协议、和解协议起草 |
| Synthesis | 17 `final_synthesis` | 会话收口、报告、PDF 前内容整合 |

## 2. 统一输入输出

每个镜头只保留最小结构：

```text
Input:
- 用户目标
- 已知事实/条款
- 已有证据/来源
- 当前模式：Quick Answer / Matter Note / Deliverable / Deep Case

Output:
- 结论或发现
- 依据：事实 / 证据 / 来源 / 合同条款
- 不确定性
- 证据或来源缺口
- 下一步
- Status: ready / draft / blocked / skipped
```

如进入 `Matter Note`、`Deliverable` 或 `Deep Case`，把上述结果写入 `matter.md` 或目标文件。只有长期协作、审计追踪或用户明确要求时，才额外维护 `skill_outputs.md`。

## 3. 场景路由矩阵

| 场景 | 触发信号 | 默认模式 | 必要镜头 | 按需镜头 | 最小产物 |
|---|---|---|---|---|---|
| 简单法律问题 | “能不能”“有没有风险”“怎么理解” | Quick Answer | Privacy, Intake | Research, Strategy | 会话回复 |
| 纠纷/案件分析 | 赔偿、返还、解除、投诉、仲裁、诉讼、对方主张 | Matter Note 或 Deep Case | Privacy, Intake, Evidence, Burden, Strategy | Research, Opponent, Judge, Contradiction, Causation, Drafting, Hearing | `matter.md`；复杂时再扩展 |
| 合同审查 | 审合同、能否签、条款风险、补充协议 | Deliverable | Privacy, Contract Review, Strategy | Research, Drafting, Review | `matter.md` + 合同审查意见 |
| 合同起草 | 写合同、拟协议、补充协议、和解协议 | Deliverable | Privacy, Contract Drafting | Research, Strategy, Drafting, Review | `matter.md` + 合同草案 |
| 法律研究 | 查法条、找案例、政策依据、最新规则 | Deliverable | Privacy, Research, Synthesis | Burden, Judge, Strategy | `matter.md` + `sources.md` + 研究结论 |
| 文书草拟 | 函、投诉、起诉状/答辩框架、沟通口径 | Deliverable | Privacy, Drafting, Strategy | Evidence, Burden, Research, Questions, Hearing | `matter.md` + 文书草稿 |
| 谈判/和解 | 怎么谈、报价、底线、让步、和解协议 | Matter Note 或 Deliverable | Privacy, Evidence, Opponent, Strategy | Drafting, Research, Review | `matter.md`；需要文件时加草案 |
| 庭审/听证准备 | 开庭、仲裁庭、调解、质证、法官追问 | Deep Case | Privacy, Evidence, Burden, Opponent, Judge, Hearing | Research, Questions, Drafting, Review | `matter.md` + `hearing_playbook.md` |
| 复盘更新 | 新证据、新合同版本、新报价、新程序节点 | Matter Note 或 Deep Case | Review | 受影响镜头 | 更新 `matter.md` 和受影响文件 |

路由原则：

- 先选择模式，再选择镜头。
- 不为可选镜头生成空产物。
- 用户只要答案时，不创建工作目录。
- 用户要文件时，只生成目标文件和必要支撑文件。
- 引用法律、案例、政策、网页、最新规则或具体期限时，`Research` 必须执行；无法执行则标记为 `Blocked` 或“待核验”。
- 纠纷复杂度高、程序节点多、证据多、需要庭审或长期跟踪时，才进入 `Deep Case`。

## 4. 镜头到产物

| Skill | 输入 | 输出去向 |
|---|---|---|
| `privacy_scope_guard` | 用户事实、材料敏感性、潜在高风险行为 | 会话回复或 `matter.md` 的边界、脱敏、拒绝项 |
| `case_intake_issue_map` | 零散事实、用户目标、程序阶段 | `matter.md` 的事实、角色、目标、争议焦点 |
| `timeline_evidence_ledger` | 时间节点、证据、合同、聊天、付款记录 | `matter.md`；复杂时拆为 `timeline.md`、`evidence.md` |
| `elements_burden_matrix` | 请求、抗辩、法律关系、证据状态 | `matter.md` 或报告的证明责任/要件分析 |
| `contradiction_analysis` | 陈述、证据、时间线、立场 | 矛盾点、追问方向、证据攻击点 |
| `causation_chain` | 行为、损害、金额、替代原因 | 因果链、损害范围、补证事项 |
| `admission_question_design` | 需确认的事实、合法沟通场景 | 合法追问清单、发问边界 |
| `opponent_perspective` | 用户主张、证据、对方可能立场 | 对方抗辩、压价点、反制建议 |
| `judge_perspective` | 争议焦点、证据、请求、程序 | 中立审查意见、裁判关注点 |
| `case_reference_research` | 法域、法律问题、关键词、程序节点 | `sources.md` 或会话来源说明；规则适用边界 |
| `strategy_risk_action` | 用户目标、风险、证据、对方动作 | 行动路径、优先级、最大风险 |
| `document_drafting` | 文书目标、对象、事实、证据、语气 | `drafts.md` 或本地化文书草稿 |
| `hearing_prep` | 庭审/仲裁/调解目标、证据、争议焦点 | `hearing_playbook.md` 或听证准备摘要 |
| `review_learning_loop` | 新事实、新证据、新版本、新程序节点 | 更新 `matter.md`，必要时生成 `review_delta.md` |
| `contract_review` | 合同文本、交易背景、用户立场 | 合同审查意见、风险分级、修改建议 |
| `contract_drafting` | 交易目标、主体、标的、风险分配 | 合同草案、条款清单、签署核验项 |
| `final_synthesis` | `matter.md`、来源、证据、目标交付文件 | 会话收口、Markdown 报告、按需 PDF 前内容 |

## 5. 常见调用组合

- 简单问题：`privacy_scope_guard` → `case_intake_issue_map` → 需要时 `case_reference_research`。
- 合同审查：`privacy_scope_guard` → `contract_review` → 需要时 `case_reference_research` → `strategy_risk_action`。
- 合同起草：`privacy_scope_guard` → `contract_drafting` → 需要时 `case_reference_research`。
- 纠纷分析：`privacy_scope_guard` → `case_intake_issue_map` → `timeline_evidence_ledger` → `elements_burden_matrix` → `strategy_risk_action`。
- 复杂争议：在纠纷分析基础上，按需加入 `opponent_perspective`、`judge_perspective`、`contradiction_analysis`、`causation_chain`。
- 文书草拟：`case_intake_issue_map` → 需要时 `case_reference_research` → `document_drafting`。
- 庭审准备：`timeline_evidence_ledger` → `elements_burden_matrix` → `opponent_perspective` → `judge_perspective` → `hearing_prep`。
- 复盘更新：`review_learning_loop` → 只重跑受影响镜头。

## 6. 最小检查

每次交付只检查与当前目标相关的五项：

| 检查项 | 通过标准 | 不通过时 |
|---|---|---|
| Safety | 不替代律师、不承诺结果、不协助违法或虚假行为 | 拒绝危险部分，给安全替代 |
| Sufficiency | 当前事实足以支持本轮目标 | 标记缺口或 `Blocked` |
| Source | 引用法律/案例/政策时已核验或已说明待核验 | 不写成确定依据 |
| Deliverable | 文件内容覆盖用户明确要求 | 标记草稿或继续补齐 |
| PDF | 仅用户请求 PDF 时检查真实、可读、同源 | 失败时说明原因，不假称完成 |

## 7. 结果吸收与阻塞

- 镜头输出必须进入会话回复、`matter.md` 或目标交付文件之一；不要生成孤立分析。
- 如果前序发现后续没有采用，删除、压缩或在 `matter.md` 中说明“未采用原因”。
- 面向用户的报告不展示内部镜头执行表。
- 只有影响用户判断时，才说明“未核验”“证据不足”“仅阶段性判断”等限制。

出现以下情况时，镜头状态为 `blocked`：

- 关键事实缺失，继续分析会误导用户。
- 需要官方或权威来源，但无法检索或无法确认来源。
- 用户要求违法、虚假陈述、非法取证、隐私侵害或威胁骚扰。
- 需要文件/PDF 工具，但当前不可用。

`blocked` 时输出：原因、缺什么、当前最多能做到什么、需要谁决策。

## 8. 状态标记

| 状态 | 使用条件 |
|---|---|
| ready | 本轮目标已完成，仍保留一般法律不确定性 |
| draft | 已形成阶段性结果，但事实、证据或来源有关键限制 |
| blocked | 缺少必要信息、工具、权限或来源，无法可靠完成目标 |
| skipped | 判断不适用，且不影响本轮目标 |
| ready_except_pdf | 用户已请求 PDF，内容已 ready，但 PDF 生成或质量检查失败 |

不要用状态表替代实质结论。状态只服务于用户理解当前结果能不能使用。
