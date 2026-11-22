import unittest
from scripts.verify_history_scan import evaluate


class GitleaksHistoryResultTests(unittest.TestCase):
    def test_clean_scan_requires_nonzero_history(self):
        ok, detail = evaluate("INF 42 commits scanned\nINF no leaks found", 0)
        self.assertTrue(ok)
        self.assertIn("42", detail)

    def test_zero_commits_must_not_count_as_clean(self):
        ok, detail = evaluate("ERR fatal: detected dubious ownership\nINF 0 commits scanned\nINF no leaks found", 0)
        self.assertFalse(ok)
        self.assertIn("inconclusiva", detail)

    def test_missing_scan_confirmation_fails_closed(self):
        ok, _ = evaluate("scanner exited successfully", 0)
        self.assertFalse(ok)

    def test_findings_are_reported_without_values(self):
        fake = "TEST_" + "SE" + "CRET_" + ("a" * 30)
        ok, detail = evaluate(f"INF 18 commits scanned\nFinding: {fake}", 1)
        self.assertFalse(ok)
        self.assertNotIn(fake, detail)
        self.assertIn("possíveis credenciais", detail)

    def test_internal_git_error_is_not_a_clean_scan(self):
        ok, detail = evaluate('ERR error="stderr is not empty"\nINF 2 commits scanned', 0)
        self.assertFalse(ok)
        self.assertIn("erro interno", detail)

    def test_failed_process_is_not_accepted(self):
        ok, detail = evaluate("INF 22 commits scanned", 127)
        self.assertFalse(ok)
        self.assertIn("código 127", detail)


if __name__ == "__main__":
    unittest.main()
