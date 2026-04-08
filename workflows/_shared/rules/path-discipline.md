# Rule: Path Discipline

## Statement

Every file path written into the wiki — frontmatter values, body wiki-links, `raw/index.md` and `raw/checklist.md` entries, MOC reading-path links — MUST point to a file that actually exists on disk at the moment of writing. Phantom paths are never acceptable, even temporarily.

Additionally, the canonical local-path prefixes are `raw/pdf/` and `raw/latex/`. The `reference/pdf/` and `reference/latex/` prefixes are stale historical paths from a pre-move vault layout and must never be reintroduced.

## The two sub-rules

### Sub-rule 1: No phantom paths

Before writing any file path into the wiki, verify the path exists with `Glob` (or equivalent). This applies to:

- Frontmatter `source_file:`, `latex_source:`, `venue_pdfs:`.
- Body wiki-links of the form `[[raw/pdf/...]]`, `[[raw/latex/...]]`.
- Rows in `raw/index.md`'s asset tables.
- Rows in `raw/checklist.md`.
- Cross-references in MOCs and analyses.

The "I will download it next" reasoning is not acceptable. The file must be on disk before its path is written. If a path is needed before the file exists, the workflow must download the file first.

### Sub-rule 2: Canonical prefixes only

The only acceptable local-path prefixes for raw assets are:

- `raw/pdf/arxiv-XXXX.XXXXX.pdf` for canonical PDFs.
- `raw/pdf/<venue>-arxiv-XXXX.XXXXX.pdf` for venue-duplicate PDFs.
- `raw/latex/arxiv-XXXX.XXXXX/` (with trailing slash) for `extract`-mode LaTeX directories.
- `raw/latex/arxiv-XXXX.XXXXX.tar.gz` for `archive`-mode LaTeX tarballs.

`reference/pdf/...` and `reference/latex/...` are stale. They predate a directory move and have caused drift in the past. The lint workflow's checklist sync check greps `raw/checklist.md` for these prefixes and requires zero matches.

## Rationale

Phantom paths propagate. A phantom `venue_pdfs:` entry in a source page's frontmatter is copied into `raw/index.md` by the next ingest, listed in `raw/checklist.md` by the next batch update, and cited in a MOC by the next enrich pass. By the time the lint workflow catches the phantom (weeks later), it lives in 4–5 files and the cleanup requires the bulk-rewrite procedure.

The "verify with `Glob` first" rule is cheap (one tool call) and catches the regression at the cheapest possible point: before the path is ever written. Every past phantom-path bug would have been prevented by enforcing this rule at write time.

The `reference/` prefix predates a directory reorganization that moved everything under `raw/`. The old prefix lingers in the agent's training data and is reintroduced during ingests by agents that haven't been told the move happened. Listing the deprecated prefix here is the durable defense.

## How violations are caught

- `workflows/_shared/procedures/raw-checklist-row.md` — invariants forbid `reference/pdf/...` and `reference/latex/...`.
- `workflows/audit/lint.md` Redundancy & Dead-Reference Audit, section A — phantom raw asset detection (greps frontmatter and body links against the actual `raw/pdf/` and `raw/latex/` listings).
- `workflows/audit/lint.md` checklist sync check — greps `raw/checklist.md` for `reference/pdf/` and `reference/latex/`, requires zero matches.

## Used by

- `workflows/_shared/procedures/raw-checklist-row.md` (canonical row format that enforces the prefixes)
- `workflows/_shared/procedures/verify-frontmatter-completeness.md` (per-page check that validates path resolution)
- `workflows/_shared/rules/frontmatter-schema.md` (the conditional `venue_pdfs:` clause references this rule)
- `workflows/create/ingest.md`, `workflows/create/batch-ingest.md` (applies to every page-creation step)
- `workflows/audit/lint.md` (applies to phantom detection sub-pass)
