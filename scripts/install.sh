#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PACKAGE_NAME="法律助手智能体 Legal-Assistant_agent"
SKILL_SLUG="legal-assistant-agent"
CLIENT="codex"
TARGET=""
PROJECT_DIR="$PWD"

usage() {
  cat <<'EOF'
Install 法律助手智能体 Legal-Assistant_agent for AI agent clients.

Usage:
  ./scripts/install.sh [--client CLIENT] [--target PATH] [--project-dir PATH]

Clients:
  codex        Install as a Codex skill to ${CODEX_HOME:-$HOME/.codex}/skills/legal-assistant-agent
  claude-code  Install as a Claude Code skill to ~/.claude/skills/legal-assistant-agent
  openclaw     Install as an OpenClaw skill to ~/.openclaw/skills/legal-assistant-agent
  gemini-cli   Install a Gemini CLI custom command at ~/.gemini/commands/legal-assistant.toml
  opencode     Install an OpenCode custom command at ~/.config/opencode/commands/legal-assistant.md
  cursor       Install a Cursor project rule at <project>/.cursor/rules/legal-assistant-agent.mdc
  all          Install global integrations for codex, claude-code, openclaw, gemini-cli, and opencode

Options:
  --client CLIENT       Client to install for. Default: codex
  --target PATH         Override package target path for skill-style installs
  --project-dir PATH    Project directory for Cursor rules. Default: current working directory
  --list-clients        Print supported clients
  -h, --help            Show this help
EOF
}

list_clients() {
  printf '%s\n' codex claude-code openclaw gemini-cli opencode cursor all
}

copy_package() {
  local target="$1"
  mkdir -p "$target"
  rsync -a \
    --exclude ".git/" \
    --exclude ".DS_Store" \
    --exclude "work/" \
    --exclude "__pycache__/" \
    "$ROOT_DIR"/ "$target"/
  chmod +x "$target/scripts/"*.py "$target/scripts/"*.sh "$target/install.sh"
}

install_codex() {
  local target="${TARGET:-${CODEX_HOME:-$HOME/.codex}/skills/$SKILL_SLUG}"
  copy_package "$target"
  echo "Installed $PACKAGE_NAME for Codex: $target"
}

install_claude_code() {
  local target="${TARGET:-$HOME/.claude/skills/$SKILL_SLUG}"
  copy_package "$target"
  echo "Installed $PACKAGE_NAME for Claude Code: $target"
}

install_openclaw() {
  local target="${TARGET:-$HOME/.openclaw/skills/$SKILL_SLUG}"
  copy_package "$target"
  echo "Installed $PACKAGE_NAME for OpenClaw: $target"
}

install_gemini_cli() {
  local package_target="${TARGET:-$HOME/.gemini/skills/$SKILL_SLUG}"
  local command_dir="$HOME/.gemini/commands"
  local command_file="$command_dir/legal-assistant.toml"
  copy_package "$package_target"
  mkdir -p "$command_dir"
  cat > "$command_file" <<EOF
description = "Use 法律助手智能体 Legal-Assistant_agent for privacy-first legal dispute analysis."
prompt = """
Use 法律助手智能体 Legal-Assistant_agent to handle this request.

Read and follow these package files when relevant:
- $package_target/SKILL.md
- $package_target/prompts/system_prompt.md
- $package_target/prompts/developer_prompt.md
- $package_target/prompts/output_schemas.md

For official-source research, use:
- $package_target/scripts/legal_research.py

For local case workspace memory and checkpoints, use:
- $package_target/scripts/case_workspace.py
- $package_target/references/case_workspace_protocol.md

For writing analysis output to a workspace, use:
- $package_target/scripts/write_analysis_output.py

User request:
{{args}}
"""
EOF
  echo "Installed $PACKAGE_NAME for Gemini CLI: $command_file"
  echo "Run /commands reload in Gemini CLI, then use /legal-assistant <request>."
}

install_opencode() {
  local package_target="${TARGET:-$HOME/.config/opencode/skills/$SKILL_SLUG}"
  local command_dir="$HOME/.config/opencode/commands"
  local command_file="$command_dir/legal-assistant.md"
  copy_package "$package_target"
  mkdir -p "$command_dir"
  cat > "$command_file" <<EOF
---
description: Use 法律助手智能体 Legal-Assistant_agent for legal dispute analysis, official-source research, drafting, and hearing preparation.
---

Use 法律助手智能体 Legal-Assistant_agent to handle this request.

Read and follow the package entrypoint and supporting files when relevant:

- $package_target/SKILL.md
- $package_target/prompts/system_prompt.md
- $package_target/prompts/developer_prompt.md
- $package_target/prompts/output_schemas.md

Use official-source research through:

- $package_target/scripts/legal_research.py

Use local case workspace memory and checkpoints through:

- $package_target/scripts/case_workspace.py
- $package_target/references/case_workspace_protocol.md

Use workspace output through:

- $package_target/scripts/write_analysis_output.py

User request:

\$ARGUMENTS
EOF
  echo "Installed $PACKAGE_NAME for OpenCode: $command_file"
  echo "Use /legal-assistant <request> in OpenCode."
}

install_cursor() {
  local package_target="${TARGET:-$HOME/.cursor/skills/$SKILL_SLUG}"
  local rule_dir="$PROJECT_DIR/.cursor/rules"
  local rule_file="$rule_dir/legal-assistant-agent.mdc"
  copy_package "$package_target"
  mkdir -p "$rule_dir"
  cat > "$rule_file" <<EOF
---
description: Use 法律助手智能体 Legal-Assistant_agent for legal dispute analysis, official-source research, drafting, and hearing preparation.
alwaysApply: false
---

When the user asks for legal dispute analysis, evidence mapping, legal research, legal-related drafting, hearing preparation, or saving legal analysis artifacts, use 法律助手智能体 Legal-Assistant_agent.

Follow these package files when relevant:

- $package_target/SKILL.md
- $package_target/prompts/system_prompt.md
- $package_target/prompts/developer_prompt.md
- $package_target/prompts/output_schemas.md

For official-source research, use:

- $package_target/scripts/legal_research.py

For local case workspace memory and checkpoints, use:

- $package_target/scripts/case_workspace.py
- $package_target/references/case_workspace_protocol.md

For writing analysis output to a workspace, use:

- $package_target/scripts/write_analysis_output.py
EOF
  echo "Installed $PACKAGE_NAME for Cursor project rules: $rule_file"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --client)
      CLIENT="$2"
      shift 2
      ;;
    --target)
      TARGET="$2"
      shift 2
      ;;
    --project-dir)
      PROJECT_DIR="$2"
      shift 2
      ;;
    --list-clients)
      list_clients
      exit 0
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

case "$CLIENT" in
  codex)
    install_codex
    ;;
  claude-code)
    install_claude_code
    ;;
  openclaw)
    install_openclaw
    ;;
  gemini-cli)
    install_gemini_cli
    ;;
  opencode)
    install_opencode
    ;;
  cursor)
    install_cursor
    ;;
  all)
    install_codex
    install_claude_code
    install_openclaw
    install_gemini_cli
    install_opencode
    ;;
  *)
    echo "Unsupported client: $CLIENT" >&2
    echo "Supported clients:" >&2
    list_clients >&2
    exit 2
    ;;
esac

echo "Installation complete. Restart or reload the target client if it is already running."
