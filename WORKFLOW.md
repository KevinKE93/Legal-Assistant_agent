# WORKFLOW.md

本文件定义 Legal-Assistant_agent 的事项工作台规则。`AGENTS.md` 是入口，本文件是执行流程标准；事项类型、角色、必跑 skill 和 gate 以 `CAPABILITIES.md` 为准；纠纷、仲裁、诉讼、听证和持续复盘事项的案件工作台输出以 `CASE_WORKBENCH.md` 为准。

## 1. 事项文件夹

复杂、多争点、多程序、合同审查、合同起草或需要持续推进的法律事项，默认创建或复用：

```text
work/<date>_<本地化事项名>/
```

规则：

- `<date>` 使用当前日期，格式 `YYYY-MM-DD`。
- `<本地化事项名>` 使用用户输入的主语言命名。中文输入必须使用中文名；英文输入使用英文名；混合输入按主语言命名。
- 名称用 2-6 个关键词概括法律主题，不写真实姓名、身份证号、完整公司名、地址等敏感信息。
- 同一事项只维护一个文件夹；后续输入新事实、新证据、新合同版本或新程序进展时，继续更新旧文件夹。
- 创建新文件夹前，先查看 `work/` 下是否已有同一事项文件夹。判断依据包括事项类型、关键词、当事人角色、合同主题、程序阶段和用户目标；不确定时在 `plan.md` 写 `Reuse check: uncertain`，并向用户确认或选择最保守的复用方案。
- 事项文件夹必须直接位于 `work/` 下，不增加任何中间分类层。
- 不提交 `work/` 下真实案件数据。

### 1A. 复用既有事项后的更新规则

复用既有事项文件夹时，不得只沿用旧结论。必须做一次“复用复核”：

- 读取既有 `plan.md`、`case.md`、`skill_outputs.md`、`sources.md`、`analysis.md`、`advice.md` 和已生成报告。
- 判断本轮输入是同一事项的新事实、同一事项的补充说明，还是应新建事项；判断理由写入 `plan.md` 的 `Reuse check`。
- 若本轮仅补充事实但没有原始证据，保持相关事实为“用户陈述/待证明事实”，不得把报告状态升级为 `complete`。
- 若本轮涉及日期、期限、最新法规、政策、案例或来源状态，必须重新核验或在 `sources.md` 标明“本轮未复核/待核验/影响”。
- 更新 `case.md` 的 `Update Log`，说明新增信息、判断是否变化、下一步动作。
- 更新 `plan.md` 的 `PDCA Log`，新增一轮复核记录，而不是覆盖旧记录。
- 若更新了专业报告 Markdown，PDF 必须同源重渲染；无法重渲染时把 `PDF status` 改为 `blocked` 或说明 PDF 仍为旧版，不得暗示 PDF 已同步。

## 2. i18n 规则

- 默认使用用户主语言输出目录名、面向用户的文件名、标题、表格字段和行动建议。
- 中文输入时，最终报告文件名必须使用中文法律主题并避免包含真实当事人隐私。
- 英文输入时，使用英文主题和英文报告名，例如 `Split Payroll Overtime Dispute Professional Report.md`。
- 法条名、合同原文、证据备注、对方原话、用户输入的特定短语保留原文，并用用户语言解释。
- 内部工作文件名保持稳定英文，便于跨工具复盘。

## 3. 默认文件

复杂事项至少维护：

```text
plan.md
case.md
skill_outputs.md
analysis.md
advice.md
<本地化主题>专业报告.md
<本地化主题>专业报告.pdf
```

按场景增加：

