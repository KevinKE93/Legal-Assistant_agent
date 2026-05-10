#!/usr/bin/env python3
"""Write legal analysis artifacts to a case workspace."""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path
from typing import Any


def safe_slug(value: str, fallback: str = "case") -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-._").lower()
    return slug[:96] or fallback


def write_analysis_bundle(
    out_dir: Path,
    case_slug: str,
    analysis_markdown: str,
    metadata: dict[str, Any] | None = None,
    artifacts: dict[str, str] | None = None,
) -> dict[str, Path]:
    metadata = dict(metadata or {})
    artifacts = dict(artifacts or {})
    case_dir = out_dir / safe_slug(case_slug)
    case_dir.mkdir(parents=True, exist_ok=True)

    generated_at = _dt.datetime.now(_dt.UTC).isoformat()
    metadata.setdefault("generated_at", generated_at)
    metadata.setdefault("case_slug", safe_slug(case_slug))

    analysis_path = case_dir / "analysis.md"
    metadata_path = case_dir / "metadata.json"
    index_path = case_dir / "INDEX.md"

    analysis_path.write_text(analysis_markdown.rstrip() + "\n", encoding="utf-8")
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    artifact_paths: dict[str, Path] = {}
    for relative_path, content in artifacts.items():
        clean_path = Path(relative_path)
        if clean_path.is_absolute() or ".." in clean_path.parts:
            raise ValueError(f"Unsafe artifact path: {relative_path}")
        target = case_dir / clean_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content.rstrip() + "\n", encoding="utf-8")
        artifact_paths[relative_path] = target

    index_lines = [
        "# Case Workspace Index",
        "",
        f"- Case slug: `{metadata['case_slug']}`",
        f"- Generated at: {metadata['generated_at']}",
        "",
        "## Core Files",
        "",
        "- `analysis.md`",
        "- `metadata.json`",
    ]
    if artifact_paths:
        index_lines.extend(["", "## Artifacts", ""])
        for relative_path in sorted(artifact_paths):
            index_lines.append(f"- `{relative_path}`")
    index_path.write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    result = {"case_dir": case_dir, "analysis": analysis_path, "metadata": metadata_path, "index": index_path}
    result.update(artifact_paths)
    return result


def parse_metadata(items: list[str]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Metadata must use key=value format: {item}")
        key, value = item.split("=", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write a legal analysis output bundle.")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--case-slug", required=True)
    parser.add_argument("--analysis-file", help="Markdown file to use as analysis. Defaults to stdin.")
    parser.add_argument("--artifact", action="append", default=[], help="Additional artifact as path=/absolute/source.md")
    parser.add_argument("--metadata", action="append", default=[], help="Metadata key=value. Can be repeated.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.analysis_file:
        analysis = Path(args.analysis_file).read_text(encoding="utf-8")
    else:
        analysis = sys.stdin.read()
    artifacts: dict[str, str] = {}
    for item in args.artifact:
        if "=" not in item:
            raise ValueError(f"Artifact must use path=/source/file format: {item}")
        relative_path, source_file = item.split("=", 1)
        artifacts[relative_path] = Path(source_file).read_text(encoding="utf-8")
    result = write_analysis_bundle(
        out_dir=Path(args.out_dir),
        case_slug=args.case_slug,
        analysis_markdown=analysis,
        metadata=parse_metadata(args.metadata),
        artifacts=artifacts,
    )
    print(f"Wrote case workspace: {result['case_dir']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
