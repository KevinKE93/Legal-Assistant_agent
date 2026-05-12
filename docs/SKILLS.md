# SKILLS.md

本文件定义每个阶段 skill 的触发条件、必须落盘的文件、`skill_outputs.md` 记忆字段和报告章节映射。每个 `skills/*/SKILL.md` 只保留阶段操作细节；本文件提供跨技能统一约束。哪些 skill 必跑、可选或可跳过，以 `docs/CAPABILITIES.md` 的事项类型矩阵为准。案件工作台文件的生成和更新规则以 `docs/CASE_WORKBENCH.md` 为准。

## 1. 统一执行要求

每执行一个 skill，必须完成三件事：

1. 读取事项文件夹中已有工作文件，避免孤立分析。
2. 将本技能产物写入对应主题文件。
3. 在 `skill_outputs.md` 追加或更新一条执行记录。

复杂纠纷、仲裁/诉讼、对方已有主张、返还/赔偿/解除等事项，必须同时遵循 `docs/LEGAL_REASONING.md`：争议焦点不能只列清单，必须形成母命题、条件命题、反制命题、推断链条和法律规则适用边界。相关发现写入 `analysis.md`，并在报告中对应“争议焦点展开与推断链”“法律规则适用边界”章节。

案件工作台事项还必须遵循 `docs/CASE_WORKBENCH.md`：初次复杂纠纷优先生成 `case_dashboard.md` 和 `consultation_note.md`；深度阶段按需生成 `case_package.md`、`pleading_framework.md`、`hearing_playbook.md`；复盘阶段生成 `review_delta.md`。这些文件不是额外模板，而是各 skill 发现的工作台表达。

`skill_outputs.md` 必须记录：

| 字段 | 要求 |
|---|---|
| Skill | skill 名称，例如 `timeline_evidence_ledger` |
| Required / Conditional / Optional | 来自 `docs/CAPABILITIES.md` 的必跑、条件必跑或可选判断 |
| Status | `done / pending / blocked / skipped` |
| Trigger | 为什么调用本 skill |
| Files Read | 读取了哪些工作文件 |
| Files Updated | 写入或更新了哪些工作文件 |
| Key Findings | 本技能产生的关键发现，不写空话 |
| Open Questions | 会影响结论的待补信息 |
| Sources Used | 使用了哪些来源；未使用写“未检索/不适用/待核验” |
| Report Section | 报告中必须出现的位置 |

如果 skill 未实际执行，不能在报告中暗示相关分析已完成。如果执行但信息不足，必须记录缺口、影响和下一步。必跑或条件必跑 skill 为 `pending`、`blocked` 或没有执行记录时，报告必须标记为 `draft` 或 `incomplete`；只有内容、来源、证据、报告和会话 gate 全部通过且仅 PDF Gate 阻塞时，才可标记为 `complete_except_pdf`。Source Gate blocked 时，报告通常为 `draft` 或 `incomplete`，不是 `complete_except_pdf`。面向读者的报告应把这些缺口转化为“材料限制/来源限制/证据限制”，不要展示 skill 执行表。

## 2. Skill 到文件和报告章节映射

