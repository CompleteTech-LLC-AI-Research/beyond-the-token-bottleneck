# Rule: Log Immutability

## Statement

Entries in `wiki/log.md` are point-in-time records. They MUST NOT be backdated, rewritten, deleted, or updated to reflect later state. Counts inside log entries are correct-as-of the entry's date by definition; the [stale count sweep](../procedures/stale-count-sweep.md) explicitly excludes `wiki/log.md` from its updates.

## What this means in practice

- **Append-only.** New log entries always append to the end of the file with a current ISO date. Past entries are never reordered.
- **No retroactive corrections.** If an old log entry says "wiki covers 25 papers" on a date when that was true, leave it alone even if the current count is 50. The entry is a historical claim about that date, not a claim about the present.
- **No "the count drifted, let me fix the old entry" temptations.** This is the most common impulse to violate this rule. The count in a log entry is what was true *then*. The current count lives in `wiki/index.md`, the README badges, and the post-state of the next log entry — not in the past.
- **No deletions, even of "wrong" entries.** If a log entry is factually incorrect about the work it describes, append a correction entry referencing the original; do not edit the original.
- **No reformatting bulk passes.** Even cosmetic changes to old entries (markdown style, link formatting) are forbidden because they pollute the audit trail and obscure when the entry was actually written.

## Rationale

`wiki/log.md` is the audit trail for every workflow run. Its value depends entirely on the entries being honest snapshots of the moment they were written. Any backdating — even well-intentioned cleanup — destroys that value.

Concretely: if a stale-count sweep updated past log entries to reflect the current count, the audit trail would no longer answer the question "what did the wiki look like on date X?". Instead it would always reflect the current state, making it useless for debugging when a regression was introduced or for understanding the wiki's history.

This rule has been enforced multiple times after near-misses where bulk-update passes (count sweeps, slug renames, terminology normalizations) almost edited log.md. The [stale count sweep](../procedures/stale-count-sweep.md) and the [bulk source-page rename](../procedures/bulk-source-rename.md) both explicitly carve out `wiki/log.md` as off-limits.

## How violations are caught

- `workflows/_shared/procedures/stale-count-sweep.md` Invariants — explicit `wiki/log.md` exclusion in the sweep procedure.
- `workflows/_shared/procedures/bulk-source-rename.md` — the sed-rewrite pattern excludes `wiki/log.md` by scoping to `wiki/sources/` and `raw/`, not the vault root.
- `workflows/lint.md` Redundancy & Dead-Reference Audit — would surface log-entry rewrites as anomalies in the wiki's git history if a violation slipped through.
- Manual: `git log -p wiki/log.md` should show only appends. Any modification to a previously-appended line is a violation worth investigating.

## Used by

- `workflows/_shared/procedures/stale-count-sweep.md` (canonical exclusion)
- `workflows/_shared/procedures/bulk-source-rename.md` (canonical exclusion)
- `workflows/CONVENTIONS.md` Meta-rules (this rule is also stated as a meta-rule there; the rule fragment is the canonical long form)
- `workflows/ingest.md`, `workflows/batch-ingest.md`, `workflows/lint.md`, `workflows/review.md`, `workflows/enrich.md`, `workflows/synthesize.md`, `workflows/gap-analysis.md`, `workflows/enrichment-audit.md` (expected, PR 2b — every workflow that appends to log.md must respect this rule)
