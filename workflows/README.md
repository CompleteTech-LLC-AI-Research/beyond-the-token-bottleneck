# Workflows

## Overview

This directory contains workflows for maintaining the research wiki. Each workflow is a self-contained procedure triggered by specific user intents. Reusable fragments live in `_shared/`. Pick the workflow whose "use when" line best matches the current task; when in doubt, consult the disambiguation tips below.

## Decision tree

Workflows are grouped by phase. Use the phase that matches the user's intent, then pick the specific workflow.

### Create — introduce new content

| Workflow | Use when... |
| --- | --- |
| [ingest](ingest.md) | Onboarding 1-2 new source papers into the wiki and propagating them through indexes, MOCs, and logs. |
| [batch-ingest](batch-ingest.md) | Onboarding 3+ sources in one session via parallel subagents, then consolidating shared files. |
| [synthesize](synthesize.md) | Building a cross-cutting analysis page (comparison, timeline, contradictions, frontier) from existing sources. |

### Enrich — deepen existing content

| Workflow | Use when... |
| --- | --- |
| [enrich](enrich.md) | Structural improvement pass: MOC coverage, backlinks, raw-asset wiring, index sync — no new substantive content. |
| [expand](expand.md) | Deepening specific thin pages with more mechanism detail, evidence, comparisons, or entity timelines. |

### Audit — check integrity

| Workflow | Use when... |
| --- | --- |
| [lint](lint.md) | Targeted health check for contradictions, orphans, red links, stale claims, and file-placement drift. |
| [review](review.md) | Comprehensive once-over combining lint + enrich + expand checks, usually after large ingests. |
| [verification](verification.md) | QA pass on output from parallel subagents before their changes merge into shared files. |
| [gap-analysis](gap-analysis.md) | Finding a research coverage gap, then procuring an arXiv paper to fill it and ingesting it. |
| [moc-gap-analysis](moc-gap-analysis.md) | Deciding whether the wiki needs new MOCs because themes have grown beyond the 5-page threshold. |
| [enrichment-audit](enrichment-audit.md) | Vault-wide page-depth, link-density, and missing-analysis audit with prioritized parallel fixes. |
| [schema-self-audit](schema-self-audit.md) | Verifying `AGENTS.md` still matches the real vault layout, MOC inventory, workflow paths, and frontmatter fields. |
| [plugin-audit](plugin-audit.md) | Checking Obsidian plugin configuration and plugin-compatibility of pages (LaTeX, Pandoc, diagrams). |

### Query — answer questions

| Workflow | Use when... |
| --- | --- |
| [query](query.md) | Answering a user question by reading the minimum necessary pages and citing them with wiki-links. |

### Meta — maintain the repo itself

| Workflow | Use when... |
| --- | --- |
| [readme-github-maintenance](readme-github-maintenance.md) | Syncing the public `README.md`, badges, paper counts, and entry-points table with vault changes. |

## Disambiguation tips

A few pairs of workflows overlap in scope. Use these rules to pick the right one.

**[ingest](ingest.md) vs [batch-ingest](batch-ingest.md)**
- 1-2 papers, sequential work, single-threaded propagation → `ingest`.
- 3+ papers, parallelizable by paper or theme, consolidate shared files at the end → `batch-ingest`.
- `batch-ingest` internally delegates per-paper work to the `ingest` workflow.

**[lint](lint.md) vs [review](review.md)**
- `lint` is a targeted integrity sweep: contradictions, orphans, red links, stale claims, placement.
- `review` is the broader periodic pass that bundles lint plus enrich and expand checks, frontmatter and source-material verification, and MOC coverage. Use after big batch ingests or for scheduled maintenance.

**[gap-analysis](gap-analysis.md) vs [moc-gap-analysis](moc-gap-analysis.md) vs [enrichment-audit](enrichment-audit.md)**
These three all look for "what's missing", but at different layers:
- `gap-analysis` — missing **research coverage**. Finds holes in the literature the wiki covers, then procures a new paper from arXiv to fill the hole and ingests it. Proactive counterpart to `ingest`.
- `moc-gap-analysis` — missing **navigation**. Checks whether existing pages cluster into themes that deserve a new MOC (5+ pages per theme). Does not add new content.
- `enrichment-audit` — missing **depth and links** on existing pages. Flags thin pages, broken/absent wiki-links, and missing analyses, then dispatches parallel enrich/expand agents to fix them.

Rule of thumb: new paper needed → `gap-analysis`; new reading path needed → `moc-gap-analysis`; existing pages too thin or under-linked → `enrichment-audit`.

## Conventions

All workflows follow the structure and terminology in `CONVENTIONS.md`. Reusable procedures, checklists, and rules live under `_shared/`.
