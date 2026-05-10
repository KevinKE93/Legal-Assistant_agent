# Legal Assistant Agent Skill Pack

![Language](https://img.shields.io/badge/language-zh--CN-blue)
![Status](https://img.shields.io/badge/status-skill--pack--draft-orange)
![Safety](https://img.shields.io/badge/safety-privacy--first-green)

一套面向法律纠纷分析、证据整理、争点拆解和策略行动的通用 Agent Skill Pack。

它不是律师替代品，也不输出未经核验的确定法律结论。它的目标是把用户提供的事实、证据、目标和程序阶段转化为可审查、可复盘、可执行的法律分析工作流。

## What It Does

Legal Assistant Agent Skill Pack 将常见纠纷处理拆成 14 个可组合技能，覆盖从初次案件摄入到文书起草、庭审准备和复盘迭代的完整流程。

核心能力包括：

- 隐私脱敏、法域确认和高风险请求过滤
- 案件事实整理、时间线重构和证据台账生成
- 法律要件、证明责任、证据缺口和抗辩入口拆解
- 陈述、证据、时间线、金额和行为逻辑的矛盾分析
- 因果链、替代原因、损害范围和减损风险分析
- 对方代理人视角、法官/仲裁员/调解员视角交叉评估
- 合法、克制、可记录的事实确认问题设计
- 协商、投诉、调解、诉讼、庭审等路径的行动方案
- 法律相关沟通文本、投诉材料、起诉状/答辩状框架和证据目录起草
- 新证据、新进展、新程序节点后的版本化复盘

## Why This Project

法律纠纷中的真正难点通常不是“把事实讲一遍”，而是把事实、证据、法律要件、因果关系、程序动作和风险边界连接成一条能被第三方审查的证明链。

这个项目提供的是一个通用方法框架：

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

每一轮分析都要求保留：

- 已确认事实
- 待证明事实
- 证据来源
- 对方可能抗辩
- 风险等级
- 下一步最小行动

## Skill Modules

| Module | Purpose |
|---|---|
| `privacy_scope_guard` | 隐私脱敏、法域确认、风险边界和高风险行为过滤 |
| `case_intake_issue_map` | 将用户叙述转化为事实清单、程序信息、诉求目标和争点地图 |
| `timeline_evidence_ledger` | 构建时间线、事实清单和证据台账 |
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
| `review_learning_loop` | 在新证据或新进展后复盘并更新分析结论 |

## Repository Structure

```text
.
├── AGENT_SPEC.md
├── METHOD_WHEEL.md
├── CODEX_SKILL_CREATOR_PROMPT.md
├── agent_manifest.yaml
├── prompts/
│   ├── system_prompt.md
│   ├── developer_prompt.md
│   └── output_schemas.md
├── skills/
│   ├── 01_privacy_scope_guard/
│   ├── 02_case_intake_issue_map/
│   ├── 03_timeline_evidence_ledger/
│   ├── 04_elements_burden_matrix/
│   ├── 05_contradiction_analysis/
│   ├── 06_causation_chain/
│   ├── 07_admission_question_design/
│   ├── 08_opponent_perspective/
│   ├── 09_judge_perspective/
│   ├── 10_case_reference_research/
│   ├── 11_strategy_risk_action/
│   ├── 12_document_drafting/
│   ├── 13_hearing_prep/
│   └── 14_review_learning_loop/
├── templates/
│   ├── case_brief_template.md
│   ├── evidence_ledger.csv
│   ├── contradiction_matrix.csv
│   ├── causation_chain_template.md
│   ├── admission_question_bank_template.md
│   ├── judge_view_report_template.md
│   ├── case_research_log_template.md
│   └── strategy_report_template.md
└── examples/
    └── generic_demo.md
```

## Quick Start

### 1. Use It As A Prompt Pack

Use the files in `prompts/` as the base instruction layer:

- `prompts/system_prompt.md` for the assistant role and safety boundary
- `prompts/developer_prompt.md` for behavior constraints and output quality
- `prompts/output_schemas.md` for common analysis formats

Then attach the relevant `skills/*/SKILL.md` file according to the user's task.

### 2. Use It As A Manual Legal Analysis Workbench

Start from the templates:

1. Fill `templates/case_brief_template.md`.
2. Build the timeline and evidence ledger.
3. Complete the contradiction matrix and causation chain.
4. Generate the judge-view report and strategy report.
5. Re-run the review loop whenever new evidence or new statements appear.

### 3. Convert It Into Codex Skills

Use `CODEX_SKILL_CREATOR_PROMPT.md` to convert the package into independent Codex skills or a single multi-skill legal assistant.

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

## Example Use Cases

- “帮我把这个纠纷整理成时间线和证据表。”
- “帮我看我现在最缺哪几类证据。”
- “帮我找对方陈述里的矛盾点。”
- “帮我设计几个合法、克制的问题，让对方确认关键事实。”
- “从法官视角看，这个案子最容易被质疑的地方是什么？”
- “帮我写一版事实确认函/催告函/投诉材料。”
- “有新证据了，帮我重新评估策略。”

See `examples/generic_demo.md` for a privacy-safe demo.

## Safety Model

This project is designed around a conservative legal safety boundary.

The assistant must not:

- replace a licensed lawyer or promise a case outcome
- fabricate laws, cases, case numbers, courts, evidence, or legal authorities
- forge, alter, hide, destroy, or misrepresent evidence
- coach false statements or induce another person to make false statements
- guide illegal evidence collection, account intrusion, tracking, harassment, threats, or privacy exposure
- treat user-provided facts as proven facts without evidence review

For jurisdiction-specific law, limitation periods, procedural deadlines, evidence rules, current regulations, and case law, the assistant must ask the user to verify against current authoritative sources or consult a qualified local lawyer.

## Design Principles

- Privacy first: minimize and redact personal identifiers by default.
- Evidence before conclusion: separate facts, assumptions, legal issues, and proof gaps.
- Structured uncertainty: every key judgment should include basis and uncertainty.
- Opponent-aware: test every claim against possible defenses and evidence attacks.
- Court-facing clarity: optimize for what a judge, arbitrator, mediator, or platform reviewer can verify.
- Actionable next step: every analysis should end with the smallest useful next action.

## Current Status

This repository is currently a skill-pack draft. The content layer is ready for use as prompt/workflow material, while the following engineering tasks are still open:

- Add a top-level installable Codex `SKILL.md`.
- Add automated validation for skill frontmatter and internal links.
- Add more privacy-safe examples across contract, labor, consumer, leasing, tort, and company disputes.
- Add jurisdiction-specific research adapters without hardcoding unverified legal conclusions.
- Add a test harness for expected output structure and safety refusals.

## Disclaimer

This project provides general legal analysis workflow support. It does not provide legal representation, does not create an attorney-client relationship, and does not replace advice from a qualified lawyer in the relevant jurisdiction.

## Contributing

Contributions should preserve the project's safety model. In particular:

- Do not add fabricated legal authorities or unverifiable examples.
- Keep examples privacy-safe and generic.
- Mark jurisdiction-specific content clearly.
- Prefer templates, checklists, and verification workflows over unsupported conclusions.

## License

No license has been selected yet. Add a license before publishing this project for broad reuse.
