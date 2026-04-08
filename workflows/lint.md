# Lint (Health Check)

```mermaid
graph TD
    Start([Start Lint]) --> CS

    subgraph CS [Content Integrity Scan]
        style CS fill:#dae8fc,stroke:#6c8ebf
        C1[Check contradictions<br>between pages]
        C2[Find stale claims<br>superseded by newer sources]
        C3[Detect orphan pages<br>with no inbound links]
        C4[Flag red links<br>mentioned but missing pages]
        C1 --> C2 --> C3 --> C4
    end

    CS --> SS

    subgraph SS [Structural Integrity Check]
        style SS fill:#fff2cc,stroke:#d6b656
        S1[Verify file placement<br>wiki/, mocs/, concepts/]
S2[Validate paths in<br>raw/index.md & AGENTS.md]
        S3[Confirm index.md<br>directory tree counts]
        S1 --> S2 --> S3
    end

    SS --> RF

    subgraph RF [Report Findings]
        style RF fill:#d5e8d4,stroke:#82b366
        R1[Group issues:<br>content vs structural]
        R2[Propose specific<br>actionable fixes]
        R1 --> R2
    end

    RF --> UA

    subgraph UA [User Approval Gate]
        style UA fill:#ffe6cc,stroke:#d79b00
        U1{User approves<br>proposed fixes?}
    end

    U1 -- Yes --> AF
    U1 -- No --> Done([End])

    subgraph AF [Apply Fixes & Log]
        style AF fill:#e1d5e7,stroke:#9673a6
        A1[Apply approved fixes]
        A2[Log lint pass<br>in wiki/log.md]
        A1 --> A2
    end

    AF --> Done
```

## Purpose
Run a health check across the wiki to find content drift, broken references, and structural inconsistencies before they spread.

## When To Use
Use this workflow when you need to audit the wiki for quality issues, especially after refactors, new ingests, bulk edits, or navigation changes.

## Trigger Phrases
- `lint`
- `health check`
- `scan for issues`
- `check the wiki`
- `find broken links`
- `review for drift`

## Do Not Use When
- You only need to answer a question from the wiki. Use `workflows/query.md`.
- You are adding new source material. Use `workflows/ingest.md`.
- You are deepening existing pages rather than checking integrity. Use `workflows/expand.md`.
- You are performing a broader full-wiki pass. Use `workflows/review.md`.

## Required Context
- Current `wiki/` structure and recent edits.
- `wiki/index.md`.
- Relevant MOCs in `wiki/mocs/`.
- `raw/index.md`.
- `AGENTS.md` workflow and path references.

## Procedure
1. Scan all wiki pages for content integrity issues:
   - Contradictions between pages.
   - Stale claims superseded by newer sources.
   - Orphan pages with no inbound links.
   - Mentioned but non-existent pages.
   - Missing cross-references.
   - Gaps worth investigating.
2. Verify structural integrity:
   - All wiki pages live under `wiki/`, not the vault root.
   - MOC files live at `wiki/mocs/*.md`.
   - Concepts live in `wiki/concepts/`.
   - Full-path wiki-links in `raw/index.md` match actual file locations.
   - `wiki/index.md` directory tree counts match actual page counts (sources, entities, MOCs, analyses, concepts).
   - `AGENTS.md` Current MOCs list matches the actual `wiki/mocs/*.md` files.
   - No stale path references remain in `AGENTS.md`, `README.md`, or index files after reorganizations.
   - Mermaid node labels use `<br>` for line breaks, not `\n` (which renders literally in Obsidian).
3. **Paper-count drift sweep** (catches the regression class where prose counts drift after ingests):
   - Determine the *authoritative* current count by `ls wiki/sources/**/*.md | wc -l` (or equivalent Glob).
   - Grep `wiki/` and `README.md` for any number followed by `papers`, `source pages`, or `source papers` (e.g., `\b\d+\s+(papers|source pages|source papers)\b`).
   - Also grep for the patterns `synthesized from all \d+`, `wiki covers \d+`, and `(across|all) \d+ papers` to catch variant phrasings.
   - Flag every match where the number does not equal the authoritative count, **except** matches in `wiki/log.md` (log entries are point-in-time records and must not be backdated).
   - Common offenders to check by name: `wiki/analyses/frontier-research-directions.md`, `wiki/analyses/benchmark-overlap.md` (4 places), `wiki/analyses/paper-timeline.md`, `wiki/analyses/latentcompress-collaboration-strategy.md` (2 places), `wiki/mocs/practical-systems.md`, `wiki/overview-state-of-field.md`, `README.md` (badges + paragraph + per-thread `(N papers)` headers), `wiki/index.md` (directory tree).
   - Also sweep entity counts, MOC counts, analysis counts, and concept counts using the same pattern (`\b\d+\s+(entit|MOC|analyses|concepts)`).
