#!/usr/bin/env python3
"""Validate the Legal Assistant Agent skill pack."""

from __future__ import annotations

import json
import py_compile
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise AssertionError(message)


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path} missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        fail(f"{path} frontmatter is not closed")
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    for required in ["name", "description"]:
        if not fields.get(required):
            fail(f"{path} missing frontmatter field: {required}")
    return fields


def parse_manifest_paths(path: Path) -> list[Path]:
    paths: list[Path] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"\s+path:\s+(.+)$", line)
        if match:
            paths.append(ROOT / match.group(1).strip())
    return paths


def validate_sources() -> None:
    path = ROOT / "references" / "official_source_registry.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    jurisdictions = registry.get("jurisdictions", {})
    for code in ["CN", "HK", "US-FEDERAL", "UK", "EU", "CA", "AU", "SG"]:
        if code not in jurisdictions:
            fail(f"source registry missing jurisdiction {code}")
        sources = jurisdictions[code].get("sources", [])
        if not any(source.get("authority") == "official" for source in sources):
            fail(f"{code} has no official source")
        for source in sources:
            for required in ["name", "domain", "base_url", "type", "authority"]:
                if not source.get(required):
                    fail(f"{code} source missing {required}: {source}")


def validate_scripts() -> None:
    for script in [
        ROOT / "scripts" / "legal_research.py",
        ROOT / "scripts" / "write_analysis_output.py",
        ROOT / "scripts" / "validate_skill.py",
    ]:
        if not script.exists():
            fail(f"missing script {script}")
        py_compile.compile(str(script), doraise=True)
    for script in [ROOT / "scripts" / "install.sh", ROOT / "install.sh"]:
        if not script.exists():
            fail(f"missing install script {script}")


def main() -> int:
    top = ROOT / "SKILL.md"
    fields = read_frontmatter(top)
    if fields["name"] != "legal-assistant-agent":
        fail("top-level skill name must be legal-assistant-agent")
    manifest_paths = parse_manifest_paths(ROOT / "agent_manifest.yaml")
    if len(manifest_paths) < 14:
        fail("manifest should list all 14 skill modules")
    for path in manifest_paths:
        if not path.exists():
            fail(f"manifest path does not exist: {path}")
        read_frontmatter(path)
    validate_sources()
    validate_scripts()
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for required in ["Kevin KE", "laoke.ai", "MIT License", "legal_research.py", "install"]:
        if required not in readme:
            fail(f"README missing {required}")
    print("Validation passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
