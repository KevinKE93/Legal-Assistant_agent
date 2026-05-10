---
name: legal-assistant-agent
description: Use 法律助手智能体 Legal-Assistant_agent for privacy-first legal dispute analysis, evidence mapping, issue spotting, official-source legal research, strategy planning, legal-related drafting, hearing preparation, and writing structured outputs to a case workspace. Trigger when the user asks to analyze a legal dispute, find relevant laws or cases, organize evidence, draft legal-related documents, prepare for mediation/arbitration/hearing, or save analysis artifacts to a folder.
---

# 法律助手智能体 Legal-Assistant_agent

This skill turns a legal-dispute request into structured, privacy-conscious work products: scope notes, issue maps, timelines, evidence ledgers, burden matrices, contradiction analysis, causation chains, official-source research logs, strategy reports, drafts, and hearing-prep bundles.

## Core Rules

- Do not replace a licensed lawyer, promise outcomes, or give absolute win/loss conclusions.
- Do not fabricate facts, evidence, laws, cases, case numbers, courts, or legal authorities.
- Treat user-provided facts as allegations or user statements until supported by evidence.
- Do not suggest forged evidence, false statements, illegal evidence collection, threats, harassment, privacy exposure, or coercive tactics.
- For jurisdiction-specific law, limitation periods, procedural deadlines, evidence rules, current regulations, and case law, verify through official or authoritative sources before relying on them.
- Minimize personal identifiers in outputs. Use party labels and evidence IDs unless the user explicitly needs formal document text.

## Default Workflow

1. Scope and privacy guard: use `skills/01_privacy_scope_guard/SKILL.md`.
2. Intake and issue map: use `skills/02_case_intake_issue_map/SKILL.md`.
3. Timeline and evidence ledger: use `skills/03_timeline_evidence_ledger/SKILL.md`.
4. Elements and burden matrix: use `skills/04_elements_burden_matrix/SKILL.md`.
5. Contradiction analysis: use `skills/05_contradiction_analysis/SKILL.md`.
6. Causation chain: use `skills/06_causation_chain/SKILL.md`.
7. Opponent and judge perspectives: use `skills/08_opponent_perspective/SKILL.md` and `skills/09_judge_perspective/SKILL.md`.
8. If laws, cases, judgments, or rules are needed, use the research workflow below.
9. Strategy, drafting, hearing prep, or review loop as needed.

Skip steps when the user asks for a narrow artifact, but keep the safety boundary active.

## Official-Source Research

When the user asks for law, cases, judgments, comparable decisions, or current legal rules:

1. Identify the jurisdiction first. If missing, ask or mark it as a blocking gap.
2. Prefer official sources for the relevant country or jurisdiction.
3. Use `references/official_source_registry.json` to select source domains.
4. Run `scripts/legal_research.py` when networked research artifacts are useful:

```bash
python3 scripts/legal_research.py \
  --jurisdiction CN \
  --query "合同 迟延履行 退款 催告" \
  --case-type "合同纠纷" \
  --out-dir work/research-demo \
  --max-results 8
```

The script writes `research_log.md`, `results.json`, and optional retrieved text snippets. Treat these files as research aids, not final legal advice.

Provider options are `auto`, `official`, `bing`, `duckduckgo`, `brave`, `tavily`, and `serpapi`. `auto` tries source-native public endpoints first, then configured API providers and no-key fallbacks. Returned URLs are filtered against the selected official source domain, and a `not_found_or_unverified` row is recorded when no official-domain result is returned.

If a source is inaccessible, report the access problem and use a narrower official-domain query or another official source in the same jurisdiction. Do not invent citations to fill gaps.

## Output To A Workspace

When the user asks to save analysis, write files, or output to a specified folder, use `scripts/write_analysis_output.py` or its `write_analysis_bundle()` function.

CLI example:

```bash
python3 scripts/write_analysis_output.py \
  --out-dir work/cases \
  --case-slug demo-contract \
  --analysis-file path/to/analysis.md \
  --metadata jurisdiction=CN \
  --metadata case_type=contract
```

The output bundle should include `INDEX.md`, `analysis.md`, `metadata.json`, and any additional artifacts such as `strategy.md`, `questions.md`, or `research_log.md`.

## Installation And Validation

Install locally:

```bash
./scripts/install.sh
```

Validate the repository:

```bash
python3 scripts/validate_skill.py
python3 -m unittest discover -s tests
```

## Output Shape

Prefer concise sections:

- Scope and assumptions
- Confirmed facts / facts requiring proof
- Issues and burden of proof
- Evidence matrix and gaps
- Contradictions and causation
- Opponent perspective
- Judge perspective
- Research citations and source risks, when applicable
- Strategy and next smallest useful action

When writing files, also include a short console/chat summary with the output path and artifact list.
