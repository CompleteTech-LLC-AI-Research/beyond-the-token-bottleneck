# Expand Workflow

```mermaid
graph TD
    subgraph identify["Identification"]
        A["Scan wiki pages"] --> B{"Page thin?"}
        B -->|"Source &lt; 500w"| C["Source target"]
        B -->|"Concept &lt; 800w"| D["Concept target"]
        B -->|"Entity missing timeline"| E["Entity target"]
        B -->|"Meets standard"| F["Skip"]
    end

    subgraph source["Source Expansion"]
        C --> S1["Re-read PDF"]
        S1 --> S2["Add mechanism details<br>& experimental numbers"]
        S2 --> S3["Add ablations,<br>limitations, wiki links"]
    end

    subgraph concept["Concept Expansion"]
        D --> K1["Add theoretical<br>foundations"]
        K1 --> K2["Add comparison tables<br>& quantitative evidence"]
        K2 --> K3["Add trade-offs,<br>open questions, PDF cites"]
    end

    subgraph entity["Entity Expansion"]
        E --> N1["Add contribution<br>timeline table"]
        N1 --> N2["Add collaboration<br>patterns & impact"]
        N2 --> N3["Add strategic positioning<br>& researcher profiles"]
    end

    subgraph logging["Completion"]
        S3 --> L["Update wiki/log.md"]
        K3 --> L
        N3 --> L
        L --> DONE["Expansion complete"]
    end

    style identify fill:#dae8fc,stroke:#6c8ebf
    style source fill:#fff2cc,stroke:#d6b656
    style concept fill:#d5e8d4,stroke:#82b366
    style entity fill:#ffe6cc,stroke:#d79b00
    style logging fill:#e1d5e7,stroke:#9673a6
```

## Purpose

Use this workflow to deepen existing wiki pages without changing the overall information architecture.

## When To Use

Use this workflow when pages already exist but need more depth, more evidence, better comparisons, or stronger technical analysis.

## Trigger Phrases

Choose this workflow when the user says things like:

- `expand this page`
- `deepen the wiki`
- `add more detail`
- `make the summary more thorough`
- `fill out the concept page`

## Do Not Use When

Do not use this workflow for new-source onboarding, direct question answering, synthesis-first work, lint-only passes, or structural reorganization.

## Required Context

- The target pages to expand
- The page type for each target: source, concept, or entity
- Any recent sources or related pages that should be cross-referenced
- The depth or emphasis the user wants preserved

## Procedure

1. Identify thin pages — source summaries under 500 words, concept pages under 800 words, entity pages without contribution timelines or strategic positioning.
2. For **source pages**: Re-read the PDF. Add mechanism details, experimental numbers, ablation results, limitations, and connections to the broader wiki. Run [verify frontmatter completeness](../_shared/procedures/verify-frontmatter-completeness.md) on each expanded source page, then return here and continue with step 3.
3. For **concept pages**: Add theoretical foundations, comparison tables, quantitative evidence, trade-off analyses, open questions, and section-specific PDF citations.
4. For **entity pages**: Add contribution timelines (date/paper/role/result tables), collaboration patterns across institutions, ecosystem impact, strategic positioning relative to frontier research directions, and enriched researcher profiles. If extracting timeline or researcher list as partials for transclusion, run [entity-partials](../_shared/procedures/entity-partials.md) in full, then return here and continue with step 5.
5. Update `wiki/log.md` with what was expanded.
6. **Commit and push.** Run [commit and push](../_shared/procedures/commit-and-push.md) in full, then return here — the workflow is complete after this step.

## Completion Checklist

- All items in [`../_shared/checklists/base.md`](../_shared/checklists/base.md) hold.
- Thin pages were identified against the depth standard.
- Source pages were re-read before being expanded.
- Concept pages include stronger theory, comparisons, and citations.
- Entity pages include timelines and strategic context where appropriate.
- `wiki/log.md` records the expansion pass.
- `wiki/log.md` was updated and committed to master.

## Related Workflows

- `workflows/enrich/enrich.md` — structural cleanup companion to depth expansion.
- `workflows/create/ingest.md` — produces the source pages that expand deepens.
- `workflows/audit/lint.md` — validates links after expansion.
- `workflows/audit/review.md` — broader audit that may trigger expansion work.
