.PHONY: validate workspace-smoke install install-all install-codex install-claude install-gemini install-opencode install-openclaw research-demo output-demo

validate:
	python3 scripts/validate_skill.py

workspace-smoke:
	python3 scripts/case_workspace.py self-test --cleanup

install:
	./scripts/install.sh

install-all:
	./scripts/install.sh --client all

install-codex:
	./scripts/install.sh --client codex

install-claude:
	./scripts/install.sh --client claude-code

install-gemini:
	./scripts/install.sh --client gemini-cli

install-opencode:
	./scripts/install.sh --client opencode

install-openclaw:
	./scripts/install.sh --client openclaw

research-demo:
	python3 scripts/legal_research.py --jurisdiction CN --query "合同 迟延履行 退款 催告" --case-type "合同纠纷" --out-dir work/research-demo --no-fetch

output-demo:
	printf "## Scope\nDemo analysis\n" | python3 scripts/write_analysis_output.py --out-dir work/cases --case-slug demo-contract --metadata jurisdiction=CN --metadata case_type=contract
