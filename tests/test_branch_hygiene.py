import unittest
from scripts.cleanup_branches import may_delete, clean

REPO = "feharo/software-foundation"


def pull(name, *, closed=True, merged=True, bot=False, sha="abc123", owner=REPO):
    return {
        "state": "closed" if closed else "open",
        "merged_at": "2026-11-22T12:00:00Z" if merged else None,
        "head": {"ref": name, "sha": sha, "repo": {"full_name": owner}},
        "user": {"login": "dependabot[bot]" if bot else "feharo"},
    }


class FakeAPI:
    def __init__(self, refs, open_prs, closed_prs):
        self.refs = dict(refs)
        self.open = open_prs
        self.closed = closed_prs
        self.deleted = []

    def prs(self, state):
        return iter(self.open if state == "open" else self.closed)

    def branch_sha(self, name):
        return self.refs.get(name)

    def delete_branch(self, name):
        self.deleted.append(name)


class BranchCleanupTests(unittest.TestCase):
    def test_only_merged_or_closed_bot_prs_are_eligible(self):
        self.assertTrue(may_delete(pull("feat/old"), REPO, set()))
        self.assertTrue(may_delete(pull("docs/ecosystem"), REPO, set()))
        self.assertFalse(may_delete(pull("docs/in-progress", merged=False), REPO, set()))
        self.assertFalse(may_delete(pull("docs/active"), REPO, {"docs/active"}))
        self.assertTrue(may_delete(pull("dependabot/pkg", merged=False, bot=True), REPO, set()))
        self.assertFalse(may_delete(pull("chore/unmerged", merged=False), REPO, set()))
        self.assertFalse(may_delete(pull("feat/active", closed=False), REPO, set()))
        self.assertFalse(may_delete(pull("feat/active"), REPO, {"feat/active"}))

    def test_ref_guard_and_repo_guard(self):
        self.assertFalse(may_delete(pull("main"), REPO, set()))
        self.assertFalse(may_delete(pull("release"), REPO, set()))
        self.assertFalse(may_delete(pull("feat/foreign", owner="external/fork"), REPO, set()))
        self.assertFalse(may_delete(pull("unknown/branch"), REPO, set()))

    def test_deleted_only_if_sha_matches_and_no_open_pr(self):
        api = FakeAPI(
            refs={"feat/old": "same", "feat/new-work": "new", "dependabot/one": "expected", "feat/active": "match"},
            open_prs=[pull("feat/active", closed=False, sha="match")],
            closed_prs=[
                pull("feat/old", sha="same"),
                pull("feat/new-work", sha="old"),
                pull("dependabot/one", bot=True, merged=False, sha="expected"),
                pull("feat/active", sha="match"),
            ],
        )
        result = clean(api, REPO)
        self.assertEqual(result, ["feat/old", "dependabot/one"])
        self.assertEqual(api.deleted, result)

    def test_dry_run_never_calls_delete(self):
        api = FakeAPI({"feat/old": "sha"}, [], [pull("feat/old", sha="sha")])
        self.assertEqual(clean(api, REPO, dry_run=True), ["feat/old"])
        self.assertEqual(api.deleted, [])


if __name__ == "__main__":
    unittest.main()
