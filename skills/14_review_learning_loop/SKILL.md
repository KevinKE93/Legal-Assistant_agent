---
name: review_learning_loop
description: 在新证据、新陈述、新程序节点出现后，读取本地案件工作台，复盘并更新事实、证据、争点、风险、checkpoint 和下一步行动。
---

# Skill：复盘、本地记忆与迭代学习

## 适用场景

每次出现新聊天记录、新证据、对方新说法、法院/仲裁员反馈、调解结果、庭审进展、和解报价、投诉反馈或用户目标变化后使用。

## 目标

1. 读取 `work/cases/<case-slug>/case_state.json` 和 `activity_log.jsonl`。
2. 判断新信息改变了哪些事实、争点、证明责任、证据强度和风险。
3. 更新案件状态、下一步行动和责任方。
4. 将本轮关键产物保存为 checkpoint。
5. 保持案件记忆连续，不从空白分析重新开始。

## 输入

- 案件工作台路径或 case slug。
- 新增事实。
- 新增证据。
- 对方新表态。
- 程序进展。
- 用户目标变化。

## 工作流

### 1. 读取本地案件状态

优先使用：

```bash
python3 scripts/case_workspace.py status --case-slug <case-slug>
```

若工作台不存在，先初始化：

```bash
python3 scripts/case_workspace.py init \
  --case-slug <case-slug> \
  --stage review-loop \
  --summary "Initialized workspace during review loop."
```

### 2. 新旧对比

| 项目 | 旧版本 | 新信息 | 影响 |
|---|---|---|---|

### 3. 假设校验

检查：

- 哪些原假设被证实。
- 哪些原假设被推翻。
- 哪些风险升高。
- 哪些缺口被补上。
- 哪些新缺口出现。

### 4. 矩阵更新

更新：

- 时间线。
- 证据台账。
- 要件矩阵。
- 矛盾矩阵。
- 因果链。
- 对方视角。
- 法官视角。
- 行动方案。

### 5. 本地记忆更新

每次复盘必须写入一条活动记录：

```bash
python3 scripts/case_workspace.py record \
  --case-slug <case-slug> \
  --stage review-loop \
  --summary "<本轮发生了什么>" \
  --owner agent \
  --next-action "agent: <下一步>" \
  --open-question "<仍缺什么>"
```

如果本轮形成了可复用分析，保存 checkpoint：

```bash
python3 scripts/case_workspace.py checkpoint \
  --case-slug <case-slug> \
  --stage review-loop \
  --title review-update \
  --content-file review_update.md
```

### 6. 经验沉淀

提炼：

- 哪类证据最有效。
- 哪些提问有用。
- 哪些表达造成风险。
- 哪些对方抗辩需要提前准备。
- 哪些策略不应重复。

## 输出格式

```markdown
## 版本信息
- 版本：
- 更新时间：
- 新增信息来源：
- Case workspace：
- 当前阶段：

## 新旧变化
| 领域 | 旧判断 | 新信息 | 更新后判断 | 风险变化 |
|---|---|---|---|---|

## 更新后的关键结论
1. 
2. 
3. 

## 需要重做的模块
- [ ] 时间线
- [ ] 证据台账
- [ ] 要件矩阵
- [ ] 矛盾分析
- [ ] 因果链
- [ ] 法官视角
- [ ] 策略行动

## 下一步最小行动

## 本地记忆更新
- 已写入 activity_log：
- 已保存 checkpoint：
- case_state 更新：

## 经验记录
```

## 质量检查

- 先读取本地案件状态，再复盘。
- 不保留已被推翻的假设。
- 不忽略新信息对风险的影响。
- 每次复盘都给出下一步动作。
- 每次复盘都记录责任方和下一步。
- 不把 templates 当作案件记忆。
- 经验记录保持抽象，不包含隐私。
