import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import foundation
from scripts import upgrade as updater


class UpgradeTests(unittest.TestCase):
    def project(self, directory):
        project = Path(directory) / "app"
        project.mkdir()
        (project / "package.json").write_text('{"dependencies":{"react":"19"}}', encoding="utf-8")
        foundation.adopt(project, apply=True)
        return project

    def test_check_does_not_change_project(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.project(directory)
            manifest = project / ".foundation/manifest.json"
            original = manifest.read_bytes()
            result = updater.upgrade(project)
            self.assertEqual(result["status"], "up_to_date")
            self.assertFalse(result["applied"])
            self.assertEqual(manifest.read_bytes(), original)

    def test_modified_catalog_blocks_update(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.project(directory)
            file = project / ".foundation/standards/performance.json"
            file.write_text('{"customized":true}', encoding="utf-8")
            res = updater.upgrade(project, apply=True)
            self.assertEqual(res["status"], "conflict")
            self.assertFalse(res["applied"])
            self.assertEqual(file.read_text(), '{"customized":true}')

    def test_new_catalog_is_backed_up_and_applied(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.project(directory)
            old_catalog = (project / ".foundation/standards/performance.json").read_bytes()
            latest = Path(directory) / "new-performance.json"
            latest.write_bytes(old_catalog + b"\n")
            with patch.object(foundation, "CATALOG", latest), patch.object(foundation, "VERSION", "0.3.1"):
                preview = updater.upgrade(project)
                self.assertEqual(preview["status"], "update_available")
                self.assertFalse(preview["applied"])
                result = updater.upgrade(project, apply=True)
                self.assertEqual(result["status"], "updated")
                self.assertEqual((project / ".foundation/standards/performance.json").read_bytes(), latest.read_bytes())
                self.assertEqual(json.loads((project / ".foundation/manifest.json").read_text())["foundation_version"], "0.3.1")
                backup = project / result["backup"]
                self.assertEqual((backup / "performance.json").read_bytes(), old_catalog)
                self.assertEqual(updater.upgrade(project)["status"], "up_to_date")

    def test_unmanaged_project_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "README.md").write_text("# test", encoding="utf-8")
            with self.assertRaises(ValueError):
                updater.upgrade(project)


if __name__ == "__main__":
    unittest.main()