| Skill | 触发场景 | 必须更新文件 | 报告章节 |
|---|---|---|---|
| `privacy_scope_guard` | 初次接触、用户给出敏感事实、可能有高风险行为 | `plan.md`、`case.md`、`skill_outputs.md` | 范围、假设、安全边界 |
| `case_intake_issue_map` | 纠纷事实零散、需要形成案件地图 | `case.md`、`analysis.md`、`case_dashboard.md`、`consultation_note.md`、`skill_outputs.md` | 事项地图、案件驾驶舱与争议焦点总览 |
| `timeline_evidence_ledger` | 有时间节点、证据、转账、聊天、合同、通知 | `timeline.md`、`evidence.md`、`case.md`、`skill_outputs.md` | 事实时间线与证据链 |
| `elements_burden_matrix` | 需要判断请求、抗辩、证明责任、要件缺口 | `analysis.md`、`case.md`、`skill_outputs.md` | 请求权基础与证明责任 |
| `contradiction_analysis` | 需要找前后矛盾、证据冲突、质证方向 | `analysis.md`、`evidence.md`、`skill_outputs.md` | 矛盾矩阵与攻防价值 |
| `causation_chain` | 需要证明行为、损害、金额之间的因果关系 | `analysis.md`、`evidence.md`、`skill_outputs.md` | 因果链与损害范围 |
| `admission_question_design` | 需要设计合法提问、事实确认、庭审发问 | `drafts.md`、`advice.md`、`skill_outputs.md` | 提问路径与补证计划 |
| `opponent_perspective` | 需要模拟对方抗辩、证据攻击、反请求 | `analysis.md`、`advice.md`、`skill_outputs.md` | 对方视角与反制 |
| `judge_perspective` | 需要中立裁判者或审稿律师视角 | `analysis.md`、`advice.md`、`skill_outputs.md` | 裁判者/审稿者视角 |
| `case_reference_research` | 需要法律、案例、政策、官方网页或最新规则 | `sources.md`、`analysis.md`、`skill_outputs.md` | 法律依据与参考文献 |
| `strategy_risk_action` | 需要谈判、投诉、仲裁、诉讼、执行路径 | `advice.md`、`plan.md`、`skill_outputs.md` | 策略路径与行动清单 |
| `document_drafting` | 需要沟通函、投诉、诉状、答辩、报告文本 | `drafts.md`、`advice.md`、`pleading_framework.md`、`skill_outputs.md` | 文书框架、草案与表达风险 |
| `hearing_prep` | 调解、仲裁、庭审、听证准备 | `hearing.md`、`hearing_playbook.md`、`drafts.md`、`skill_outputs.md` | 庭审/听证准备 |
| `review_learning_loop` | 新证据、新程序、新报价、新合同版本 | `plan.md`、`case.md`、`review_delta.md`、相关主题文件、`skill_outputs.md` | 复盘更新与变化说明 |
| `contract_review` | 审查合同、协议、补充协议、条款清单 | `contract.md`、`clause_review.md`、`advice.md`、`skill_outputs.md` | 合同条款摘要与风险清单 |
| `contract_drafting` | 起草合同、补充协议、和解协议、条款清单 | `term_sheet.md`、`contract_draft.md`、`advice.md`、`skill_outputs.md` | 合同草案与条款选择 |
| `final_synthesis` | 阶段完成、用户要总结/报告/PDF、复杂事项收口 | `case_package.md`、Markdown 报告、按需 PDF 报告、`plan.md`、`skill_outputs.md` | 案件包与全部报告章节 |

## 3. 必跑、可选和跳过规则

- `required`：来自 `docs/CAPABILITIES.md` 的必跑 skill。必须执行；若无法执行，状态写为 `blocked`，说明原因、影响和下一步。
- `conditional_required`：原本可选，但因用户目标、法律引用、最新规则、程序节点或报告内容而变成必须执行的 skill。执行和阻塞规则等同 required。
- `case_intake_issue_map` 在事实、角色、目标或程序阶段尚未写入 `case.md` 时视为 conditional_required。
- `case_reference_research` 在任何报告、文书、合同意见或策略引用法律依据时视为 conditional_required。
- `optional`：来自 `docs/CAPABILITIES.md` 的可选 skill。可根据材料、目标和风险选择执行；若跳过，状态写为 `skipped` 并说明理由。
- `derived`：执行过程中因新信息触发的额外 skill。必须记录触发原因和产物。
- `not applicable`：明显不适用的 skill，不必写入执行索引；但如果用户特别要求或会影响结论，应写入 `skipped`。

状态含义：

| Status | 含义 | 对交付影响 |
|---|---|---|
| done | 已执行并写入主题文件 | 可以进入完整报告 |
| pending | 已识别但尚未执行 | 报告只能是阶段性草稿 |
| blocked | 因缺证据、缺权限、无法联网、缺 PDF 能力等阻塞 | 若是来源/证据/必跑 skill 阻塞，报告为 `draft/incomplete`；若仅 PDF 阻塞且其他 gate 通过，可为 `complete_except_pdf` |
| skipped | 判断不适用或用户暂不需要 | 可以交付，但必须说明理由 |

## 4. skill_outputs.md 写入模板

每次 skill 执行后，在 `skill_outputs.md` 写入：

```markdown
### <Seq>. <skill_name>
- Trigger:
- Required / conditional / optional:
- Status: done / pending / blocked / skipped
- User goal:
- Files read:
- Files updated:
- Key findings:
- Evidence status:
- Sources used:
- Open questions:
- Next action:
- Must appear in report section:
```

