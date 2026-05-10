# 法律助手智能体 Legal-Assistant_agent

![Language](https://img.shields.io/badge/language-中文%20%7C%20English-blue)
![Agent](https://img.shields.io/badge/type-Legal%20Workflow%20Agent-green)
![Output](https://img.shields.io/badge/output-Markdown%20%7C%20PDF-orange)
![Memory](https://img.shields.io/badge/memory-Skill%20Outputs-purple)
![Gates](https://img.shields.io/badge/gates-Capability%20Matrix-black)
![Safety](https://img.shields.io/badge/safety-privacy--first-success)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> 面向法律纠纷、合同审查、合同起草和法律研究的纯文档型法律助手 Agent 工作流。

**作者：Kevin KE / [laoke.ai](https://laoke.ai)**

---

## 中文

### 项目定位

**法律助手智能体 Legal-Assistant_agent** 是一个以 `AGENTS.md` 为主入口的法律事项工作台型 Agent。它不是传统代码包，也不是律师替代品；它是一套可被 AI 助手遵循的专业工作流，用来把复杂法律事项拆解成可持续更新的事实、证据、争点、法律依据、策略行动和专业最终报告。

v0.3+ 强化了三项核心能力：

- **能力覆盖矩阵**：先识别法律工作场景，再确定角色、必跑 skill、可选 skill、工具和 gate。
- **Skill 产物记忆**：每个被调用的阶段 skill 都必须在事项文件夹中留下记录，避免分析过程散落在对话里。
- **专业报告交付**：最终输出不再是简短概述，而是读取所有工作底稿和 skill 记忆后生成完整报告，并输出 Markdown 和 PDF。

### 核心能力

| 能力 | 说明 |
|---|---|
| 事项工作台 | 同一法律事项只维护一个 `work/<日期>_<本地化事项名>/` 文件夹 |
| 能力矩阵 | `CAPABILITIES.md` 定义不同法律场景的角色、必跑 skill、工具和 gate |
| Skill 记忆 | `skill_outputs.md` 记录每个 skill 的触发原因、输入、产出、关键发现和报告章节 |
| 事实与证据 | 区分已证事实、待证事实、争议事实、推测和法律结论 |
| 争点与证明责任 | 建立争议焦点、请求权基础、证明责任和证据缺口矩阵 |
| 官方来源 | 引用法律、案例、政策或网页时写入 `sources.md` 并标注核验状态 |
| 合同工作 | 支持合同审查、条款风险、缺失条款、谈判点和合同草案 |
| 多视角推理 | 模拟对方视角、法官/仲裁员视角、调解视角和审稿律师视角 |
| 专业报告 | 生成带封面、目录、摘要、争点关系、证据链、来源和附录的报告 |
| i18n 准备 | 中文输入生成中文目录和中文报告；英文输入生成英文目录和英文报告 |

### Agent Workflow

```text
用户输入
→ 隐私与范围守门
→ 语言与事项类型识别
→ CAPABILITIES.md 能力矩阵与 gate
→ 创建或读取事项文件夹
→ plan.md 任务计划
→ case.md 事项记忆
→ skill_outputs.md 阶段产物索引
→ 时间线 / 条款 / 证据台账
→ 争议焦点 / 条款风险 / 证明责任
→ 矛盾、因果、对方视角、裁判视角
→ 官方来源检索并写入 sources.md
→ analysis.md 工作底稿
→ advice.md 行动建议
→ <主题>专业报告.md
→ <主题>专业报告.pdf
→ 新证据或新进展后的复盘更新
```

### 输出规则

复杂法律事项默认输出到：

```text
work/<日期>_<本地化事项名>/
```

示例：

```text
work/2026-05-10_劳动争议_拆分发薪加班费/
work/2026-05-10_service-agreement-review/
```

中文输入必须保留中文事项名，不默认翻译成英文 slug。不要在 `work/` 下再套 `cases/` 层。

默认文件：

| 文件 | 用途 |
|---|---|
| `plan.md` | 当前阶段、已完成事项、下一步、责任方、待补信息、PDF 状态 |
| `case.md` | 事项核心记忆、事实分层、争议焦点、程序进展和关键结论 |
| `skill_outputs.md` | 每个阶段 skill 的执行记录和最终报告章节映射 |
| `analysis.md` | 工作底稿型完整分析 |
| `advice.md` | 面向用户的策略、行动路径和禁忌动作 |
| `<主题>专业报告.md` | 面向用户交付的完整专业报告 |
| `<主题>专业报告.pdf` | 与 Markdown 报告一致的 PDF 版本 |

按需增加：

| 文件 | 用途 |
|---|---|
| `timeline.md` | 事件时间线 |
| `evidence.md` | 证据台账、证明对象和证据缺口 |
| `sources.md` | 法规、案例、官方来源、访问日期和引用风险 |
| `drafts.md` | 沟通函、投诉材料、仲裁/诉讼框架、庭审提纲 |
| `contract.md` | 合同背景、版本信息和条款摘要 |
| `clause_review.md` | 条款风险、修改建议和谈判点 |
| `term_sheet.md` | 合同起草前的交易要点和条款结构 |
| `contract_draft.md` | 合同、补充协议或和解协议草案 |

PDF 必须真实存在且基本可读。若当前环境无法导出合格 PDF，Agent 必须在 `plan.md` 和对话中说明阻塞原因，不能假称已生成。

### 专业报告结构

复杂事项的专业报告默认包含：

- 封面信息和重要提示
- 目录
- 执行摘要
- 报告范围、假设与材料清单
- Skill 产物索引
- 能力覆盖与执行完整性
- 事项地图与程序状态
- 事实时间线
- 核心争议焦点矩阵
- 争议焦点关系图
- 请求权基础与证明责任
- 证据链与缺口
- 法律依据与参考来源
- 对方视角与反制
- 裁判者/审稿者视角
- 金额、胜率和风险区间
- 策略路径与行动清单
- 禁忌动作与表达风险
- 待补信息和附录

### 使用方式

临时调用：

```text
请按照 Legal-Assistant_agent 的工作流分析下面这个法律事项，并输出事项文件夹、专业报告 Markdown 和 PDF。
```

全局或 `/` 指令调用：

```text
/legal-assistant 分析这个法律事项……
```

如果你的 AI 客户端支持自定义命令，可以将命令配置为“读取并遵循本仓库的 `AGENTS.md`”。本仓库保持纯文档工作流，不提供安装脚本。

### 适用场景

| 场景 | 支持状态 | 产物 |
|---|---|---|
| 劳动争议、合同纠纷等复杂争议 | 已支持 | 争点矩阵、证据台账、来源记录、策略建议、专业报告 |
| 合同审查 | 已支持 | 条款摘要、风险清单、修改建议、签署前清单、专业报告 |
| 合同起草 | 已支持 | 条款结构、合同草案、可谈判条款、签署清单 |
| 法律研究 | 已支持 | 官方来源、规则摘要、引用风险、研究报告 |
| 文书准备 | 已支持 | 沟通函、投诉材料、仲裁/诉讼框架 |
| 谈判/和解 | 已支持 | 筹码、底线、让步顺序、话术、和解文本 |
| 庭审/听证准备 | 已支持 | 庭审主线、证据使用、质证意见、发问清单 |
| 高风险专业领域 | 谨慎支持 | 需要用户核验和专业律师审阅 |

### 安全边界

Legal-Assistant_agent 不会：

- 替代律师或承诺案件结果
- 编造法条、案例、案号、法院、证据或裁判观点
- 指导伪造、篡改、隐藏、销毁或歪曲证据
- 指导虚假陈述或诱导他人作虚假陈述
- 指导非法取证、盗号、定位、跟踪、骚扰、威胁或公开隐私
- 在未审查证据的情况下，把用户单方陈述当作已证明事实

涉及诉讼时效、程序期限、证据规则、最新法规和具体案件行动时，应优先核验官方或权威来源，并在必要时咨询相关法域的合格律师。

---

## English

### What It Is

**Legal-Assistant_agent** is a document-first legal workflow agent for legal disputes, contract review, contract drafting, legal research, and legal-document preparation. It uses `AGENTS.md` as the main entrypoint and turns a legal matter into a structured workspace with facts, evidence, issues, legal theories, burden of proof, source notes, strategy, skill execution memory, and professional final reports.

It is not a lawyer replacement and does not promise legal outcomes. It helps AI assistants work like a disciplined legal matter workspace: organized, source-aware, evidence-aware, privacy-conscious, and reviewable.

### Capabilities

| Capability | Description |
|---|---|
| Matter workspace | Keeps one folder per legal matter under `work/<date>_<localized-matter-name>/` |
| Capability matrix | Maps legal work scenarios to roles, required skills, optional skills, tools, and gates |
| Skill memory | Tracks executed skills, inputs, outputs, findings, sources, and report sections in `skill_outputs.md` |
| Fact and evidence discipline | Separates proven facts, alleged facts, disputed facts, assumptions, and legal conclusions |
| Issue and burden mapping | Connects claims, defenses, proof burdens, evidence gaps, and procedural risks |
| Official-source research | Records statutes, cases, policies, URLs, access dates, verification status, and citation risks in `sources.md` |
| Contract workflows | Supports contract review, clause-risk analysis, missing clauses, negotiation points, and draft agreements |
| Professional reports | Produces structured Markdown/PDF reports with cover, table of contents, issue relations, evidence chains, sources, strategy, and appendices |
| i18n-ready output | Uses the user's input language for folder names, filenames, headings, and report content |

### Workflow

```text
User input
→ Privacy and scope guard
→ Language and matter-type routing
→ CAPABILITIES.md capability matrix and gates
→ Create or read matter folder
→ plan.md task plan
→ case.md matter memory
→ skill_outputs.md skill execution index
→ Timeline / clause / evidence ledger
→ Issue map / clause risk / burden of proof
→ Contradiction, causation, opponent view, adjudicator view
→ Official-source research into sources.md
→ analysis.md working analysis
→ advice.md action guidance
→ <topic> Professional Report.md
→ <topic> Professional Report.pdf
→ Review loop after new evidence or procedural events
```

### Usage

Temporary invocation:

```text
Use Legal-Assistant_agent to analyze this legal matter, create a matter folder, and generate a professional Markdown/PDF report.
```

Slash-command style:

```text
/legal-assistant analyze this matter...
```

If your AI client supports custom commands, configure the command to read and follow this repository's `AGENTS.md`. This repository intentionally stays as a pure document workflow and does not ship an installer.

### Safety

Legal-Assistant_agent must not fabricate legal authority, coach false evidence, replace licensed counsel, or present one-sided user statements as proven facts. For deadlines, statutes of limitation, procedural rules, current law, and high-stakes actions, verify authoritative sources and consult qualified counsel in the relevant jurisdiction.

## Author

**Kevin KE**  
**laoke.ai**  
Website: [https://laoke.ai](https://laoke.ai)

## License

MIT License. See `LICENSE` for details.
