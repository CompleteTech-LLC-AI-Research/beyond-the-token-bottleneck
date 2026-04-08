# Living Analyses Review

## Purpose

Living analyses in `wiki/analyses/` are synthesis pages whose internal structure (numbered tensions, numbered directions, clustered questions, benchmark rows, timeline entries, method-comparison rows) must be reviewed per item, not per page. A single new paper often updates multiple directions/tensions/questions within one analysis file, so the high-level "is this page relevant?" question hides individual matches and causes drift. This fragment is the canonical enumeration — all consuming workflows should reference it rather than re-listing analyses inline.

## When to run

- After every ingest (single or batch).
- During gap-analysis and enrichment-audit passes.
- Any time a new source is added that could affect existing claims.

## The full set of living analyses

Check **every** living analysis page in `wiki/analyses/` and update any that the new source touches. Do not skip any. Every direction in `frontier-research-directions.md` and every tension in `contradictions.md` must be reviewed individually, not just the analysis page as a whole, because a single new paper often updates multiple directions or tensions and the high-level "is this page relevant?" question hides individual matches.

- `contradictions.md` — for each numbered tension, ask whether the new source adds a new claim, resolves an existing one, or shifts the status. Update the per-tension sub-claims table and the summary table at the end.
- `frontier-research-directions.md` — for each numbered direction (1-8), ask whether the new source provides additional empirical support, a new blocker, or a new "concrete next step" that is now closed. **A new paper often blocks or advances multiple directions** — review every direction individually before moving on.
- `open-questions.md` — for each clustered question, ask whether the new source partially or fully answers it, or raises a new question that fits an existing cluster.
- `benchmark-overlap.md` — add new rows to the master matrix and the per-benchmark focused tables; update paper count, methodology paragraph, and any "<XB cluster" or blind-spot notes affected.
- `paper-timeline.md` — add the paper to the correct year/month entry in chronological order; update the year-narrative paragraph if the new paper changes the field's trajectory.
- `method-comparison.md` — add a row to the appropriate method category table (Reasoning / Communication / Unified / Diagnostic), or note in the cross-cutting analysis if the paper alters a trade-off.
- Any other `wiki/analyses/*.md` page that exists at ingest time (the analysis directory grows over time — re-list it before assuming this enumeration is complete).

## Extensibility rule

The analysis directory grows over time. Before assuming this enumeration is complete, re-list `wiki/analyses/*.md` and review any file not covered above. If you find a new analysis file, review it against the same per-item discipline (identify its atomic unit — tension, direction, question, row, entry — and iterate over each instance).

## Invariants

- Per-item review, not just per-page review.
- Every numbered direction in `frontier-research-directions.md` must be individually reviewed.
- Every numbered tension in `contradictions.md` must be individually reviewed.
- Every clustered question in `open-questions.md` must be individually reviewed.
- New rows in `benchmark-overlap.md` must update the master matrix AND the per-benchmark focused tables AND the methodology paragraph.
- `paper-timeline.md` entries must be inserted in chronological order, and the year-narrative paragraph updated if the trajectory shifts.
- `method-comparison.md` additions must land in the correct method category table (Reasoning / Communication / Unified / Diagnostic).

## After completion

Return to the calling workflow and proceed with its next numbered step. This fragment is a subroutine — it has no terminal action of its own, and its caller's remaining steps (stale-count sweep, log entry, commit, report) are not optional just because the per-item review is done.

## Used by

- `workflows/ingest.md` (Procedure step 11)
- `workflows/batch-ingest.md` (expected, PR 2)
- `workflows/enrich.md` (expected, PR 2)
- `workflows/verification.md` (expected, PR 2)
- `workflows/gap-analysis.md` (expected, PR 2)
- `workflows/enrichment-audit.md` (expected, PR 2)
