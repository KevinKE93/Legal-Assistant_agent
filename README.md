# 法律助手智能体 Legal-Assistant_agent

![Language](https://img.shields.io/badge/language-中文%20%7C%20English-blue)
![Package](https://img.shields.io/badge/package-Agent%20Skill-green)
![Safety](https://img.shields.io/badge/safety-privacy--first-success)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> 面向法律纠纷场景的可安装 Agent Package：把事实、证据、法律检索、策略和文书准备整理成可复用的专业工作流。

**作者：Kevin KE / [laoke.ai](https://laoke.ai)**

---

## 中文

### ⚖️ 这是什么

**法律助手智能体 Legal-Assistant_agent** 是一个隐私优先、证据驱动的法律分析智能体包。它用于辅助整理纠纷事实、建立证据台账、发现矛盾点、检索官方法律来源、生成策略方案，并将分析结果输出到指定工作目录。

它不是律师替代品，不承诺案件结果，也不会编造法律依据。它更适合作为“法律问题整理、证据管理、文书准备和行动规划”的智能工作台。

### ✨ 核心能力

- **案件梳理**：法域、案件类型、角色、目标、期限、事实和证据归纳
- **证据管理**：时间线、证据台账、证明对象、证据缺口和补强方向
- **法律分析**：法律要件、证明责任、争点、抗辩入口和不确定性
- **矛盾审查**：陈述、证据、时间线、金额和行为逻辑交叉校验
- **视角模拟**：对方视角、法官视角、调解/仲裁视角风险评估
- **官方检索**：优先检索对应法域的官方法规、案例、判决和程序规则
- **文书辅助**：事实确认函、催告函、投诉材料、诉讼/答辩框架、证据目录、庭审提纲
- **结果落盘**：把分析结果、元数据和补充材料输出到案件工作目录

### 🧭 Agent Workflow

```text
案件输入
→ 范围与隐私守门
→ 时间线和证据台账
→ 法律要件与证明责任矩阵
→ 矛盾分析与因果链审查
→ 官方来源检索
→ 对方视角与法官视角评估
→ 策略、文书或庭审准备
→ 输出到案件工作目录
→ 新证据/新程序节点后的复盘迭代
```

| 阶段 | 产物 |
|---|---|
| 范围守门 | 法域、案件类型、风险等级、隐私脱敏要求 |
| 事实整理 | 时间线、事实清单、争议事实、待证明事实 |
| 证据映射 | 证据台账、证明对象、证据缺口、补证建议 |
| 法律分析 | 要件矩阵、证明责任、抗辩入口、不确定性 |
| 压力测试 | 矛盾点、因果风险、对方攻击路径、法官视角弱点 |
| 官方检索 | 检索记录、官方 URL、访问状态、来源风险 |
| 行动输出 | 策略方案、问题清单、文书草稿、庭审提纲、工作目录 |

### 🚀 快速安装

```bash
git clone https://github.com/KevinKE93/Legal-Assistant_agent.git
cd Legal-Assistant_agent
./install.sh
```

默认安装到 Codex。安装其他客户端：

```bash
./scripts/install.sh --client codex
./scripts/install.sh --client claude-code
./scripts/install.sh --client gemini-cli
./scripts/install.sh --client opencode
./scripts/install.sh --client openclaw
./scripts/install.sh --client cursor --project-dir /path/to/project
```

一次性安装到支持全局集成的客户端：

```bash
./scripts/install.sh --client all
```

查看支持项：

```bash
./scripts/install.sh --list-clients
```

### 🧩 支持的软件

| 软件 | 安装命令 | 使用方式 |
|---|---|---|
| OpenAI Codex / Codex CLI / Codex App | `./scripts/install.sh --client codex` | 重启 Codex 后，直接提出法律分析类需求 |
| Claude Code | `./scripts/install.sh --client claude-code` | 重启/刷新 Claude Code，可自动触发或使用 `/legal-assistant-agent` |
| Cursor | `./scripts/install.sh --client cursor --project-dir /path/to/project` | 在目标项目中触发法律分析、检索或文书任务 |
| Gemini CLI | `./scripts/install.sh --client gemini-cli` | 执行 `/commands reload` 后使用 `/legal-assistant <需求>` |
| OpenCode | `./scripts/install.sh --client opencode` | 使用 `/legal-assistant <需求>` |
| OpenClaw | `./scripts/install.sh --client openclaw` | 重启 OpenClaw 后触发法律分析类任务 |

### 🔎 官方来源检索

```bash
python3 scripts/legal_research.py \
  --jurisdiction CN \
  --query "合同 迟延履行 退款 催告" \
  --case-type "合同纠纷" \
  --out-dir work/research/cn-contract \
  --max-results 8
```

支持 provider：`auto`、`official`、`bing`、`duckduckgo`、`brave`、`tavily`、`serpapi`。

检索结果会写入 `research_log.md` 和 `results.json`。脚本会按官方来源域名过滤结果；如果没有返回官方域名内的结果，会记录 `not_found_or_unverified`，避免把泛搜索内容误当作法律依据。

### 📁 输出到案件工作目录

```bash
python3 scripts/write_analysis_output.py \
  --out-dir work/cases \
  --case-slug demo-contract \
  --analysis-file analysis.md \
  --metadata jurisdiction=CN \
  --metadata case_type=contract
```

输出包包含：

- `INDEX.md`
- `analysis.md`
- `metadata.json`
- 通过 `--artifact` 指定的其他材料

### ✅ 可用性检查

```bash
python3 scripts/validate_skill.py
```

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

**法律助手智能体 Legal-Assistant_agent** is an installable, privacy-first legal analysis agent package. It helps organize dispute facts, map evidence, identify contradictions, run official-source legal research, prepare strategy and drafting outputs, and save structured results into a case workspace.

It does **not** replace a licensed lawyer, promise outcomes, or fabricate legal authority. It is designed as a practical workbench for legal issue organization, evidence discipline, drafting preparation, and action planning.

### ✨ Capabilities

- Case intake, jurisdiction and scope checks
- Timeline reconstruction and evidence ledger generation
- Legal elements, burden of proof, proof gaps, and defense mapping
- Contradiction and causation analysis
- Opponent-view and judge-view review
- Official-source research for laws, cases, judgments, and procedural rules
- Legal-related drafting and hearing preparation
- Structured workspace output

### 🧭 Agent Workflow

```text
Intake
→ Scope and privacy guard
→ Timeline and evidence ledger
→ Legal elements and burden matrix
→ Contradiction and causation review
→ Official-source research
→ Opponent and judge perspective checks
→ Strategy, drafting, or hearing preparation
→ Case workspace output
→ Review loop after new evidence or procedural events
```

### 🚀 Install

```bash
git clone https://github.com/KevinKE93/Legal-Assistant_agent.git
cd Legal-Assistant_agent
./install.sh
```

Install for a specific client:

```bash
./scripts/install.sh --client codex
./scripts/install.sh --client claude-code
./scripts/install.sh --client gemini-cli
./scripts/install.sh --client opencode
./scripts/install.sh --client openclaw
./scripts/install.sh --client cursor --project-dir /path/to/project
```

### 🧩 Supported Clients

| Client | Command | Usage |
|---|---|---|
| OpenAI Codex / Codex CLI / Codex App | `./scripts/install.sh --client codex` | Restart Codex and ask for legal-analysis help |
| Claude Code | `./scripts/install.sh --client claude-code` | Restart/refresh Claude Code or use `/legal-assistant-agent` |
| Cursor | `./scripts/install.sh --client cursor --project-dir /path/to/project` | Use legal analysis, research, or drafting requests in that project |
| Gemini CLI | `./scripts/install.sh --client gemini-cli` | Run `/commands reload`, then `/legal-assistant <request>` |
| OpenCode | `./scripts/install.sh --client opencode` | Use `/legal-assistant <request>` |
| OpenClaw | `./scripts/install.sh --client openclaw` | Restart OpenClaw and ask for legal-analysis help |

### 🔎 Official-Source Research

```bash
python3 scripts/legal_research.py \
  --jurisdiction US-FEDERAL \
  --query "late delivery contract damages" \
  --case-type contract \
  --out-dir work/research/us-contract \
  --max-results 8
```

Supported providers: `auto`, `official`, `bing`, `duckduckgo`, `brave`, `tavily`, and `serpapi`.

### 📁 Case Workspace Output

```bash
python3 scripts/write_analysis_output.py \
  --out-dir work/cases \
  --case-slug demo-contract \
  --analysis-file analysis.md \
  --metadata jurisdiction=CN \
  --metadata case_type=contract
```

### 🛡️ Safety

This agent must not fabricate legal authorities, promise outcomes, coach false statements, guide illegal evidence collection, or treat user allegations as proven facts without evidence review.

## 作者 / Author

**Kevin KE**  
**laoke.ai**  
Website: [https://laoke.ai](https://laoke.ai)

## License / 许可证

MIT License. See `LICENSE` for details.
