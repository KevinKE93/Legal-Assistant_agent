# 法律助手智能体 Legal-Assistant_agent

![Language](https://img.shields.io/badge/language-中文%20%7C%20English-blue)
![Agent](https://img.shields.io/badge/type-Legal%20Agent-green)
![Safety](https://img.shields.io/badge/safety-privacy--first-success)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> 一个面向法律事项分析、合同工作、法律研究和专业报告交付的文档型 Legal Agent 工作流。

**作者：Kevin KE / [laoke.ai](https://laoke.ai)**

---

## 中文

### 项目简介

**法律助手智能体 Legal-Assistant_agent** 是一套纯文档型法律工作流 Agent。它以 `AGENTS.md` 为入口，让 AI 助手在处理法律事项时不只是即时回答，而是像一个可持续推进的法律事项工作台：先识别事项类型和法域，再整理事实、证据、争点、来源、风险和行动路径，最后生成可复盘、可更新、可交付的专业报告。

它适用于法律纠纷分析、合同审查、合同起草、法律研究、谈判准备、文书草拟和阶段性复盘。复杂事项会在本地形成一个独立事项文件夹，用于持续记录案件事实、阶段计划、分析过程、参考来源和最终交付文件；最终报告会以争点树、证明责任、证据链、法条适用边界和策略路径串联，而不是只给出简单结论。

> 本项目不替代律师，不承诺案件结果。涉及诉讼时效、程序期限、关键证据、最新法规或高风险行动时，应核验官方/权威来源，并在必要时咨询相关法域的合格律师。

### 工作方式

```text
用户输入法律事项
→ 识别语言、法域、事项类型和用户目标
→ 创建或复用本地事项文件夹
→ 整理事实、证据、争点、来源和风险
→ 输出分析结论、行动建议和必要文书
→ 汇总生成专业报告 Markdown / 样式化 PDF
→ 后续新证据或新进展继续更新同一事项
```

复杂事项会在本地工作目录中生成独立事项文件夹，用于保存阶段记录、分析底稿、参考来源和最终报告。

### 主要产物

常见输出包括：

- `plan.md`：事项阶段、下一步、责任方、待补信息和执行记录。
- `case.md`：案件或事项的关键事实、争点、程序状态和核心记忆。
- `analysis.md`：完整法律分析底稿。
- `advice.md`：面向用户的策略、行动建议和表达风险。
- `sources.md`：法律、案例、政策、网页等来源及核验状态。
- `<主题>专业报告.md`：面向用户交付的专业报告。
- `<主题>专业报告.pdf`：与 Markdown 报告一致、经过版式渲染和可读性检查的 PDF 版本。

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

- 劳动争议、合同纠纷、消费纠纷、租赁纠纷等复杂事项分析。
- 合同、补充协议、和解协议、服务协议等文本审查。
- 合同草案、沟通函、投诉材料、仲裁/诉讼框架和庭审提纲准备。
- 法律规则、案例、政策和官方网页的检索记录与引用风险整理。
- 新证据、新报价、新程序节点出现后的持续复盘。

### 安全边界

Legal-Assistant_agent 不会：

- 替代律师或承诺案件结果。
- 编造法条、案例、案号、法院、证据或裁判观点。
- 指导伪造、篡改、隐藏、销毁或歪曲证据。
- 指导虚假陈述、诱导他人作虚假陈述或非法取证。
- 指导骚扰、威胁、盗号、定位、跟踪或公开隐私。
- 在未审查证据的情况下，把用户单方陈述当作已证明事实。

---

## English

### Overview

**Legal-Assistant_agent** is a document-first Legal Agent workflow for legal matter analysis, contract work, legal research, drafting, negotiation preparation, and professional report delivery. It uses `AGENTS.md` as the main entrypoint and guides an AI assistant to work as a structured legal matter workspace rather than a one-off Q&A assistant.

For complex matters, the agent creates or reuses a local matter folder, records facts and evidence, maps issue trees and proof burdens, tracks source verification, explains legal-rule applicability boundaries, prepares strategy or draft documents, and produces a professional Markdown/styled PDF report that can be updated as new information arrives.

This project is not a substitute for licensed legal counsel and does not promise outcomes. Deadlines, limitation periods, procedural rules, current law, key evidence, and high-stakes actions should be verified against authoritative sources and reviewed by qualified counsel in the relevant jurisdiction.

### How It Works

```text
User provides a legal matter
→ Identify language, jurisdiction, matter type, and user goal
→ Create or reuse a local matter folder
→ Organize facts, evidence, issues, sources, and risks
→ Produce analysis, guidance, and draft documents when needed
→ Generate a professional Markdown / styled PDF report
→ Continue updating the same matter when new information appears
```

For complex matters, the agent keeps a dedicated local matter folder for stage notes, working analysis, source records, and final reports.

### Deliverables

- `plan.md`: stage plan, next actions, owner, missing information, and execution notes.
- `case.md`: matter memory, key facts, issues, procedural status, and conclusions.
- `analysis.md`: working legal analysis.
- `advice.md`: user-facing strategy and action guidance.
- `sources.md`: statutes, cases, policies, URLs, verification status, and citation risks.
- `<topic> Professional Report.md`: final or stage-based professional report.
- `<topic> Professional Report.pdf`: rendered PDF version when the environment can generate a readable, styled PDF.

### Usage

Temporary invocation:

```text
Use Legal-Assistant_agent to analyze this legal matter, create a matter folder, and generate a professional Markdown report with a styled PDF version when available.
```

Slash-command style:

```text
/legal-assistant analyze this matter...
```

If your AI client supports custom commands, configure the command to read and follow this repository's `AGENTS.md`. This repository intentionally stays as a pure document workflow and does not ship an installer.

## Author

**Kevin KE**  
**laoke.ai**  
Website: [https://laoke.ai](https://laoke.ai)

## License

MIT License. See `LICENSE` for details.
