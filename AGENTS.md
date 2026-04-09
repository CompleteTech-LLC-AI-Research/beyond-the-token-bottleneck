# LLM Wiki Schema

You are a wiki maintainer for this Obsidian vault. Every interaction follows these rules.

## Directory Structure

```
raw/                                    # Immutable source documents. Never modify these.
raw/pdf/                                # Source PDFs (referenced by source_file frontmatter).
raw/latex/                              # LaTeX sources (arxiv-*.tar.gz archives or arxiv-* dirs).
raw/download_arxiv_papers.py            # Downloader for arXiv-managed raw assets; keep it in sync.
raw/checklist.md                        # Ingest preparation checklist
raw/index.md                            # Asset index mapping files to wiki pages.
workflows/                              # Task-oriented workflow playbooks. Choose one primary workflow before acting.
  README.md
  CONVENTIONS.md
  _shared/
    checklists/                         # base.md, audit-additions.md, ingest-additions.md
    procedures/                         # 15+ reusable subroutines
    rules/                              # frontmatter-schema.md, log-immutability.md, path-discipline.md, shared-file-off-limits.md, slug-disambiguation.md
    glossary.md
  create/                               # ingest.md, batch-ingest.md, synthesize.md
  enrich/                               # enrich.md, expand.md
  audit/                                # lint.md, review.md, verification.md, gap-analysis.md, moc-gap-analysis.md, enrichment-audit.md, schema-self-audit.md, plugin-audit.md
  query/                                # query.md
  meta/                                 # readme-github-maintenance.md
wiki/                                   # LLM-generated and LLM-maintained pages. You own this entirely.
wiki/index.md                           # Top-level catalog — links to MOCs + flat concept/entity/analysis lists.
wiki/log.md                             # Chronological activity log — append-only. Create if missing.
wiki/overview-state-of-field.md         # Narrative synthesis of the research landscape.
wiki/mocs/*.md                           # Maps of Content — thematic navigation with reading paths.
wiki/mocs/_partials/                    # MOC-partial pages (compatibility-spectrum.md, compression-ratios.md)
wiki/sources/                           # Source summary pages, organized by research theme:
  <theme>/short-title.md                # Shell page with ![[short-title/one-liner]] embed
  <theme>/short-title/
    one-liner.md                        # Source-partial: one-line summary for MOC transclusion
  wiki/sources/reasoning/               #   Intra-agent latent reasoning
  wiki/sources/communication/embeddings/#   Output-layer communication (CIPHER, SDE, etc.)
  wiki/sources/communication/activations/#  Hidden-state communication (AC, Interlat, etc.)
  wiki/sources/communication/kv-cache/  #   KV-cache communication (KVComm, C2C, etc.)
  wiki/sources/communication/structured/#   Disentangled/structured (ThoughtComm, etc.)
  wiki/sources/unified/                 #   Combined reasoning + communication frameworks
  wiki/sources/meta/                    #   Scaling frameworks, external projects
wiki/concepts/                          # Concept pages (ideas, theories, patterns)
wiki/concepts/_partials/                # Concept-partial pages
  framings/                             # Concept framing partials
wiki/entities/                          # Entity pages (people, orgs, products)
  institution-name.md                   # Shell page
  institution-name/
    timeline.md                         # Entity-partial: contribution timeline
    researchers.md                      # Entity-partial: researcher profiles
wiki/analyses/                          # Analysis pages (syntheses, comparisons)
```

### Session Start

At the beginning of each conversation, orient yourself before acting:

1. **`wiki/index.md`** — Read first. This is the page catalog with directory tree counts, MOC links, and flat listings of all concepts/entities/analyses. Tells you what exists.
2. **`wiki/log.md`** (last 5-10 entries) — Check recent activity. Tells you what changed recently and avoids redoing work.
3. **`wiki/overview-state-of-field.md`** — Read only when you need the full narrative context (e.g., for synthesis tasks, query answering, or understanding how a new paper fits the field). Skip for targeted tasks like expanding a single page or fixing a link.
4. **MOCs** — Read the relevant MOC(s) when working on a specific theme. Don't read all 9 unless doing a full review.

For targeted tasks (expand one page, fix one link, ingest one paper), steps 1-2 suffice. For broad tasks (review, synthesis, MOC gap analysis), read step 3 as well.

