# Rule: Coordinator-Only Files

## Statement

A specific set of files is **coordinator-only**: subagents launched in parallel from a workflow MUST NOT edit them. The coordinator (the human user or the orchestrator agent running the workflow) is the only writer for these files. Subagents that need to surface changes to a coordinator-only file MUST report the need rather than editing the file themselves.

## The canonical enumeration

The complete list of coordinator-only files. Subagents must treat all of these as read-only:

- `wiki/index.md`
- `wiki/log.md`
- `wiki/overview-state-of-field.md`
- All MOCs under `wiki/mocs/*.md`
- All living analyses under `wiki/analyses/*.md`
- `raw/index.md`
- `raw/checklist.md`
- `raw/download_arxiv_papers.py`
- `AGENTS.md`
- `README.md`
- Any fragment under `workflows/_shared/`
- Any workflow file under `workflows/*.md`

## Why this enumeration is canonical

Earlier inlined off-limits lists in `batch-ingest.md`, `verification.md`, `moc-gap-analysis.md`, and `enrichment-audit.md` each enumerated a different subset. The drift was real and produced bugs:

- `enrichment-audit.md` Phase 3 omitted `raw/index.md`, allowing parallel agents to race-edit it.
- `moc-gap-analysis.md` step 11 omitted both `raw/index.md` and `AGENTS.md`.
- `batch-ingest.md` was the only workflow that explicitly forbade `AGENTS.md`.
- `verification.md` named "shared files" generically without an enumeration at all.

This rule fragment is the single source of truth. Workflow-level enumerations are forbidden; workflows reference this rule instead.

## Rationale

Coordinator-only files have one or more of these properties:

1. **Aggregate state** (`wiki/index.md`, `raw/index.md`, `raw/checklist.md`) — they summarize the entire vault, so concurrent edits race-condition into corruption.
2. **Append-only audit trails** (`wiki/log.md`) — see [log-immutability.md](log-immutability.md). Subagents writing to log.md break the chronological ordering invariant.
3. **Cross-cutting synthesis** (`wiki/overview-state-of-field.md`, all `wiki/analyses/*.md`, all `wiki/mocs/*.md`) — they reflect editorial judgments that span the whole vault. A subagent working on a single page lacks the context to update them correctly.
4. **Reproducibility surfaces** (`raw/download_arxiv_papers.py`) — must remain runnable from a clean clone. Subagent edits without the full asset list can break the downloader.
5. **Process documentation** (`AGENTS.md`, `workflows/*.md`, `workflows/_shared/**`) — they shape future workflow runs and deserve PR review even when the author is the same agent.
6. **Public surfaces** (`README.md`) — visible to external readers and curated separately.

The cost of forbidding subagent edits to these files is small (the coordinator consolidates after the parallel phase). The cost of allowing them is high (race conditions, lost work, audit trail corruption).

## How violations are caught

- `workflows/_shared/procedures/parallel-subagent-protocol.md` — enforces the rule at subagent dispatch time. Subagent prompts MUST include the enumeration and the "report, do not edit" instruction.
- `workflows/_shared/procedures/spot-check-agent-output.md` — would surface unexpected edits to coordinator-only files in the post-phase sample.
- `workflows/verification.md` — full verification pass would catch any edits to coordinator-only files in the parallel-phase output.
- Manual: `git diff --stat` on the parallel-phase output should show zero changes to any file in this enumeration.

## How to extend the enumeration

When a new file becomes coordinator-only — typically because a workflow change makes it aggregate, append-only, or cross-cutting — add it here. Do not add it to individual workflows; that path is what produced the original drift.

## Used by

- `workflows/_shared/procedures/parallel-subagent-protocol.md` (canonical enforcement point — every subagent dispatch consumes this enumeration)
- `workflows/_shared/procedures/spot-check-agent-output.md` (post-phase verification reference)
- `workflows/_shared/procedures/commit-and-push.md` (the "do not touch" bucket overlaps with this enumeration)
- `workflows/batch-ingest.md`, `workflows/verification.md`, `workflows/moc-gap-analysis.md`, `workflows/enrichment-audit.md`, `workflows/plugin-audit.md` (replacing each workflow's drifted inline enumeration)
