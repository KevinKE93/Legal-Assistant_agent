# 法律助手智能体 Legal-Assistant_agent

![Language](https://img.shields.io/badge/language-中文%20%7C%20English-blue)
![Agent](https://img.shields.io/badge/type-Legal%20Agent-green)
![Safety](https://img.shields.io/badge/safety-privacy--first-success)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> 面向法律事项分析、合同工作、法律研究、策略推演和报告交付的 AI 法律工作台。

**作者：Kevin KE / [laoke.ai](https://laoke.ai)**  
[English Version](#english-version)

![Legal Assistant Agent feature overview](assets/legal-assistant-intro.png)

> 功能总览图使用虚构信息，仅展示工作流能力，不包含真实案件信息。

## 中文说明

- [适用场景](#适用场景)
- [我为你做什么](#我为你做什么)
- [轻量工作方式](#轻量工作方式)
- [使用方式](#使用方式)
- [安全边界](#安全边界)

**法律助手智能体 Legal-Assistant_agent** 让大模型不只是“回答法律问题”，而是按当前目标选择最小可靠路径：能在对话中回答就直接回答，需要持续记忆才落盘，需要报告或文书才生成文件，复杂案件才展开案件工作台。

它适合用于法律纠纷分析、合同审查与起草、法律研究、谈判准备、文书草拟、庭审/听证准备和案件复盘。默认情况下，Agent 会先在对话中输出结构化汇总结论；如果你需要归档、发给律师或用于内部讨论，可以继续要求生成 Markdown 报告或 PDF 报告。

> 本项目不替代律师，不承诺案件结果。涉及期限、诉讼时效、程序规则、最新法规、关键证据或高风险行动时，应核验官方或权威来源，并在必要时咨询相关法域的合格律师。

## 适用场景

| 场景 | 适合解决的问题 |
|---|---|
| 纠纷分析 | 劳动争议、合同纠纷、消费纠纷、租赁纠纷、赔偿/返还争议 |
| 合同工作 | 审查合同风险、补充关键条款、起草协议或和解方案 |
| 法律研究 | 梳理法律依据、案例、政策和引用风险 |
| 策略准备 | 谈判方案、投诉路径、仲裁/诉讼思路、证据补强 |
| 阶段复盘 | 新证据、新报价、新程序节点出现后的判断更新 |

## 我为你做什么

普通咨询会优先得到一份对话内 briefing，通常包括：

- 核心结论与主要限制。
- 争议焦点或条款风险之间的关系。
- 关键证据缺口与补充材料清单。
- 法律依据、来源核验状态和引用风险。
- 对方可能主张、裁判者视角和策略路径。
- 下一步行动建议。

当你需要报告或文书时，可以继续生成：

- Markdown 报告。
- PDF 报告。
- 沟通函、投诉材料、合同草案、诉讼/仲裁框架、庭审提纲等文书草稿。

## 轻量工作方式

| 模式 | 何时使用 | 典型输出 |
|---|---|---|
| Quick Answer | 简单问题、短条款疑问、一次性咨询 | 会话内结论、限制和下一步 |
| Matter Note | 同一事项可能继续追问，但暂不需要正式文件 | `matter.md` |
| Deliverable | 明确需要合同审查意见、合同草案、函件、投诉材料或报告 | `matter.md` + 目标交付文件 |
| Deep Case | 多争议焦点、多程序、听证/仲裁/诉讼或长期案件 | 按需案件工作台、证据文件、文书框架 |

## 使用方式

推荐先安装后使用。安装后，客户端可以直接读取本仓库的工作流、阶段技能和报告规则。

### 1. 本地脚本安装

在本仓库目录运行：

```bash
./tools/install_native_skill.sh
```

安装后重启 Codex，然后使用：

```text
/legal-assistant 分析这个法律事项……
```

### 2. 让客户端从 GitHub 安装

在支持安装技能或读取项目规则的客户端里，可以直接输入：

```text
帮我安装 https://github.com/KevinKE93/Legal-Assistant_agent
```

然后按客户端提示刷新技能列表或重启应用。

### 3. 引用使用

不安装也可以使用。把下面这句话复制到你常用的大模型对话框里，然后补充你的事实、合同文本或问题：

```text
请参考这个 https://github.com/KevinKE93/Legal-Assistant_agent ，帮我分析下面这个法律事项/合同/问题……
```

## 安全边界

Legal-Assistant_agent 不会：

- 替代律师或承诺案件结果。
- 编造法条、案例、案号、法院、证据或裁判观点。
- 把用户单方陈述直接当作已证明事实。
- 指导伪造、篡改、隐藏、销毁或歪曲证据。
- 指导虚假陈述、非法取证、骚扰、威胁、跟踪或公开隐私。

---

## English Version

- [Common Use Cases](#common-use-cases)
- [What I Do For You](#what-i-do-for-you)
- [Working Model](#working-model)
- [How To Use](#how-to-use)
- [Safety Boundaries](#safety-boundaries)
- [Author](#author)
- [License](#license)

**Legal-Assistant_agent** is an AI legal assistant for legal matter analysis, contract work, legal research, strategy planning, drafting, negotiation preparation, and report delivery.

Instead of forcing every matter into a heavy workflow, it chooses the smallest reliable path: answer in chat when that is enough, keep a matter note when continuity matters, generate files only when requested, and expand into a case workbench only for complex matters.

It can support dispute analysis, contract review and drafting, legal research, negotiation preparation, document drafting, hearing preparation, and matter updates. By default, the agent provides a structured briefing in chat first. If you need a report file, you can ask for a Markdown report or PDF report.

> This project is not a substitute for licensed legal counsel and does not promise outcomes. Deadlines, limitation periods, procedural rules, current law, key evidence, and high-risk actions should be checked against authoritative sources and reviewed by qualified counsel when needed.

## Common Use Cases

| Scenario | Suitable For |
|---|---|
| Dispute analysis | Employment, contract, consumer, lease, compensation, and restitution disputes |
| Contract work | Reviewing risk, adding missing clauses, drafting agreements or settlement terms |
| Legal research | Summarizing legal rules, cases, policies, and citation risks |
| Strategy preparation | Negotiation plans, complaint routes, arbitration/litigation thinking, evidence strengthening |
| Matter updates | Updating analysis after new evidence, offers, or procedural events |

## What I Do For You

For ordinary analysis, the agent first returns a structured briefing in chat, usually covering:

- Core conclusions and major limitations.
- Relationships between issues or contract risks.
- Key evidence gaps and requested materials.
- Legal-source status and citation risks.
- Opponent arguments, adjudicator view, and strategy path.
- Next recommended actions.

When you request a report or draft, it can also generate:

- A Markdown report.
- A PDF report.
- Draft letters, complaints, contract drafts, litigation/arbitration frameworks, hearing outlines, and similar legal work products.

## Working Model

| Mode | When To Use | Typical Output |
|---|---|---|
| Quick Answer | Simple questions, short clause questions, one-off consultations | In-chat conclusion, limits, and next steps |
| Matter Note | A matter may continue, but no formal file is needed yet | `matter.md` |
| Deliverable | The user asks for a contract review, draft, letter, complaint, memo, or report | `matter.md` plus the requested file |
| Deep Case | Multi-issue, multi-procedure, hearing, arbitration, litigation, or long-running matters | Case workbench files only as needed |

## How To Use

Installation is recommended. After installation, your client can load the repository workflow, stage skills, and report rules directly.

### 1. Install Locally

Run this command from the repository folder:

```bash
./tools/install_native_skill.sh
```

Restart Codex, then use:

```text
/legal-assistant analyze this legal matter...
```

### 2. Ask Your Client To Install From GitHub

In a client that supports skill installation or project rules, you can type:

```text
Install https://github.com/KevinKE93/Legal-Assistant_agent for me.
```

Then refresh the skill list or restart the app as prompted.

### 3. Use By Reference

You can also use the workflow without installation. Paste this into your AI chat, then add your facts, contract text, or question:

```text
Please refer to this https://github.com/KevinKE93/Legal-Assistant_agent and help me analyze the following legal matter, contract, or question...
```

## Safety Boundaries

Legal-Assistant_agent will not:

- Replace a lawyer or promise case outcomes.
- Fabricate statutes, cases, docket numbers, courts, evidence, or judicial views.
- Treat one-sided user statements as proven facts.
- Help forge, alter, hide, destroy, or distort evidence.
- Help with false statements, illegal evidence collection, harassment, threats, tracking, or privacy exposure.

## Author

**Kevin KE**  
**laoke.ai**  
Website: [https://laoke.ai](https://laoke.ai)

## License

MIT License. See `LICENSE` for details.
