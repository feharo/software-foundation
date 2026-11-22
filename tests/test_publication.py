import tempfile
import unittest
from pathlib import Path

from scripts.check_publication import scan_files, check, TOKEN_PATTERNS


class PublicationChecksTests(unittest.TestCase):
    def test_detects_sensitive_file_names_and_private_key(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            file1 = root / ".env.local"
            file1.write_text("NO_REAL_SECRETS_HERE=1\n", encoding="utf-8")
            file2 = root / "test.ts"
            file2.write_text("-----BEGIN PRIVATE KEY-----\nfake\n", encoding="utf-8")
            findings = scan_files(root, [Path(".env.local"), Path("test.ts")])
            self.assertIn((".env.local", "sensitive_filename"), findings)
            self.assertIn(("test.ts", "private_key"), findings)

    def test_sample_env_is_permitted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sample = root / ".env.example"
            sample.write_text("DATABASE_URL=\nBETTER_AUTH_SECRET=\n", encoding="utf-8")
            self.assertEqual(scan_files(root, [Path(".env.example")]), [])

    def test_known_token_pattern_is_detected_without_printing_secret(self):
        token = "gh" + "p_" + ("x" * 35)
        self.assertTrue(TOKEN_PATTERNS[1][1].search(token))

    def test_non_strict_does_not_require_license(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("README.md", "SECURITY.md", "CONTRIBUTING.md"):
                (root / name).write_text("ok", encoding="utf-8")
            self.assertTrue(check(root, strict=False, paths=[]))
            self.assertFalse(check(root, strict=True, paths=[]))


if __name__ == "__main__":
    unittest.main()