`Execution Index` 表必须同步更新，便于汇总时逐项覆盖。

## 5. 汇总覆盖规则

调用 `final_synthesis` 时：

- 先读取 `docs/CAPABILITIES.md` 和 `plan.md`，确认事项类型、必跑 skill、条件必跑 skill 和 gate 状态。
- 先读取 `skill_outputs.md`，确定哪些 skill 实际执行过。
- 再逐项读取 `plan.md`、`case.md`、`timeline.md`、`evidence.md`、`sources.md`、`analysis.md`、`advice.md` 和其他存在的主题文件。
- 报告必须吸收 `Execution Index` 中每个已执行 skill 的关键发现，并转化为事实、证据、争议焦点、法律依据、风险或行动建议。
- 报告不得展示必跑和条件必跑 skill 的执行表；必跑或条件必跑 skill 未执行、`pending` 或 `blocked` 时，报告状态不能标记为 `complete`，并应根据影响标记为 `draft` 或 `incomplete`，同时在“分析范围与可靠性说明”中写成读者能理解的限制。
- 如果某个 skill 的关键发现没有进入报告，必须在内部 `skill_outputs.md` 或 `plan.md` 说明未纳入原因；只有影响读者判断时，才在报告中说明为材料或分析限制。
- 会话回复必须展示实质汇总内容，不能只列“已生成文件路径”。

## 5A. 案件工作台产物规则

案件工作台文件与 skill 的关系如下：

| 工作台文件 | 主要来源 skill | 必须吸收的内容 | 不应包含 |
|---|---|---|---|
| `case_dashboard.md` | `privacy_scope_guard`、`case_intake_issue_map`、已完成的证据/来源/对方/裁判视角 skill | 一句话地图、程序状态、关键判断变量、争议焦点关系图、证明责任、证据缺口、对方打法、来源状态、可信度 | 下一步五个动作、输出分流、长篇法条摘录 |
| `consultation_note.md` | `case_intake_issue_map`、`strategy_risk_action`、`case_reference_research` | 当前能判断什么、不能判断什么、风险、补证材料、不宜采取的动作、下一次协作清单 | 内部 gate、skill 执行索引、过度确定的结果倾向 |
| `case_package.md` | 证据、要件、来源、对方视角、裁判视角、策略和草拟类 skill | 事实、证据、争议焦点、请求权基础、来源边界、攻防、策略、文书/庭审索引 | 对外报告式包装、无依据的绝对结论 |
| `pleading_framework.md` | `document_drafting`、`elements_burden_matrix`、`case_reference_research` | 文书目标、请求/抗辩、事实叙事、法律依据、证据附件、兜底主张、表达风险 | 未核验即提交的正式文书承诺 |
| `hearing_playbook.md` | `hearing_prep`、`opponent_perspective`、`judge_perspective`、`admission_question_design` | 庭审目标、举证顺序、质证、合法发问、裁判者追问、安全回答原则 | 诱导虚假陈述、非法取证或威胁性表达 |
| `review_delta.md` | `review_learning_loop` | 新旧差异、受影响事实/争议焦点、变化判断、需更新文件、需重跑 skill | 从头重写却不说明变化 |

这些文件每次更新都要在 `skill_outputs.md` 中记录来源 skill、读取文件、更新内容和报告章节映射。

## 6. 来源使用规则

`case_reference_research` 不是唯一能写来源的 skill。任何 skill 只要引用外部法律、案例、政策、网页或权威资料，都必须更新 `sources.md`，并在 `skill_outputs.md` 的 `Sources used` 字段记录：

- 已核验来源数量。
- 来源类型：法律/司法解释/案例/政策/网页/数据库。
- 核心可用规则。
- 引用风险。

若没有联网或没有外部来源，必须写明：

```text
Sources used: 未联网检索；当前规则仅为待核验法律分析假设，报告不得表述为已核验。
```

## 7. 质量门槛

- 不把待证明事实写成已证明事实。
- 不把法律研究结果留在对话里而不写入 `sources.md`。
- 不把 skill 产物留在零散对话里而不写入事项文件夹。
- 不把报告写成短摘要。
- 不跳过 `docs/CAPABILITIES.md` 中的必跑或条件必跑 skill；确实不能执行时必须写明 blocked/skipped 和影响。
- 不交付乱码、未渲染表格、残留 Markdown 管道符或 Mermaid 源码的 PDF。
