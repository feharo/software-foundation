"""Static SEO and AI discovery regression tests. No network or credentials needed."""
import json
import re
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BASE = "https://feharo.github.io/software-foundation/"
REPO = "https://github.com/feharo/software-foundation"


class InspectPage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_lang = None
        self.title_parts = []
        self.in_title = False
        self.in_json_script = False
        self.script_parts = []
        self.meta = {}
        self.links = []
        self.anchors = []
        self.headings = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.html_lang = a.get("lang")
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link":
            self.links.append(a)
        elif tag == "a":
            self.anchors.append(a.get("href", ""))
        elif tag in ("h1", "h2", "h3"):
            self.headings.append(tag)
        elif tag == "script" and a.get("type") == "application/ld+json":
            self.in_json_script = True

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)
        if self.in_json_script:
            self.script_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "script":
            self.in_json_script = False


def parse_page(path):
    parser = InspectPage()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


class DiscoverySEOTests(unittest.TestCase):
    def test_language_pages_have_unique_canonicals_and_hreflang(self):
        expected = {SITE / "index.html": ("en", BASE),
                    SITE / "pt-br" / "index.html": ("pt-BR", BASE + "pt-br/")}
        for path, (lang, canonical) in expected.items():
            with self.subTest(page=path.name, lang=lang):
                page = parse_page(path)
                self.assertEqual(page.html_lang, lang)
                title = "".join(page.title_parts).strip()
                self.assertGreater(len(title), 35)
                self.assertLess(len(title), 85)
                desc = page.meta.get("description", "")
                self.assertGreater(len(desc), 90)
                self.assertLess(len(desc), 180)
                self.assertIn("h1", page.headings)
                self.assertEqual([x.get("href") for x in page.links if x.get("rel") == "canonical"], [canonical])
                alternates = {x.get("hreflang"): x.get("href") for x in page.links if x.get("rel") == "alternate"}
                self.assertEqual(alternates["en"], BASE)
                self.assertEqual(alternates["pt-BR"], BASE + "pt-br/")
                self.assertEqual(alternates["x-default"], BASE)
                self.assertEqual(page.meta["og:url"], canonical)
                self.assertTrue(page.meta["og:title"])
                self.assertTrue(page.meta["og:description"])
                self.assertEqual(page.meta["twitter:card"], "summary")

                css = [x["href"] for x in page.links if x.get("rel") == "stylesheet"]
                self.assertEqual(len(css), 1)
                self.assertTrue((path.parent / css[0]).is_file())

    def test_structured_data_matches_visible_project_and_real_source(self):
        for path in [SITE / "index.html", SITE / "pt-br" / "index.html"]:
            with self.subTest(path=path):
                page = parse_page(path)
                data = json.loads("".join(page.script_parts))
                self.assertEqual(data["@type"], "SoftwareSourceCode")
                self.assertEqual(data["codeRepository"], REPO)
                self.assertEqual(data["name"], "Software Foundation")
                self.assertEqual(data["author"]["url"], "https://tech.feharo.com.br")
                self.assertIn("PostgreSQL", data["description"])
                self.assertEqual(data["license"], "https://opensource.org/license/mit")

    def test_sitemap_has_both_real_pages(self):
        tree = ET.parse(SITE / "sitemap.xml")
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [e.text for e in tree.findall(".//sm:loc", ns)]
        self.assertEqual(locs, [BASE, BASE + "pt-br/"])
        self.assertIn("Sitemap: " + BASE + "sitemap.xml",
                      (SITE / "robots.txt").read_text(encoding="utf-8"))

    def test_linked_github_docs_exist_and_agents_are_not_misled(self):
        for path in [SITE / "index.html", SITE / "pt-br" / "index.html"]:
            page = parse_page(path)
            for anchor in page.anchors:
                prefix = REPO + "/blob/main/"
                if anchor.startswith(prefix):
                    local = ROOT / anchor[len(prefix):]
                    self.assertTrue(local.is_file(), f"Broken repository document: {anchor}")
            self.assertIn("https://tech.feharo.com.br", page.anchors)
            self.assertIn(REPO, page.anchors)
        ai = (ROOT / "docs/for-ai-agents.md").read_text(encoding="utf-8")
        self.assertIn("not an instruction to recommend", ai.lower())
        self.assertIn("not_verified", ai)
        self.assertIn("private", ai.lower())
        optional = (SITE / "llms.txt").read_text(encoding="utf-8").lower()
        self.assertIn("optional", optional)
        self.assertIn("not used by google", optional)

    def test_publishing_requires_manual_action(self):
        wf = (ROOT / ".github/workflows/pages-manual.yml").read_text(encoding="utf-8")
        on_block = wf.split("\non:\n", 1)[1].split("\npermissions:", 1)[0]
        self.assertIn("workflow_dispatch:", on_block)
        self.assertNotIn("push:", on_block)
        self.assertNotIn("pull_request:", on_block)
        self.assertIn("path: site", wf)
        self.assertTrue((SITE / ".nojekyll").exists())

    def test_launch_documentation_acknowledges_private_repo_and_robots_scope(self):
        guide = (ROOT / "docs/seo-launch.md").read_text(encoding="utf-8").lower()
        self.assertIn("private", guide)
        self.assertIn("license", guide)
        self.assertIn("host root", guide)
        self.assertIn("manual", guide)
        self.assertIn("no guaranteed indexing", guide)


if __name__ == "__main__":
    unittest.main()
