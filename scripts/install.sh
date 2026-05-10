#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${CODEX_HOME:-$HOME/.codex}/skills/legal-assistant-agent"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

mkdir -p "$TARGET"

rsync -a \
  --exclude ".git/" \
  --exclude ".DS_Store" \
  --exclude "tests/" \
  --exclude "work/" \
  --exclude "__pycache__/" \
  "$ROOT_DIR"/ "$TARGET"/

chmod +x "$TARGET/scripts/"*.py "$TARGET/scripts/"*.sh "$TARGET/install.sh"

echo "Installed legal-assistant-agent skill to: $TARGET"
echo "Restart Codex to load newly installed skills."