```text
timeline.md
evidence.md
sources.md
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

## 4. 文件职责

| 文件 | 职责 |
|---|---|
| `plan.md` | 当前阶段、已完成、进行中、下一步、责任方、待用户补充信息、PDF 状态 |
| `case.md` | 事项核心记忆、事实/条款分层、争议焦点、证据状态、程序进展、关键结论 |
| `skill_outputs.md` | 每个已执行 skill 的输入、输出、关键发现、来源使用和最终报告章节映射 |
| `timeline.md` | 事件时间线、合同版本流转或程序节点 |
| `evidence.md` | 证据台账、证明对象、三性风险、证据缺口和补强动作 |
| `sources.md` | 官方/权威来源、网页、法规、案例、访问日期、核验状态、引用风险 |
| `case_dashboard.md` | 面向法律工作者的一页式案件地图、胜败关键、争点树、证明责任和可信度 |
| `consultation_note.md` | 面向用户或客户的咨询纪要、当前判断、限制、补证材料和禁忌动作 |
| `case_package.md` | 法律团队使用的完整案件包，串联事实、证据、争点、来源、攻防和策略 |
| `pleading_framework.md` | 文书、仲裁申请、起诉状、答辩、代理意见或投诉材料的结构框架 |
| `hearing_playbook.md` | 调解、仲裁、庭审或听证准备：举证、质证、发问和裁判者追问 |
| `review_delta.md` | 新证据、新程序、新报价或新材料导致的变化复盘和需重跑内容 |
| `analysis.md` | 工作底稿型完整分析，保留专业推理过程 |
| `advice.md` | 面向用户的策略、行动路径、谈判建议和禁忌动作 |
| `drafts.md` | 沟通函、投诉材料、仲裁/诉讼框架、庭审提纲 |
| `contract.md` | 合同背景、版本、条款摘要 |
| `clause_review.md` | 条款风险、缺失条款、修改建议、谈判点 |
| `term_sheet.md` | 合同起草前的交易要点和条款结构 |
| `contract_draft.md` | 合同、补充协议或和解协议草案 |

## 5. 路由与 gate 规则

复杂事项不能直接进入最终汇总。必须先完成：

```text
识别事项类型
→ 查 CAPABILITIES.md
→ 确定必跑 skill / 条件必跑 skill / 可选 skill / 必备文件 / 工具要求
→ 写入 plan.md 和 skill_outputs.md
→ 执行必跑和条件必跑 skill
→ 检查 gates
→ final_synthesis
```

`plan.md` 必须记录：

- 主事项类型和子任务类型。
- 必跑 skill 清单。
- 条件必跑 skill 清单。
- 可选 skill 清单。
- 每个 gate 的状态：`pass / pending / blocked / skipped`。
- 专业报告状态：`complete / complete_except_pdf / draft / incomplete`。
- 当前 PDCA 阶段和 Check 结论。

`skill_outputs.md` 必须记录每个必跑和条件必跑 skill 的状态：`done / pending / blocked / skipped`。必跑或条件必跑 skill 若为 `pending`、`blocked` 或无理由缺失，最终报告只能标记为 `draft` 或 `incomplete`；若为 `skipped`，必须说明为什么不适用，以及是否影响完整交付。面向阅读对象的报告不展示 skill 执行表，应把影响结论的缺口写成材料限制、来源限制或证据限制。

## 6. PDCA 闭环

复杂事项必须通过 PDCA 传递：

| PDCA | Agent 动作 | 文件落点 |
|---|---|---|
| Plan | 判断语言、法域、事项类型、复用文件夹、必跑/条件必跑 skill、gate、用户目标 | `plan.md`、`case.md` |
| Do | 执行 skill，沉淀事实、时间线、证据、来源、分析、建议、文书或合同草案 | 主题文件、`skill_outputs.md` |
| Check | 检查 skill 覆盖、来源、证据、报告、会话展示、PDF、i18n 和目录规则 | `plan.md`、专业报告 |
| Act | 输出下一步、补证、重跑 skill、升级/降级报告状态，或触发 `review_learning_loop` | `plan.md`、`case.md`、相关主题文件 |

`plan.md` 是 PDCA 控制面板。每次阶段推进后都要更新当前 PDCA 阶段、Check 结果和 Act 动作，不能只更新最终报告。

## 7. plan.md 标准结构

```markdown
# Plan

- Matter folder:
- Matter type:
- Required skills:
- Conditional required skills:
- Optional skills:
- Output language:
- Workbench mode: yes / no / not applicable
- Workbench files:
- Professional report Markdown:
- Professional report PDF:
- PDF status: pending / ready / blocked
- Report status: complete / complete_except_pdf / draft / incomplete
- PDCA stage: Plan / Do / Check / Act
- Reuse check: new folder / reused existing folder / uncertain
- Current stage:
- Updated at:

## Gate Status
| Gate | Status | Reason / Evidence | Next Step |
|---|---|---|---|
| Routing Gate |  |  |  |
| Folder Gate |  |  |  |
| Workbench Gate |  |  |  |
| Skill Gate |  |  |  |
| Source Gate |  |  |  |
| Evidence Gate |  |  |  |
| Report Gate |  |  |  |
| Conversation Gate |  |  |  |
| PDF Gate |  |  |  |

## Done
-

## In Progress
-

## Next Actions
| Priority | Owner | Action | Purpose | Due / Trigger | Output |
|---|---|---|---|---|---|

## PDCA Log
| Cycle | Plan | Do | Check | Act | Status |
|---|---|---|---|---|---|

## Open Questions For User
1.

## Agent Notes
-
```

每完成一个主要阶段，都更新 `plan.md`。下一步必须有责任方：`user`、`agent`、`lawyer`、`court/arbitrator`、`agency`、`opponent`。

## 8. case.md 标准结构

```markdown
# Case

## One-Line Matter Map

## Basic Information
| Field | Value | Evidence / Source | Status |
|---|---|---|---|

## Facts Or Clauses
| ID | Content | Type: proven / alleged / disputed / inferred / clause | Evidence / Source | Impact |
|---|---|---|---|---|

## Core Issues
| ID | Issue | Type | Burden / Owner | User Position | Opponent Position | Evidence | Gap | Impact |
|---|---|---|---|---|---|---|---|---|

## Evidence Status
| Evidence | Holder | Proves | Strength | Authenticity / Legality / Relevance Risk | Next Step |
|---|---|---|---|---|---|

## Legal Analysis Notes
-

