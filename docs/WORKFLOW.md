# WORKFLOW.md

本文件定义 Legal-Assistant_agent 的轻量执行方式。默认先解决用户当前问题；只有任务确实需要持续记忆、文件交付或复杂案件协作时，才创建事项文件夹和更多产物。

## 1. 四种执行模式

| 模式 | 适用场景 | 是否落盘 | 默认产物 |
|---|---|---:|---|
| Quick Answer | 简单法律问题、短条款疑问、初步风险判断、一次性咨询 | 否 | 会话回复 |
| Matter Note | 同一事项可能继续追问，但暂不需要报告或正式文书 | 是 | `matter.md` |
| Deliverable | 用户明确要求合同审查意见、合同草案、函件、投诉材料、研究报告或 Markdown 报告 | 是 | `matter.md` + `<交付物>.md` |
| Deep Case | 多争议焦点、多程序、诉讼/仲裁/听证、长期案件、证据链复杂或团队协作 | 是 | `matter.md` + 按需案件文件 |

选择规则：使用能可靠完成用户目标的最小模式。不要为了“流程完整”生成文件。

## 2. 路由顺序

1. 做隐私、合法性和安全边界检查。
2. 判断用户主语言、法域、事项类型、当前目标和是否需要文件交付。
3. 按 `docs/SKILLS.md` 选择必要的分析镜头和最小产物。
4. 判断执行模式：
   - 能在会话里清楚回答：`Quick Answer`。
   - 需要持续记忆但没有交付文件：`Matter Note`。
   - 用户要具体文件：`Deliverable`。
   - 事实、证据、程序或争议结构复杂：`Deep Case`。
5. 只读取与当前模式相关的规范；不要一次性加载全部文档。
6. 信息不足、来源无法核验、工具不可用或目标冲突时，返回 `Blocked`，交由用户或上一级流程决策。

## 3. 文件规则

只有 `Matter Note`、`Deliverable`、`Deep Case` 创建或复用事项文件夹：

```text
work/<date>_<本地化事项名>/
```

规则：

- 事项文件夹必须直接位于 `work/` 下。
- `<date>` 使用 `YYYY-MM-DD`。
- `<本地化事项名>` 跟随用户主语言，用 2-6 个关键词概括主题，避免真实姓名、身份证号、完整公司名、地址等敏感信息。
- 同一事项复用同一文件夹；不确定是否同一事项时，先在会话中说明判断并请求确认。
- 不提交 `work/` 下真实案件数据。

## 4. matter.md

`matter.md` 是默认唯一的持续记忆文件，替代普通任务里的 `plan.md`、`case.md`、`skill_outputs.md`、`analysis.md` 和 `advice.md`。

建议结构：

```markdown
# Matter

## Current Goal

## Jurisdiction And Stage

## Known Facts Or Clauses
| Item | Status: user-stated / evidenced / disputed / unknown | Evidence / Source | Impact |
|---|---|---|---|

## Core Issues Or Risks
| Issue | Why It Matters | Current View | Uncertainty |
|---|---|---|---|

## Evidence And Source Status

## Advice And Next Actions

## Update Log
| Date | New Input | Changed View | Next Step |
|---|---|---|---|
```

复杂案件需要更细文件时，再从 `matter.md` 拆出 `timeline.md`、`evidence.md`、`case_dashboard.md`、`hearing_playbook.md` 等。

## 5. 交付文件

用户明确要求文件时才生成 `<交付物>.md`。常见文件：

| 场景 | 交付文件 |
|---|---|
| 合同审查 | `合同审查意见.md` 或 `clause_review.md` |
| 合同起草 | `合同草案.md` 或 `contract_draft.md` |
| 法律研究 | `法律研究报告.md` |
| 函件/投诉/诉状框架 | `drafts.md` 或本地化文件名 |
| 阶段报告 | `<本地化主题>报告.md` |

PDF 只在用户明确要求 PDF、可下载 PDF 报告或阶段交付 PDF 时生成，并按 `docs/REPORT.md` 的 PDF 按需交付规则检查。

## 6. 来源规则

引用法律、案例、政策、网页或“已核验来源”时，必须说明来源状态。

- `Quick Answer`：可以在会话中列出来源；若没有检索，明确写“未核验/待核验”。
- 其他模式：创建或更新 `sources.md`。
- 涉及最新法规、期限、诉讼时效、证据规则、程序规则或具体法域规则时，优先使用官方或权威来源。
- 不能核验时，不得写成确定法律依据。

## 7. Deep Case 扩展

只有进入 `Deep Case` 时，才按需要使用以下文件：

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

`plan.md` 和 `skill_outputs.md` 不再是默认文件。仅在以下情况启用：

- 用户需要审计轨迹或团队协作状态。
- 事项进入长期、多轮、多人协作。
- 需要证明哪些分析镜头已执行、哪些被阻塞。

Deep Case 的报告或 PDF 交付必须吸收已存在的案件工作台、时间线、证据、来源、对方/裁判视角、庭审或策略文件；缺失项写入材料限制，不为凑结构新建空文件。

## 8. Blocked 返回

处理不了时不要硬做。使用以下结构返回：

```text
Blocked
- 原因：
- 缺少的信息/资源：
- 当前最多能做到：
- 需要用户或上一级流程决定：
```

常见阻塞：

- 法域、身份、程序阶段或目标缺失且会影响结论。
- 关键证据未提供。
- 需要最新法律/案例/政策但无法核验。
- PDF 或文件转换工具不可用。
- 用户目标存在违法、虚假陈述、非法取证或隐私侵害风险。

## 9. 会话回复

默认回复要让用户直接获得价值，而不是只列文件路径。根据任务复杂度展示：

- 核心结论或当前判断。
- 关键风险、争议焦点或条款问题。
- 证据缺口和来源核验状态。
- 最大风险。
- 下一步 1-3 项动作。
- 已生成/更新的文件路径。
- 若需要 PDF 报告，可以继续提出。
