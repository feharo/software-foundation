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
            instructions = (destination / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn(".foundation/standards/performance.json", instructions)
            self.assertTrue((destination / ".github" / "workflows" / "ci.yml").is_file())
            schema = (destination / "supabase" / "schema.sql").read_text(encoding="utf-8").lower()
            for entity in ("workspaces", "workspace_memberships", "tasks"):
                self.assertIn(f"alter table public.{entity} enable row level security", schema)
            self.assertIn("is_workspace_member", schema)
            env_lines = (destination / ".env.example").read_text().splitlines()
            public_values = [line.split("=", 1)[1].strip() for line in env_lines
                             if line.startswith("NEXT_PUBLIC_") and "=" in line]
            self.assertTrue(public_values)
            self.assertTrue(all(not value for value in public_values),
                            "Template must not contain actual credential values")
            with self.assertRaises(FileExistsError):
                module.create("Outro Produto", destination)

    def test_postgres_option_is_isolated_and_keeps_quality_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "postgres-saas"
            module.create("Meu Negócio", dest, database="postgres")
            pkg = json.loads((dest / "package.json").read_text())
            self.assertIn("pg", pkg["dependencies"])
            self.assertIn("better-auth", pkg["dependencies"])
            self.assertNotIn("@supabase/supabase-js", pkg["dependencies"])
            self.assertFalse((dest / "lib" / "supabase.ts").exists())
            self.assertFalse((dest / "supabase" / "schema.sql").exists())
            self.assertTrue((dest / "app" / "api" / "tasks" / "route.ts").exists())
            self.assertTrue((dest / "db" / "schema.sql").exists())
            self.assertTrue((dest / "docker-compose.yml").exists())
            self.assertTrue((dest / "AGENTS.md").exists())
            self.assertEqual(json.loads((dest / ".foundation" / "profile.json").read_text())["name"], "nextjs-postgres")

    def test_unknown_database_rejected_without_creating_files(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "invalid"
            with self.assertRaises(ValueError):
                module.create("Teste", target, database="../../wrong")
            self.assertFalse(target.exists())

    def test_blueprint_no_unresolved_vars(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "app"
            module.create("Teste", destination)
            for source in destination.rglob("*"):
                if source.is_file():
                    contents = source.read_text(encoding="utf-8")
                    for placeholder in module.REPLACE:
                        self.assertNotIn(placeholder, contents, f"{source}: {placeholder}")
            pg_destination = Path(directory) / "postgres"
            module.create("Teste", pg_destination, database="postgres")
            for source in pg_destination.rglob("*"):
                if source.is_file():
                    contents = source.read_text(encoding="utf-8")
                    for placeholder in module.REPLACE:
                        self.assertNotIn(placeholder, contents, f"{source}: {placeholder}")


if __name__ == "__main__":
    unittest.main()
