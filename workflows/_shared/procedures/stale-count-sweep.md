# Stale Count Sweep

## Purpose

Hardcoded counts in body prose (paper counts, entity counts, MOC counts, analysis counts, concept counts) drift every time the vault grows, because "update index/README counts" instructions typically only catch badge counts and the directory tree — not the prose counts buried in MOC blurbs, analysis intros, and collaboration pitches. This is a first-class regression class that has bitten previous ingests and lints, so it gets its own mandatory sweep.

Often called alongside [living analyses review](living-analyses-review.md), which addresses content drift rather than count drift.

## When to run

- After any ingest that changes the source page count (ingest, batch-ingest).
- As part of the lint workflow's content integrity pass.
- Any time a count in prose might have drifted (e.g., after bulk entity/MOC/analysis/concept additions or deletions).

## Procedure

1. **Determine the authoritative current count.** Run `ls wiki/sources/**/*.md | wc -l` (or the equivalent Glob) to get the true on-disk source page count. Do not rely on memory or on "before this ingest there were N" framing alone — for ingest contexts, note both the old count ($N$) and the new count ($N+1$, or $N+k$ for batch) explicitly, but the authoritative post-state always comes from the filesystem, not arithmetic.

2. **Grep `wiki/` and `README.md` for the stale count phrasings.** Run all of the following patterns:
   - `\b\d+\s+(papers|source pages|source papers)\b` — the dominant phrasing.
   - `synthesized from all \d+` — catches "synthesized from all 25 papers" style intros.
   - `wiki covers \d+` — catches "wiki covers 25 papers" style summaries.
   - `(across|all)\s+\d+\s+papers` — catches "across 25 papers" / "all 25 papers" variants.
   When running during an ingest with a known old count, you may substitute `{old_count}` for `\d+` to narrow the sweep, but the broader `\d+` form is preferred during lint passes because it also surfaces counts that were already wrong before this run.

3. **Flag and update every match where the number does not equal the authoritative count, except matches inside `wiki/log.md`.** See the invariants section — log entries are point-in-time records and must never be backdated.

4. **Common offenders to check by name** (re-verify each one even if grep returns clean — grep misses line-broken phrasings, table cells, and templated summary blocks):
   - `wiki/analyses/frontier-research-directions.md` (intro line, around line 11).
   - `wiki/analyses/benchmark-overlap.md` — 4 places: page intro, methodology paragraph, the "Multilingual benchmarks" blind-spot bullet, and the "Source Materials" footer.
   - `wiki/analyses/paper-timeline.md` (page intro).
   - `wiki/analyses/latentcompress-collaboration-strategy.md` — 2 places: the "What We Have That They Don't" section and the collaboration pitch.
   - `wiki/mocs/practical-systems.md` (paper-timeline blurb).
   - `wiki/overview-state-of-field.md` (opening paragraph).
   - `README.md` — badges, paragraph text, and per-thread `(N papers)` summary headers.
   - `wiki/index.md` (directory tree counts).

5. **Also sweep entity, MOC, analysis, and concept counts** using the same grep-then-update pattern. These counts appear in `wiki/index.md`'s directory tree, in the README badges, and occasionally in MOC text. Pattern: `\b\d+\s+(entit|MOC|analyses|concepts)`. The same authoritative-count rule applies: get the true count from the filesystem (`ls wiki/entities/*.md | wc -l`, etc.), not memory.

6. **Exclude `wiki/log.md` from all updates.** Log entries are immutable point-in-time records; if an old log entry says "wiki covers 25 papers" on a date when that was true, leave it alone even if the current count is different.

## Invariants

- `wiki/log.md` entries are never backdated. Every count inside `wiki/log.md` is correct-as-of the entry's date by definition, and must be left untouched by this sweep.
- The authoritative current count comes from `ls wiki/sources/**/*.md | wc -l` (or equivalent Glob over the appropriate directory for entity/MOC/analysis/concept counts), not from memory, not from the previous badge value, and not from arithmetic alone.
- Every common-offender file must be re-verified by name, even if the grep patterns return clean. Grep regularly misses line-broken phrasings, table cells, templated summary blocks, and counts that have been spelled out as words.
- All four grep patterns must be run; none of them subsumes the others.
- The entity/MOC/analysis/concept sweep is not optional — it is part of the same regression class and runs alongside the paper-count sweep.

## After completion

Return to the calling workflow and proceed with its next numbered step. This fragment is a subroutine — it has no terminal action of its own, and its caller's remaining steps (log entry, commit, report) are not optional just because the sweep is done.

## Used by

- `workflows/create/ingest.md` (Procedure step 10 — "Stale paper-count sweep").
- `workflows/audit/lint.md` (Procedure step 3 — "Paper-count drift sweep").
- `workflows/create/batch-ingest.md` (Procedure step 4, consolidation).
- `workflows/audit/gap-analysis.md`.
- `workflows/enrich/enrich.md`.
- `workflows/audit/enrichment-audit.md` (Phase 4 step 3).
- `workflows/query/query.md` (Procedure step 6, conditional after filing an analysis page).
