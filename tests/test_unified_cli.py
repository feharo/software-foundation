import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts import foundation as cli


class UnifiedFoundationTests(unittest.TestCase):
    def make_project(self, parent, dependencies=None):
        project = Path(parent) / "my-project"
        project.mkdir()
        pkg = {
            "name": "my-project",
            "private": True,
            "scripts": {"build": "next build"},
            "dependencies": dependencies or {"next": "^16.0.0", "react": "^19.0.0", "pg": "^8.0.0"},
        }
        (project / "package.json").write_text(json.dumps(pkg), encoding="utf-8")
        (project / "README.md").write_text("# My existing SaaS\n", encoding="utf-8")
        (project / "AGENTS.md").write_text("Custom instructions — do not change.\n", encoding="utf-8")
        return project

    def test_two_paths_are_reachable_through_one_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            generated = Path(directory) / "fresh"
            with contextlib.redirect_stdout(io.StringIO()):
                status = cli.main(["init", "--name", "Novo SaaS", "--database", "postgres",
                                   "--output", str(generated), "--non-interactive"])
            self.assertEqual(status, 0)
            manifest = json.loads((generated / ".foundation" / "manifest.json").read_text())
            self.assertEqual(manifest["profile"], "nextjs-postgres")
            self.assertEqual(manifest["foundation_version"], cli.VERSION)
            self.assertEqual(cli.audit(generated)["profile"], "nextjs-postgres")
            self.assertFalse((generated / "lib" / "supabase.ts").exists())

    def test_detect_suggests_profile(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_project(directory)
            self.assertEqual(cli.suggested_profile(cli.detect(project)), "nextjs-postgres")
            (project / "package.json").write_text(json.dumps({
                "dependencies": {"next": "^16", "react": "^19", "@supabase/supabase-js": "^2"}
            }), encoding="utf-8")
            self.assertEqual(cli.suggested_profile(cli.detect(project)), "nextjs-supabase")
            (project / "package.json").write_text(json.dumps({
                "dependencies": {"next": "^16", "react": "^19"}
            }), encoding="utf-8")
            self.assertEqual(cli.suggested_profile(cli.detect(project)), "nextjs-generic")

    def test_adoption_preview_apply_and_idempotence(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_project(directory)
            previous = (project / "AGENTS.md").read_bytes()
            preview = cli.adopt(project)
            self.assertIn(".foundation/manifest.json", preview["create"])
            self.assertIn("AGENTS.md", preview["preserve"])
            self.assertFalse((project / ".foundation").exists())
            installed = cli.adopt(project, apply=True)
            self.assertTrue(installed["applied"])
            self.assertEqual(previous, (project / "AGENTS.md").read_bytes())
            self.assertTrue((project / ".foundation" / "agent-guide.md").is_file())
            self.assertEqual(cli.adopt(project, apply=True)["create"], [])
            self.assertEqual(json.loads((project / ".foundation" / "manifest.json").read_text())["profile"], "nextjs-postgres")

    def test_conflicts_abort_without_partial_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_project(directory)
            folder = project / ".foundation"
            folder.mkdir()
            (folder / "manifest.json").write_text('{"custom":"do not overwrite"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Conflitos"):
                cli.adopt(project, apply=True)
            self.assertFalse((folder / "profile.json").exists())
            self.assertFalse((project / "CLAUDE.md").exists())

    def test_audit_does_not_mutate_or_claim_performance_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_project(directory)
            (project / ".env.local").write_text("PRIVATE_API_KEY=should-not-appear-in-report", encoding="utf-8")
            before = sorted(p.relative_to(project).as_posix() for p in project.rglob("*"))
            report = cli.audit(project)
            after = sorted(p.relative_to(project).as_posix() for p in project.rglob("*"))
            self.assertEqual(before, after)
            self.assertEqual(len(report["results"]), 31)
            self.assertTrue(all(x["status"] in ("not_verified", "not_applicable") for x in report["results"]))
            self.assertEqual(report["inspection"], "static_only")
            self.assertNotIn("should-not-appear-in-report", json.dumps(report))
            self.assertIn("ci_present", [x["id"] for x in report["checks"]])
            text = cli.markdown_report(report)
            self.assertIn("P031", text)
            self.assertIn("Auditoria estática", text)

    def test_existing_files_not_overwritten_by_reports(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_project(directory)
            output = Path(directory) / "audit.json"
            with contextlib.redirect_stdout(io.StringIO()):
                status = cli.main(["audit", str(project), "--format", "json", "--output", str(output)])
            self.assertEqual(status, 0)
            self.assertEqual(json.loads(output.read_text())["project"], "my-project")
            with contextlib.redirect_stderr(io.StringIO()):
                status = cli.main(["audit", str(project), "--output", str(output)])
            self.assertEqual(status, 2)

    def test_api_only_project_marks_ui_rules_not_applicable(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_project(directory, {"express": "^5", "pg": "^8"})
            report = cli.audit(project)
            self.assertEqual(report["profile"], "api-service")
            rules = {r["id"]: r for r in report["results"]}
            self.assertEqual(rules["P001"]["status"], "not_applicable")
            self.assertEqual(rules["P031"]["status"], "not_verified")
            self.assertFalse(any(r["status"] == "pass" for r in report["results"]))


if __name__ == "__main__":
    unittest.main()
