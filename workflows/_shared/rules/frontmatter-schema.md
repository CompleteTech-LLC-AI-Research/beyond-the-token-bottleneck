# Rule: Frontmatter Schema

## Statement

Every wiki page MUST have frontmatter conforming to the canonical schema for its `type:`. Pages without a recognized `type:` are invisible to `workflows/schema-self-audit.md` and break plugin compatibility.

## Schema

### Universal minimum (every wiki page)

- `type:` — one of `source`, `entity`, `entity-partial`, `concept`, `moc`, `analysis`, `overview`, `workflow-doc`. No freeform values.
- `title:` — human-readable title. The Pandoc plugin requires this on every page.
- `created:` — ISO date the page was first authored.

### `type: source` (additionally)

- `source_file:` — path to the canonical PDF, typically `raw/pdf/arxiv-XXXX.XXXXX.pdf`.
- `latex_source:` — path to the LaTeX source if available. Use `raw/latex/arxiv-XXXX.XXXXX/` (with trailing slash) for `extract`-mode papers, or `raw/latex/arxiv-XXXX.XXXXX.tar.gz` for `archive`-mode papers. Omit cleanly if no LaTeX is on disk; never list a phantom path.
- `author:` — paper author list.
- `date_published:` — paper publication date.
- `date_ingested:` — date the source was added to the wiki.
- `tags:` — bracketed list for cross-referencing.
- *(conditional)* `venue_pdfs:` — only if venue-duplicate PDFs are actually present in `raw/pdf/`. Verify each path with `Glob` before writing the frontmatter. Phantom `venue_pdfs:` entries propagate into `raw/index.md` and break lint passes weeks later.

### `type: entity` (additionally)

- `aliases:` — bracketed list of alternate names (institutions often have several).
- `tags:` — bracketed list.
- `updated:` — date of the most recent edit.

When the entity uses transcluded partials (`timeline.md`, `researchers.md`), see `workflows/_shared/procedures/entity-partials.md` for the partial-structure conventions.

### `type: entity-partial` (additionally)

- `parent:` — slug of the parent entity (e.g. `amazon` for `wiki/entities/amazon/timeline.md`).
- `partial:` — one of `timeline`, `researchers`. Add new partial types here as they are introduced.

### `type: concept | moc | analysis | overview | workflow-doc`

Require only the universal minimum unless an individual workflow's documentation demands more.

## Rationale

The schema-self-audit workflow uses `type:` to inventory pages. Missing or freeform `type:` values create invisible drift — the audit reports clean while pages are missing from the inventory.

The Pandoc plugin requires `title:` on every page; pages without it fail to render in the published view, and the failure surface is the entire publish pipeline rather than a single page.

Source pages without `source_file:` or `latex_source:` lose their connection to the underlying paper, breaking the wiki's source-of-truth invariant. Future ingests cannot cite back to the canonical asset, and `raw/index.md` ↔ source-page bijection breaks.

Phantom file path entries in `source_file:`, `latex_source:`, or `venue_pdfs:` propagate into `raw/index.md` through the ingest workflow and break lint passes weeks after the original ingest. The "verify with Glob before writing" rule has been enforced multiple times after past breakage.

## How violations are caught

- `workflows/_shared/procedures/verify-frontmatter-completeness.md` — the per-page check, run during ingest, review, plugin-audit, and verification passes.
- `workflows/schema-self-audit.md` — the vault-wide audit that inventories pages by `type:` and flags inconsistencies.
- `workflows/lint.md` Redundancy & Dead-Reference Audit, section A — phantom path detection in frontmatter.

## Used by

- `workflows/_shared/procedures/verify-frontmatter-completeness.md` — canonical schema source for the per-page check
- `workflows/_shared/procedures/raw-checklist-row.md` — the raw-checklist row format depends on `source_file:` and `latex_source:` field consistency
- `workflows/schema-self-audit.md` (expected, PR 2b)
- `workflows/lint.md` (expected, PR 2b)
- `workflows/ingest.md`, `workflows/batch-ingest.md` (expected, PR 2b — page creation must conform)
- `workflows/review.md`, `workflows/plugin-audit.md`, `workflows/verification.md` (expected, PR 2b — verification consumers)
