# Procedure fragments

Multi-step imperative sequences reused verbatim across workflows. Each file here describes an action sequence a workflow runs end-to-end.

Planned fragments:

- `stale-count-sweep.md` — recompute and refresh any cached counts that appear in MOCs or READMEs.
- `living-analyses-review.md` — walk the living-analyses set and flag entries needing refresh.
- `raw-checklist-row.md` — append a new row to the raw-ingest checklist in the canonical format.
- `bulk-source-rename.md` — rename a source across notes, MOCs, and backlinks in one pass.
- `moc-update.md` — regenerate a MOC's entry list from its underlying folder.
- `commit-and-push.md` — stage, commit with a conventional message, and push the branch.

Fragment bodies land in PR 2; this PR only establishes the directory.
