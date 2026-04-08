# Spot-Check Agent Output

## Purpose

Subagents working in parallel on a wiki workflow commonly make small but consequential mistakes — wrong file paths, imprecise claims, numbers off by small amounts, conflated findings from different papers, or stale frontmatter. This fragment defines the **lightweight spot-check** the coordinator runs after a parallel-subagent phase completes, before the work is treated as final. It is not a full verification pass (`workflows/verification.md` is the heavyweight workflow for that); it is the minimum trust-but-verify check every parallel workflow owes its own outputs.

## When to run

- Immediately after a parallel-subagent phase completes, before the consolidation phase that touches shared files.
- Inside the `enrichment-audit.md` Phase 4 consolidation pass.
- Inside the `batch-ingest.md` consolidation step.
- Any time subagent output is about to be promoted to the wiki without the user having seen it page-by-page.

## Procedure

1. **Sample, do not exhaustively review.** Pick 2–3 pages from the agent output (or one per agent if there are few). Exhaustive review is the job of `workflows/verification.md`; this is the catch-the-obvious-stuff pass.
2. **Check numbers.** For each sampled page, verify any quantitative claims (parameter counts, accuracy figures, paper years, benchmark scores) against the underlying source. Numbers off by small amounts are the most common subagent error and the easiest to miss in casual reading.
3. **Check links.** For each `[[wiki-link]]` in the sampled pages, confirm the target file exists. Phantom wiki-links propagate quickly through indexes and break navigation.
4. **Check frontmatter.** Confirm each sampled page has the required frontmatter fields per the canonical schema (`type:`, `title:`, `created:`, plus any type-specific fields). Subagents sometimes drop fields or use the wrong `type:` value.
5. **Flag, do not silently fix.** If the spot check finds an issue, surface it back to the user (or the workflow's findings list) rather than editing the page in place. Silent fixes hide patterns of subagent error that would otherwise inform later workflows.
6. **Decide whether to escalate.** If the spot check finds two or more issues across the sample, the parallel phase's output is suspect at scale and the workflow should escalate to a full verification pass via `workflows/verification.md` before the work is consolidated.

## Invariants

- This is a sampling check, not an exhaustive review. Do not let it expand into a per-page audit — that escalation belongs to `workflows/verification.md`.
- Findings are flagged, not silently corrected. Silent fixes hide error patterns and prevent future workflows from learning where subagent failure modes cluster.
- The escalation rule is non-negotiable: 2+ issues across the sample → full verification pass before consolidation. Treating "looks mostly fine" as good enough is how a bad parallel phase ships.
- Numbers, links, and frontmatter are the three load-bearing categories. Other concerns (prose quality, redundancy, depth) belong to `workflows/review.md` and `workflows/enrich.md`, not this spot check.

## After completion

Return to the calling workflow and proceed with its next numbered step. This fragment is a subroutine — it has no terminal action of its own, and its caller's remaining steps (consolidation, log entry, report) are not optional just because the spot check is done. If the spot check escalated to full verification, the calling workflow must wait for verification to complete before resuming consolidation.

## Used by

- `workflows/enrichment-audit.md` (Phase 4 step 4, replacing the inlined "Spot-check agent output" line)
- `workflows/verification.md` (as the entry-point lightweight check before the heavier per-page review subagents are dispatched)
- `workflows/batch-ingest.md` (after parallel ingest phase, before consolidation)
- `workflows/moc-gap-analysis.md` (after parallel MOC-creation subagents complete)
