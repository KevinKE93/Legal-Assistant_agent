# 法律助手智能体 Legal-Assistant_agent

![Language](https://img.shields.io/badge/language-中文%20%7C%20English-blue)
![Agent](https://img.shields.io/badge/type-Document%20Agent-green)
![Safety](https://img.shields.io/badge/safety-privacy--first-success)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> 一个干净、纯粹、可持续记录案件进展的法律助手 Agent 工作流。

**作者：Kevin KE / [laoke.ai](https://laoke.ai)**

---

## 中文

### ⚖️ 这是什么

**法律助手智能体 Legal-Assistant_agent** 是一个面向法律纠纷场景的纯文档 Agent 工作流。它通过 `AGENTS.md` 指导 AI 助手逐层拆解案件：事实、证据、争议焦点、法律路径、证明责任、对方视角、法官视角、风险和行动方案。

它不是律师替代品，不承诺案件结果，也不会编造法律依据。它适合作为“法律问题整理、证据管理、策略规划、文书准备和持续复盘”的工作流助手。

### ✨ 核心能力

- **案件梳理**：法域、案件类型、程序阶段、角色、目标、期限
- **事实拆解**：区分事实、推测、评价和法律结论
- **争点分析**：事实争点、法律争点、证据争点、因果争点、程序争点
- **证据管理**：证据台账、证明对象、证据缺口和补强动作
- **法律分析**：请求权基础、证明责任、抗辩入口和不确定性
- **视角模拟**：对方视角、法官/仲裁员视角、调解视角
- **行动建议**：谈判、补证、投诉、仲裁、诉讼、答辩、庭审准备
- **案件记忆**：同一案件只维护一个文件夹，持续更新 `plan.md` 和 `case.md`

### 🧭 工作流

```text
用户输入
→ 隐私与范围守门
→ 案件文件夹创建或读取
→ plan.md 任务计划
→ case.md 案件记忆
→ 时间线与证据台账
→ 争议焦点与证明责任
→ 矛盾、因果、对方视角、法官视角
→ 官方来源检索
→ analysis.md 分析报告
→ advice.md 行动建议
→ 新证据/新进展后的复盘更新
```

### 📁 案件文件夹

复杂案件默认输出到：

```text
work/cases/<date>_<case-type>-<keywords>/
```

示例：

```text
work/cases/2026-05-10_labor-dispute-wage-overtime/
```

默认文件：

| 文件 | 用途 |
|---|---|
| `plan.md` | 当前阶段、已完成、进行中、下一步、责任方、待补信息 |
| `case.md` | 案情摘要、事实分层、争议焦点、证据状态、程序进展、关键结论 |
| `analysis.md` | 完整分析报告 |
| `advice.md` | 行动建议、谈判策略、维权路径和禁忌动作 |

按需增加：

| 文件 | 用途 |
|---|---|
| `timeline.md` | 事件时间线 |
| `evidence.md` | 证据台账 |
| `sources.md` | 法规、案例、官方来源和引用风险 |
| `drafts.md` | 沟通函、投诉材料、起诉/答辩框架、庭审提纲 |

### 🚀 如何使用

临时调用：

```text
请按照 Legal-Assistant_agent 的工作流分析下面这个案件，并把分析过程输出到案件文件夹。
```

全局或 `/` 指令调用：

```text
/legal-assistant 分析这个案件……
```

如果你的 AI 客户端支持自定义命令，可以把命令内容配置为“读取并遵循本仓库的 `AGENTS.md`”。本仓库不提供安装器，保持纯文档工作流。

### 🔎 官方来源检索

需要法律条文、案例、判决、司法解释或政策时，Agent 应优先使用官方或权威来源，并把来源写入 `sources.md`。

每条来源应记录：

- 标题
- 发布机构或数据库
- URL
- 访问日期
- 核验状态
- 可用规则
- 引用风险

### 🛡️ 安全边界

法律助手智能体不会：

- 替代律师或承诺案件结果
- 编造法条、案例、案号、法院、证据或法律依据
- 指导伪造、篡改、隐藏、销毁或歪曲证据
- 指导虚假陈述或诱导他人作虚假陈述
- 指导非法取证、盗号、定位、跟踪、骚扰、威胁或公开隐私
- 在未审查证据的情况下，把用户单方陈述当作已证明事实

涉及诉讼时效、程序期限、证据规则、最新法规和具体案件行动时，应以权威来源核验，并在必要时咨询相关法域的合格律师。

---

## English

### ⚖️ What It Is

**Legal-Assistant_agent** is a document-first legal workflow agent for legal-dispute analysis. It uses `AGENTS.md` as the main instruction entrypoint and guides an AI assistant to break a matter down into facts, evidence, issues, legal theories, burden of proof, opponent perspective, adjudicator perspective, risk, and practical next actions.

It is not a lawyer replacement, does not promise outcomes, and must not fabricate legal authority. It is designed as a structured workflow for case organization, evidence discipline, legal research notes, drafting preparation, and iterative review.

### ✨ Capabilities

- **Case intake**: jurisdiction, case type, procedural stage, party role, goal, and deadlines
- **Fact separation**: facts, assumptions, evaluations, and legal conclusions
- **Issue mapping**: factual, legal, evidentiary, causation, and procedural issues
- **Evidence work**: evidence ledger, proof targets, evidence gaps, and strengthening actions
- **Legal analysis**: claim basis, burden of proof, defenses, uncertainty, and verification needs
- **Perspective checks**: opponent view, judge/arbitrator view, mediation view
- **Action planning**: negotiation, evidence collection, complaint, arbitration, litigation, response, and hearing preparation
- **Case memory**: one folder per case, continuously updated through `plan.md` and `case.md`

### 🧭 Workflow

```text
User input
→ Privacy and scope guard
→ Create or read case folder
→ plan.md task plan
→ case.md case memory
→ Timeline and evidence ledger
→ Issue map and burden of proof
→ Contradiction, causation, opponent view, adjudicator view
→ Official-source research
→ analysis.md report
→ advice.md action guidance
→ Review loop after new evidence or procedural events
```

### 📁 Case Folder

Complex matters are written to:

```text
work/cases/<date>_<case-type>-<keywords>/
```

Example:

```text
work/cases/2026-05-10_labor-dispute-wage-overtime/
```

Core files:

| File | Purpose |
|---|---|
| `plan.md` | Current stage, completed work, in-progress work, next actions, owners, open questions |
| `case.md` | Case summary, fact layers, issue map, evidence status, procedural progress, key conclusions |
| `analysis.md` | Full structured legal analysis |
| `advice.md` | Practical action strategy, negotiation path, rights-protection routes, prohibited actions |

Optional files:

| File | Purpose |
|---|---|
| `timeline.md` | Event timeline |
| `evidence.md` | Evidence ledger |
| `sources.md` | Legal sources, official references, verification status, citation risk |
| `drafts.md` | Letters, complaints, claim/response outlines, hearing notes |

### 🚀 How To Use

Temporary invocation:

```text
Use Legal-Assistant_agent to analyze this dispute and create a case folder with plan.md, case.md, analysis.md, and advice.md.
```

Global or slash-command invocation:

```text
/legal-assistant analyze this dispute...
```

If your AI client supports custom commands, configure the command to read and follow this repository's `AGENTS.md`. This repository intentionally does not ship an installer; it stays as a pure document workflow.

### 🔎 Official-Source Research

When statutes, cases, judgments, judicial interpretations, or policy rules are needed, the agent should prioritize official or authoritative sources and write them to `sources.md`.

Each source should record:

- Title
- Publishing authority or database
- URL
- Access date
- Verification status
- Usable rule or holding
- Citation risk

### 🛡️ Safety

Legal-Assistant_agent must not:

- Replace a licensed lawyer or promise a case outcome
- Fabricate laws, cases, case numbers, courts, evidence, or legal authority
- Coach forged, altered, hidden, destroyed, or distorted evidence
- Coach false statements or induce others to make false statements
- Guide illegal evidence collection, account access, tracking, harassment, threats, or privacy exposure
- Treat one-sided user statements as proven facts without evidence review

For limitation periods, procedural deadlines, evidence rules, current law, and concrete case actions, verify with authoritative sources and consult a qualified lawyer in the relevant jurisdiction when needed.

## 作者 / Author

**Kevin KE**  
**laoke.ai**  
Website: [https://laoke.ai](https://laoke.ai)

## License / 许可证

MIT License. See `LICENSE` for details.
