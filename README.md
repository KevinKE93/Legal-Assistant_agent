# 法律助手智能体 Legal-Assistant_agent

![Language](https://img.shields.io/badge/language-中文%20%7C%20English-blue)
![Agent](https://img.shields.io/badge/type-Document%20Agent-green)
![Safety](https://img.shields.io/badge/safety-privacy--first-success)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> 一个干净、纯粹、可持续记录法律事项进展并生成最终交付文件的法律助手 Agent 工作流。

**作者：Kevin KE / [laoke.ai](https://laoke.ai)**

---

## 中文

### ⚖️ 这是什么

**法律助手智能体 Legal-Assistant_agent** 是一个面向法律纠纷、合同审查、合同起草、法律研究和文书准备的纯文档 Agent 工作流。它通过 `AGENTS.md` 指导 AI 助手逐层拆解事项：事实、证据、合同条款、争议焦点、法律路径、证明责任、对方视角、法官/审稿律师视角、风险、行动方案和最终交付文件。

它不是律师替代品，不承诺案件结果，也不会编造法律依据。它适合作为“法律问题整理、证据管理、合同风险审查、策略规划、文书准备、最终报告生成和持续复盘”的工作流助手。

### ✨ 核心能力

- **案件梳理**：法域、案件类型、程序阶段、角色、目标、期限
- **合同工作**：合同审查、条款风险、缺失条款、谈判点、合同草案
- **事实拆解**：区分事实、推测、评价和法律结论
- **争点分析**：事实争点、法律争点、证据争点、因果争点、程序争点
- **证据管理**：证据台账、证明对象、证据缺口和补强动作
- **法律分析**：请求权基础、证明责任、抗辩入口和不确定性
- **视角模拟**：对方视角、法官/仲裁员视角、调解视角
- **行动建议**：谈判、补证、投诉、仲裁、诉讼、答辩、庭审准备
- **最终交付**：基于工作底稿生成面向用户的最终分析报告、合同审查报告或合同草案
- **事项记忆**：同一法律事项只维护一个文件夹，持续更新 `plan.md` 和 `case.md`
- **i18n 准备**：文件夹名、最终文件名和正文语言默认跟随用户输入语言

### 🧭 工作流

```text
用户输入
→ 隐私与范围守门
→ 语言和事项类型识别
→ 事项文件夹创建或读取
→ plan.md 任务计划
→ case.md 事项记忆
→ 时间线/条款/证据台账
→ 争议焦点/条款风险与证明责任
→ 矛盾、因果、对方视角、法官视角
→ 官方来源检索
→ analysis.md 分析报告
→ advice.md 行动建议
→ 最终交付文件
→ 新证据/新进展后的复盘更新
```

### 📁 事项文件夹

复杂法律事项默认输出到：

```text
work/<date>_<localized-matter-name>/
```

示例：

```text
work/2026-05-10_劳动争议_拆分发薪加班费/
work/2026-05-10_contract-review_service-agreement/
```

默认文件：

| 文件 | 用途 |
|---|---|
| `plan.md` | 当前阶段、已完成、进行中、下一步、责任方、待补信息 |
| `case.md` | 事项摘要、事实/条款分层、争议焦点、证据状态、程序进展、关键结论 |
| `analysis.md` | 工作底稿型完整分析报告 |
| `advice.md` | 行动建议、谈判策略、维权路径和禁忌动作 |
| 本地化最终文件 | 面向用户交付的最终分析报告、合同审查报告、合同草案或研究备忘录 |

按需增加：

| 文件 | 用途 |
|---|---|
| `timeline.md` | 事件时间线 |
| `evidence.md` | 证据台账 |
| `sources.md` | 法规、案例、官方来源和引用风险 |
| `drafts.md` | 沟通函、投诉材料、起诉/答辩框架、庭审提纲 |
| `contract.md` | 合同背景、版本信息和条款摘要 |
| `clause_review.md` | 合同条款风险、修改建议和谈判点 |
| `contract_draft.md` | 合同或补充协议草案 |

### 🚀 如何使用

临时调用：

```text
请按照 Legal-Assistant_agent 的工作流分析下面这个法律事项，并把分析过程输出到事项文件夹，最后生成一份面向用户的最终文件。
```

全局或 `/` 指令调用：

```text
/legal-assistant 分析这个法律事项……
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

**Legal-Assistant_agent** is a document-first legal workflow agent for legal disputes, contract review, contract drafting, legal research, and legal-document preparation. It uses `AGENTS.md` as the main instruction entrypoint and guides an AI assistant to break a matter down into facts, evidence, contract clauses, issues, legal theories, burden of proof, opponent perspective, adjudicator/reviewer perspective, risk, practical next actions, and final deliverables.

It is not a lawyer replacement, does not promise outcomes, and must not fabricate legal authority. It is designed as a structured workflow for matter organization, evidence discipline, contract-risk review, legal research notes, drafting preparation, final report generation, and iterative review.

### ✨ Capabilities

- **Case intake**: jurisdiction, case type, procedural stage, party role, goal, and deadlines
- **Contract work**: contract review, clause risk, missing clauses, negotiation points, and draft agreements
- **Fact separation**: facts, assumptions, evaluations, and legal conclusions
- **Issue mapping**: factual, legal, evidentiary, causation, and procedural issues
- **Evidence work**: evidence ledger, proof targets, evidence gaps, and strengthening actions
- **Legal analysis**: claim basis, burden of proof, defenses, uncertainty, and verification needs
- **Perspective checks**: opponent view, judge/arbitrator view, mediation view
- **Action planning**: negotiation, evidence collection, complaint, arbitration, litigation, response, and hearing preparation
- **Final deliverables**: user-facing final reports, contract review reports, draft agreements, or legal research memos
- **Matter memory**: one folder per matter, continuously updated through `plan.md` and `case.md`
- **i18n-ready output**: folder names, final filenames, and document language follow the user's input language by default

### 🧭 Workflow

```text
User input
→ Privacy and scope guard
→ Language and matter-type routing
→ Create or read matter folder
→ plan.md task plan
→ case.md matter memory
→ Timeline / clause / evidence ledger
→ Issue map / clause risk and burden of proof
→ Contradiction, causation, opponent view, adjudicator view
→ Official-source research
→ analysis.md report
→ advice.md action guidance
→ Final deliverable
→ Review loop after new evidence or procedural events
```

### 📁 Matter Folder

Complex matters are written to:

```text
work/<date>_<localized-matter-name>/
```

Example:

```text
work/2026-05-10_劳动争议_拆分发薪加班费/
work/2026-05-10_contract-review_service-agreement/
```

Core files:

| File | Purpose |
|---|---|
| `plan.md` | Current stage, completed work, in-progress work, next actions, owners, open questions |
| `case.md` | Matter summary, fact/clause layers, issue map, evidence status, procedural progress, key conclusions |
| `analysis.md` | Full structured working analysis |
| `advice.md` | Practical action strategy, negotiation path, rights-protection routes, prohibited actions |
| Localized final file | User-facing final report, contract review report, contract draft, or legal research memo |

Optional files:

| File | Purpose |
|---|---|
| `timeline.md` | Event timeline |
| `evidence.md` | Evidence ledger |
| `sources.md` | Legal sources, official references, verification status, citation risk |
| `drafts.md` | Letters, complaints, claim/response outlines, hearing notes |
| `contract.md` | Contract background, version information, and clause summary |
| `clause_review.md` | Clause risks, proposed revisions, and negotiation points |
| `contract_draft.md` | Draft agreement or amendment |

### 🚀 How To Use

Temporary invocation:

```text
Use Legal-Assistant_agent to analyze this legal matter, create a matter folder, and generate a user-facing final deliverable.
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