### Source Categorization

When placing a new source in `wiki/sources/`, use the paper's **primary contribution** to pick the subdirectory:

| Subdirectory | Place here when the paper's main contribution is… |
|---|---|
| `reasoning/` | A method for a single model to reason in continuous/latent space (Coconut, iCoT, Pause Tokens, SoftCoT, etc.) |
| `communication/embeddings/` | Agents exchanging output-layer embeddings (CIPHER, SDE) |
| `communication/activations/` | Agents sharing hidden-state activations (AC, Interlat) |
| `communication/kv-cache/` | Agents sharing or aligning KV-cache entries (KVComm, C2C, KV Alignment) |
| `communication/structured/` | Agents exchanging structured latent objects like disentangled thoughts (ThoughtComm) |
| `unified/` | Systems that combine latent reasoning + communication as co-designed components (LatentMAS, Vision Wormhole, Agent Primitives) |
| `meta/` | Theoretical foundations, scaling analyses, representation theory, or external projects that inform the field but aren't themselves a reasoning/communication method |

**When ambiguous**: If a paper contributes to multiple categories, choose the one that best describes *what's novel*. A paper that uses KV-cache sharing as an implementation detail but primarily proposes a unified multi-agent framework belongs in `unified/`, not `kv-cache/`.

### Adding New Source Subdirectories

Create a new subdirectory under `wiki/sources/` when:
- 3+ papers share a coherent theme that doesn't fit existing categories.
- The theme represents a genuinely distinct research approach, not just a variation on an existing one.

When creating one: add it to the directory tree above, update `wiki/index.md`'s tree, and document it in the categorization table.

## Page Types

Wiki pages use YAML frontmatter. The canonical frontmatter schema and field requirements live in [`workflows/_shared/rules/frontmatter-schema.md`](workflows/_shared/rules/frontmatter-schema.md). This section shows example templates; for the complete specification, required fields, and rationale, consult the rule.

Every page MUST have `type` and `created` fields.

The `updated` field records the date of the last **substantive content change** — new claims, revised analysis, added sources. Bump it when information changes, not for typo fixes, link additions, or formatting.

### Source Summary
```yaml
---
type: source
title: "Article or document title"
source_file: "[[raw/pdf/arxiv-XXXX.XXXXX.pdf]]"        # contextual — see note below
latex_source: "[[raw/latex/arxiv-XXXX.XXXXX.tar.gz]]"  # contextual — see note below
venue_pdfs: ["[[raw/pdf/openreview-ID.pdf|OpenReview]]"]  # optional, if duplicates exist
author: "First Author, Second Author, ..."
date_published: "YYYY-MM-DD"
date_ingested: "YYYY-MM-DD"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"                                  # optional — same "substantive content change" rule as other page types
venue: "Conference or Journal Name"
arxiv: "XXXX.XXXXX"                                    # contextual — see note below
institution: "University, Lab, Company"
tags: []
---
```
For non-arXiv sources (GitHub repos, blog posts), omit `arxiv:` and `latex_source:`. Use `source_file:` to link to whatever raw asset represents the source (PDF, repo directory, etc.).

One per ingested source. Summarizes key claims, data, and takeaways. Links to entity/concept pages.

### Entity Page
```yaml
---
type: entity
title: "Entity Name"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
aliases: []
tags: []
---
```
A person, organization, place, product, or other named thing. Accumulates information across sources. Each claim cites its source summary.

### Concept Page
```yaml
---
type: concept
title: "Concept Name"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: []
---
```
An idea, theory, framework, pattern, or theme. Cross-references related concepts and entities. Evolves as new sources add nuance.

### Analysis Page
```yaml
---
type: analysis
title: "Analysis Title"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: []
---
```
Comparisons, syntheses, arguments, or explorations generated from queries. Filed back into the wiki when valuable. Living analyses (contradictions, open questions, benchmark overlap) get updated on each relevant ingest.

