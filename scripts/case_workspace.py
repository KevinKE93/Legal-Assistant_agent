#!/usr/bin/env python3
"""Manage local case workspaces for Legal-Assistant_agent."""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"
DEFAULT_OUT_DIR = Path("work/cases")
DEFAULT_ACTOR = "legal-assistant-agent"


def utc_now() -> str:
    return _dt.datetime.now(_dt.UTC).isoformat(timespec="seconds")


def safe_slug(value: str, fallback: str = "case") -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-._").lower()
    return slug[:96] or fallback


def derive_slug(case_slug: str | None, title: str | None, case_type: str | None) -> str:
    if case_slug:
        return safe_slug(case_slug)
    today = _dt.datetime.now(_dt.UTC).strftime("%Y%m%d")
    basis = " ".join(part for part in [case_type, title, today] if part)
    return safe_slug(basis, fallback=f"case-{today}")


def case_dir(out_dir: Path, case_slug: str) -> Path:
    return out_dir / safe_slug(case_slug)


def state_path(path: Path) -> Path:
    return path / "case_state.json"


def log_path(path: Path) -> Path:
    return path / "activity_log.jsonl"


def ensure_workspace(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for child in ["checkpoints", "outputs", "research"]:
        (path / child).mkdir(parents=True, exist_ok=True)


def load_state(path: Path) -> dict[str, Any]:
    target = state_path(path)
    if not target.exists():
        raise FileNotFoundError(f"Case workspace is not initialized: {path}")
    return json.loads(target.read_text(encoding="utf-8"))


def write_state(path: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = utc_now()
    state_path(path).write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_log(path: Path, event: dict[str, Any]) -> None:
    event.setdefault("timestamp", utc_now())
    event.setdefault("actor", DEFAULT_ACTOR)
    with log_path(path).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def merge_list(existing: list[Any], additions: list[str]) -> list[Any]:
    result = list(existing or [])
    for item in additions:
        if item and item not in result:
            result.append(item)
    return result


def update_state_from_event(state: dict[str, Any], args: argparse.Namespace) -> None:
    if getattr(args, "stage", None):
        state["current_stage"] = args.stage
    if getattr(args, "risk_level", None):
        state["risk_level"] = args.risk_level
    state["open_questions"] = merge_list(state.get("open_questions", []), getattr(args, "open_question", []))
    state["next_actions"] = merge_list(state.get("next_actions", []), getattr(args, "next_action", []))
    state["issues"] = merge_list(state.get("issues", []), getattr(args, "issue", []))
    state["evidence_status"] = merge_list(state.get("evidence_status", []), getattr(args, "evidence_status", []))
    owners = getattr(args, "owner", [])
    if isinstance(owners, str):
        owners = [owners]
    state["responsible_parties"] = merge_list(state.get("responsible_parties", []), owners)


def command_init(args: argparse.Namespace) -> int:
    slug = derive_slug(args.case_slug, args.title, args.case_type)
    path = case_dir(Path(args.out_dir), slug)
    ensure_workspace(path)
    now = utc_now()
    state = {
        "schema_version": SCHEMA_VERSION,
        "case_slug": slug,
        "case_title": args.title or slug,
        "created_at": now,
        "updated_at": now,
        "jurisdiction": args.jurisdiction or "",
        "case_type": args.case_type or "",
        "procedural_stage": args.procedural_stage or "",
        "current_stage": args.stage,
        "risk_level": args.risk_level or "",
        "issues": list(args.issue),
        "evidence_status": list(args.evidence_status),
        "open_questions": list(args.open_question),
        "next_actions": list(args.next_action),
        "responsible_parties": list(args.owner),
        "checkpoint_count": 0,
        "last_checkpoint": "",
    }
    write_state(path, state)
    append_log(
        path,
        {
            "event_type": "init",
            "stage": args.stage,
            "summary": args.summary or "Initialized case workspace.",
            "owner": args.owner,
            "next_actions": args.next_action,
            "open_questions": args.open_question,
        },
    )
    print(f"Initialized case workspace: {path}")
    return 0


def command_record(args: argparse.Namespace) -> int:
    path = case_dir(Path(args.out_dir), args.case_slug)
    state = load_state(path)
    update_state_from_event(state, args)
    write_state(path, state)
    append_log(
        path,
        {
            "event_type": "record",
            "stage": args.stage,
            "summary": args.summary,
            "owner": args.owner,
            "next_actions": args.next_action,
            "open_questions": args.open_question,
            "issues": args.issue,
            "evidence_status": args.evidence_status,
            "risk_level": args.risk_level,
        },
    )
    print(f"Recorded activity: {path}")
    return 0


def read_content(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def command_checkpoint(args: argparse.Namespace) -> int:
    path = case_dir(Path(args.out_dir), args.case_slug)
    state = load_state(path)
    raw_content = read_content(args.content_file)
    if not raw_content.strip():
        raise ValueError("Checkpoint content is empty; pass --content-file or pipe markdown content.")
    content = raw_content.rstrip() + "\n"
    timestamp = _dt.datetime.now(_dt.UTC).strftime("%Y%m%dT%H%M%SZ")
    stage_slug = safe_slug(args.stage)
    title_slug = safe_slug(args.title or "checkpoint")
    relative = Path("checkpoints") / f"{timestamp}_{stage_slug}_{title_slug}.md"
    target = path / relative
    target.write_text(content, encoding="utf-8")

    state["checkpoint_count"] = int(state.get("checkpoint_count", 0)) + 1
    state["last_checkpoint"] = str(relative)
    update_state_from_event(state, args)
    write_state(path, state)
    append_log(
        path,
        {
            "event_type": "checkpoint",
            "stage": args.stage,
            "summary": args.summary or f"Saved checkpoint: {args.title}",
            "checkpoint": str(relative),
            "owner": args.owner,
            "next_actions": args.next_action,
            "open_questions": args.open_question,
            "issues": args.issue,
            "evidence_status": args.evidence_status,
            "risk_level": args.risk_level,
        },
    )
    print(f"Saved checkpoint: {target}")
    return 0


def render_status(path: Path, state: dict[str, Any]) -> str:
    lines = [
        "# Case Workspace Status",
        "",
        f"- Case slug: `{state.get('case_slug', '')}`",
        f"- Title: {state.get('case_title', '')}",
        f"- Current stage: `{state.get('current_stage', '')}`",
        f"- Procedural stage: {state.get('procedural_stage', '')}",
        f"- Risk level: {state.get('risk_level', '')}",
        f"- Updated at: {state.get('updated_at', '')}",
        f"- Workspace: `{path}`",
        "",
        "## Issues",
    ]
    issues = state.get("issues") or []
    lines.extend(f"- {item}" for item in issues) if issues else lines.append("- None recorded")
    lines.extend(["", "## Open Questions"])
    questions = state.get("open_questions") or []
    lines.extend(f"- {item}" for item in questions) if questions else lines.append("- None recorded")
    lines.extend(["", "## Next Actions"])
    actions = state.get("next_actions") or []
    lines.extend(f"- {item}" for item in actions) if actions else lines.append("- None recorded")
    lines.extend(["", "## Last Checkpoint"])
    lines.append(f"- `{state.get('last_checkpoint') or 'None recorded'}`")
    return "\n".join(lines) + "\n"


def command_status(args: argparse.Namespace) -> int:
    path = case_dir(Path(args.out_dir), args.case_slug)
    state = load_state(path)
    if args.json:
        print(json.dumps({"case_dir": str(path), "state": state}, ensure_ascii=False, indent=2))
    else:
        print(render_status(path, state), end="")
    return 0


def command_self_test(args: argparse.Namespace) -> int:
    tmp_root = Path(args.tmp_dir) if args.tmp_dir else Path(tempfile.mkdtemp(prefix="legal-assistant-case-workspace-"))
    slug = "self-test-labor-dispute"
    try:
        command_init(
            argparse.Namespace(
                out_dir=tmp_root,
                case_slug=slug,
                title="Self Test Labor Dispute",
                jurisdiction="CN",
                case_type="labor-dispute",
                procedural_stage="intake",
                stage="intake",
                risk_level="medium",
                issue=["wage basis"],
                evidence_status=["offer: pending review"],
                open_question=["confirm jurisdiction"],
                next_action=["agent: build issue matrix"],
                owner=["agent"],
                summary="Initialize smoke test workspace.",
            )
        )
        command_record(
            argparse.Namespace(
                out_dir=tmp_root,
                case_slug=slug,
                stage="issue-map",
                summary="Mapped initial disputes.",
                owner=["agent"],
                next_action=["user: provide payroll records"],
                open_question=["whether third-party payment was authorized"],
                issue=["overtime pay"],
                evidence_status=["payroll: requested"],
                risk_level="high",
            )
        )
        checkpoint_file = tmp_root / "checkpoint.md"
        checkpoint_file.write_text("## Issue Matrix\n\nSmoke test checkpoint.\n", encoding="utf-8")
        command_checkpoint(
            argparse.Namespace(
                out_dir=tmp_root,
                case_slug=slug,
                stage="burden-matrix",
                title="issue-matrix",
                content_file=str(checkpoint_file),
                summary="Saved issue matrix.",
                owner=["agent"],
                next_action=["agent: prepare judge view"],
                open_question=[],
                issue=[],
                evidence_status=[],
                risk_level="high",
            )
        )
        state = load_state(case_dir(tmp_root, slug))
        assert state["current_stage"] == "burden-matrix"
        assert "agent: prepare judge view" in state["next_actions"]
        assert "agent" in state["responsible_parties"]
        assert state["checkpoint_count"] == 1
        assert log_path(case_dir(tmp_root, slug)).read_text(encoding="utf-8").count("\n") >= 3
        print(f"Self-test passed: {case_dir(tmp_root, slug)}")
    finally:
        if args.cleanup:
            shutil.rmtree(tmp_root, ignore_errors=True)
    return 0


def add_common_case_args(parser: argparse.ArgumentParser, require_slug: bool = True) -> None:
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Root directory for case workspaces.")
    parser.add_argument("--case-slug", required=require_slug, help="Case workspace slug.")


def add_update_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--stage", required=True, help="Workflow stage name.")
    parser.add_argument("--risk-level", default="", help="Risk level to store in case_state.json.")
    parser.add_argument("--owner", action="append", default=[], help="Responsible party, e.g. agent, user, lawyer.")
    parser.add_argument("--next-action", action="append", default=[], help="Next action in owner: action format.")
    parser.add_argument("--open-question", action="append", default=[], help="Open question or missing fact.")
    parser.add_argument("--issue", action="append", default=[], help="Issue to add to case_state.json.")
    parser.add_argument("--evidence-status", action="append", default=[], help="Evidence status note.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Legal-Assistant_agent local case workspaces.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize a case workspace.")
    add_common_case_args(init_parser, require_slug=False)
    init_parser.add_argument("--title", help="Human-readable case title.")
    init_parser.add_argument("--jurisdiction", default="", help="Jurisdiction, e.g. CN, HK, US-FEDERAL.")
    init_parser.add_argument("--case-type", default="", help="Case type, e.g. labor-dispute.")
    init_parser.add_argument("--procedural-stage", default="", help="Procedural posture, e.g. negotiation, arbitration.")
    init_parser.add_argument("--summary", default="", help="Initial activity summary.")
    add_update_args(init_parser)
    init_parser.set_defaults(func=command_init)

    record_parser = subparsers.add_parser("record", help="Append an activity log and update case state.")
    add_common_case_args(record_parser)
    record_parser.add_argument("--summary", required=True, help="What happened in this stage.")
    add_update_args(record_parser)
    record_parser.set_defaults(func=command_record)

    checkpoint_parser = subparsers.add_parser("checkpoint", help="Save a stage checkpoint artifact.")
    add_common_case_args(checkpoint_parser)
    checkpoint_parser.add_argument("--title", required=True, help="Checkpoint title.")
    checkpoint_parser.add_argument("--summary", default="", help="Checkpoint summary for the activity log.")
    checkpoint_parser.add_argument("--content-file", help="Markdown file to save. Defaults to stdin.")
    add_update_args(checkpoint_parser)
    checkpoint_parser.set_defaults(func=command_checkpoint)

    status_parser = subparsers.add_parser("status", help="Read current case status.")
    add_common_case_args(status_parser)
    status_parser.add_argument("--json", action="store_true", help="Print JSON instead of markdown.")
    status_parser.set_defaults(func=command_status)

    test_parser = subparsers.add_parser("self-test", help="Run a smoke test in a temporary workspace.")
    test_parser.add_argument("--tmp-dir", help="Optional temporary root directory.")
    test_parser.add_argument("--cleanup", action="store_true", help="Remove temporary files after the smoke test.")
    test_parser.set_defaults(func=command_self_test)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, ValueError, AssertionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