4. **Checklist sync check** (catches drift between `raw/index.md` and `raw/checklist.md`, the URL audit trail). The checklist tracks arXiv papers only; non-arXiv sources (e.g., the latentcompress GitHub project) are intentionally excluded, so the row count must be compared against the *Canonical PDFs* count in `raw/index.md`'s summary table, **not** the total unique source pages count.
   - Count the canonical PDF rows in `raw/index.md` (the "Canonical PDFs" table, excluding the venue-duplicate section and any non-arXiv rows).
   - Count the data rows in `raw/checklist.md` (the markdown table, excluding the header and separator rows).
   - Confirm the two counts match. If they do not, flag the delta.
   - Grep `raw/checklist.md` for `reference/pdf/` and `reference/latex/`. Zero matches are required — these are stale historical paths from a directory move and must be rewritten to `raw/pdf/...` / `raw/latex/...`.
   - For each canonical PDF arxiv ID in `raw/index.md`, confirm a matching row exists in `raw/checklist.md` (match by arxiv ID in either the "Original refs from list" column or the "Local PDF" path). Flag any arxiv IDs present in `raw/index.md` but missing from `raw/checklist.md`, and any rows in `raw/checklist.md` whose arxiv ID is not in `raw/index.md`.
5. Run the **Redundancy & Dead-Reference Audit** (see section below). This is a four-class sub-pass that catches phantom raw assets, source-page ↔ raw asset bijection breaks, slug collisions, and MOC/concept overlap.
6. Report findings and suggest fixes.
7. Apply fixes only after user approval.
8. Log the lint pass in `wiki/log.md`.

## Redundancy & Dead-Reference Audit

A focused sub-pass that catches the four classes of bug found in the 2026-04-08 audit. Run all four checks; report each class separately.

### A. Phantom raw asset references

Every `source_file:`, `latex_source:`, and `venue_pdfs:` value, plus every `[[raw/...|...]]` body link, must point to an actual file on disk.

1. `Glob raw/pdf/*` and `Glob raw/latex/*` to enumerate what exists.
2. `Grep -n 'source_file:|latex_source:|venue_pdfs:' wiki/sources/` to enumerate frontmatter claims.
3. `Grep -n '\[\[raw/' wiki` to enumerate body-link claims.
4. Diff: any path referenced but not present is a phantom. Fix by either (a) re-acquiring the file, or (b) deleting the reference and updating `raw/index.md` and the summary table.

### B. Source-page ↔ raw asset bijection

The wiki's invariant: every `arxiv:` ID in `wiki/sources/**/*.md` maps 1:1 to a PDF in `raw/pdf/`, and vice versa. Exceptions: pages with no `arxiv:` field (external projects, GitHub-only sources).

1. `Grep -n '^arxiv:' wiki/sources` → list of ingested arXiv IDs.
2. `Glob raw/pdf/arxiv-*.pdf` → list of stored PDFs.
3. Diff. An ID in (1) but not (2) means a missing download. A PDF in (2) but not (1) means an unreferenced raw asset (potentially redundant).
4. Cross-check the same against `raw/index.md`'s "Canonical PDFs" table — any row that no longer matches a source page is stale.

### C. Slug collisions and naming ambiguity

When two source pages share a leading filename token (e.g., `kvcomm-*`, `coconut-*`), readers can't disambiguate without opening both. Flag any cluster of 2+ files in the same `wiki/sources/**/` directory whose slugs share the first token.

1. `Glob wiki/sources/**/*.md` and group basenames by their first hyphenated token.
2. For any group with size ≥ 2 from different papers, suggest a hybrid rename: `<technique>-<institution>-<distinguisher>.md` (e.g., `kvcomm-kth-selective.md` vs `kvcomm-duke-online-reuse.md`).
3. Renames are bulk operations — see "Bulk source-page rename" below.

### D. MOC and concept overlap

Two MOCs are redundant when one defers to the other for its primary content. Two concept pages are redundant when their bullet lists overlap by more than ~50%.

1. `Grep -n 'see \*\*\[\[|see the full' wiki/mocs/` — explicit deferrals are a smell.
2. For any MOC whose body section is duplicated in another MOC, propose collapsing it to the unique scaffolding (cross-cutting concepts, key entities, theoretical foundations) and adding a one-line pointer to the canonical source.
3. For concept-page overlap, prefer keeping the synthesis page and folding the duplicate into a section anchor.

## Bulk source-page rename

When option **C** above triggers (or any other rename of a source page slug), follow this exact sequence to keep all backlinks consistent. **Do not** edit one file at a time — the surface area is large enough that a single missed link breaks navigation.

1. **Enumerate references first**: `Grep '\[\[<old-slug>' .` — confirm the count and the files affected.
2. **Move the file with `git mv`** so history is preserved. Never use `Write` to create a new file alongside the old.
3. **Bulk rewrite all references**. The blessed tool for this single case is `sed` (the only place where `sed` overrides the "use Edit, not sed" default), because (a) the slug is unique enough that collateral damage is impossible to introduce, and (b) the alternative is 30+ Read+Edit pairs:

   ```bash
   find wiki raw -name "*.md" -print0 | xargs -0 sed -i 's/<old-slug>/<new-slug>/g'
   ```

4. **Verify**: re-run `Grep '<old-slug>' .` — must return zero matches.
5. **Update `raw/index.md`** if the source page is also referenced there (the sed pass usually handles this — confirm).
6. **Log it** in `wiki/log.md` with action `lint` or `update`, listing both the old and new slugs.

## Completion Checklist
- Findings are grouped by content vs structural issues.
- Proposed fixes are specific and actionable.
- No files were edited without approval.
- The lint pass is logged in `wiki/log.md` after changes are made.

## Related Workflows
- `workflows/query.md`
- `workflows/ingest.md`
- `workflows/expand.md`
- `workflows/review.md`
- `workflows/batch-ingest.md`
