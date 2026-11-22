#!/usr/bin/env python3
"""Remove stale merged PR branches and closed Dependabot branches, with safety checks.

Intended for Actions push to main. Only uses GitHub's own REST API and its
scoped GITHUB_TOKEN. It does not delete tags, the default branch, unmerged human
branches, active PR branches, or any branch whose SHA has changed.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

REPO = "feharo/software-foundation"
PROTECTED = {"main", "master", "develop", "development", "production", "staging", "release"}
EXPECTED_PREFIXES = ("feat/", "chore/", "docs/", "dependabot/")


def may_delete(pr, repository, open_branches):
    head = pr.get("head") or {}
    head_repo = head.get("repo") or {}
    name = head.get("ref", "")
    sha = head.get("sha", "")
    if head_repo.get("full_name") != repository or not name or not sha:
        return False
    if name in PROTECTED or not name.startswith(EXPECTED_PREFIXES):
        return False
    if name in open_branches:
        return False
    if pr.get("state") != "closed":
        return False
    merged = bool(pr.get("merged_at"))
    bot_closed = (pr.get("user") or {}).get("login") == "dependabot[bot]"
    return merged or bot_closed


class GitHub:
    def __init__(self, repo, token):
        self.url = "https://api.github.com/repos/" + repo
        self.token = token

    def request(self, method, path, missing_ok=False):
        url = self.url + "/" + path.lstrip("/")
        request = urllib.request.Request(url, method=method, headers={
            "Authorization": "Bearer " + self.token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "software-foundation-maintenance",
        })
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                content = response.read()
                return json.loads(content) if content else {}
        except urllib.error.HTTPError as error:
            if missing_ok and error.code == 404:
                return None
            raise

    def prs(self, state):
        page = 1
        while True:
            batch = self.request("GET", f"pulls?state={state}&per_page=100&page={page}")
            if not isinstance(batch, list):
                raise ValueError("Unexpected GitHub pull requests response")
            yield from batch
            if len(batch) < 100:
                break
            page += 1

    def branch_sha(self, name):
        ref = self.request("GET", "git/ref/heads/" + urllib.parse.quote(name, safe="/"), missing_ok=True)
        return (ref or {}).get("object", {}).get("sha")

    def delete_branch(self, name):
        self.request("DELETE", "git/refs/heads/" + urllib.parse.quote(name, safe="/"), missing_ok=True)


def clean(api, repository, dry_run=False):
    open_names = {pr.get("head", {}).get("ref") for pr in api.prs("open")
                  if (pr.get("head", {}).get("repo") or {}).get("full_name") == repository}
    deleted = []
    skipped = 0
    for pr in api.prs("closed"):
        if not may_delete(pr, repository, open_names):
            continue
        name = pr["head"]["ref"]
        expected = pr["head"]["sha"]
        current = api.branch_sha(name)
        if not current or current != expected:
            skipped += 1
            continue
        if dry_run:
            print("READY: " + name)
        else:
            api.delete_branch(name)
            print("DELETED: " + name)
        deleted.append(name)
    print(f"Resumo: {len(deleted)} branches {'candidatas' if dry_run else 'removidas'}; "
          f"{skipped} branches preservadas por SHA alterado/inexistente.")
    return deleted


def main(argv=None):
    parser = argparse.ArgumentParser(description="Delete only eligible closed-PR head branches.")
    parser.add_argument("--dry-run", action="store_true", help="Do not delete refs.")
    args = parser.parse_args(argv)
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    token = os.environ.get("GH_TOKEN", "")
    if repo != REPO:
        print("ERRO: repository mismatch; cleanup disabled.", file=sys.stderr)
        return 2
    if not token:
        print("ERRO: GH_TOKEN not configured; cleanup disabled.", file=sys.stderr)
        return 2
    try:
        clean(GitHub(repo, token), repo, dry_run=args.dry_run)
    except (ValueError, OSError, urllib.error.URLError) as error:
        # Never log API response body or authorization header.
        print("ERRO: branch cleanup failed; inspect repository permissions.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
