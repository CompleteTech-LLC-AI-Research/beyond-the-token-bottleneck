# Parallel Subagent Protocol

## Purpose

When a workflow dispatches work across multiple subagents (per-paper ingest, per-page review, per-task enrichment, per-MOC creation), the coordinator must enforce a strict isolation contract: subagents own only their assigned files, never touch coordinator-only files, and surface findings rather than silently fixing them. Without this protocol, parallel work race-conditions on shared indexes, double-edits MOCs, and produces irreproducible state. This fragment is the canonical isolation contract every parallel-subagent workflow must follow.

The off-limits file enumeration in this fragment is the **complete** list. Earlier inlined copies in `batch-ingest.md`, `verification.md`, `moc-gap-analysis.md`, and `enrichment-audit.md` each listed a different subset (`raw/index.md` was missing from one, `AGENTS.md` was forbidden in only one, etc.). The drift introduced real bugs. The fragment reconciles them.

## When to run

- Before launching any parallel-subagent phase. The coordinator reads this fragment, applies the contract to its subagent prompts, and only then dispatches.
- Inside `workflows/batch-ingest.md` (per-paper ingest agents).
- Inside `workflows/verification.md` (per-page review agents — note: review agents return findings only, never edit).
- Inside `workflows/moc-gap-analysis.md` (per-MOC creation agents).
- Inside `workflows/enrichment-audit.md` Phase 3 (per-task enrichment agents).
- Anywhere a workflow says "launch parallel subagents" or "dispatch in parallel".

## Procedure

1. **Decompose the work into independent units** before launching anything. A unit is independent if its files have no overlap with any other unit's files. Per-paper ingest, per-page review, per-task enrichment, and per-MOC creation are the canonical decompositions.

2. **Write each subagent prompt with explicit scope boundaries.** Each prompt MUST include:
   - The exact files the agent owns (read + write).
   - The exact files the agent may read but never write (typically: source pages, references).
   - The off-limits file list (see step 3).
   - A clear instruction to **report** any need to touch an off-limits file rather than touching it.
   - The agent's deliverable (a created page, a returned findings list, a checklist of completed sub-tasks).

3. **Apply the canonical off-limits enumeration from [`../rules/shared-file-off-limits.md`](../rules/shared-file-off-limits.md).** That rule is the single source of truth for which files are coordinator-only. Subagents MUST NOT edit any file in the rule's enumeration; if they need to, they must surface the need to the coordinator and wait. The rule fragment lists the complete set and explains why each file is included; do not maintain a separate enumeration in this procedure or in any individual workflow.

4. **Launch the subagents in parallel.** Use the `Agent` tool with `run_in_background: true` for genuinely independent work, or batch tool calls in a single message for foreground parallel execution.

5. **Track completion incrementally.** Do not wait for all agents to finish before reporting. Surface per-agent completion to the user as it happens; this lets long-running phases stay observable.

6. **After all subagents complete, run the [spot-check agent output](spot-check-agent-output.md) sub-procedure** before consolidation. The spot-check is the minimum trust-but-verify pass; if it escalates to full verification, run `workflows/verification.md` before consolidating shared files.

7. **Consolidate shared files yourself, as the coordinator.** Update each off-limits file from step 3 with the aggregated outputs of the subagents. Stage and commit the consolidation as a single coherent change, not interleaved with subagent work.

8. **Run the [stale count sweep](stale-count-sweep.md) and the [living analyses review](living-analyses-review.md)** if the parallel phase added or removed source pages. Both fragments are mandatory for any phase that changes the source-page count or touches analyses.

## Invariants

- **Subagents never edit off-limits files.** Violations of this rule have produced multi-hour cleanups in past sessions; the rule is non-negotiable.
- **The off-limits enumeration in this fragment is canonical.** No workflow may inline a shorter list. If a new file becomes coordinator-only, add it here, not in individual workflows.
- **Subagents report, coordinators consolidate.** This is the single most important habit for keeping parallel work auditable. A coordinator who lets subagents touch shared files is no longer running this protocol.
- **Verification subagents are a special case** — they read pages and return findings, never edit. The off-limits list still applies; they simply have a stricter "no writes anywhere" constraint on top.
- **Spot-check before consolidation, always.** Skipping the spot-check has, in past sessions, shipped numbers-off-by-small-amounts errors into the wiki that weren't caught for weeks.
- **Stale count sweep + living analyses review run after consolidation, not before.** The sweep needs the post-consolidation count to be authoritative.

## After completion

Return to the calling workflow and proceed with its next numbered step. This fragment is a subroutine — it has no terminal action of its own, and the calling workflow's remaining steps (final consolidation reports, log entry, commit, user report) are not optional just because the parallel phase has completed.

## Used by

- `workflows/batch-ingest.md` (expected, PR 2b — Procedure step 2, replacing the inlined "Launch parallel subagents" enumeration)
- `workflows/verification.md` (expected, PR 2b — Procedure step 3, "Run the content accuracy check in parallel")
- `workflows/moc-gap-analysis.md` (expected, PR 2b — Procedure steps 8–11, "Use parallel subagents if creating 2+ MOCs")
- `workflows/enrichment-audit.md` (expected, PR 2b — Phase 3, "Execute in Parallel")
- `workflows/plugin-audit.md` (expected, PR 2b — Procedure step 3, "Bulk fix any issues found using parallel subagents")
