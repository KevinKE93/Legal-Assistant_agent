# 输出模板总览

本文件提供 Legal-Assistant_agent 的可复用输出结构。默认使用最小模板；只有用户要求报告、PDF 或复杂案件协作时，才使用更重的模板。

## 0. 通用规则

- 默认使用用户输入的主语言输出标题、表格字段、文件夹名和报告文件名。
- 用户只要答案时，不创建文件。
- 需要持续记忆或文件交付时，事项目录为 `work/<date>_<本地化事项名>/`，并直接位于 `work/` 下。
- 默认持续记忆文件是 `matter.md`。
- `plan.md`、`case.md`、`skill_outputs.md` 只在长期协作、审计追踪、团队交接或用户明确要求时启用。
- 引用法律、案例、政策、网页或“已核验来源”时，必须说明来源状态；非 Quick Answer 模式下写入 `sources.md`。
- Markdown 报告只在用户要求报告文件、阶段交付或归档时输出。
- PDF 报告只在用户明确要求 PDF 时输出，且必须先渲染为可读版式；无法生成或质量不合格时标记 blocked。

## 1. matter.md 模板

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

## 2. Quick Answer 模板

```markdown
## 核心判断

## 关键依据

## 不确定性与证据缺口

## 来源状态

## 最大风险

## 下一步
1.
2.
3.
```

## 3. Blocked 模板

```markdown
## Blocked

- 原因：
- 缺少的信息/资源：
- 当前最多能做到：
- 需要用户或上一级流程决定：
```

## 4. 合同审查意见模板

```markdown
# 合同审查意见

## 1. 审查范围

## 2. 核心结论

## 3. 重点风险
| 条款/事项 | 风险等级 | 问题 | 建议改法 |
|---|---|---|---|

## 4. 缺失或需补充条款

## 5. 谈判优先级

## 6. 签署前核验清单

## 7. 来源与限制
```

## 5. 合同草案模板

```markdown
# 合同草案

## 1. 交易结构

## 2. 核心条款

## 3. 风险分配

## 4. 可谈判条款

## 5. 签署前核验清单

## 6. 待确认事项
```

## 6. 文书草稿模板

```markdown
# 文书草稿

## 1. 用途与对象

## 2. 事实基础

## 3. 请求或主张

## 4. 正文草稿

## 5. 表达风险

## 6. 使用前核验
```

## 7. 来源记录模板

```markdown
# Sources

| ID | Title | Institution / Source | URL | Access Date | Verification Status | Useful Rule | Citation Risk |
|---|---|---|---|---|---|---|---|
```

## 8. Deep Case 可选模板

复杂纠纷、仲裁、诉讼、听证或长期案件才使用以下文件。

### case_dashboard.md

```markdown
# 案件驾驶舱

## 一句话案件地图

## 程序状态

## 关键判断变量
| 关键问题 | 为什么关键 | 当前证据状态 | 最大风险 |
|---|---|---|---|

## 争议焦点关系图
| 层级 | 争议焦点 | 依赖事实 | 影响 |
|---|---|---|---|

## 证明责任与证据缺口
| 要证明什么 | 责任方 | 现有证据 | 缺口 | 风险 |
|---|---|---|---|---|
```

### hearing_playbook.md

```markdown
# 庭审/听证准备

## 目标

## 举证顺序

## 质证意见

## 合法发问清单

## 可能追问与回答边界
```
