# MOC Update

## Purpose

When a new source page is added to the wiki (via ingest or batch-ingest), the relevant MOC's reading path must be updated so the new page is reachable through navigation, not just through `wiki/index.md`. This fragment defines the lightweight per-ingest MOC update — distinct from a full MOC gap analysis (which decides whether new MOCs are needed) and distinct from MOC creation (which is its own workflow).

## When to run

- After a single-paper ingest, once the source page exists.
- After each paper in a batch-ingest.
- Any time a new page joins an existing theme that already has a MOC.

## Procedure

1. **Identify the relevant MOC(s).** A new source page typically belongs to one or two MOCs based on its theme. Open `wiki/mocs/` and pick the MOC whose reading path covers the new page's primary contribution. If the page contributes to multiple themes, update each MOC.
2. **Add the new page to the MOC's reading path** in the position that respects the path's existing ordering principle (chronological, conceptual progression, mechanism-first, etc. — see the MOC's own header to determine which principle applies). Do not append to the end by default.
3. **Update any prose descriptions in the MOC** that reference page counts, key papers, or thematic clusters that the new page changes. Watch for "5+ papers cover X" style sentences whose count would now drift.
4. **Verify the `AGENTS.md` Current MOCs list still matches the actual `wiki/mocs/*.md` files** — this is a fast check (`Glob wiki/mocs/*.md` vs the AGENTS.md list) that catches the rare case where a MOC was accidentally created or deleted in the same session.

## Invariants

- A new source page must appear in at least one MOC's reading path before its ingest is considered complete. Pages that exist only in `wiki/index.md` are not navigable through the wiki's curated paths.
- The reading path's existing ordering principle is load-bearing — do not insert the new page at the end by default. Position it where the ordering principle says it belongs.
- Prose page counts inside MOC files must be updated to the new value at MOC-update time. Stale counts in MOC blurbs are also caught by the [stale count sweep](stale-count-sweep.md), but updating them here prevents the sweep from finding extra work and reduces the risk of two ingests racing on the same MOC count.
- This fragment does not create new MOCs. If a theme has 5+ pages and no MOC, that is the job of `workflows/moc-gap-analysis.md`, not this procedure.
- "MOC" and "reading path" are not synonyms. The MOC is the file; the reading path is the ordered traversal baked into the file's body. This procedure updates the reading path (and any prose around it) without creating a new file.

## After completion

Return to the calling workflow and proceed with its next numbered step. This fragment is a subroutine — it has no terminal action of its own, and its caller's remaining steps (raw/index update, analyses review, count sweep, log entry, commit, report) are not optional just because the MOC update is done.

## Used by

- `workflows/ingest.md` (expected, PR 2b — Procedure step 8)
- `workflows/batch-ingest.md` (expected, PR 2b — once per ingested paper, before consolidation)
