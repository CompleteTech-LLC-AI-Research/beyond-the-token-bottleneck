# Base Completion Checklist

## Purpose

The universal post-conditions every workflow must satisfy before it is considered complete, regardless of which workflow ran. This fragment is the floor — domain-specific workflows compose their own checklist by starting from this base and adding their own items via [`ingest-additions.md`](ingest-additions.md), [`audit-additions.md`](audit-additions.md), or workflow-specific bullets.

## When to use

- Embed this checklist (by reference, not by copy) into the `## Completion Checklist` section of every workflow.
- Run through each item before marking a workflow run as complete.
- During a review pass, verify that each item below holds.

## The base checklist

- [ ] **No coordinator-only files were edited by subagents.** The canonical enumeration is in [`../rules/shared-file-off-limits.md`](../rules/shared-file-off-limits.md). If a parallel-subagent phase ran, `git diff --stat` on the parallel-phase output must show zero changes to any file in that enumeration.
- [ ] **Every file path referenced in this run exists on disk.** Frontmatter `source_file:`, `latex_source:`, `venue_pdfs:`, body `[[wiki-links]]`, `[[raw/...|...]]` body links, and `Glob`/`Read` targets must all resolve. Phantom paths are caught by the lint workflow's Redundancy & Dead-Reference Audit; do not let this run be the one that introduces them. See [`../rules/path-discipline.md`](../rules/path-discipline.md).
- [ ] **`wiki/log.md` has an entry for this run** (for any workflow that mutated state). The entry follows the existing log format and reflects what actually happened, not what was planned. Log entries are immutable point-in-time records — never backdate, never rewrite, never sweep counts inside them. See [`../rules/log-immutability.md`](../rules/log-immutability.md).
- [ ] **If the page count changed, the [stale count sweep](../procedures/stale-count-sweep.md) was performed.** The sweep is a first-class regression class — it is not optional just because the workflow doing the count change is not `ingest`. Any workflow that adds, removes, renames, or reorganizes pages must run the sweep before marking complete.
- [ ] **`wiki/index.md` reflects the current vault state.** Directory tree counts, entry lists, and ordering principles are all in sync with the filesystem. The authoritative counts come from `Glob`, not memory.
- [ ] **The terminology in any new prose uses canonical terms** from [`../glossary.md`](../glossary.md). Drift variants ("gap-tracking analysis pages", "shared files", "stub pages", etc.) should not be introduced by this run.

## Composition with workflow-specific items

Workflows extend this checklist by adding their own items in their `## Completion Checklist` section. The composition pattern is:

1. The workflow's checklist begins with a one-line reference: "All items in [`_shared/checklists/base.md`](_shared/checklists/base.md) hold."
2. Followed by workflow-specific items (page created, MOC updated, analysis reviewed, audit findings reported, etc.).

For ingest, batch-ingest, and gap-analysis, the workflow-specific items are pre-bundled in [`ingest-additions.md`](ingest-additions.md). For lint, review, enrichment-audit, and verification, they live in [`audit-additions.md`](audit-additions.md). Other workflows enumerate their items inline.

## Why a base checklist exists

Before this fragment, every workflow's `## Completion Checklist` re-listed the same universal items (log entry, no shared-file edits, count sync) with subtly different wording. The drift hid violations: a workflow that omitted the count-sync bullet trained agents to skip it. Centralizing the universal items here makes the floor visible and the omissions impossible.

## Used by

- Every workflow's `## Completion Checklist` section, by reference.
