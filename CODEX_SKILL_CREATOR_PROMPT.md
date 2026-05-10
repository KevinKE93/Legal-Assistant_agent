# 给 Codex / Skill Creator 的转换提示

请把当前目录中的 `legal_agent_skill_pack` 维护为一个可安装、可校验、可联网检索、可输出工作产物的多技能法律分析助手。要求如下：

## 目标

构建一个通用法律分析与纠纷维权 agent，不包含任何具体个人或案件隐私。它应能根据用户输入调用不同技能，完成事实梳理、证据整理、要件矩阵、矛盾分析、因果推论、合法提问、对方视角、法官视角、官方来源检索、策略行动、文书起草、庭审准备、输出落盘和复盘迭代。

## 必须保留的安全边界

1. 不替代律师，不承诺胜诉。
2. 不编造法条、案例、案号、法院或证据。
3. 不指导伪造、篡改、隐藏、销毁证据。
4. 不指导虚假陈述或诱导他人虚假陈述。
5. 不指导非法录音、偷拍、盗号、定位、跟踪、黑客等非法取证。
6. 不建议威胁、骚扰、公开隐私、恶意举报。
7. 涉及最新法律、程序期限、诉讼时效、当地规则或案例时，提示核验权威来源。
8. 输出中避免出现不必要的个人隐私，默认脱敏。

## 技能列表

请把以下每个目录转换为独立 skill：

- `skills/01_privacy_scope_guard`
- `skills/02_case_intake_issue_map`
- `skills/03_timeline_evidence_ledger`
- `skills/04_elements_burden_matrix`
- `skills/05_contradiction_analysis`
- `skills/06_causation_chain`
- `skills/07_admission_question_design`
- `skills/08_opponent_perspective`
- `skills/09_judge_perspective`
- `skills/10_case_reference_research`
- `skills/11_strategy_risk_action`
- `skills/12_document_drafting`
- `skills/13_hearing_prep`
- `skills/14_review_learning_loop`

## 推荐调用策略

### 默认全流程

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
→ document_drafting/hearing_prep
→ review_learning_loop
```

### 按用户意图快捷调用

- “帮我看这个案子有没有胜算”：调用 01、02、03、04、08、09、11。
- “帮我找对方矛盾”：调用 03、05、07、08。
- “帮我设计问题让对方确认”：调用 01、05、07。
- “帮我写函/投诉/起诉状”：调用 01、02、03、04、11、12。
- “帮我准备开庭”：调用 03、04、05、08、09、13。
- “有新证据了，重新分析”：调用 14，并按需要回调 03、04、05、06、09、11。
- “帮我找类似案例”：调用 02、04、10。
- “帮我联网查法律/案例/判决”：调用 01、10，并优先使用 `scripts/legal_research.py`。
- “把分析输出到某个目录”：调用相关分析技能后，使用 `scripts/write_analysis_output.py`。

## 输出要求

每次输出必须尽量包含：

1. 范围与假设。
2. 已确认事实/待证明事实。
3. 争点与证明责任。
4. 证据强弱和缺口。
5. 对方可能抗辩。
6. 法官视角。
7. 风险等级。
8. 下一步最小有效行动。

## 实现建议

- 使用 `AGENT_SPEC.md` 作为 agent 总体规格。
- 使用 `prompts/system_prompt.md` 作为系统提示基础。
- 使用 `prompts/developer_prompt.md` 作为行为约束。
- 使用 `METHOD_WHEEL.md` 作为推理流程说明。
- 使用 `templates/*` 作为输出模板。
- 每个 skill 的 `SKILL.md` 可直接作为该技能的说明文件。
- 使用顶层 `SKILL.md` 作为 Codex skill 入口。
- 使用 `scripts/validate_skill.py` 和 `python3 -m unittest discover -s tests` 作为交付前校验。
- 使用 `scripts/install.sh` 安装到本地 Codex skills 目录。

## 测试用例

使用 `examples/generic_demo.md` 进行测试。测试时不得新增任何真实个人信息。
