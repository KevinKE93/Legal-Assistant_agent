# Case Workspace Protocol

This protocol defines the local memory layer for 法律助手智能体 Legal-Assistant_agent. Use it for complex, multi-issue, or multi-stage legal matters so later work continues from recorded state rather than starting over.

## When To Use

Use a case workspace by default when any of these are true:

- The matter has multiple issues, procedures, parties, claims, or evidence categories.
- The user asks for strategy, negotiation, arbitration, litigation, complaint, drafting, or hearing preparation.
- The user asks to continue, update, review, save, or output analysis.
- New evidence, new statements, a ruling, a hearing, or a settlement offer changes the case posture.

For a narrow one-off question, a workspace is optional unless the user asks to save outputs.

## Default Location

Write runtime memory only under:

```text
work/cases/<safe-case-slug>/
```

Do not write real case data into tracked skill files. Keep `work/` ignored by git.

If the user does not provide a case slug, derive one from case type, short topic, and current date. Use only ASCII letters, digits, dots, underscores, and hyphens.

## Directory Contract

```text
work/cases/<case-slug>/
├── case_state.json
├── activity_log.jsonl
├── checkpoints/
├── outputs/
└── research/
```

- `case_state.json`: current stage, issues, evidence status, open questions, responsible parties, next actions, and last checkpoint.
- `activity_log.jsonl`: append-only event stream of what happened, who owns the next step, and what changed.
- `checkpoints/`: stage artifacts such as issue maps, burden matrices, judge-view reviews, strategy reports, and hearing-prep notes.
- `outputs/`: final or user-facing reports.
- `research/`: official-source research logs and result files.

## Stage Discipline

For complex matters, do not jump directly to conclusions. Complete and record these stages in order unless the user asks for a narrow artifact:

1. `scope-guard`: jurisdiction, case type, procedural stage, privacy, risk level.
2. `case-map`: one-sentence map, known facts, disputed facts, procedural posture.
3. `issue-map`: factual, legal, evidentiary, causation, and procedural issues.
4. `burden-matrix`: claims, legal elements, burden of proof, evidence, gaps.
5. `evidence-ledger`: evidence list, source, formation time, holder, proof target, risks.
6. `contradiction-review`: contradictions, explanation risk, cross-examination direction.
7. `research`: official-source research and citation risk.
8. `opponent-view`: likely defenses, counterclaims, proof attacks, settlement posture.
9. `judge-view`: neutral adjudicator path, likely questions, dispositive gaps.
10. `strategy`: options, negotiation anchors, complaint/litigation tracks, next actions.
11. `output`: final or stage report.
12. `review-loop`: update state after new evidence or procedural events.

Every completed stage must update `case_state.json` and append one `activity_log.jsonl` row.

## Record Fields

Each log entry should include:

- `event_type`: `init`, `record`, or `checkpoint`.
- `stage`: current workflow stage.
- `summary`: what happened.
- `actor`: usually `legal-assistant-agent`.
- `owner`: who owns follow-up work: `agent`, `user`, `lawyer`, `opponent`, `court`, `agency`, or another clear label.
- `next_actions`: concrete next actions in `owner: action` form.
- `open_questions`: missing facts or evidence.
- `issues`: new or updated issues.
- `evidence_status`: evidence updates.
- `risk_level`: low, medium, high, or critical.
- `checkpoint`: relative path when an artifact is saved.

## Checkpoint Rules

Create a checkpoint when a stage produces durable reasoning, such as:

- issue map
- burden matrix
- evidence ledger
- contradiction matrix
- research summary
- opponent-view report
- judge-view report
- strategy report
- hearing-prep package
- final report

Each checkpoint must be usable by a later agent without reading the entire conversation.

## Required Analysis Binding

Every key conclusion in checkpoints and reports must bind:

```text
conclusion -> facts -> evidence status -> legal basis or verification need -> burden of proof -> opponent attack -> uncertainty -> next action
```

Do not use templates as a substitute for this binding.

## CLI

Use `scripts/case_workspace.py`:

```bash
python3 scripts/case_workspace.py init \
  --case-slug demo-labor \
  --title "Demo Labor Dispute" \
  --jurisdiction CN \
  --case-type labor-dispute \
  --procedural-stage arbitration \
  --stage scope-guard \
  --owner agent \
  --next-action "agent: build issue map"

python3 scripts/case_workspace.py record \
  --case-slug demo-labor \
  --stage issue-map \
  --summary "Mapped factual, legal, evidence, causation, and procedural issues." \
  --owner user \
  --next-action "user: provide payroll records"

python3 scripts/case_workspace.py checkpoint \
  --case-slug demo-labor \
  --stage burden-matrix \
  --title issue-and-burden-matrix \
  --content-file burden_matrix.md \
  --next-action "agent: prepare judge-view review"

python3 scripts/case_workspace.py status --case-slug demo-labor
```
