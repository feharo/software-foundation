# Dependabot and branch maintenance

Dependabot is enabled for GitHub Actions and the two Next.js starters.
Weekly updates are grouped by impact. Major `typescript` and `@types/node`
updates are intentionally ignored in **version-update PRs**, because the tested
starter runtime is Node.js 22 and TypeScript 5.9.3. Revisit this rule when the
runtime/framework baseline is upgraded. Dependency security alerts require
separate review; ignoring major versions is not proof that the project is secure.

The workflow `Clean old merged PR branches` runs after a push to `main`
and may be triggered manually. It uses a scoped GitHub Actions token to remove
only:

- branches from PRs confirmed merged in this repository, with prefixes `feat/`, `chore/` or `docs/`;
- `dependabot/` branches from PRs closed as superseded or deliberately ignored.

In both cases, branch SHA must match the closed PR's last head SHA, and there
must be **no open PR** for that branch. The workflow never deletes `main`,
release branches, forks or modified/reused branches. It does not delete tags
or rewrite commit history.

To preview manually with GitHub Actions permissions, execute
`python3 scripts/cleanup_branches.py --dry-run` with `GH_TOKEN` and
`GITHUB_REPOSITORY=feharo/software-foundation`.

To avoid accidental churn, do **not** enable unconditional auto-merge for
major dependency upgrades. Review production changes, CI and real user flows.

GitHub Pages deployment is **manual** and not live yet. Major version upgrades of
`actions/configure-pages`, `actions/upload-pages-artifact` and
`actions/deploy-pages` are temporarily excluded from Dependabot version PRs.
Review those actions together when the owner authorizes the public Pages launch;
run a manual staging/deployment validation before adopting new majors. The
`actions/checkout` update to v7 was separately validated in Linux and Windows CI.
