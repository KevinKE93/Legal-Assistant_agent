#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
DEST_DIR="$CODEX_HOME_DIR/skills/legal-assistant"

mkdir -p "$DEST_DIR"
mkdir -p "$DEST_DIR/references/docs" "$DEST_DIR/references/prompts" "$DEST_DIR/references/skills"
mkdir -p "$DEST_DIR/assets" "$DEST_DIR/tools"

RSYNC_EXCLUDES=(--exclude ".DS_Store")

rsync -a "${RSYNC_EXCLUDES[@]}" "$ROOT_DIR/native/legal-assistant/" "$DEST_DIR/"
rsync -a --delete "${RSYNC_EXCLUDES[@]}" "$ROOT_DIR/native/legal-assistant/commands/" "$DEST_DIR/commands/"
rsync -a "${RSYNC_EXCLUDES[@]}" "$ROOT_DIR/AGENTS.md" "$DEST_DIR/references/AGENTS.md"
rsync -a --delete "${RSYNC_EXCLUDES[@]}" "$ROOT_DIR/docs/" "$DEST_DIR/references/docs/"
rsync -a "${RSYNC_EXCLUDES[@]}" "$ROOT_DIR/prompts/" "$DEST_DIR/references/prompts/"
rsync -a "${RSYNC_EXCLUDES[@]}" "$ROOT_DIR/skills/" "$DEST_DIR/references/skills/"
rsync -a "${RSYNC_EXCLUDES[@]}" "$ROOT_DIR/assets/" "$DEST_DIR/assets/"
find "$DEST_DIR/tools" -mindepth 1 -maxdepth 1 -type f -delete
rsync -a "${RSYNC_EXCLUDES[@]}" "$ROOT_DIR/tools/render_report_pdf.py" "$DEST_DIR/tools/"

find "$DEST_DIR" -name ".DS_Store" -type f -delete

printf 'Installed legal-assistant native skill to %s\n' "$DEST_DIR"
printf 'Restart Codex to pick up new skills.\n'
