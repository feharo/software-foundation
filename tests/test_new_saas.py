import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("new_saas", ROOT / "scripts/new_saas.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ScaffoldTests(unittest.TestCase):
    def test_slug_and_color_validation(self):
        self.assertEqual(module.make_slug("Gestão Clínica 360"), "gestao-clinica-360")
        with self.assertRaises(ValueError):
            module.valid_slug("../insecure")
        with self.assertRaises(ValueError):
            module.valid_color("red; background: url(foo)")
        with self.assertRaises(ValueError):
            module.valid_color("#ff5533")
        with self.assertRaises(ValueError):
            module.valid_name("bad\nname")

    def test_create_project_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "novo-saas"
            module.create("Minha Agenda", destination, slug="minha-agenda", color="#1b4bb1")
            package = json.loads((destination / "package.json").read_text())
            self.assertEqual(package["name"], "minha-agenda")
            self.assertIn("next", package["dependencies"])
            self.assertIn("Minha Agenda", (destination / "app" / "page.tsx").read_text())
            self.assertIn("#1b4bb1", (destination / "app" / "globals.css").read_text())
            self.assertTrue((destination / "supabase" / "schema.sql").is_file())
            self.assertTrue((destination / ".env.example").is_file())
            self.assertTrue((destination / "AGENTS.md").is_file())
            self.assertTrue((destination / "CLAUDE.md").is_file())
            self.assertTrue((destination / ".foundation" / "standards" / "performance.json").is_file())
            self.assertTrue((destination / ".github" / "workflows" / "ci.yml").is_file())
            schema = (destination / "supabase" / "schema.sql").read_text(encoding="utf-8").lower()
            for entity in ("workspaces", "workspace_memberships", "tasks"):
                self.assertIn(f"alter table public.{entity} enable row level security", schema)
            self.assertIn("is_workspace_member", schema)
            self.assertNotIn("service_role", (destination / ".env.example").read_text().split("=", 1)[-1])
            with self.assertRaises(FileExistsError):
                module.create("Outro Produto", destination)

    def test_blueprint_no_unresolved_vars(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "app"
            module.create("Teste", destination)
            for source in destination.rglob("*"):
                if source.is_file():
                    contents = source.read_text(encoding="utf-8")
                    for placeholder in module.REPLACE:
                        self.assertNotIn(placeholder, contents, f"{source}: {placeholder}")


if __name__ == "__main__":
    unittest.main()
