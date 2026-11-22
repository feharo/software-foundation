"""Validate the public ecosystem map against the actual repository tree.

The docs are read by developers and coding agents, so every local Markdown
link and claimed subsystem should point to something real. No network calls.
"""
import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DOCS = (ROOT / "README.md", ROOT / "docs/README.pt-BR.md", ROOT / "docs/ecosystem.md")
LINK = re.compile(r"\]\(([^\s)]+)(?:\s+[^)]*)?\)")


class EcosystemDocumentationTests(unittest.TestCase):
    def test_all_local_markdown_links_resolve(self):
        for path in DOCS:
            text = path.read_text(encoding="utf-8")
            for address in LINK.findall(text):
                target = address.split("#", 1)[0]
                if not target or target.startswith(("https://", "http://", "mailto:", "tel:")):
                    continue
                actual = (path.parent / unquote(target)).resolve()
                with self.subTest(page=str(path.relative_to(ROOT)), target=target):
                    self.assertTrue(actual.is_relative_to(ROOT), "Link escaped repository")
                    self.assertTrue(actual.exists(), "Broken local Markdown link")

    def test_claimed_ecosystem_has_real_sources(self):
        profiles = list((ROOT / "profiles").glob("*.json"))
        skills = list((ROOT / "skills").glob("*/SKILL.md"))
        variants = list((ROOT / "blueprints").glob("saas-nextjs-*"))
        catalog = json.loads((ROOT / "standards/performance.json").read_text(encoding="utf-8"))
        self.assertEqual(len(profiles), 7)
        self.assertEqual(len(skills), 2)
        self.assertEqual(len(variants), 2)
        self.assertEqual(len(catalog["rules"]), 31)
        for page in DOCS:
            text = page.read_text(encoding="utf-8").lower()
            with self.subTest(page=str(page.relative_to(ROOT))):
                for command in ("init", "adopt", "audit", "upgrade", "doctor"):
                    self.assertIn(command, text)
                self.assertIn("mermaid", text)
                self.assertIn("supabase", text)
                self.assertIn("postgres", text)
                self.assertIn("performance-guardian", text)
                self.assertIn("saas-builder", text)

    def test_diagrams_have_balanced_fences_and_dont_claim_autofix(self):
        for page in DOCS:
            text = page.read_text(encoding="utf-8")
            with self.subTest(page=str(page.relative_to(ROOT))):
                self.assertEqual(text.count("```") % 2, 0, "Unterminated Markdown code fence")
                self.assertIn("```mermaid\n", text)
        main = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("not an autonomous coding agent", main.lower())
        self.assertIn("not_verified", main)
        self.assertIn("not automatically", main.lower())

    def test_ai_discovery_and_public_site_link_to_ecosystem(self):
        for path in ("llms.txt", "site/llms.txt", "docs/for-ai-agents.md",
                     "docs/architecture.md", "site/index.html", "site/pt-br/index.html"):
            content = (ROOT / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn("ecosystem.md", content)


if __name__ == "__main__":
    unittest.main()
