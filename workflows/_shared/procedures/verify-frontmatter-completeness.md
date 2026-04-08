# Verify Frontmatter Completeness

## Purpose

Wiki page frontmatter is the source of truth for type, title, provenance, and indexing. Drift in frontmatter (missing fields, wrong `type:` values, stale `latex_source:` paths) propagates into indexes and breaks plugin compatibility weeks later. This fragment defines the **canonical frontmatter schema by page type** and the per-context completeness check, replacing the four drifted inlined copies in `ingest.md`, `review.md`, `plugin-audit.md`, and `verification.md` (where the field set differed in every copy: ingest listed 9 fields, review listed 5, plugin-audit checked only `title:`, verification checked 2).

## When to run

- During an ingest, when creating a new source page (full schema for the page's type).
- During a review pass, when spot-checking a sample of pages (universal-minimum check + per-type extensions).
- During a plugin-audit pass (universal-minimum check; the plugin-specific extensions are tracked elsewhere).
- During a verification pass on subagent-produced pages (full schema for the page's type — subagents commonly drop fields).

## Canonical schema

The canonical frontmatter schema by page type lives in [`../rules/frontmatter-schema.md`](../rules/frontmatter-schema.md). That rule is the single source of truth — this procedure references it and never restates the schema inline. Load-bearing summary for in-procedure decisions:

- **Universal minimum** (every page): `type:`, `title:`, `created:`.
- **Source pages** add: `source_file:`, `latex_source:` (if on disk), `author:`, `date_published:`, `date_ingested:`, `tags:`, conditionally `venue_pdfs:`.
- **Entity pages** add: `aliases:`, `tags:`, `updated:`.
- **Entity-partial pages** add: `parent:`, `partial:`.
- **Other types** require only the universal minimum.

For the full per-type schema, the recognized `type:` enumeration, and the field-by-field rationale, open the rule fragment.

## Procedure

1. **Determine the page's `type:`.** This selects which schema applies. Pages without a `type:` field are an immediate fail — flag and stop.
2. **Verify the universal-minimum fields are present and well-formed.** `type`, `title`, `created`. Empty values count as missing.
3. **Verify the per-type extensions** from the schema above. For source pages, all 8 fields plus the conditional `venue_pdfs:`. For entities, all 4 plus partial conventions if applicable. For concept/MOC/analysis/overview, the universal minimum is sufficient unless the workflow says otherwise.
4. **Verify file path references resolve.** Every `source_file:`, `latex_source:`, `venue_pdfs:` path must exist on disk. Use `Glob` to confirm; never trust the frontmatter alone. Phantom paths are the most common drift class for source pages.
5. **Verify `type:` matches the page's directory.** Source pages in `wiki/sources/`, entities in `wiki/entities/`, concepts in `wiki/concepts/`, MOCs in `wiki/mocs/`, analyses in `wiki/analyses/`. Mismatches indicate the page was created in the wrong place or its `type:` was set wrong.
6. **Flag findings, do not silently fix during a review pass.** During an ingest where the page is newly created, fix in place. During a review/audit, surface the issue back to the workflow's findings list so the pattern is visible.

## Invariants

- The universal minimum (`type`, `title`, `created`) is non-negotiable for every wiki page. No exceptions.
- `type:` values must come from the canonical enumeration. Custom or freeform `type:` values are caught by `workflows/schema-self-audit.md`.
- File path references in frontmatter must exist on disk. Phantom `source_file:`, `latex_source:`, or `venue_pdfs:` entries are bugs, not documentation.
- The conditional `venue_pdfs:` is only listed when the venue PDF is in `raw/pdf/`. Listing it before the file is downloaded creates a phantom that propagates into `raw/index.md` and breaks lint passes weeks later.
- During a review/audit pass, this procedure flags findings rather than silently fixing them. Silent fixes hide drift patterns.
- During an ingest, this procedure fixes in place because the page is being authored from scratch.

## After completion

Return to the calling workflow and proceed with its next numbered step. This fragment is a subroutine — it has no terminal action of its own, and the calling workflow's remaining steps (further checks, fixes, log entry, report) are not optional just because the frontmatter check is done.

## Used by

- `workflows/ingest.md` (Procedure step 4, "Create a source page")
- `workflows/enrich.md` (Procedure step 3, raw asset linking pass)
- `workflows/review.md` (Procedure step 2, "Spot-check that all pages have required frontmatter fields")
- `workflows/plugin-audit.md` (Procedure step 2, Pandoc compliance check; the universal-minimum check covers the `title:` requirement)
- `workflows/verification.md` (Procedure step 2, "Confirm frontmatter is complete and consistent")