### Overview / Map of Content (MOC) Page
```yaml
---
type: overview
title: "MOC Title"
category: thread | reference | synthesis | lens  # optional
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: [moc]
---
```
Curated navigation pages that organize related wiki pages around a theme. MOCs provide **guided reading paths** with narrative context — not just link lists, but ordered sequences explaining why to read each page and how they connect. A page can appear in multiple MOCs. Create a new MOC when a cluster of pages (typically 5+) forms a coherent theme that benefits from guided navigation. MOCs live at `wiki/mocs/*.md`.

### Source-Partial

```yaml
---
type: source-partial
parent: "<parent-source-slug>"
partial: one-liner
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
---
```
A transcludable fragment of a source page. Currently used for one-liner summaries embedded into MOCs via `![[short-title/one-liner]]`.

### Entity-Partial

```yaml
---
type: entity-partial
parent: "<parent-entity-slug>"
partial: timeline | researchers
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
---
```
A transcludable fragment of an entity page. Used for contribution timelines and researcher profile tables embedded into the parent entity shell page.

### Concept-Partial

```yaml
---
type: concept-partial
partial: "<partial-name>"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
---
```
A transcludable fragment of a concept page. Lives under `wiki/concepts/_partials/`.

### MOC-Partial

```yaml
---
type: moc-partial
partial: "<partial-name>"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
---
```
A transcludable fragment shared across MOC pages. Lives under `wiki/mocs/_partials/`.

Current MOCs:
- `latent-reasoning` — Intra-agent reasoning in continuous space
- `latent-communication` — Inter-agent communication depth spectrum
- `communication-depth-spectrum` — 10-level walkthrough of communication methods by depth
- `unified-frameworks` — Systems combining reasoning + communication
- `theoretical-foundations` — Mathematical underpinnings: complexity theory, representation geometry, convergence hypotheses
- `cross-architecture` — Cross-architecture compatibility: problem statement, theoretical grounding, solutions spectrum
- `practical-systems` — Engineering lens: scaling framework, method selection, deployment trade-offs
- `compression-information-theory` — Compression & Information-Theoretic Bounds
- `safety-interpretability` — Safety, Interpretability & Auditability of Latent Systems

## Linking Conventions

- Use Obsidian wiki-links: `[[Page Name]]` or `[[Page Name|display text]]`.
- Link liberally. Every mention of an entity or concept that has its own page should be linked.
- When creating a new page, scan existing pages for mentions of the new topic and add backlinks.
- Use `[[raw/filename.md|Source: Title]]` to cite raw sources from wiki pages.

## Raw Asset Linking

Source pages link to their raw materials through three frontmatter fields and a footer section:

### Frontmatter Fields
- `source_file:` — Wiki-link to the canonical PDF in `raw/pdf/`. Required for all source pages.
- `latex_source:` — Wiki-link to the LaTeX source in `raw/latex/` (directory or `.tar.gz`). Added when available. **Optional** for non-PDF sources (GitHub repos, blog posts, etc.).
- `venue_pdfs:` — Array of wiki-links to alternate venue copies (OpenReview, ACL Anthology) of the same paper. Added when duplicates exist in `raw/pdf/`.

### Source Materials Footer
Every source page ends with a `## Source Materials` section containing direct links to the PDF and LaTeX source:
```
## Source Materials

- [[raw/pdf/arxiv-XXXX.XXXXX.pdf|PDF]] ([[raw/latex/arxiv-XXXX.XXXXX.tar.gz|LaTeX source]])
```

### Section-Specific PDF Citations
When concept or analysis pages reference specific experimental results, figures, or theorems, cite the PDF section directly inline:
```
...emergent BFS via superposition ([[raw/pdf/arxiv-2412.06769.pdf|Coconut §4.2, Figure 3]]).
```
Use this format only for claims pointing to a specific section/figure/table — not for general references (use wiki-links to source summary pages for those).

### Raw Asset Index
`raw/index.md` maps every file in `raw/pdf/` and `raw/latex/` to its wiki source page, documents naming conventions, and flags duplicate venue PDFs.

### When to Use Each Link Type
- **Wiki-link to source page** (`[[coconut|Coconut]]`): Default for all citations. Reader gets the summary.
- **PDF section link** (`([[raw/pdf/file.pdf|Paper §X]])`): When pointing to a specific section, figure, table, or theorem the reader should verify.
- **LaTeX source link**: Rarely used inline; primarily for the Source Materials footer and for readers who want to inspect equations, figure generation code, or appendix details.

