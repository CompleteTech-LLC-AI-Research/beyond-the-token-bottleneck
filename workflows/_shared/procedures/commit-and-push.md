# Commit and Push

## Purpose

Uncommitted work is fragile — it can be lost to a tab crash, an accidental `git restore`, or a context-window reset on the next session. Workflow changes deserve explicit review even when research changes are routine. This fragment encodes both disciplines: research files ship straight to `master` because they are content-only and the user reviews them continuously through the wiki, while workflow files go through a feature-branch + PR review surface because they shape every future ingest. The split is based on **blast radius**.

## When to run

- At the end of any ingest, batch-ingest, gap-analysis, enrich, expand, synthesize, or audit pass that produced commitable changes.
- Whenever a workflow's procedure says to commit and push.
- Never as a freestanding action — this fragment is always invoked from a calling workflow whose remaining steps (log entry, report) it does not own.

## Procedure

1. **Identify which files belong to which bucket** before staging anything. Walk the output of `git status` and classify each modified file:
   - **Research bucket** (commit on `master`): `wiki/**`, `raw/**`, `README.md`, anything created or updated by the workflow itself.
   - **Workflow bucket** (PR): `workflows/**`, `AGENTS.md` (if the workflow index changed), and any new schema or process documentation.
   - **Do not touch**: any modified file you did *not* write to during this session. Pre-existing in-progress work in the working tree must not be staged. The session-start `git status` (captured in the system context) is the source of truth for what was already dirty before you began.

2. **Stage the research files explicitly by path**, not with `git add -A` or `git add .`. Explicit paths prevent accidentally staging the user's pre-existing in-progress work, the `.codex/` or `.mcp.json` shells, or `.obsidian/graph.json` auto-saves. Verify with `git status` that the staged set matches your research bucket exactly and that any workflow files remain unstaged.

3. **Commit on `master`** with a descriptive message that names the work, summarizes the contribution, lists created/updated pages, and notes any cleanup work bundled in (e.g., paper-count sweeps, checklist resync). Follow the existing repo style — run `git log --oneline -5` to compare. Always include the `Co-Authored-By` trailer.

4. **Push `master`** to `origin`. The research commit is now durable.

5. **If workflow files were also touched**, create a PR for them — do not commit workflow changes directly to `master`:
   1. `git checkout -b workflow-<short-descriptor>` (e.g. `workflow-improvements-gap-analysis-discipline`). The branch starts from current `master` so the unstaged workflow changes carry over automatically.
   2. Stage the workflow files explicitly (`workflows/*.md` and any related schema files).
   3. Commit on the branch with a message that explains the **regression class** the workflow change prevents, not just the line-level diff. (E.g. "Add per-direction analysis review + count-drift sweep + checklist sync to ingest workflow" with a body explaining what was missed in the most recent run.)
   4. `git push -u origin <branch>`.
   5. `gh pr create --title "..." --body "..."` with a body that includes a Summary section (regression classes addressed) and a Test plan section (how to verify the new instructions work on the next ingest).
   6. Return to `master` (`git checkout master`) so subsequent work does not accidentally land on the PR branch.

6. **If only research files were touched**, skip step 5 — no PR needed.

## Invariants

- **Research → master, workflows → PR.** This split is non-negotiable. Workflow changes shape every future ingest and benefit from a PR review surface even when the author is the same.
- **Stage by explicit path.** `git add -A` and `git add .` are forbidden. They have, in past sessions, swept up pre-existing in-progress work, `.codex/`, `.mcp.json`, and `.obsidian/graph.json`.
- **Pre-existing dirty files are off-limits.** The session-start `git status` is the source of truth for what was already dirty. Anything in that snapshot must not be staged by this workflow's commit.
- **The `Co-Authored-By` trailer is mandatory** on every commit produced by an agent-driven workflow.
- **PR commit messages explain regression classes**, not line-level diffs. The reviewer needs to understand *why* the workflow needed the change.
- **Never `--no-verify` and never `--no-gpg-sign`** unless the user has explicitly asked for it. If a hook fails, investigate the underlying issue.
- **Never amend a published commit.** If a hook fails after a successful commit, fix the issue and create a new commit; do not `--amend` and rewrite history that may already be elsewhere.

## After completion

Return to the calling workflow and proceed with its next numbered step. This fragment is a subroutine — it has no terminal action of its own, and the calling workflow's remaining steps (final report to user, any post-commit verification) are not optional just because the commit and push are done.

## Used by

- `workflows/create/ingest.md` (Procedure step 13)
- `workflows/create/batch-ingest.md` (Procedure step 7)
- `workflows/audit/gap-analysis.md` (Phase 6 — this fragment is the canonical home of the procedure that used to live inline in Phase 6)
- `workflows/enrich/enrich.md` (Procedure step 8)
- `workflows/create/synthesize.md` (Procedure step 8)
- `workflows/audit/enrichment-audit.md` (Phase 4 step 5)
- `workflows/audit/moc-gap-analysis.md` (Procedure step 12)
