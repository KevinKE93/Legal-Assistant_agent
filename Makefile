.PHONY: test validate install research-demo output-demo

test:
	python3 -m unittest discover -s tests

validate:
	python3 scripts/validate_skill.py

install:
	./scripts/install.sh

research-demo:
	python3 scripts/legal_research.py --jurisdiction CN --query "合同 迟延履行 退款 催告" --case-type "合同纠纷" --out-dir work/research-demo --no-fetch

output-demo:
	printf "## Scope\nDemo analysis\n" | python3 scripts/write_analysis_output.py --out-dir work/cases --case-slug demo-contract --metadata jurisdiction=CN --metadata case_type=contract
