# legal assistant

Use the `$legal-assistant` native skill.

This is the preferred user-facing entry for Legal-Assistant_agent. If the client does not support spaces in command names, use `legal-assistant` instead.

Follow the bundled `references/AGENTS.md` workflow, then route the matter through `references/docs/CAPABILITIES.md`. For complex matters, create or reuse `work/<date>_<localized matter name>/`, maintain PDCA state, execute required stage skills, update `skill_outputs.md`, and return a substantive legal-workbench briefing. Generate Markdown reports only on request and PDFs only on explicit PDF request.
