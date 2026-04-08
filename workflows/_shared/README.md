# _shared

This directory holds reusable fragments referenced by the workflows in the parent `workflows/` directory. Fragments exist so that multi-step procedures, completion criteria, and invariants can be authored once and transcluded (or referenced) from every workflow that needs them, rather than copy-pasted and drifting out of sync.

## Subdirectories

- `procedures/` — imperative multi-step procedures (do X, then Y, then Z). These are action sequences a workflow runs verbatim.
- `checklists/` — declarative completion criteria. Items that must be true before a workflow is considered done.
- `rules/` — invariants and constraints the wiki must always satisfy, independent of which workflow is running.

## Conventions

- Any file whose name starts with `_` is not itself a runnable workflow; it is a fragment or index.
- Every fragment file must end with a `## Used by` footer listing the workflows that reference it, one per line, as a relative path. This lets `workflows/audit/lint.md` grep-verify that references are bidirectional and that no fragment is orphaned.
- Fragments should be self-contained: a reader should be able to understand what the fragment does without opening the calling workflow.
- When a fragment changes, update every workflow listed in its `## Used by` footer in the same commit.