## Workflows

Detailed workflow instructions live in `workflows/*.md`. Do not improvise workflow steps from memory when a workflow file exists.

### Workflow Selection

Read [`workflows/README.md`](workflows/README.md) for the full decision tree and disambiguation tips. Quick rules:

1. Identify exactly one **primary workflow** that best matches the user's request.
2. Choose the **narrowest** workflow that fully covers the task.
3. Read the primary workflow file first. Read secondary workflow files only when the primary workflow explicitly calls for them.
4. Respect workflow boundaries: shared files stay coordinator-owned unless the workflow explicitly says otherwise; if a workflow says to get user approval before applying fixes, stop and ask.
5. When no single workflow fits exactly, combine the minimum number needed and state which workflow is primary.

### Overview Update Triggers

`wiki/overview-state-of-field.md` is the entry point for newcomers. Update it when:

- **3+ papers ingested** in a batch — the field narrative may have shifted.
- **A new research thread emerges** that doesn't fit existing sections (e.g., a new communication channel type).
- **A major contradiction is resolved** or a frontier direction is pursued by a new paper.
- **New MOCs are created** — add them to the overview's navigation references.
- **Entity landscape changes** — new major institutions enter the field.

Do NOT update for minor ingests (1-2 papers that fit cleanly into existing themes) or structural changes (MOC reorganization, backlink fixes) that don't alter the narrative.

### Entity Page Scope

For the canonical Role vocabulary used in Contribution Timeline tables, see the "Entity Contribution Timeline: Role vocabulary" section in [`workflows/CONVENTIONS.md`](workflows/CONVENTIONS.md).

- **One institution, one page**: Default. Create a separate page for each institution (e.g., `harvard.md`, `kth.md`).
- **Multi-institution page**: Use when institutions are tightly coupled on the **same papers** with deeply shared author lists and no independent contributions in the wiki. Example: `princeton-uiuc-stanford.md` — all three appear together on LatentMAS and Agent Primitives with overlapping authors.
- **Split threshold**: If a multi-institution entity later gains an independent contribution from just one member institution, split into separate pages.
- **Never merge** institutions that collaborate on one paper but have independent contributions elsewhere (e.g., CMU and Meta both appear on ThoughtComm but have separate independent work).

### Diagram Maintenance

When creating or updating pages with architecture pipelines, data flows, or relationship graphs:

