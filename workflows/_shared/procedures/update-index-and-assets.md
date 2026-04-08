# Update Index and Assets

## Purpose

When wiki content changes — pages added, pages removed, raw assets ingested, downloader scripts updated — multiple coordinator-only files must be kept in sync: `wiki/index.md` (directory tree counts and entry lists), `raw/index.md` (asset map), and `raw/download_arxiv_papers.py` (the reproducible download list). This fragment defines the canonical sync procedure, replacing five drifted inlined copies in `ingest.md`, `batch-ingest.md`, `enrich.md`, `synthesize.md`, and `enrichment-audit.md` (where the orderings, sub-step counts, and included files all diverged).

This fragment **does not** include log appends (`wiki/log.md` is its own concern, kept separate so the log is appended exactly once per workflow run, not once per index sync) and **does not** include MOC updates (those live in [`moc-update.md`](moc-update.md), kept separate so the moc-update logic is invoked exactly once per affected MOC, not once per index sync).

## When to run

- After any ingest (single or batch) once the source pages exist.
- After any enrich pass that adds, removes, or restructures pages.
- After any synthesize pass that creates new analysis pages.
- After any enrichment-audit Phase 4 consolidation.
- Any time a page count changes or a raw asset is added/removed/renamed.

## Procedure

1. **Update `wiki/index.md`'s directory tree.** Get the authoritative current counts from the filesystem (`Glob wiki/sources/**/*.md`, `Glob wiki/entities/*.md`, `Glob wiki/mocs/*.md`, `Glob wiki/analyses/*.md`, `Glob wiki/concepts/*.md`) and update each count in the tree to match. Do not rely on memory or arithmetic.

2. **Update `wiki/index.md`'s entry lists.** Each section (Sources, Entities, MOCs, Analyses, Concepts) has a curated list of pages with one-line descriptions. Add the new pages in the position the section's ordering principle dictates (alphabetical, chronological, theme-grouped). Remove any deleted pages from the list. Do not append at the end by default.

3. **Update `raw/index.md`** if the workflow added or removed raw assets. The "Canonical PDFs" table must reflect every PDF in `raw/pdf/arxiv-*.pdf`, the "LaTeX Sources" table must reflect every directory or tarball in `raw/latex/`, and the "Duplicate PDFs (Venue Copies)" section must reflect every venue-duplicate PDF actually present on disk. Verify each path with `Glob` before listing.

4. **Update `raw/download_arxiv_papers.py`** if a new arXiv paper was added during the workflow. The new paper's ID must be in the downloader's list with the correct LaTeX storage mode (`archive` for tarball, `extract` for unpacked directory). The downloader must remain reproducible — running it from a clean clone should produce the on-disk state.

5. **Append the corresponding row to `raw/checklist.md`** for each newly added arXiv paper using the [raw checklist row](raw-checklist-row.md) procedure. Skip this step if no arXiv assets were added.

6. **Verify the bijection.** Every arXiv ID in `raw/index.md`'s "Canonical PDFs" table must have exactly one row in `raw/checklist.md`, and every row in `raw/checklist.md` must correspond to a PDF in `raw/pdf/`. Use the lint workflow's checklist sync check pattern if the workflow doing the sync is large.

## Invariants

- **Authoritative counts come from the filesystem**, not memory or arithmetic. Use `Glob` to count, and update `wiki/index.md` to match the count, not the other way around.
- **Entry lists respect their section's ordering principle.** Appending at the end by default is wrong; the ordering principle (alphabetical, chronological, theme-grouped) is load-bearing.
- **Path references must exist on disk** before being listed in `raw/index.md`. Phantom entries propagate and break lint passes.
- **`raw/index.md` and `raw/checklist.md` are bijective for arXiv papers.** Every entry in one must have a corresponding entry in the other (excluding non-arXiv sources, which are intentionally excluded from the checklist).
- **The downloader must remain reproducible.** A clean clone + downloader run must produce the on-disk state. Adding a paper to `raw/index.md` without adding it to the downloader is a bug, not a deferred task.
- **This fragment does not append to `wiki/log.md`** (that is the calling workflow's responsibility, exactly once at the end) and **does not update MOCs** (that is [`moc-update.md`](moc-update.md), called once per affected MOC).
- **This fragment does not run the [stale count sweep](stale-count-sweep.md).** The sweep is the calling workflow's responsibility after both the index update and any prose-count drift sites are visible.

## After completion

Return to the calling workflow and proceed with its next numbered step. This fragment is a subroutine — it has no terminal action of its own, and the calling workflow's remaining steps (MOC updates, stale count sweep, living analyses review, log entry, commit, report) are not optional just because the index and asset sync is done.

## Used by

- `workflows/ingest.md` (expected, PR 2b — Procedure steps 7, 9, 10, replacing the inlined directory-tree update + raw/index.md + downloader update)
- `workflows/batch-ingest.md` (expected, PR 2b — Procedure step 4, the consolidation pass)
- `workflows/enrich.md` (expected, PR 2b — Procedure steps 4, 5, 6, the index/raw/downloader sync sub-steps)
- `workflows/synthesize.md` (expected, PR 2b — Procedure step 5, "Update `wiki/index.md` and any relevant MOCs")
- `workflows/enrichment-audit.md` (expected, PR 2b — Phase 4 step 1, "Update `wiki/index.md` with new or changed page counts and entries")
