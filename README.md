# 法律助手智能体 Legal-Assistant_agent

![Language](https://img.shields.io/badge/language-zh--CN%20%7C%20English-blue)
![Status](https://img.shields.io/badge/status-installable--agent--package-green)
![Safety](https://img.shields.io/badge/safety-privacy--first-green)
![Agent](https://img.shields.io/badge/agent-legal--analysis-purple)

**法律助手智能体 Legal-Assistant_agent** 是一套隐私优先、证据驱动、可安装的法律分析 Agent Package，面向纠纷分析、证据整理、官方来源检索、策略规划、文书起草、庭审准备和工作目录输出。

作者：**Kevin KE / [laoke.ai](https://laoke.ai)**

---

## 中文

### 项目概览

法律助手智能体 Legal-Assistant_agent 将用户提供的事实、证据、主张、约束条件和程序阶段，转化为结构化争点地图、证据台账、矛盾分析、因果链、官方来源检索记录、对方视角、法官视角和下一步行动方案。

它**不是律师替代品**，不承诺案件结果，也不输出未经核验的确定法律结论。它的定位是帮助用户更清楚地组织事实、更严格地管理证据、更稳妥地准备问题、文书和行动路径。

### 核心能力

- 隐私脱敏、法域确认和高风险请求守门
- 案件事实提取、时间线重构和证据台账生成
- 法律要件、证明责任、证明缺口和抗辩入口拆解
- 陈述、记录、时间线、金额和行为逻辑矛盾分析
- 行为、损害、替代原因和损害扩大之间的因果链分析
- 对方视角、法官视角和中立裁判者视角交叉评估
- 合法、克制、可记录的事实确认问题设计
- 谈判、投诉、调解、诉讼、仲裁和庭审策略规划
- 事实确认消息、催告函、投诉材料、起诉状/答辩状框架、证据目录和庭审提纲起草
- 官方法规、案例、判决和程序规则检索记录
- 将分析结果输出到指定案件工作目录

### Agent Workflow

```text
案件输入
→ 范围与隐私守门
→ 时间线和证据台账
→ 法律要件和证明责任矩阵
→ 矛盾分析和因果链审查
→ 官方来源检索，需要法律依据时触发
→ 对方视角和法官视角评估
→ 策略、文书或庭审准备
→ 工作目录输出
→ 新证据或新程序节点后的复盘迭代
```

| 阶段 | 智能体输出 |
|---|---|
| 案件输入 | 案件类型、法域、角色、目标、期限和现实约束 |
| 范围守门 | 安全边界、脱敏需求、缺失信息和高风险提示 |
| 证据映射 | 时间线、证据台账、证明对象和证据缺口 |
| 法律分析 | 法律要件、证明责任、争议焦点和不确定性 |
| 压力测试 | 矛盾点、因果风险、对方抗辩和法官视角弱点 |
| 官方检索 | 官方来源 URL、访问状态、检索记录和来源风险 |
| 交付输出 | 策略报告、事实确认问题、文书草稿、庭审提纲或案件工作目录 |
| 复盘迭代 | 更新后的事实、风险、证明缺口和下一步最小行动 |

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
| `case_reference_research` | 执行官方来源法规、案例、判决和裁判观点检索 |
| `strategy_risk_action` | 生成谈判、投诉、调解、诉讼等路径的行动方案 |
| `document_drafting` | 起草或审查法律相关沟通文本和程序材料框架 |
| `hearing_prep` | 准备调解、仲裁、庭审、质证和发问 |
| `review_learning_loop` | 在新证据或新进展后复盘并更新事实、争点、风险和策略 |

### 快速安装

克隆仓库后进入目录：

```bash
git clone https://github.com/KevinKE93/Legal-Assistant_agent.git
cd Legal-Assistant_agent
```

最简单安装方式，默认安装到 Codex：

```bash
./install.sh
```

也可以明确指定客户端：

```bash
./scripts/install.sh --client codex
./scripts/install.sh --client claude-code
./scripts/install.sh --client gemini-cli
./scripts/install.sh --client opencode
./scripts/install.sh --client openclaw
```

一次性安装到支持全局集成的客户端：

```bash
./scripts/install.sh --client all
```

Cursor 是项目级规则，建议在目标项目中安装：

```bash
./scripts/install.sh --client cursor --project-dir /path/to/your/project
```

查看所有支持项：

```bash
./scripts/install.sh --list-clients
```

### 支持的软件和安装方式

| 软件 | 安装命令 | 安装位置 | 使用方式 |
|---|---|---|---|
| OpenAI Codex / Codex CLI / Codex App | `./scripts/install.sh --client codex` | `${CODEX_HOME:-$HOME/.codex}/skills/legal-assistant-agent` | 重启 Codex 后，相关法律分析任务会触发该 skill |
| Claude Code | `./scripts/install.sh --client claude-code` | `~/.claude/skills/legal-assistant-agent` | 重启或刷新 Claude Code 后，可自动触发，也可用 `/legal-assistant-agent` |
| Cursor | `./scripts/install.sh --client cursor --project-dir /path/to/project` | `<project>/.cursor/rules/legal-assistant-agent.mdc` | 在目标项目中触发法律分析、检索或文书任务 |
| Gemini CLI | `./scripts/install.sh --client gemini-cli` | `~/.gemini/commands/legal-assistant.toml` | 在 Gemini CLI 执行 `/commands reload`，再用 `/legal-assistant <需求>` |
| OpenCode | `./scripts/install.sh --client opencode` | `~/.config/opencode/commands/legal-assistant.md` | 在 OpenCode 中用 `/legal-assistant <需求>` |
| OpenClaw | `./scripts/install.sh --client openclaw` | `~/.openclaw/skills/legal-assistant-agent` | 重启 OpenClaw 后，相关任务会加载该 skill |

说明：Codex、Claude Code、OpenClaw 支持 `SKILL.md` 风格的完整技能包；Cursor、Gemini CLI、OpenCode 通过规则或自定义命令接入，并引用同一份 Legal-Assistant_agent 包内容。

### 使用方式

运行校验和测试：

```bash
make test
python3 scripts/validate_skill.py
```

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

示例请求：

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

法律助手智能体不得：

- 替代律师或承诺案件结果
- 编造法条、案例、案号、法院、证据或法律依据
- 伪造、篡改、隐藏、销毁或歪曲证据
- 指导虚假陈述或诱导他人作虚假陈述
- 指导非法取证、盗号、定位、跟踪、骚扰、威胁或公开隐私
- 在未审查证据的情况下把用户单方陈述当作已证明事实

涉及具体法域、诉讼时效、程序期限、证据规则、最新法规和案例时，应以权威来源核验，或咨询相关法域的合格律师。

---

## English

### Overview

**法律助手智能体 Legal-Assistant_agent** is a privacy-first, evidence-driven, installable agent package for legal dispute analysis, evidence mapping, official-source legal research, strategy planning, legal-related drafting, hearing preparation, and workspace output.

It does **not** replace a licensed lawyer, promise legal outcomes, or generate unverified legal conclusions. It helps users organize facts, preserve evidence discipline, prepare better questions, draft safer documents, and plan practical next actions.

### Highlights

- Privacy and scope guardrails before legal analysis
- Fact extraction, timeline reconstruction, and evidence ledger generation
- Legal elements, burden of proof, proof gaps, and defense-entry mapping
- Contradiction analysis across statements, records, timelines, amounts, and behavior logic
- Causation-chain analysis with alternative causes and damage-scope review
- Opponent perspective, judge perspective, and neutral decision-maker review
- Lawful, restrained, and recordable factual-confirmation question design
- Strategy planning for negotiation, complaints, mediation, litigation, arbitration, and hearings
- Official-source research logs for laws, cases, judgments, and procedural rules
- Structured output bundles for case workspaces

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

### Install

Clone the repository:

```bash
git clone https://github.com/KevinKE93/Legal-Assistant_agent.git
cd Legal-Assistant_agent
```

Default Codex install:

```bash
./install.sh
```

Install for a specific client:

```bash
./scripts/install.sh --client codex
./scripts/install.sh --client claude-code
./scripts/install.sh --client gemini-cli
./scripts/install.sh --client opencode
./scripts/install.sh --client openclaw
```

Install global integrations at once:

```bash
./scripts/install.sh --client all
```

Install a Cursor project rule:

```bash
./scripts/install.sh --client cursor --project-dir /path/to/your/project
```

### Supported Clients

| Client | Command | Target | Usage |
|---|---|---|---|
| OpenAI Codex / Codex CLI / Codex App | `./scripts/install.sh --client codex` | `${CODEX_HOME:-$HOME/.codex}/skills/legal-assistant-agent` | Restart Codex and use legal-analysis requests |
| Claude Code | `./scripts/install.sh --client claude-code` | `~/.claude/skills/legal-assistant-agent` | Restart or refresh Claude Code, then use automatic triggering or `/legal-assistant-agent` |
| Cursor | `./scripts/install.sh --client cursor --project-dir /path/to/project` | `<project>/.cursor/rules/legal-assistant-agent.mdc` | Use legal analysis, research, or drafting requests in that project |
| Gemini CLI | `./scripts/install.sh --client gemini-cli` | `~/.gemini/commands/legal-assistant.toml` | Run `/commands reload`, then `/legal-assistant <request>` |
| OpenCode | `./scripts/install.sh --client opencode` | `~/.config/opencode/commands/legal-assistant.md` | Use `/legal-assistant <request>` |
| OpenClaw | `./scripts/install.sh --client openclaw` | `~/.openclaw/skills/legal-assistant-agent` | Restart OpenClaw and use legal-analysis requests |

### Official-Source Research

Use `scripts/legal_research.py` for statutes, cases, judgments, and procedural rules. The script prioritizes jurisdiction-specific official sources from `references/official_source_registry.json`, supports external providers through environment variables, filters results back to official domains, and writes auditable files.

```bash
python3 scripts/legal_research.py \
  --jurisdiction US-FEDERAL \
  --query "late delivery contract damages" \
  --case-type contract \
  --out-dir work/research/us-contract \
  --max-results 8
```

Supported providers: `auto`, `official`, `bing`, `duckduckgo`, `brave`, `tavily`, and `serpapi`.

### Case Workspace Output

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

The agent must not:

- replace a licensed lawyer or promise an outcome
- fabricate laws, cases, case numbers, courts, evidence, or authorities
- forge, alter, hide, destroy, or misrepresent evidence
- coach false statements or induce another person to make false statements
- guide illegal evidence collection, account intrusion, tracking, harassment, threats, or privacy exposure
- treat user-provided facts as proven without evidence review

For jurisdiction-specific law, limitation periods, procedural deadlines, evidence rules, current regulations, and case law, users should verify against authoritative sources or consult a qualified local lawyer.

## 项目状态 / Project Status

法律助手智能体 Legal-Assistant_agent 已支持可安装入口、校验测试、官方来源检索工具、多客户端适配和工作目录输出。后续可以继续增强：

- 增加更多法域的官方检索适配器
- 增加 PDF、DOCX、截图和聊天记录的文档导入与脱敏工具
- 在每个分析产物中加入更完整的结构化 citation 对象

## 作者 / Author

**Kevin KE**  
**laoke.ai**  
Website: [https://laoke.ai](https://laoke.ai)

## 免责声明 / Disclaimer

本项目只提供通用法律分析工作流支持，不提供法律代理服务，不构成律师-客户关系，也不能替代相关法域合格律师的专业意见。

This project provides general legal analysis workflow support. It does not provide legal representation, does not create an attorney-client relationship, and does not replace advice from a qualified lawyer in the relevant jurisdiction.

## 开发流程 / Development Workflow

日常修改默认提交到 `dev` 分支，并推送到 `dev`。

Use `dev` as the default branch for ongoing changes. Push normal iterations to `dev`.

`main` 仅用于明确要求合并或发布时更新；没有维护者明确要求时，不直接推送到 `main`。

`main` is reserved for explicit release or merge requests. Do not push to `main` unless the maintainer asks to merge or publish.

重大或高风险改动应先建立独立 feature/backup 分支，通过校验后再合回 `dev`。

For major or risky changes, create a separate feature or backup branch first, then merge back into `dev` after validation.

## 贡献 / Contributing

贡献内容应保留本项目的安全边界：

- 不添加编造的法律依据或不可核验的示例事实
- 后续测试夹具必须保持隐私安全和抽象化
- 明确标记任何法域特定内容
- 优先使用模板、清单和验证流程，而不是无依据结论

Contributions should preserve the safety model:

- Do not add fabricated legal authorities or unverifiable demo facts.
- Keep any future fixtures privacy-safe and generic.
- Mark jurisdiction-specific content clearly.
- Prefer templates, checklists, and verification workflows over unsupported conclusions.

## License / 许可证

This project is released under the MIT License. See `LICENSE` for details.

本项目采用 MIT License。详情见 `LICENSE` 文件。
