# Rule fragments

Invariants and constraints the wiki must maintain at all times, independent of which workflow is currently running. Rules are the "must never" and "must always" statements that any workflow can assume hold before it starts and must leave holding when it finishes.

## Rules

- `frontmatter-schema.md` — Required YAML fields per page type (source, entity, concept, analysis, MOC, partial).
- `log-immutability.md` — wiki/log.md is append-only; no retroactive edits or corrections.
- `path-discipline.md` — All file paths must be verified on disk before being written into wiki content.
- `shared-file-off-limits.md` — Coordinator-only files (wiki/index.md, wiki/log.md, MOCs, overview) cannot be edited by subagents.
- `slug-disambiguation.md` — How to handle ambiguous filenames that could resolve to multiple wiki pages.
