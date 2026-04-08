# Checklist fragments

Declarative completion criteria — items that must be true before a workflow is considered done. Unlike procedures, checklists do not prescribe an order; they describe a state.

Compositional pattern: each workflow builds its completion checklist by starting from `base.md` (universal items that apply to every workflow, such as "all referenced paths exist" and "log entry appended") and then adding domain-specific items for its own concern (ingest, enrich, lint, etc.).

Planned fragments:

- `base.md` — universal completion items.
- Domain-specific checklists composed on top of `base.md`.

Fragment bodies land in PR 2; this PR only establishes the directory.
