# Enrich (Structural Improvement Pass)

```mermaid
graph TD
    Start([Start Enrich Pass]) --> MOC

    subgraph MOC["MOC Gap Analysis"]
        style MOC fill:#dae8fc,stroke:#6c8ebf
        M1[Check themes with 5+ uncovered pages]
        M2[Update existing MOCs for new pages]
M3[Verify AGENTS.md MOC list matches files]
        M1 --> M2 --> M3
    end

    MOC --> BL

    subgraph BL["Backlink Audit"]
        style BL fill:#fff2cc,stroke:#d6b656
        B1[Scan prose for unlinked entities/concepts]
        B2[Add missing wiki-links]
        B3[Ensure bidirectional cross-references]
        B1 --> B2 --> B3
    end

    BL --> RA

    subgraph RA["Raw Asset Verification"]
        style RA fill:#d5e8d4,stroke:#82b366
        R1[Check source_file / latex_source / venue_pdfs]
        R2[Verify Source Materials footers]
        R3[Add section-specific PDF citations]
        R1 --> R2 --> R3
    end

    RA --> IX

    subgraph IX["Index Sync"]
        style IX fill:#ffe6cc,stroke:#d79b00
        I1[Verify wiki/index.md tree counts]
        I2[Verify all pages listed in correct sections]
        I3[Update raw/index.md for new assets]
        I4[Update download_arxiv_papers.py]
        I1 --> I2 --> I3 --> I4
    end

    IX --> LOG

    subgraph LOG["Log & Complete"]
        style LOG fill:#e1d5e7,stroke:#9673a6
        L1[Update wiki/log.md with changes]
        L2[Run completion checklist]
        L1 --> L2
    end

    LOG --> Done([Done])
```

## Purpose
Improve navigation, linking, and discoverability across the wiki without adding new substantive content.

## When To Use
Use this workflow when the wiki already has content and you need to clean up structure, links, asset references, or index consistency.

## Trigger Phrases
- `enrich`
- `improve navigation`
- `fix backlinks`
- `audit links`
- `sync indexes`
- `update asset references`
- `structural cleanup`

## Do Not Use When
- You need to add or deepen substantive page content. Use `workflows/expand.md`.
- You need a broader health check or issue scan. Use `workflows/lint.md`.
- You are ingesting new papers or sources. Use `workflows/ingest.md`.
- You need a full wiki review pass. Use `workflows/review.md`.

## Required Context
- `wiki/index.md`
- Relevant MOCs in `wiki/mocs/`
- Current wiki pages in the affected themes
- `raw/index.md`
- `raw/download_arxiv_papers.py` if arXiv assets were added
- `AGENTS.md` current workflow and MOC references

## Procedure
1. Run a lightweight MOC Gap Analysis:
   - Check whether any theme has 5+ uncovered pages.
   - Update existing MOCs when new pages are added to their theme.
- Verify the `AGENTS.md` Current MOCs list matches actual MOC files.
2. Audit backlinks:
   - Scan for entity and concept names mentioned in prose but not wiki-linked.
   - Add missing links.
   - Check that cross-concept references are bidirectional where the connection is discussed on both sides.
3. Verify raw asset linking:
   - Ensure all source pages have `source_file:`, `latex_source:`, and `venue_pdfs:` when applicable.
   - Ensure all source pages include a `## Source Materials` footer.
   - Add section-specific PDF citations like `[[raw/pdf/file.pdf|Paper §X]]` to concept pages for key claims.
4. Sync indexes:
   - Verify `wiki/index.md` directory tree counts match actual page counts.
   - Verify all pages appear in the appropriate index sections.
5. Update `raw/index.md` if new PDFs or LaTeX sources were added.
6. Update `raw/download_arxiv_papers.py` if arXiv assets were added so the download list stays reproducible.
7. Update `wiki/log.md` with what changed.

## Completion Checklist
- MOC coverage gaps were checked and only expected gaps remain.
- Internal links are present where prose refers to entities or concepts.
- Source pages expose required asset metadata and source-material footers.
- Index counts and page listings match the actual vault state.
- Any arXiv-related changes are reflected in `raw/download_arxiv_papers.py`.
- The work is logged in `wiki/log.md`.

## Related Workflows
- `workflows/lint.md`
- `workflows/expand.md`
- `workflows/ingest.md`
- `workflows/review.md`
- `workflows/moc-gap-analysis.md`
