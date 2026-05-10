# Official-Source Research Workflow

Use this reference when the task needs current statutes, regulations, cases, judgments, procedural rules, or comparable decisions.

## Source Priority

1. Official legislation databases for the jurisdiction.
2. Official court, judiciary, or tribunal sources.
3. High-authority government publications.
4. Secondary sources only for orientation, never as the sole legal basis.

## Execution Pattern

1. Confirm jurisdiction and procedural stage.
2. Extract legal relationship, conduct, harm, defense, evidence, and procedural keywords.
3. Select source domains from `official_source_registry.json`.
4. Run `scripts/legal_research.py` to produce a research log.
5. Read retrieved snippets and official pages before citing.
6. Mark every citation as verified, partial, inaccessible, or secondary.
7. Explain source risks: access limitations, outdated law, non-binding cases, factual differences, or jurisdiction mismatch.

## External Search Providers

`scripts/legal_research.py` supports provider selection:

- `official`: uses source-native public endpoints when available, currently UK `legislation.gov.uk` Atom feeds and The National Archives Find Case Law Atom feed.
- `duckduckgo`: no API key; uses official-domain restricted web queries.
- `bing`: no API key; uses Bing RSS results and filters URLs back to the official source domain.
- `brave`: requires `BRAVE_SEARCH_API_KEY`.
- `tavily`: requires `TAVILY_API_KEY`.
- `serpapi`: requires `SERPAPI_API_KEY`.
- `auto`: tries source-native public endpoints first, then configured API providers, then Bing RSS and DuckDuckGo.

Do not store API keys in the repo. Use environment variables for one run only.

Search engines can ignore `site:` filters or return automated-traffic challenges. The helper filters returned URLs against the selected official domain and records a `not_found_or_unverified` row when no official-domain result is returned. Treat that row as a cue for manual source review or a configured API provider, not as proof that no law or case exists.

## Citation Discipline

- Do not cite a source unless the URL, title, source name, and access date are recorded.
- Do not invent case numbers or statutory provisions.
- Do not treat one case as a guaranteed outcome.
- Do not use unofficial reposts when an official source is available.
