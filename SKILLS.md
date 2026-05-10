# SKILLS.md

本文件定义每个阶段 skill 的触发条件、必须落盘的文件、`skill_outputs.md` 记忆字段和最终报告章节映射。每个 `skills/*/SKILL.md` 只保留阶段操作细节；本文件提供跨技能统一约束。

## 1. 统一执行要求

每执行一个 skill，必须完成三件事：

1. 读取事项文件夹中已有工作文件，避免孤立分析。
2. 将本技能产物写入对应主题文件。
3. 在 `skill_outputs.md` 追加或更新一条执行记录。

`skill_outputs.md` 必须记录：

| 字段 | 要求 |
|---|---|
| Skill | skill 名称，例如 `timeline_evidence_ledger` |
| Trigger | 为什么调用本 skill |
| Files Read | 读取了哪些工作文件 |
| Files Updated | 写入或更新了哪些工作文件 |
| Key Findings | 本技能产生的关键发现，不写空话 |
| Open Questions | 会影响结论的待补信息 |
| Sources Used | 使用了哪些来源；未使用写“未检索/不适用/待核验” |
| Report Section | 最终报告中必须出现的位置 |

如果 skill 未实际执行，不能在最终报告中声称执行过。如果执行但信息不足，必须记录缺口、影响和下一步。

## 2. Skill 到文件和报告章节映射

| Skill | 触发场景 | 必须更新文件 | 最终报告章节 |
|---|---|---|---|
| `privacy_scope_guard` | 初次接触、用户给出敏感事实、可能有高风险行为 | `plan.md`、`case.md`、`skill_outputs.md` | 范围、假设、安全边界 |
| `case_intake_issue_map` | 纠纷事实零散、需要形成案件地图 | `case.md`、`analysis.md`、`skill_outputs.md` | 事项地图与争点总览 |
| `timeline_evidence_ledger` | 有时间节点、证据、转账、聊天、合同、通知 | `timeline.md`、`evidence.md`、`case.md`、`skill_outputs.md` | 事实时间线与证据链 |
| `elements_burden_matrix` | 需要判断请求、抗辩、证明责任、要件缺口 | `analysis.md`、`case.md`、`skill_outputs.md` | 请求权基础与证明责任 |
| `contradiction_analysis` | 需要找前后矛盾、证据冲突、质证方向 | `analysis.md`、`evidence.md`、`skill_outputs.md` | 矛盾矩阵与攻防价值 |
| `causation_chain` | 需要证明行为、损害、金额之间的因果关系 | `analysis.md`、`evidence.md`、`skill_outputs.md` | 因果链与损害范围 |
| `admission_question_design` | 需要设计合法提问、事实确认、庭审发问 | `drafts.md`、`advice.md`、`skill_outputs.md` | 提问路径与补证计划 |
| `opponent_perspective` | 需要模拟对方抗辩、证据攻击、反请求 | `analysis.md`、`advice.md`、`skill_outputs.md` | 对方视角与反制 |
| `judge_perspective` | 需要中立裁判者或审稿律师视角 | `analysis.md`、`advice.md`、`skill_outputs.md` | 裁判者/审稿者视角 |
| `case_reference_research` | 需要法律、案例、政策、官方网页或最新规则 | `sources.md`、`analysis.md`、`skill_outputs.md` | 法律依据与参考文献 |
| `strategy_risk_action` | 需要谈判、投诉、仲裁、诉讼、执行路径 | `advice.md`、`plan.md`、`skill_outputs.md` | 策略路径与行动清单 |
| `document_drafting` | 需要沟通函、投诉、诉状、答辩、报告文本 | `drafts.md`、`advice.md`、`skill_outputs.md` | 文书草案与表达风险 |
| `hearing_prep` | 调解、仲裁、庭审、听证准备 | `hearing.md`、`drafts.md`、`skill_outputs.md` | 庭审/听证准备 |
| `review_learning_loop` | 新证据、新程序、新报价、新合同版本 | `plan.md`、`case.md`、相关主题文件、`skill_outputs.md` | 复盘更新与变化说明 |
| `contract_review` | 审查合同、协议、补充协议、条款清单 | `contract.md`、`clause_review.md`、`advice.md`、`skill_outputs.md` | 合同条款摘要与风险清单 |
| `contract_drafting` | 起草合同、补充协议、和解协议、条款清单 | `term_sheet.md`、`contract_draft.md`、`advice.md`、`skill_outputs.md` | 合同草案与条款选择 |
| `final_synthesis` | 阶段完成、用户要总结/报告/PDF、复杂事项收口 | 专业报告 `.md`、专业报告 `.pdf`、`plan.md`、`skill_outputs.md` | 全部章节 |

## 3. skill_outputs.md 写入模板

每次 skill 执行后，在 `skill_outputs.md` 写入：

```markdown
### <Seq>. <skill_name>
- Trigger:
- User goal:
- Files read:
- Files updated:
- Key findings:
- Evidence status:
- Sources used:
- Open questions:
- Next action:
- Must appear in final report section:
```

`Execution Index` 表必须同步更新，便于最终汇总逐项覆盖。

## 4. 最终汇总覆盖规则

调用 `final_synthesis` 时：

- 先读取 `skill_outputs.md`，确定哪些 skill 实际执行过。
- 再逐项读取 `plan.md`、`case.md`、`timeline.md`、`evidence.md`、`sources.md`、`analysis.md`、`advice.md` 和其他存在的主题文件。
- 专业报告必须为 `Execution Index` 中每个已执行 skill 提供对应章节或子章节。
- 如果某个 skill 的关键发现没有进入报告，必须在报告附录说明未纳入原因。
- 会话回复必须展示实质汇总内容，不能只列“已生成文件路径”。

## 5. 来源使用规则

`case_reference_research` 不是唯一能写来源的 skill。任何 skill 只要引用外部法律、案例、政策、网页或权威资料，都必须更新 `sources.md`，并在 `skill_outputs.md` 的 `Sources used` 字段记录：

- 已核验来源数量。
- 来源类型：法律/司法解释/案例/政策/网页/数据库。
- 核心可用规则。
- 引用风险。

若没有联网或没有外部来源，必须写明：

```text
Sources used: 未联网检索；当前规则仅为待核验法律分析假设，最终报告不得表述为已核验。
```

## 6. 质量门槛

- 不把待证明事实写成已证明事实。
- 不把法律研究结果留在对话里而不写入 `sources.md`。
- 不把 skill 产物留在零散对话里而不写入事项文件夹。
- 不把最终报告写成短摘要。
- 不交付乱码或无法阅读的 PDF。
