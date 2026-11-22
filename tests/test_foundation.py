import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validator", ROOT / "scripts/validate_foundation.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class FoundationTests(unittest.TestCase):
    def test_catalog_and_profiles(self):
        self.assertTrue(validator.validate(ROOT))

    def test_catalog_conditions(self):
        data = json.loads((ROOT / "standards/performance.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["rules"]), 31)
        self.assertTrue(any(x["level"] == "conditional" for x in data["rules"]))
        self.assertTrue(any(x["applies_when"] == "when_ui" for x in data["rules"]))


if __name__ == "__main__":
    unittest.main()
