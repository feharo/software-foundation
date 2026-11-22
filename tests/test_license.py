"""The repository MIT notice and generated-app provenance are intentional, tested contracts."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MITLicenseTests(unittest.TestCase):
    def test_canonical_mit_notice_present(self):
        full = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(full.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2026 Felipe Haro", full)
        self.assertIn("Permission is hereby granted, free of charge", full)
        self.assertIn("The above copyright notice and this permission notice shall be included", full)
        self.assertIn('THE SOFTWARE IS PROVIDED "AS IS"', full)

    def test_generator_includes_provenance_without_relicensing_user_work(self):
        generator = (ROOT / "scripts/new_saas.py").read_text(encoding="utf-8")
        self.assertIn('"LICENSE": "LICENSE-SOFTWARE-FOUNDATION"', generator)
        for blueprint in ("saas-nextjs-supabase", "saas-nextjs-postgres"):
            readme = (ROOT / "blueprints" / blueprint / "README.md").read_text(encoding="utf-8")
            self.assertIn("LICENSE-SOFTWARE-FOUNDATION", readme)
            self.assertIn("MIT", readme)


if __name__ == "__main__":
    unittest.main()
