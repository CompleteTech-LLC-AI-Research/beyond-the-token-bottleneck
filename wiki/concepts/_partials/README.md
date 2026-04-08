---
type: workflow-doc
title: "Concept Partials"
created: "2026-04-08"
updated: "2026-04-08"
---

This folder holds **content fragments that are embedded into multiple concept notes** via Obsidian transclusion (`![[partial-name]]`). They are the **concept-partial** member of the wiki's partials family, alongside `source-partial` (per-paper atoms at `wiki/sources/<slug>/<partial>.md`), `entity-partial` (per-institution atoms at `wiki/entities/<slug>/<partial>.md`), and `moc-partial` (cross-cutting MOC fragments at [`wiki/mocs/_partials/`](../../mocs/_partials/README.md)).

A **concept-partial** is appropriate when the same conceptual framing would otherwise be hand-copied into two or more concept notes *and* it cannot be naturally owned by any single source, entity, or MOC. Single-concept content stays inline in its concept note; single-source content is a `source-partial`; single-entity content is an `entity-partial`; cross-MOC tables are a `moc-partial`.

## Conventions

- Each partial carries lightweight frontmatter (`type: concept-partial`, `partial: <slug>`, `created`, `updated`). No `parent` field — concept-partials are explicitly cross-cutting and not owned by a single concept note.
- No H1 in the partial body — the embedding concept supplies the surrounding heading.
- Filename = the embed target. `![[depth-spectrum]]` resolves to `depth-spectrum.md` from anywhere in the vault, since basenames are unique inside `_partials/`.
- Wikilinks inside partials use plain `[[basename]]` form (Obsidian resolves regardless of the embedding concept's location).
- One framing per file. If a partial grows beyond ~30 lines, it probably wants to be promoted to a first-class concept note.
- The leading underscore on the folder name keeps it sorted to the top of the concepts directory and signals "fragments, not pages" to humans and tooling.
- Every fragment ends with a `## Used by` footer listing the consuming concept notes as relative wikilinks. This is the bidirectional contract — workflows-style discipline (see [`workflows/_shared/README.md`](../../../workflows/_shared/README.md)) applied to wiki content so fragments cannot quietly orphan.

## Subdirectories

- `framings/` — recurring conceptual framings that span multiple concepts (e.g. depth spectrum, superposition, representation alignment). This is where most concept-partials land.
- `definitions/` — short canonical definitions reused across notes. Currently empty; populated as needed when a definition is cited verbatim in two or more concepts.

## Current partials

- [`framings/depth-spectrum.md`](framings/depth-spectrum.md) — the canonical 5-stage spine of latent communication (tokens → output embeddings → KV → activations → weights) plus the depth–compatibility trade-off. Embedded by [`activation-communication.md`](../activation-communication.md), [`embedding-space-communication.md`](../embedding-space-communication.md), and [`kv-cache-communication.md`](../kv-cache-communication.md).
- [`framings/superposition.md`](framings/superposition.md) — superposition as a structural property of continuous vector spaces (basis projection vs full vector space, KL cost-of-collapse, capacity vs exploitation). Embedded by [`continuous-vs-discrete-representation.md`](../continuous-vs-discrete-representation.md) and [`latent-space-reasoning.md`](../latent-space-reasoning.md).
- [`framings/representation-alignment.md`](framings/representation-alignment.md) — Platonic Representation Hypothesis + Relative Representations + linear relational embeddings as the enabling condition for the deep end of the depth spectrum. Embedded by [`activation-communication.md`](../activation-communication.md). Eligible to be embedded by `embedding-space-communication.md` and `kv-cache-communication.md` once those concepts are next refactored.
- [`framings/temperature-scaling-behavior.md`](framings/temperature-scaling-behavior.md) — diversity as a precondition for ensemble methods, the too-low / too-high / productive-middle pattern, temperature as a proxy for distributional coverage. Embedded by [`multiagent-debate.md`](../multiagent-debate.md) and [`temperature-diversity.md`](../temperature-diversity.md).

<!-- subagents: add entries here as fragments are created -->

## When to extract a fragment as a concept-partial

Rule of thumb: **if you're about to copy-paste the same framing paragraph into a second concept note, extract it instead.**

Extract:

- Recurring conceptual framings that appear verbatim or near-verbatim in 2+ concept notes (e.g. the depth spectrum framing used by multiple communication-method concepts).
- Cross-method comparison framings that situate several concepts on a shared axis.
- Foundational definitions cited by multiple concepts, where any drift in wording would be a wiki bug.

Leave inline:

- Framings specific to a single concept's narrative.
- Source-specific content (use a `source-partial` instead).
- Entity-specific content (use an `entity-partial` instead).
- Cross-MOC tables that aggregate data from multiple sources (use a `moc-partial` instead).

## Relationship to other partial types

| Type              | Lives in                               | Owned by        | Used for                                                                        |
| ----------------- | -------------------------------------- | --------------- | ------------------------------------------------------------------------------- |
| `source-partial`  | `wiki/sources/.../<slug>/<partial>.md` | One source page | Reusable atoms from a single paper (e.g. `one-liner.md`)                        |
| `entity-partial`  | `wiki/entities/<slug>/<partial>.md`    | One entity page | Reusable structured data per institution (e.g. `timeline.md`, `researchers.md`) |
| `moc-partial`     | `wiki/mocs/_partials/<partial>.md`     | No single owner | Cross-cutting fragments aggregating data from multiple sources or entities      |
| `concept-partial` | `wiki/concepts/_partials/<partial>.md` | No single owner | Recurring conceptual framings reused across multiple concept notes              |

The patterns are documented in their respective procedure files under `workflows/_shared/procedures/`.

## Why transclusion (and the contrast with workflows/_shared/)

The wiki's partials family — `source-partial`, `entity-partial`, `moc-partial`, and `concept-partial` — uses Obsidian `![[basename]]` transclusion so that edits to a fragment propagate to every consumer automatically, with no copy-paste drift and no manual sync commit. This is the wiki standard because the wiki is Obsidian-primary.

The sibling [`workflows/_shared/`](../../../workflows/_shared/README.md) directory instead references its fragments with plain markdown links. That is **not** a divergence from a wiki standard — it is the wiki standard applied to a different audience. Workflow files are also read directly on GitHub and by non-Obsidian agents, where `![[...]]` syntax silently renders as literal text. Plain links survive both renderers at the cost of the reader following a link instead of seeing the fragment inline. Both patterns enforce single-source-of-truth; they differ only in how the embed is materialized for the reader.
