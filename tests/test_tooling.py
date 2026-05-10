import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class LegalAssistantToolingTests(unittest.TestCase):
    def test_top_level_skill_entrypoint_exists(self):
        skill = ROOT / "SKILL.md"
        self.assertTrue(skill.exists())
        text = skill.read_text(encoding="utf-8")
        self.assertIn("name: legal-assistant-agent", text)
        self.assertIn("法律助手智能体 Legal-Assistant_agent", text)
        self.assertIn("scripts/legal_research.py", text)
        self.assertIn("scripts/write_analysis_output.py", text)

    def test_readme_is_chinese_first_and_documents_clients(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertLess(text.index("## 中文"), text.index("## English"))
        self.assertIn("# 法律助手智能体 Legal-Assistant_agent", text)
        for client in ["codex", "claude-code", "cursor", "gemini-cli", "opencode", "openclaw"]:
            self.assertIn(f"--client {client}", text)

    def test_official_source_registry_has_core_jurisdictions(self):
        registry = json.loads((ROOT / "references" / "official_source_registry.json").read_text(encoding="utf-8"))
        for jurisdiction in ["CN", "HK", "US-FEDERAL", "UK", "EU", "CA", "AU", "SG"]:
            self.assertIn(jurisdiction, registry["jurisdictions"])
            sources = registry["jurisdictions"][jurisdiction]["sources"]
            self.assertTrue(any(source["authority"] == "official" for source in sources))
            self.assertTrue(any(source["type"] in {"legislation", "case_law"} for source in sources))

    def test_research_script_builds_official_domain_queries(self):
        research = load_module(ROOT / "scripts" / "legal_research.py", "legal_research")
        registry = research.load_source_registry(ROOT / "references" / "official_source_registry.json")
        queries = research.build_queries(
            registry=registry,
            jurisdiction="US-FEDERAL",
            issue="late delivery contract damages",
            case_type="contract",
            max_sources=3,
        )
        self.assertGreaterEqual(len(queries), 2)
        self.assertTrue(all("site:" in query.search_query for query in queries))
        self.assertTrue(any("govinfo.gov" in query.search_query for query in queries))
        self.assertTrue(research.url_matches_domain("https://www.govinfo.gov/app/details/USCODE", "www.govinfo.gov"))
        self.assertFalse(research.url_matches_domain("https://example.com/govinfo.gov", "www.govinfo.gov"))
        self.assertIn("bing", research.build_parser()._option_string_actions["--provider"].choices)
        self.assertIn("official", research.build_parser()._option_string_actions["--provider"].choices)

    def test_output_writer_creates_case_workspace(self):
        writer = load_module(ROOT / "scripts" / "write_analysis_output.py", "write_analysis_output")
        with tempfile.TemporaryDirectory() as temp_dir:
            result = writer.write_analysis_bundle(
                out_dir=Path(temp_dir),
                case_slug="demo-contract",
                analysis_markdown="## Scope\nDemo analysis",
                metadata={"jurisdiction": "CN", "case_type": "contract"},
                artifacts={"strategy.md": "## Strategy\nNext step"},
            )
            self.assertTrue(result["case_dir"].exists())
            self.assertTrue((result["case_dir"] / "analysis.md").exists())
            self.assertTrue((result["case_dir"] / "metadata.json").exists())
            self.assertTrue((result["case_dir"] / "strategy.md").exists())
            self.assertIn("analysis.md", (result["case_dir"] / "INDEX.md").read_text(encoding="utf-8"))

    def test_validate_script_runs(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_skill.py")],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout)

    def test_install_script_lists_supported_clients(self):
        completed = subprocess.run(
            [str(ROOT / "scripts" / "install.sh"), "--list-clients"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout)
        for client in ["codex", "claude-code", "cursor", "gemini-cli", "opencode", "openclaw", "all"]:
            self.assertIn(client, completed.stdout)


if __name__ == "__main__":
    unittest.main()