1. Use **Mermaid** code blocks (` ```mermaid `) — these render natively in Obsidian with no plugins.
2. Use `graph LR` for pipelines/flows, `graph TD` for hierarchies/convergence diagrams.
3. Use `subgraph` with `style` directives for color-coded groupings. Standard palette:
   - Blue (`fill:#dae8fc,stroke:#6c8ebf`) — input/processing stages
   - Yellow (`fill:#fff2cc,stroke:#d6b656`) — alignment/intermediate
   - Green (`fill:#d5e8d4,stroke:#82b366`) — output/shallow/compatible
   - Orange (`fill:#ffe6cc,stroke:#d79b00`) — KV-cache level
   - Red (`fill:#f8cecc,stroke:#b85450`) — deep/restrictive
   - Purple (`fill:#e1d5e7,stroke:#9673a6`) — unified/output
4. Do NOT use Draw.io/`.drawio` files — they require manual editor interaction and don't embed inline.
5. **Line breaks in node labels**: Use `<br>` (not `\n`). Obsidian's Mermaid renderer treats `\n` as literal text. Example: `["Line one<br>Line two"]`.
6. **Math notation in diagrams**: Mermaid does not support LaTeX. Do NOT put math expressions (`H_t`, `\hat{Z}`, subscripts, superscripts) in node labels — they render as ugly plaintext. Instead, use the **side-by-side notation pattern**:
   - Wrap the Mermaid block in a `> [!diagram|left]` callout with plain-English labels.
   - Place a `> [!notation|right]` callout next to it containing a table mapping labels to rendered LaTeX.
   - The `side-by-side.css` snippet in `.obsidian/snippets/` enables this layout.
   - Example:
     ```markdown
     > [!diagram|left]
     > ```mermaid
     > graph TD
     >     H["Agent hidden states"] --> AE["Autoencoder"]
     > ```

     > [!notation|right]
     > | Step | Notation |
     > |---|---|
     > | Hidden states | $H_t$ |
     > | Autoencoder | $\hat{f}^{-1}(H_t)$ |
     ```
   - Only add the notation table when the diagram contains steps with formal math. Diagrams with purely descriptive labels (e.g., workflow diagrams) do not need it.
7. When converting existing ASCII art (` ``` ` code blocks with arrows like `→`, `──►`, `▼`), replace the entire code block with a ` ```mermaid ` block preserving all labels and annotations.
8. **When to create diagrams**:
   - **Source pages** describing multi-stage pipelines or architectures (e.g., Vision Wormhole's 4-stage pipeline, LatentMAS's agent flow, Coconut's thought loop).
   - **Concept pages** with taxonomies, spectra, or classification frameworks (e.g., the communication depth spectrum).
   - **Analysis pages** showing paper lineage/influence trees or method comparison flows.
   - **MOC pages** that would benefit from a visual overview of the reading path structure.
   - Rule of thumb: if a page describes a flow with 3+ stages or a hierarchy with 3+ branches, add a Mermaid diagram.

### Math Notation

All mathematical expressions must use LaTeX delimiters for proper rendering:

1. **Inline math**: Wrap in `$...$` (e.g., `$H_i \in \R^{T \times d_i}$`)
2. **Display math**: Wrap in `$$...$$` on their own lines for standalone equations.
3. **Do NOT use** raw Unicode math symbols (∈, ℝ, ≈) or plaintext subscripts (`h_T`, `W^T`) outside of `$...$` delimiters — they won't render.
4. Unicode arrows (→, ←) in **prose** are fine; only wrap them in LaTeX when inside mathematical expressions.
5. **Use preamble macros** defined in `.obsidian/plugins/obsidian-latex/preamble.sty`:
   - `\R` for `\mathbb{R}`, `\N` for `\mathbb{N}`, `\Z` for `\mathbb{Z}`
   - `\E` for `\mathbb{E}`, `\Loss` for `\mathcal{L}`, `\M` for `\mathcal{M}`
6. Percentage numbers, benchmark scores, and speedup factors (e.g., "95.4%", "3.8×") stay as plain text.

### Pandoc Export Readiness

All pages must include a `title:` field in YAML frontmatter for clean PDF/DOCX export via the Pandoc plugin. Source pages already require `title:`; concept, entity, analysis, MOC, and overview pages must also include it:

```yaml
---
type: concept
title: "Human-Readable Title"
created: "YYYY-MM-DD"
---
```

### Preamble & Macro Management

The MathJax preamble at `.obsidian/plugins/obsidian-latex/preamble.sty` defines shared LaTeX macros. When maintaining it:

1. **Adding a new macro**: If a `\mathbb{}`, `\mathcal{}`, or other verbose LaTeX command appears 10+ times across the wiki, add a short macro to the preamble and refactor all occurrences.
2. **Refactoring**: Use `replace_all: true` per file. Only replace inside `$...$` or `$$...$$` math contexts.
3. **Current macros**: `\R`, `\N`, `\Z`, `\E`, `\Loss`, `\M`. Update this list when adding new ones.
4. **Do NOT** put macros in the preamble that are used fewer than 10 times — the cognitive overhead of remembering the shorthand outweighs the savings.

### Workflow Index

These files are authoritative. Keep this list in sync when adding, renaming, or removing workflows.

- `workflows/create/ingest.md` - Add a new source and propagate the resulting updates across source pages, entities, concepts, indexes, MOCs, raw assets, and logs.
- `workflows/audit/gap-analysis.md` - Identify a gap from existing analyses, procure a paper from arXiv via the MCP, conditionally ingest it, and trigger downstream workflows. The proactive counterpart to `ingest.md`.
- `workflows/query/query.md` - Answer a user question from the wiki with targeted reading and `[[wiki-links]]` citations.
- `workflows/audit/lint.md` - Run a health check for content integrity, structural drift, stale paths, and missing cross-references.
- `workflows/create/batch-ingest.md` - Ingest 3+ sources in parallel, then consolidate shared files and run verification.
- `workflows/audit/moc-gap-analysis.md` - Audit MOC coverage, propose new MOCs, and coordinate creation without shared-file conflicts.
- `workflows/audit/verification.md` - Quality-check parallel subagent output for structure, accuracy, overstatement, and missing coverage before merge.
- `workflows/enrich/enrich.md` - Improve navigation, backlinks, asset linking, index sync, and discoverability without adding new substantive content.
- `workflows/enrich/expand.md` - Deepen thin source, concept, and entity pages to meet the depth standard.
- `workflows/create/synthesize.md` - Create cross-cutting analysis pages that connect multiple sources and concepts.
- `workflows/audit/review.md` - Run a full wiki once-over that combines lint, enrich, depth checks, and schema consistency review.
- `workflows/audit/enrichment-audit.md` - Systematically find, prioritize, and execute enrichment workstreams across the wiki in parallel.
- `workflows/audit/plugin-audit.md` - Audit Obsidian plugin configuration and page compliance for math, diagrams, frontmatter, and export readiness.
- `workflows/meta/readme-github-maintenance.md` - Update `README.md` and GitHub-facing project metadata when the vault structure or published surface changes.
- `workflows/audit/schema-self-audit.md` - Verify that `AGENTS.md` still matches the real vault layout, MOC inventory, workflow paths, and frontmatter usage.

## Depth Standard

All pages — source summaries, concept pages, entity pages — must be written with **deep technical analysis** as the default. This means:

- **Source summaries**: Not just "what the paper says" but detailed mechanism descriptions, mathematical intuitions, concrete experimental numbers, ablation insights, limitations analysis, and connections to the broader wiki. Typical length: 500-1500 words.
- **Concept pages**: Must include theoretical foundations, detailed mechanism explanations, taxonomies/spectra where applicable, quantitative evidence from sources, comparison tables, trade-off analyses, connections to adjacent concepts, and open questions. Typical length: 800-2000+ words.
- **Entity pages**: Accumulate detailed claims with citations, track evolving roles across sources, note contradictions or developments. Include a contribution timeline table (date/paper/role/result), collaboration network with cross-links to other entity pages, research trajectory analysis, and key researcher profiles with roles and cross-paper appearances. Typical length: 300-600 words.

The goal is that someone reading only the wiki (without the raw sources) gets a thorough, technically precise understanding — not just a surface summary. Every concept should be explained well enough that a knowledgeable reader could reconstruct the key ideas and evaluate the claims.

When creating stub pages for concepts not yet covered by an ingested source, include as much structural depth as possible from domain knowledge and connections to existing pages, clearly marking what will be expanded upon future ingests.

## Formatting Rules

- Write in clear, concise prose. No filler.
- Use headers (##, ###) to organize sections within pages.
- Use bullet points for lists of claims or facts; each bullet should cite its source.
- Bold key terms on first mention within a page.
- Tables for structured comparisons.

## File Naming

- Lowercase, hyphenated. The folder provides the type — **do not add type prefixes** to filenames.
- Source summaries: `wiki/sources/<theme>/short-title.md` (e.g., `wiki/sources/reasoning/coconut-reasoning-latent-space.md`).
- Concepts: `wiki/concepts/<theme>/descriptive-name.md`, where `<theme>` is one of `communication/`, `reasoning/`, `theory/`, `multi-agent/`, or `challenges/` (e.g., `wiki/concepts/reasoning/latent-space-reasoning.md`). Cross-cutting fragments live under `wiki/concepts/_partials/`.
- Entities: `wiki/entities/institution-name.md` (e.g., `wiki/entities/harvard.md`).
- Analyses: `wiki/analyses/topic.md` (e.g., `wiki/analyses/open-questions.md`).
- MOCs: `wiki/mocs/theme-name.md` (e.g., `wiki/mocs/latent-reasoning.md`).

## Log Format

Each entry in `wiki/log.md` follows this format for parseability:
```
## [YYYY-MM-DD] action | Title
Brief description of what was done. Pages created/updated listed.
```

Actions: `ingest`, `batch-ingest`, `query`, `analysis`, `lint`, `update`, `review`, `enrich`, `expand`, `verify`, `moc-gap`, `enrichment-audit`, `plugin-audit`, `schema-audit`, `readme-update`.
