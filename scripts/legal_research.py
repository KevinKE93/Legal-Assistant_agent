#!/usr/bin/env python3
"""Official-source legal research helper.

This script builds jurisdiction-aware, official-domain search queries and can
write a research bundle with search results and lightweight page snippets. It is
not a legal authority by itself; it records sources for human/agent review.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


DEFAULT_USER_AGENT = "LegalAssistantAgent/1.0 (+https://laoke.ai)"
ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "tna": "https://caselaw.nationalarchives.gov.uk",
}


class ResearchQuery:
    def __init__(self, jurisdiction: str, source: dict[str, Any], search_query: str):
        self.jurisdiction = jurisdiction
        self.source = source
        self.search_query = search_query

    def as_dict(self) -> dict[str, Any]:
        return {
            "jurisdiction": self.jurisdiction,
            "source": self.source,
            "search_query": self.search_query,
        }


def load_source_registry(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_jurisdiction(registry: dict[str, Any], jurisdiction: str) -> str:
    wanted = jurisdiction.strip().lower()
    jurisdictions = registry.get("jurisdictions", {})
    for code, data in jurisdictions.items():
        if code.lower() == wanted:
            return code
        aliases = [alias.lower() for alias in data.get("aliases", [])]
        if wanted in aliases:
            return code
    raise ValueError(f"Unknown jurisdiction: {jurisdiction}")


def build_queries(
    registry: dict[str, Any],
    jurisdiction: str,
    issue: str,
    case_type: str = "",
    max_sources: int = 6,
    official_only: bool = True,
) -> list[ResearchQuery]:
    code = normalize_jurisdiction(registry, jurisdiction)
    sources = registry["jurisdictions"][code]["sources"]
    filtered = [
        source
        for source in sources
        if not official_only or source.get("authority") == "official"
    ][:max_sources]
    keywords = " ".join(part.strip() for part in [issue, case_type] if part.strip())
    return [
        ResearchQuery(
            jurisdiction=code,
            source=source,
            search_query=f"site:{source['domain']} {keywords}".strip(),
        )
        for source in filtered
    ]


def http_json(url: str, headers: dict[str, str] | None = None, timeout: int = 20) -> Any:
    request = urllib.request.Request(url, headers=headers or {"User-Agent": DEFAULT_USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def http_text(url: str, headers: dict[str, str] | None = None, timeout: int = 20) -> str:
    request = urllib.request.Request(url, headers=headers or {"User-Agent": DEFAULT_USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read()
    return raw.decode("utf-8", errors="replace")


def search_duckduckgo(search_query: str, max_results: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"q": search_query})
    url = f"https://duckduckgo.com/html/?{params}"
    page = http_text(url)
    if "Unfortunately, bots use DuckDuckGo too" in page or "anomaly-modal" in page:
        raise RuntimeError("DuckDuckGo returned an automated-traffic challenge")
    results: list[dict[str, Any]] = []
    pattern = re.compile(
        r'<a[^>]+class="result__a"[^>]+href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>',
        re.IGNORECASE | re.DOTALL,
    )
    for match in pattern.finditer(page):
        href = html.unescape(match.group("href"))
        title = clean_html(match.group("title"))
        parsed = urllib.parse.urlparse(href)
        query = urllib.parse.parse_qs(parsed.query)
        if "uddg" in query:
            href = query["uddg"][0]
        results.append({"title": title, "url": href, "provider": "duckduckgo"})
        if len(results) >= max_results:
            break
    return results


def search_bing(search_query: str, max_results: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"q": search_query, "format": "rss", "mkt": "en-US", "setlang": "en-US"})
    feed = http_text(f"https://www.bing.com/search?{params}")
    root = ET.fromstring(feed)
    results: list[dict[str, Any]] = []
    for item in root.findall(".//item"):
        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        description = item.findtext("description") or ""
        published = item.findtext("pubDate") or ""
        results.append(
            {
                "title": clean_html(title),
                "url": html.unescape(link.strip()),
                "snippet": clean_html(description),
                "published": published,
                "provider": "bing",
            }
        )
        if len(results) >= max_results:
            break
    return results


def atom_entry_link(entry: ET.Element) -> str:
    alternate = ""
    for link in entry.findall("atom:link", ATOM_NS):
        href = link.attrib.get("href", "")
        rel = link.attrib.get("rel", "alternate")
        content_type = link.attrib.get("type", "")
        if rel == "alternate" and content_type in {"", "text/html"}:
            return href
        if rel == "alternate" and not alternate:
            alternate = href
    return alternate


def parse_atom_feed(feed: str, provider: str, max_results: int) -> list[dict[str, Any]]:
    root = ET.fromstring(feed)
    results: list[dict[str, Any]] = []
    for entry in root.findall("atom:entry", ATOM_NS):
        title = entry.findtext("atom:title", default="", namespaces=ATOM_NS)
        summary = entry.findtext("atom:summary", default="", namespaces=ATOM_NS)
        published = entry.findtext("atom:published", default="", namespaces=ATOM_NS)
        updated = entry.findtext("atom:updated", default="", namespaces=ATOM_NS)
        author = entry.findtext("atom:author/atom:name", default="", namespaces=ATOM_NS)
        results.append(
            {
                "title": clean_html(title),
                "url": atom_entry_link(entry),
                "snippet": clean_html(summary),
                "published": published,
                "updated": updated,
                "court_or_authority": clean_html(author),
                "provider": provider,
            }
        )
        if len(results) >= max_results:
            break
    return results


def search_legislation_gov_uk(keywords: str, max_results: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"title": keywords, "results-count": max_results})
    url = f"https://www.legislation.gov.uk/all/data.feed?{params}"
    results = parse_atom_feed(http_text(url), "official:legislation.gov.uk", max_results)
    for result in results:
        result["search_url"] = url
    return results


def search_find_case_law(keywords: str, max_results: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"query": keywords})
    url = f"https://caselaw.nationalarchives.gov.uk/atom.xml?{params}"
    results = parse_atom_feed(http_text(url), "official:find-case-law", max_results)
    for result in results:
        result["search_url"] = url
    return results


def run_official_source_search(research_query: ResearchQuery, keywords: str, max_results: int) -> list[dict[str, Any]]:
    adapter = research_query.source.get("search_adapter", "")
    domain = research_query.source.get("domain", "")
    if adapter == "legislation_gov_uk_atom" or domain == "www.legislation.gov.uk":
        results = search_legislation_gov_uk(keywords, max_results)
    elif adapter == "find_case_law_atom" or domain == "caselaw.nationalarchives.gov.uk":
        results = search_find_case_law(keywords, max_results)
    else:
        results = []
    for result in results:
        result.setdefault("search_query", keywords)
        result["source_adapter"] = adapter or domain
    return results


def search_brave(search_query: str, max_results: int) -> list[dict[str, Any]]:
    token = os.environ.get("BRAVE_SEARCH_API_KEY")
    if not token:
        raise RuntimeError("BRAVE_SEARCH_API_KEY is not set")
    params = urllib.parse.urlencode({"q": search_query, "count": max_results})
    data = http_json(
        f"https://api.search.brave.com/res/v1/web/search?{params}",
        headers={
            "Accept": "application/json",
            "X-Subscription-Token": token,
            "User-Agent": DEFAULT_USER_AGENT,
        },
    )
    return [
        {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "snippet": item.get("description", ""),
            "provider": "brave",
        }
        for item in data.get("web", {}).get("results", [])[:max_results]
    ]


def search_tavily(search_query: str, max_results: int) -> list[dict[str, Any]]:
    token = os.environ.get("TAVILY_API_KEY")
    if not token:
        raise RuntimeError("TAVILY_API_KEY is not set")
    payload = json.dumps({"api_key": token, "query": search_query, "max_results": max_results}).encode()
    request = urllib.request.Request(
        "https://api.tavily.com/search",
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": DEFAULT_USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8", errors="replace"))
    return [
        {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "snippet": item.get("content", ""),
            "provider": "tavily",
        }
        for item in data.get("results", [])[:max_results]
    ]


def search_serpapi(search_query: str, max_results: int) -> list[dict[str, Any]]:
    token = os.environ.get("SERPAPI_API_KEY")
    if not token:
        raise RuntimeError("SERPAPI_API_KEY is not set")
    params = urllib.parse.urlencode({"engine": "google", "q": search_query, "api_key": token, "num": max_results})
    data = http_json(f"https://serpapi.com/search.json?{params}")
    return [
        {
            "title": item.get("title", ""),
            "url": item.get("link", ""),
            "snippet": item.get("snippet", ""),
            "provider": "serpapi",
        }
        for item in data.get("organic_results", [])[:max_results]
    ]


def run_search(provider: str, search_query: str, max_results: int) -> list[dict[str, Any]]:
    providers = {
        "bing": search_bing,
        "duckduckgo": search_duckduckgo,
        "brave": search_brave,
        "tavily": search_tavily,
        "serpapi": search_serpapi,
    }
    if provider != "auto":
        return providers[provider](search_query, max_results)
    for candidate in ["brave", "tavily", "serpapi", "bing", "duckduckgo"]:
        try:
            return providers[candidate](search_query, max_results)
        except Exception:
            continue
    return []


def clean_html(value: str) -> str:
    value = re.sub(r"<script.*?</script>", " ", value, flags=re.IGNORECASE | re.DOTALL)
    value = re.sub(r"<style.*?</style>", " ", value, flags=re.IGNORECASE | re.DOTALL)
    value = re.sub(r"<[^>]+>", " ", value)
    return html.unescape(re.sub(r"\s+", " ", value)).strip()


def fetch_snippet(url: str, max_chars: int = 4000) -> tuple[str, str | None]:
    try:
        text = http_text(url, timeout=20)
        return clean_html(text)[:max_chars], None
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        return "", str(exc)


def safe_slug(value: str, fallback: str = "item") -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-._").lower()
    return slug[:80] or fallback


def url_matches_domain(url: str, domain: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower().split("@")[-1].split(":")[0]
    wanted = domain.strip().lower()
    if not host or not wanted:
        return False
    return host == wanted or host.endswith(f".{wanted}")


def provider_search_url(provider: str, search_query: str) -> str:
    encoded = urllib.parse.quote_plus(search_query)
    if provider in {"auto", "bing"}:
        return f"https://www.bing.com/search?q={encoded}"
    if provider == "duckduckgo":
        return f"https://duckduckgo.com/?q={encoded}"
    if provider == "brave":
        return f"https://search.brave.com/search?q={encoded}"
    if provider == "serpapi":
        return f"https://www.google.com/search?q={encoded}"
    if provider == "tavily":
        return f"https://app.tavily.com/search?query={encoded}"
    return f"https://www.google.com/search?q={encoded}"


def no_official_results_record(
    provider: str,
    research_query: ResearchQuery,
    reason: str,
) -> dict[str, Any]:
    return {
        "title": "No official-domain results returned",
        "url": research_query.source.get("base_url", ""),
        "provider": provider,
        "search_query": research_query.search_query,
        "search_url": provider_search_url(provider, research_query.search_query),
        "source_name": research_query.source.get("name"),
        "source_domain": research_query.source.get("domain"),
        "verification_status": "not_found_or_unverified",
        "fetch_error": reason,
    }


def write_research_bundle(
    out_dir: Path,
    jurisdiction: str,
    query: str,
    case_type: str,
    provider: str,
    queries: list[ResearchQuery],
    results: list[dict[str, Any]],
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    retrieved_dir = out_dir / "retrieved"
    retrieved_dir.mkdir(exist_ok=True)
    generated_at = _dt.datetime.now(_dt.UTC).isoformat()
    payload = {
        "generated_at": generated_at,
        "jurisdiction": jurisdiction,
        "query": query,
        "case_type": case_type,
        "provider": provider,
        "queries": [item.as_dict() for item in queries],
        "results": results,
    }
    results_path = out_dir / "results.json"
    results_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Legal Research Log",
        "",
        f"- Generated at: {generated_at}",
        f"- Jurisdiction: {jurisdiction}",
        f"- Query: {query}",
        f"- Case type: {case_type or 'not specified'}",
        f"- Provider: {provider}",
        "",
        "## Search Queries",
        "",
    ]
    for item in queries:
        lines.append(f"- `{item.search_query}` ({item.source['name']})")
    lines.extend(["", "## Results", ""])
    for index, item in enumerate(results, start=1):
        lines.append(f"### {index}. {item.get('title') or 'Untitled'}")
        lines.append(f"- URL: {item.get('url', '')}")
        lines.append(f"- Provider: {item.get('provider', provider)}")
        if item.get("search_query"):
            lines.append(f"- Search query: `{item['search_query']}`")
        if item.get("search_url"):
            lines.append(f"- Search URL: {item['search_url']}")
        if item.get("source_name"):
            lines.append(f"- Source: {item['source_name']}")
        if item.get("verification_status"):
            lines.append(f"- Verification status: {item['verification_status']}")
        if item.get("search_error"):
            lines.append(f"- Search status: {item['search_error']}")
        if item.get("fetch_error"):
            lines.append(f"- Fetch status: {item['fetch_error']}")
        if item.get("snippet_file"):
            lines.append(f"- Snippet file: {item['snippet_file']}")
        if item.get("snippet"):
            lines.append(f"- Snippet: {item['snippet'][:500]}")
        lines.append("")
    lines.extend(
        [
            "## Use Notes",
            "",
            "- Verify the currentness and binding force of each source before citing.",
            "- Do not infer a rule from a single case without comparing facts and jurisdiction.",
            "- Treat inaccessible sources as unverified, not as negative authority.",
        ]
    )
    log_path = out_dir / "research_log.md"
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"results_json": results_path, "research_log": log_path, "retrieved_dir": retrieved_dir}


def perform_research(args: argparse.Namespace) -> dict[str, Path]:
    registry_path = Path(args.registry)
    registry = load_source_registry(registry_path)
    jurisdiction = normalize_jurisdiction(registry, args.jurisdiction)
    queries = build_queries(
        registry=registry,
        jurisdiction=jurisdiction,
        issue=args.query,
        case_type=args.case_type,
        max_sources=args.max_sources,
        official_only=not args.include_secondary,
    )
    all_results: list[dict[str, Any]] = []
    seen_urls: set[str] = set()
    per_query = max(1, args.max_results // max(1, len(queries)))
    official_keywords = args.query.strip()
    for research_query in queries:
        query_added = 0
        source_domain = research_query.source.get("domain", "")
        try:
            query_results = []
            if args.provider in {"auto", "official"}:
                query_results = run_official_source_search(research_query, official_keywords, per_query)
            if not query_results and args.provider != "official":
                query_results = run_search(args.provider, research_query.search_query, per_query)
        except Exception as exc:
            query_results = [{"title": "Search failed", "url": "", "provider": args.provider, "search_error": str(exc)}]
        for result in query_results:
            url = result.get("url", "")
            if result.get("search_error"):
                result["verification_status"] = "search_failed"
            elif url and not url_matches_domain(url, source_domain):
                continue
            elif not url:
                continue
            if url and url in seen_urls:
                continue
            if url:
                seen_urls.add(url)
            result["jurisdiction"] = jurisdiction
            result["source_name"] = research_query.source.get("name")
            result["source_domain"] = source_domain
            result.setdefault("search_query", research_query.search_query)
            result.setdefault("search_url", provider_search_url(args.provider, research_query.search_query))
            result.setdefault("verification_status", "source_url_recorded")
            if url and not args.no_fetch:
                snippet, error = fetch_snippet(url, args.max_chars)
                result["snippet"] = snippet
                if error:
                    result["fetch_error"] = error
            all_results.append(result)
            query_added += 1
            if len(all_results) >= args.max_results:
                break
        if query_added == 0 and len(all_results) < args.max_results:
            all_results.append(
                no_official_results_record(
                    args.provider,
                    research_query,
                    "Search provider returned no result URL inside the official source domain; open the search URL/source manually or configure an API provider.",
                )
            )
        if len(all_results) >= args.max_results:
            break

    out_dir = Path(args.out_dir)
    paths = write_research_bundle(out_dir, jurisdiction, args.query, args.case_type, args.provider, queries, all_results)
    retrieved_dir = paths["retrieved_dir"]
    for index, item in enumerate(all_results, start=1):
        if item.get("snippet"):
            snippet_name = f"{index:02d}-{safe_slug(item.get('title', 'source'))}.txt"
            (retrieved_dir / snippet_name).write_text(item["snippet"], encoding="utf-8")
            item["snippet_file"] = f"retrieved/{snippet_name}"
    (out_dir / "results.json").write_text(
        json.dumps(
            {
                "generated_at": _dt.datetime.now(_dt.UTC).isoformat(),
                "jurisdiction": jurisdiction,
                "query": args.query,
                "case_type": args.case_type,
                "provider": args.provider,
                "queries": [item.as_dict() for item in queries],
                "results": all_results,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    write_research_bundle(out_dir, jurisdiction, args.query, args.case_type, args.provider, queries, all_results)
    return paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run official-source legal research.")
    parser.add_argument("--jurisdiction", required=True, help="Jurisdiction code or alias, e.g. CN, US-FEDERAL, HK.")
    parser.add_argument("--query", required=True, help="Legal issue or search query.")
    parser.add_argument("--case-type", default="", help="Optional case type, e.g. contract, labor, tort.")
    parser.add_argument("--out-dir", required=True, help="Output directory for research artifacts.")
    parser.add_argument("--registry", default="references/official_source_registry.json", help="Source registry path.")
    parser.add_argument("--provider", default="auto", choices=["auto", "official", "bing", "duckduckgo", "brave", "tavily", "serpapi"])
    parser.add_argument("--max-sources", type=int, default=6)
    parser.add_argument("--max-results", type=int, default=10)
    parser.add_argument("--max-chars", type=int, default=4000)
    parser.add_argument("--include-secondary", action="store_true", help="Include non-official sources in registry if present.")
    parser.add_argument("--no-fetch", action="store_true", help="Do not fetch result pages; only record search results.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    paths = perform_research(args)
    print(f"Wrote research log: {paths['research_log']}")
    print(f"Wrote results JSON: {paths['results_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
