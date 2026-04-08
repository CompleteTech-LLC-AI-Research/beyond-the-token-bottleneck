# Entity Partials

## Purpose

Entity pages in `wiki/entities/` accumulate two kinds of structured data that other pages want to reuse: the **Contribution Timeline** table (who did what, when) and the **Key Researchers** list. When each entity was a single monolithic file, MOCs and analyses could not embed these sections — they had to re-type paper lists or link to `[[entity#Contribution Timeline]]` anchors that only partially render. Every ingest that added a paper required hand-editing every page that duplicated the entity's timeline or researcher list.

This procedure defines a **per-entity subdirectory** layout that splits each entity into a narrative shell plus reusable partials, so MOCs, analyses, and the parent entity file can all embed the same timeline table and researcher list via Obsidian's `![[file]]` transclusion syntax. When a paper is added, only the partial changes, and every consumer updates automatically.

## Directory structure

Each entity owns a directory named after its slug, with the narrative shell at the top level and the partials inside the subdirectory:

```
wiki/entities/
├── <slug>.md                # Narrative shell: intro, themes, collaboration, strategy, trajectory
├── <slug>/
│   ├── timeline.md          # Contribution Timeline table (frontmatter + table only)
│   └── researchers.md       # Key Researchers list (frontmatter + list only)
```

For example, the `amazon` entity lives at `wiki/entities/amazon.md` (shell) with partials at `wiki/entities/amazon/timeline.md` and `wiki/entities/amazon/researchers.md`. The shell keeps the `## Contribution Timeline` and `## Key Researchers` headings so the file's outline is unchanged; immediately below each heading sits a transclusion embed.

## Transclusion syntax

The shell file embeds each partial with Obsidian's native embed syntax:

```markdown
## Contribution Timeline

![[<slug>/timeline]]

## Key Researchers

![[<slug>/researchers]]
```

MOCs and analyses that want to reuse a timeline or researcher list embed the same way — `![[amazon/timeline]]`, `![[cmu/researchers]]`, etc. Obsidian resolves the relative path against the vault root, so `![[amazon/timeline]]` works from any file in the vault. Do **not** include the `.md` extension in the embed target; Obsidian appends it automatically.

Inline wiki-links that target the legacy section headings (e.g., `[[amazon#Contribution Timeline]]`) continue to work because the shell file still carries those headings — the embed sits under the heading rather than replacing it.

## Partial frontmatter

Partial files carry a lighter frontmatter than full entity pages. They are not standalone pages and should not be catalogued like one; the `type: entity-partial` field signals this to any tooling that walks the vault. The required fields are:

```yaml
---
type: entity-partial
parent: <slug>
partial: timeline        # or: researchers
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
---
```

- `type: entity-partial` — distinguishes the file from first-class page types (`entity`, `concept`, `source`, `analysis`, `overview`, `index`).
- `parent: <slug>` — the slug of the entity shell file the partial belongs to. Must match the subdirectory name.
- `partial: timeline` or `partial: researchers` — which of the two partial roles this file fills. Future partial types (e.g., `publications`, `awards`) can extend this enum.
- `created` / `updated` — same "substantive content change" rule as other page types.

Partials do **not** carry `title:`, `tags:`, or `aliases:`. The parent shell file owns those fields for the entity as a whole.

## When to extract a section as a partial

Rule of thumb: **if MOCs or analyses will reference the section, extract it; if it is narrative-only, leave it inline in the shell.**

Extract as a partial:
- Contribution Timeline tables (paper list, always reused by `paper-timeline.md` and thematic MOCs).
- Key Researchers lists (person list, reused by collaboration-network analyses).
- Any other structured table or list that 2+ other pages already duplicate by hand.

Leave inline in the shell:
- Narrative Research Themes prose.
- Collaboration Network paragraphs (unless they harden into a structured table).
- Strategic Position / Research Trajectory analyses.
- Why This Entity Matters closers.

If you find yourself copy-pasting a section from an entity file into an MOC or analysis, that is the signal to promote it to a partial.

## Adding a new entity under this convention

When a new paper introduces a previously uncovered institution:

1. Create `wiki/entities/<slug>.md` as the narrative shell with full entity frontmatter (`type: entity`, `title`, `aliases`, `tags`, `created`, `updated`). Write the intro, research themes, collaboration network, strategic position, research trajectory, and closing sections inline.
2. Create `wiki/entities/<slug>/timeline.md` with the partial frontmatter (`type: entity-partial`, `parent: <slug>`, `partial: timeline`) and the Contribution Timeline table underneath.
3. Create `wiki/entities/<slug>/researchers.md` with the partial frontmatter (`partial: researchers`) and the Key Researchers list underneath.
4. In the shell, under `## Contribution Timeline` insert `![[<slug>/timeline]]`. Under `## Key Researchers` insert `![[<slug>/researchers]]`.
5. Add the entity to `wiki/index.md`'s Entities section and bump the `entities/` count in the directory tree.
6. Run `workflows/_shared/procedures/stale-count-sweep.md` — the new subdirectory changes counts that appear in `wiki/index.md` and `README.md`.

Future ingests that add a paper to an existing entity edit only `wiki/entities/<slug>/timeline.md` (and possibly `researchers.md`); the shell and every consumer (MOCs, analyses) update automatically via transclusion.

## Invariants

- The parent shell file retains `## Contribution Timeline` and `## Key Researchers` as headings even after extraction, so `[[<slug>#Contribution Timeline]]` and `[[<slug>#Key Researchers]]` anchor links keep working.
- Partial files always carry `type: entity-partial` frontmatter. A file under `wiki/entities/<slug>/` without this frontmatter is either a mistake or a new partial type that needs to be documented here first.
- Never flatten a partial back into the shell file "because it is short" — the partial boundary is what makes reuse possible, and the cost of the frontmatter is negligible.
- Never extract narrative prose into a partial. Partials are structured data (tables, lists); narrative stays in the shell where it can be edited in context.
- The partial subdirectory name must exactly equal the shell file's basename (minus `.md`). `wiki/entities/amazon.md` ↔ `wiki/entities/amazon/`.

## After completion

Return to the calling workflow and proceed with its next numbered step. This fragment is a subroutine — it has no terminal action of its own, and the calling workflow's remaining steps (index update, MOC update, raw asset sync, log entry, commit, report) are not optional just because the entity partial has been created or updated.

## Used by

- `workflows/create/ingest.md` — when an ingest introduces a new entity or adds a paper to an existing entity's timeline.
