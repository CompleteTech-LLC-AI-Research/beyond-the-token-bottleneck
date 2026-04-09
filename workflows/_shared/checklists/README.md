# Checklist fragments

Declarative completion criteria — items that must be true before a workflow is considered done. Unlike procedures, checklists do not prescribe an order; they describe a state.

## Checklists

- `base.md` — Universal completion items every workflow must verify (e.g., all referenced paths exist, log entry appended, frontmatter complete).
- `ingest-additions.md` — Additional items for ingest/batch-ingest workflows. Composed on top of base.md.
- `audit-additions.md` — Additional items for audit workflows (lint, review, verification, enrichment-audit, plugin-audit). Composed on top of base.md.

## Composition

Each workflow builds its completion checklist by starting from `base.md` and then layering the domain-specific additions file for its concern. For example, a batch-ingest workflow's completion section references:

```markdown
## Completion checklist

1. All items in `workflows/_shared/checklists/base.md` are satisfied.
2. All items in `workflows/_shared/checklists/ingest-additions.md` are satisfied.
```

This keeps universal invariants (path existence, log entry, frontmatter) in one place while letting each domain add its own requirements without duplicating the base set.