## Risk And Strategy Notes
-

## Final Deliverable Notes
- 文件名：
- 当前状态：not started / draft / ready for user review / needs evidence update
- 必须纳入的主题：

## Update Log
| Date | New Information | Changed Judgment | Next Step |
|---|---|---|---|
```

## 9. skill_outputs.md 标准结构

```markdown
# Skill Outputs

## Execution Index
| Seq | Skill | Required / Conditional / Optional | Status | Trigger | Files Read | Files Updated | Key Findings | Open Questions | Sources Used | Report Section |
|---:|---|---|---|---|---|---|---|---|---|---|

## Detailed Notes

### <Seq>. <skill_name>
- Trigger:
- Required / conditional / optional:
- Status: done / pending / blocked / skipped
- User goal:
- Inputs read:
- Files updated:
- Key findings:
- Evidence or source status:
- Open questions:
- Next action:
- Must appear in final report section:
```

规则：

- 每执行一个 skill，必须追加或更新一条记录。
- 如果必跑或条件必跑 skill 被跳过或阻塞，必须在内部记录理由、影响和下一步，不能在最终报告中暗示相关分析已经完成；对读者只展示由此产生的材料、来源或证据限制。
- 如果执行时信息不足，仍要记录“信息不足、影响、下一步补充”。
- 最终报告必须吸收 `Execution Index` 中所有已执行 skill 的关键发现，并转化为事实、证据、争点、来源、风险或行动建议。

## 10. 来源记录规则

需要法律条文、司法解释、案例、判决、行政规则、合同监管规则、网页或最新政策时：

- 优先检索所属国家/管辖区的官方来源、法院官网、政府官网、官方法规库或权威数据库。
- 允许使用浏览器、搜索引擎、法律数据库、官方网页或宿主环境提供的外部工具。
- 每条可引用来源写入 `sources.md`，至少包含标题、机构/来源、URL、访问日期、核验状态、可用规则、引用风险。
- 未核验来源只能作为线索，不能当作确定法律依据。
- 若本轮未联网检索，必须在 `sources.md` 写明“未检索/待核验/原因/影响”。
- 最终报告和会话回复必须展示来源数量、来源类型、核心可用规则和引用风险。

### 10A. 来源复核规则

来源可能随时间变化或出现更权威版本时，应优先复核：

- 法律、司法解释、行政规则、地方政策、诉讼/仲裁期限、社保公积金基数、裁判规则和案例。
- 旧报告中使用“新闻发布会、转载版本、问答、实务文章”作为来源，而本轮可找到正式条文、主管机关页面或更权威来源时，应补入新来源并保留引用风险。
- 复核时必须写明访问/复核日期；新增来源使用新的编号或子编号，不覆盖旧来源导致上下文丢失。
- 如果复核不改变结论，也要在 `plan.md` 或 `sources.md` 中写明“核心判断不变”的理由。

## 11. 默认阶段流程

1. 隐私与范围守门。
2. 语言与事项类型路由。
3. 查 `CAPABILITIES.md`，确定必跑 skill、条件必跑 skill、可选 skill、必备文件和 gate。
4. 事项摄入，拆分事实、推测、评价、法律结论、条款和目标。
5. 创建或复用事项文件夹，初始化 `plan.md`、`case.md`、`skill_outputs.md`。
6. 对案件工作台事项，先输出或更新 `case_dashboard.md` 与 `consultation_note.md`。
7. 时间线、条款、证据台账。
8. 争议焦点、条款风险、请求权基础、证明责任。
9. 按 `LEGAL_REASONING.md` 深挖母命题、条件命题、反制命题、推断链条和法条适用边界。
10. 矛盾、因果、对方视角、裁判视角。
11. 官方或权威来源检索，写入 `sources.md`。
12. 策略行动、文书或合同草案；必要时生成 `case_package.md`、`pleading_framework.md` 或 `hearing_playbook.md`。
13. Gate 与 PDCA Check 检查，标记 `complete / complete_except_pdf / draft / incomplete`。
14. 最终汇总，逐项读取所有工作文件，输出专业报告 Markdown。
15. 按 `PDF_RENDERING.md` 将报告渲染为 styled HTML、DOCX 或宿主支持的富文本版式后导出 PDF。
16. 会话界面展示实质汇总。
17. 后续新信息触发 `review_delta.md`、Act 和复盘，更新既有事项文件夹。

## 12. 信息不足时如何处理

只在缺口会明显影响结论、金额、期限、管辖、证明责任或行动选择时提问。用户暂时无法补充时，继续分析，但必须把缺口写入 `plan.md`、`case.md` 和 `skill_outputs.md`。

优先追问：

- 法域和城市/地区。
- 纠纷类型和程序阶段。
- 用户身份与目标。
- 关键日期和期限。
- 已有证据清单。
- 对方主张或已提交材料。
- 是否已经仲裁、起诉、答辩、调解或投诉。
- 合同类事项的合同版本、交易背景、签署状态、谈判空间、不可接受条款和用户立场。
