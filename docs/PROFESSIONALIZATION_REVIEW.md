# Professionalization Review

This review was written after reading every existing file in the repository: the agent spec, method wheel, conversion prompt, system/developer prompts, output schemas, 14 skill modules, templates, example, README, manifest, and license.

## Current Strengths

- The safety boundary is unusually clear for a legal assistant: no fabricated authorities, no illegal evidence collection, no false statements, no outcome promises.
- The method wheel is coherent and maps naturally to professional dispute work: scope, facts, issues, evidence, contradictions, causation, opponent view, judge view, strategy, review.
- The 14 modules are well separated and can be invoked independently for common legal workflows.
- The templates encourage evidence discipline rather than free-form advice.
- The README already presents the project as a public bilingual skill pack.

## Main Gaps Before This Iteration

- No top-level `SKILL.md`, so Codex could not discover the project as a single installable skill.
- `case_reference_research` described a research process but did not provide a networked execution layer.
- No official source registry existed for selecting jurisdiction-specific legislation and case-law sources.
- No deterministic way existed to save analysis artifacts into a user-specified output folder.
- No validation or test command existed, so regressions in skill metadata, scripts, and source registry were easy to miss.
- No install script existed, so users had to manually copy files into a Codex skill path.

## Implemented Upgrade

- Added top-level `SKILL.md` as the installable skill entrypoint.
- Added official-source registry under `references/official_source_registry.json`.
- Added research workflow reference under `references/research_workflow.md`.
- Added `scripts/legal_research.py` for jurisdiction-aware official-domain queries, UK source-native Atom adapters, external search providers, and research logs.
- Added `scripts/write_analysis_output.py` for writing analysis bundles to case workspaces.
- Added `scripts/validate_skill.py`, `tests/test_tooling.py`, and `Makefile` targets.
- Added install scripts at `install.sh` and `scripts/install.sh`.
- Added `agents/openai.yaml` UI metadata.

## Remaining Product Opportunities

- Add jurisdiction-specific adapters for China, Hong Kong, U.S. federal, and common-law jurisdictions that understand each source's native search syntax.
- Add structured citation objects to downstream analysis outputs: source, URL, access date, rule extracted, binding force, and reliability status.
- Add document-ingestion helpers for PDFs, DOCX, screenshots, and chat exports.
- Add a formal case-state model so each analysis run can diff facts, evidence, issues, and strategy across versions.
- Add redaction tooling for names, phone numbers, IDs, addresses, and financial account numbers before writing outputs.
- Add bilingual output toggles and jurisdiction-specific writing conventions.
- Add sample workspaces for contract, labor, consumer, leasing, tort, company, and family disputes.
