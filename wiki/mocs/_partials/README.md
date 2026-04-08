---
type: workflow-doc
title: "MOC Partials"
created: "2026-04-08"
updated: "2026-04-08"
---

This folder holds **content fragments that are embedded into multiple MOCs** via Obsidian transclusion (`![[partial-name]]`). They are the cross-cutting analogue to per-source partials at `wiki/sources/<slug>/<partial>.md` and per-entity partials at `wiki/entities/<slug>/<partial>.md`.

A **moc-partial** is appropriate when the same table, list, or fragment would otherwise be hand-copied into two or more MOCs *and* it cannot be naturally owned by any single source or entity. Single-MOC content stays inline in its MOC; single-source content is a `source-partial`; single-entity content is an `entity-partial`.

## Conventions

- Each partial carries lightweight frontmatter (`type: moc-partial`, `partial: <slug>`, `created`, `updated`). No `parent` field — moc-partials are explicitly cross-cutting and not owned by a single MOC.
- No H1 in the partial body — the embedding MOC supplies the surrounding heading.
- Filename = the embed target. `![[compatibility-spectrum]]` resolves to `compatibility-spectrum.md` from anywhere in the vault, since basenames are unique inside `_partials/`.
- Wikilinks inside partials use plain `[[basename]]` form (Obsidian resolves regardless of the embedding MOC's location).
- One concept per file. If a partial grows beyond ~30 lines, it probably wants to become its own first-class page.
- The leading underscore on the folder name keeps it sorted to the top of the MOC directory and signals "fragments, not pages" to humans and tooling.

## Current partials

- [`compatibility-spectrum.md`](compatibility-spectrum.md) — cross-architecture support table for 9 communication methods. Embedded by [`cross-architecture.md`](../cross-architecture.md). Eligible to be embedded by `latent-communication.md` and `communication-depth-spectrum.md` once those MOCs are next refactored.
- [`compression-ratios.md`](compression-ratios.md) — compression-ratio comparison for 4 systems with task-dependence column. Embedded by [`compression-information-theory.md`](../compression-information-theory.md).

## When to extract a fragment as a moc-partial

Rule of thumb: **if you're about to copy-paste the same table into a second MOC, extract it instead.**

Extract:

- Cross-method comparison tables that aggregate data from multiple sources (e.g. compatibility spectrum, compression ratios, decision guides).
- Lists of methods grouped by an axis that cuts across categories.
- Fragments that already exist verbatim in 2+ MOCs.

Leave inline:

- Tables specific to a single MOC's narrative.
- Source-specific content (use a `source-partial` instead).
- Entity-specific content (use an `entity-partial` instead).

## Relationship to other partial types

| Type             | Lives in                               | Owned by        | Used for                                                                        |
| ---------------- | -------------------------------------- | --------------- | ------------------------------------------------------------------------------- |
| `source-partial` | `wiki/sources/.../<slug>/<partial>.md` | One source page | Reusable atoms from a single paper (e.g. `one-liner.md`)                        |
| `entity-partial` | `wiki/entities/<slug>/<partial>.md`    | One entity page | Reusable structured data per institution (e.g. `timeline.md`, `researchers.md`) |
| `moc-partial`    | `wiki/mocs/_partials/<partial>.md`     | No single owner | Cross-cutting fragments aggregating data from multiple sources or entities      |

The three patterns are documented in their respective procedure files under `workflows/_shared/procedures/`.
