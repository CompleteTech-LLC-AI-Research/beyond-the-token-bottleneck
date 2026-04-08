# Ingest Completion Additions

## Purpose

The completion items specific to workflows that add new source pages to the wiki: `ingest.md`, `batch-ingest.md`, and `gap-analysis.md` (Phase 3 onward). Compose with [`base.md`](base.md) — both must hold for an ingest-class workflow to be considered complete.

## When to use

- At the end of any single-paper or multi-paper ingest.
- At the end of `gap-analysis.md` once the procured paper has been ingested.
- During a review of a recent ingest, to verify completeness after the fact.

## The ingest additions

- [ ] **The source page exists in the correct `wiki/sources/` subdirectory** at full depth standard, with a `## One-liner` heading + `![[<slug>/one-liner]]` embed below the H1, and a matching `wiki/sources/<category>/<slug>/one-liner.md` partial file with `type: source-partial`, `parent: <slug>`, `partial: one-liner` frontmatter per [`../procedures/source-partials.md`](../procedures/source-partials.md). Frontmatter passes [`../procedures/verify-frontmatter-completeness.md`](../procedures/verify-frontmatter-completeness.md). The page has a `## Source Materials` footer pointing to existing files.
- [ ] **All relevant entity and concept pages were updated or created.** Entity updates use the partial structure defined in [`../procedures/entity-partials.md`](../procedures/entity-partials.md): edits to `wiki/entities/<slug>/timeline.md` and (if applicable) `wiki/entities/<slug>/researchers.md`, never to MOC or analysis transclusion sites.
- [ ] **Relevant MOCs include the new reading-path entry**, inserted in the position the MOC's ordering principle dictates (not appended at the end). Per [`../procedures/moc-update.md`](../procedures/moc-update.md).
- [ ] **`wiki/index.md` and `raw/index.md` and `raw/download_arxiv_papers.py` are in sync** with the new source. Per [`../procedures/update-index-and-assets.md`](../procedures/update-index-and-assets.md).
- [ ] **`raw/checklist.md` includes a new row for the ingested paper** with the eight columns filled per [`../procedures/raw-checklist-row.md`](../procedures/raw-checklist-row.md). The bijection holds: every arXiv paper in `raw/index.md`'s "Canonical PDFs" table has exactly one row in `raw/checklist.md`. No `reference/pdf/...` paths.
- [ ] **Every numbered direction in `frontier-research-directions.md` and every numbered tension in `contradictions.md` was reviewed individually**, not just the page as a whole. Per [`../procedures/living-analyses-review.md`](../procedures/living-analyses-review.md). The high-level "is this page relevant?" question hides individual matches.
- [ ] **All living analyses were reviewed per item**, not just per page. Per [`../procedures/living-analyses-review.md`](../procedures/living-analyses-review.md). The current set is enumerated in the fragment.
- [ ] **The [stale count sweep](../procedures/stale-count-sweep.md) was performed**, every common-offender file re-verified by name. Already in [`base.md`](base.md), but elevated here because ingest is the highest-leverage place for the sweep.
- [ ] **`README.md` badge counts, paragraph text, and per-thread `(N papers)` summary headers all reflect the new count.**
- [ ] **The work was committed and pushed** per [`../procedures/commit-and-push.md`](../procedures/commit-and-push.md). Research files on `master`; workflow files on a feature branch + PR. Pre-existing in-progress work in the working tree was not staged.

## Used by

- `workflows/create/ingest.md`
- `workflows/create/batch-ingest.md`
- `workflows/audit/gap-analysis.md`
