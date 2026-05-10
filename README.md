# Legal Assistant Agent Skill Pack

![Language](https://img.shields.io/badge/language-zh--CN%20%7C%20English-blue)
![Status](https://img.shields.io/badge/status-installable--skill-green)
![Safety](https://img.shields.io/badge/safety-privacy--first-green)
![Agent](https://img.shields.io/badge/agent-legal--analysis-purple)

**A privacy-first, evidence-driven legal analysis agent skill pack for dispute strategy, document drafting, hearing preparation, and Codex-style skill workflows.**

**一套隐私优先、证据驱动的法律分析 Agent Skill Pack，面向纠纷策略、文书起草、庭审准备和 Codex Skill 工作流。**

Author: **Kevin KE / [laoke.ai](https://laoke.ai)**

---

## English

### Overview

Legal Assistant Agent Skill Pack is a modular workflow system for legal dispute analysis. It turns user-provided facts, evidence, claims, constraints, and procedural context into structured issue maps, evidence ledgers, contradiction analysis, causation chains, official-source research logs, opponent-view simulations, judge-view reviews, and practical next steps.

It does **not** replace a licensed lawyer, promise legal outcomes, or generate unverified legal conclusions. It is designed to help users reason more clearly, preserve evidence discipline, and prepare better questions, documents, and action plans.

### Highlights

- Privacy and scope guardrails before any legal analysis
- Fact extraction, timeline reconstruction, and evidence ledger generation
- Legal elements, burden of proof, proof gaps, and defense-entry mapping
- Contradiction analysis across statements, records, timelines, amounts, and behavior logic
- Causation-chain analysis with alternative causes and damage-scope review
- Opponent perspective, judge perspective, and neutral decision-maker review
- Lawful, restrained, and recordable question design for factual confirmation
- Strategy planning for negotiation, complaints, mediation, litigation, and hearings
- Drafting support for confirmation messages, demand letters, complaints, pleadings, evidence lists, and hearing outlines
- Iteration loop for new evidence, new statements, and new procedural events
- Installable Codex skill entrypoint, validation scripts, and case-workspace output tooling

### Method Wheel

```text
Scope Guard
→ Fact Reconstruction
→ Issue Mapping
→ Evidence Mapping
→ Contradiction Testing
→ Causation Analysis
→ Opponent Perspective
→ Judge Perspective
→ Strategy And Action
→ Review And Iteration
```

Every round should preserve:

- confirmed facts
- facts still requiring proof
- evidence sources
- likely opponent defenses
- risk level
- smallest useful next action

### Skill Modules

| Module | Purpose |
|---|---|
| `privacy_scope_guard` | Privacy redaction, jurisdiction check, scope boundary, and high-risk request filtering |
| `case_intake_issue_map` | Converts user narratives into facts, procedural context, goals, and issue maps |
| `timeline_evidence_ledger` | Builds timelines, fact tables, and evidence ledgers |
| `elements_burden_matrix` | Maps legal elements, burden of proof, factual basis, and evidence gaps |
| `contradiction_analysis` | Finds contradictions across statements, evidence, timelines, and logic |
| `causation_chain` | Analyzes conduct, harm, alternative causes, and damage expansion |
| `admission_question_design` | Designs lawful, restrained, recordable factual-confirmation questions |
| `opponent_perspective` | Simulates opponent defenses, evidence attacks, and negotiation leverage |
| `judge_perspective` | Reviews claim clarity, proof closure, credibility, and enforceability |
| `case_reference_research` | Designs research workflows for statutes, cases, and reasoning patterns |
| `strategy_risk_action` | Generates action plans across negotiation, complaints, mediation, and litigation |
| `document_drafting` | Drafts or reviews legal-related messages, letters, complaints, pleadings, and evidence lists |
| `hearing_prep` | Prepares mediation, arbitration, trial, cross-examination, and questioning |
| `review_learning_loop` | Updates facts, issues, risks, and strategy after new evidence or events |

### Agent Workflow

```text
Intake
→ Scope and privacy guard
→ Timeline and evidence ledger
→ Legal elements and burden matrix
→ Contradiction and causation review
→ Official-source research, when legal authority is needed
→ Opponent and judge perspective checks
→ Strategy, drafting, or hearing preparation
→ Workspace output bundle
→ Review loop after new evidence or procedural events
```

| Stage | Agent output |
|---|---|
| Intake | Case type, jurisdiction, role, goals, deadlines, and known constraints |
| Scope guard | Safety boundary, privacy redaction needs, missing context, and high-risk flags |
| Evidence map | Timeline, evidence ledger, proof targets, and evidence gaps |
| Legal analysis | Elements, burden of proof, disputed issues, and uncertainty notes |
| Stress test | Contradictions, causation risks, opponent defenses, and judge-view weaknesses |
| Research | Official-source research log with URLs, access status, and source risk notes |
| Delivery | Strategy report, factual questions, draft document, hearing outline, or saved case workspace |
| Iteration | Updated facts, updated risks, new proof gaps, and next smallest useful action |

### Quick Start

Install this repository as a local Codex skill:

```bash
./scripts/install.sh
```

Validate the package:

```bash
make test
```

Use the files in `prompts/` as the instruction layer:

- `prompts/system_prompt.md` defines the assistant role and legal safety boundary.
- `prompts/developer_prompt.md` defines behavior constraints and output quality rules.
- `prompts/output_schemas.md` provides reusable response structures.

Then attach the relevant `skills/*/SKILL.md` module for the task.

Recommended default flow:

```text
privacy_scope_guard
→ case_intake_issue_map
→ timeline_evidence_ledger
→ elements_burden_matrix
→ contradiction_analysis
→ causation_chain
→ opponent_perspective
→ judge_perspective
→ admission_question_design
→ strategy_risk_action
→ document_drafting / hearing_prep
→ review_learning_loop
```

### Example Requests

- "Turn this dispute into a timeline and evidence table."
- "What evidence is currently missing?"
- "Find contradictions in the other party's statements."
- "Design lawful questions that ask the other party to confirm key facts."
- "Review this dispute from a judge's perspective."
- "Draft a factual confirmation letter, demand letter, or complaint."
- "New evidence arrived. Re-evaluate the strategy."

### Networked Legal Research

For statutes, cases, judgments, and procedural rules, use `scripts/legal_research.py`. The script prioritizes jurisdiction-specific official sources from `references/official_source_registry.json`, supports external providers through environment variables, and writes auditable output files.

```bash
python3 scripts/legal_research.py \
  --jurisdiction US-FEDERAL \
  --query "late delivery contract damages" \
  --case-type contract \
  --out-dir work/research/us-contract \
  --max-results 8
```

Supported providers:

- `auto`: tries source-native public endpoints first, then configured API providers, then Bing RSS and DuckDuckGo
- `official`: uses source-native public endpoints where available, currently UK Legislation Atom feeds and The National Archives Find Case Law Atom feed
- `bing`: no API key required; filters returned URLs back to the official source domain
- `duckduckgo`: no API key required, but may return automated-traffic challenges in some environments
- `brave`: requires `BRAVE_SEARCH_API_KEY`
- `tavily`: requires `TAVILY_API_KEY`
- `serpapi`: requires `SERPAPI_API_KEY`

Outputs include `research_log.md`, `results.json`, and optional retrieved snippets. Search results are filtered against the selected official source domain; if no official-domain result is returned, the log records a `not_found_or_unverified` entry with a manual search URL.

### Case Workspace Outputs

To save an analysis bundle to a folder:

```bash
python3 scripts/write_analysis_output.py \
  --out-dir work/cases \
  --case-slug demo-contract \
  --analysis-file analysis.md \
  --metadata jurisdiction=CN \
  --metadata case_type=contract
```

The bundle contains `INDEX.md`, `analysis.md`, `metadata.json`, and any additional artifacts passed with `--artifact`.

### Safety Model

The assistant must not:

- replace a licensed lawyer or promise an outcome
- fabricate laws, cases, case numbers, courts, evidence, or authorities
- forge, alter, hide, destroy, or misrepresent evidence
- coach false statements or induce another person to make false statements
- guide illegal evidence collection, account intrusion, tracking, harassment, threats, or privacy exposure
- treat user-provided facts as proven without evidence review

For jurisdiction-specific law, limitation periods, procedural deadlines, evidence rules, current regulations, and case law, users should verify against authoritative sources or consult a qualified local lawyer.

---

## 中文

### 项目概览

Legal Assistant Agent Skill Pack 是一套模块化法律纠纷分析工作流。它把用户提供的事实、证据、主张、约束条件和程序阶段，转化为结构化争点地图、证据台账、矛盾分析、因果链、官方来源检索记录、对方视角、法官视角和下一步行动方案。

它**不是律师替代品**，不承诺案件结果，也不输出未经核验的确定法律结论。它的定位是帮助用户更清楚地组织事实、更严格地管理证据、更稳妥地准备问题、文书和行动路径。

### 核心能力

- 在任何法律分析前进行隐私脱敏和范围守门
- 提取事实、重构时间线、生成证据台账
- 拆解法律要件、证明责任、证据缺口和抗辩入口
- 分析陈述、记录、时间线、金额和行为逻辑中的矛盾
- 梳理行为、损害、替代原因和损害扩大之间的因果关系
- 从对方代理人、法官、仲裁员或调解员视角交叉评估
- 设计合法、克制、可记录的事实确认问题
- 生成谈判、投诉、调解、诉讼、庭审等路径的策略方案
- 支持事实确认消息、催告函、投诉材料、起诉状/答辩状框架、证据目录和庭审提纲
- 在出现新证据、新陈述、新程序节点后进行复盘迭代
- 支持本地安装、校验测试、联网官方来源检索和输出到指定工作目录

### 方法轮

```text
范围约束
→ 事实还原
→ 争点拆解
→ 证据映射
→ 矛盾测试
→ 因果推论
→ 对方视角
→ 法官视角
→ 策略行动
→ 复盘迭代
```

每一轮分析都应保留：

- 已确认事实
- 待证明事实
- 证据来源
- 对方可能抗辩
- 风险等级
- 下一步最小行动

### 技能模块

| 模块 | 用途 |
|---|---|
| `privacy_scope_guard` | 隐私脱敏、法域确认、范围边界和高风险请求过滤 |
| `case_intake_issue_map` | 将用户叙述转化为事实、程序信息、诉求目标和争点地图 |
| `timeline_evidence_ledger` | 构建时间线、事实表和证据台账 |
| `elements_burden_matrix` | 拆解法律要件、证明责任、事实基础和证据缺口 |
| `contradiction_analysis` | 识别陈述、证据、时间线和行为逻辑之间的矛盾 |
| `causation_chain` | 分析行为、损害、替代原因和损害扩大因素 |
| `admission_question_design` | 设计合法、克制、可记录的事实确认问题 |
| `opponent_perspective` | 模拟对方抗辩、证据攻击和谈判筹码 |
| `judge_perspective` | 从裁判者视角评估请求清晰度、证据闭环和可执行性 |
| `case_reference_research` | 设计法规、案例和裁判观点的检索学习流程 |
| `strategy_risk_action` | 生成谈判、投诉、调解、诉讼等路径的行动方案 |
| `document_drafting` | 起草或审查法律相关沟通文本和程序材料框架 |
| `hearing_prep` | 准备调解、仲裁、庭审、质证和发问 |
| `review_learning_loop` | 在新证据或新进展后复盘并更新事实、争点、风险和策略 |

### 使用方式

安装为本地 Codex skill：

```bash
./scripts/install.sh
```

运行校验和测试：

```bash
make test
```

将 `prompts/` 目录作为基础指令层：

- `prompts/system_prompt.md`：定义助手角色和法律安全边界
- `prompts/developer_prompt.md`：定义行为约束和输出质量规则
- `prompts/output_schemas.md`：提供常用输出结构

然后根据任务选择对应的 `skills/*/SKILL.md` 模块。

推荐默认流程：

```text
privacy_scope_guard
→ case_intake_issue_map
→ timeline_evidence_ledger
→ elements_burden_matrix
→ contradiction_analysis
→ causation_chain
→ opponent_perspective
→ judge_perspective
→ admission_question_design
→ strategy_risk_action
→ document_drafting / hearing_prep
→ review_learning_loop
```

也可以把 `templates/` 作为人工法律分析工作台使用：

1. 填写 `templates/case_brief_template.md`。
2. 建立时间线和证据台账。
3. 完成矛盾矩阵和因果链。
4. 输出法官视角报告和策略报告。
5. 每次出现新证据或新陈述后重新运行复盘流程。

### 示例请求

- “帮我把这个纠纷整理成时间线和证据表。”
- “帮我看我现在最缺哪几类证据。”
- “帮我找对方陈述里的矛盾点。”
- “帮我设计几个合法、克制的问题，让对方确认关键事实。”
- “从法官视角看，这个案子最容易被质疑的地方是什么？”
- “帮我写一版事实确认函、催告函或投诉材料。”
- “有新证据了，帮我重新评估策略。”

### 联网法律检索

法规、案例、判决和程序规则检索使用 `scripts/legal_research.py`。脚本会根据 `references/official_source_registry.json` 优先选择对应法域的官方来源，并将检索记录写入可审计文件。

```bash
python3 scripts/legal_research.py \
  --jurisdiction CN \
  --query "合同 迟延履行 退款 催告" \
  --case-type "合同纠纷" \
  --out-dir work/research/cn-contract \
  --max-results 8
```

可选外部检索工具：

- `auto`：优先使用官方来源公开接口，再使用已配置的 API provider，最后回退到 Bing RSS 和 DuckDuckGo
- `official`：优先调用官方来源公开接口；当前支持 UK Legislation Atom feeds 和 The National Archives Find Case Law Atom feed
- `bing`：不需要 API key；会把结果过滤回对应官方来源域名
- `duckduckgo`：不需要 API key，但某些环境可能触发自动流量验证
- `brave`：需要 `BRAVE_SEARCH_API_KEY`
- `tavily`：需要 `TAVILY_API_KEY`
- `serpapi`：需要 `SERPAPI_API_KEY`

输出包括 `research_log.md`、`results.json` 和可选网页摘要。检索结果会按官方来源域名过滤；如果没有返回官方域名内的结果，日志会写入 `not_found_or_unverified` 记录和人工检索 URL。

### 输出到案件工作目录

将分析结果保存到指定目录：

```bash
python3 scripts/write_analysis_output.py \
  --out-dir work/cases \
  --case-slug demo-contract \
  --analysis-file analysis.md \
  --metadata jurisdiction=CN \
  --metadata case_type=contract
```

输出包包含 `INDEX.md`、`analysis.md`、`metadata.json`，以及通过 `--artifact` 指定的其他文件。

### 安全边界

助手不得：

- 替代律师或承诺案件结果
- 编造法条、案例、案号、法院、证据或法律依据
- 伪造、篡改、隐藏、销毁或歪曲证据
- 指导虚假陈述或诱导他人作虚假陈述
- 指导非法取证、盗号、定位、跟踪、骚扰、威胁或公开隐私
- 在未审查证据的情况下把用户单方陈述当作已证明事实

涉及具体法域、诉讼时效、程序期限、证据规则、最新法规和案例时，应以权威来源核验，或咨询相关法域的合格律师。

---

## Project Status / 项目状态

This repository is now an installable skill-pack with validation, official-source research tooling, and workspace output support. The content layer is ready for prompt/workflow use, while the following engineering tasks remain open.

本仓库现在已经具备可安装 skill 入口、校验测试、官方来源检索工具和工作目录输出能力。内容层已可作为提示词和工作流材料使用，后续还可以继续工程化。

- Add deeper jurisdiction-specific research adapters without hardcoding unverified legal conclusions.
- Add document ingestion and redaction helpers for PDFs, DOCX, screenshots, and chat exports.
- Add structured citation objects across every downstream analysis artifact.

## Author / 作者

**Kevin KE**  
**laoke.ai**  
Website: [https://laoke.ai](https://laoke.ai)

## Disclaimer / 免责声明

This project provides general legal analysis workflow support. It does not provide legal representation, does not create an attorney-client relationship, and does not replace advice from a qualified lawyer in the relevant jurisdiction.

本项目只提供通用法律分析工作流支持，不提供法律代理服务，不构成律师-客户关系，也不能替代相关法域合格律师的专业意见。

## Development Workflow / 开发流程

Use `dev` as the default branch for ongoing changes. Push normal iterations to `dev`.

日常修改默认提交到 `dev` 分支，并推送到 `dev`。

`main` is reserved for explicit release or merge requests. Do not push to `main` unless the maintainer asks to merge or publish.

`main` 仅用于明确要求合并或发布时更新；没有维护者明确要求时，不直接推送到 `main`。

For major or risky changes, create a separate feature or backup branch first, then merge back into `dev` after validation.

重大或高风险改动应先建立独立 feature/backup 分支，通过校验后再合回 `dev`。

## Contributing / 贡献

Contributions should preserve the safety model:

贡献内容应保留本项目的安全边界：

- Do not add fabricated legal authorities or unverifiable demo facts.
- Keep any future fixtures privacy-safe and generic.
- Mark jurisdiction-specific content clearly.
- Prefer templates, checklists, and verification workflows over unsupported conclusions.

## License / 许可证

This project is released under the MIT License. See `LICENSE` for details.

本项目采用 MIT License。详情见 `LICENSE` 文件。
