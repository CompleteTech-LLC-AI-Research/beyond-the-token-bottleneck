# Source Partials

## Purpose

Source pages in `wiki/sources/` accumulate short, reusable fragments that MOCs and analyses want to embed verbatim — most notably the **one-liner** synthesis (a 1–3 sentence "what is this paper" framing that names the method, the mechanism, and the key constraint or headline result). When each source was a single monolithic file, MOCs that wanted this fragment had to either re-type it (introducing drift) or anchor-link to a `## One-liner` heading (fragile if the heading is renamed). Every cross-MOC refactor required tracking down each duplicated paragraph by hand.

This procedure defines a **per-source subdirectory** layout that splits each source into a narrative shell plus reusable partials, so MOCs and analyses can embed the same fragment via Obsidian's `![[file]]` transclusion syntax. When a paper's one-liner needs sharpening, only the partial changes, and every consumer updates automatically.

It mirrors the entity-partials pattern in [`entity-partials.md`](entity-partials.md) — read that first for the broader rationale.

## Directory structure

Each source owns a directory named after its slug, with the narrative shell at the top level and the partials inside the subdirectory:

```
wiki/sources/<category>/
├── <slug>.md                # Narrative shell: summary, mechanism, results, etc.
├── <slug>/
│   └── one-liner.md         # 1–3 sentence synthesis (frontmatter + body)
```

For example, the CIPHER source page lives at `wiki/sources/communication/embeddings/cipher-multiagent-debate-embeddings.md` (shell) with its one-liner partial at `wiki/sources/communication/embeddings/cipher-multiagent-debate-embeddings/one-liner.md`. The shell keeps the `## One-liner` heading so the file's outline is unchanged; immediately below the heading sits a transclusion embed.

The subdirectory may also hold future partial types (e.g. `key-results.md`, `timeline-entry.md`) as the convention extends.

## Transclusion syntax

The shell file embeds its one-liner with Obsidian's native embed syntax:

```markdown
## One-liner

![[<slug>/one-liner]]

## Summary
```

MOCs and analyses that want to reuse a one-liner embed the same way — `![[cipher-multiagent-debate-embeddings/one-liner]]`, `![[coconut-reasoning-latent-space/one-liner]]`, etc. Obsidian resolves the relative path against the vault root, so the embed works from any file in the vault. Do **not** include the `.md` extension in the embed target; Obsidian appends it automatically.

Inline wiki-links that target the legacy section heading (e.g. `[[cipher-multiagent-debate-embeddings#One-liner]]`) continue to work because the shell file still carries the heading — the embed sits under the heading rather than replacing it.

## Partial frontmatter

Partial files carry a lighter frontmatter than full source pages. They are not standalone pages and should not be catalogued like one; the `type: source-partial` field signals this to any tooling that walks the vault. The required fields are:

```yaml
---
type: source-partial
parent: <slug>
partial: one-liner       # current vocabulary; extend deliberately (see below)
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
---
```

- `type: source-partial` — distinguishes the file from first-class page types (`source`, `entity`, `concept`, `analysis`, `overview`, `index`).
- `parent: <slug>` — the slug of the source shell file the partial belongs to. Must match the subdirectory name.
- `partial: one-liner` — which partial role this file fills. Future partial types (e.g., `key-results`, `headline-figure`) can extend this enum, but each new value must be added here with a precise definition before being used in source files.
- `created` / `updated` — same "substantive content change" rule as other page types.

Partials do **not** carry `title:`, `tags:`, or `aliases:`. The parent shell file owns those fields for the source as a whole.

## When to extract a section as a partial

Rule of thumb: **if MOCs or analyses will reference the section verbatim, extract it; if it is narrative-only or only consumed once, leave it inline in the shell.**

Extract as a partial:

- The **one-liner**: a 1–3 sentence framing of the paper that MOCs use to introduce it. Always extract — this is the canonical reusable atom.
- Future structured atoms (e.g. headline numerical results, a single canonical figure caption) that 2+ MOCs already duplicate by hand.

Leave inline in the shell:

- Long-form Summary, Mechanism, Results sections.
- Diagrams and walkthroughs.
- Discussion and limitations narrative.
- Anything specific to a single MOC's framing — that belongs in the MOC.

If you find yourself copy-pasting a paragraph from a source file into an MOC, that is the signal to promote it to a partial.

## Writing a one-liner

A good one-liner has a consistent shape: **bold method name + one-sentence mechanism + one sentence on the key constraint or headline result**. Aim for 1–3 sentences total. The audience is a reader scanning a MOC who wants to know "what is this paper, in one breath."

Examples (current corpus):

- "**CIPHER** replaces sampled tokens with the softmax-weighted average of vocabulary embeddings — a 'soft token' that preserves the full distributional belief. Stays inside the vocabulary's convex hull so no architecture changes are needed; requires a shared tokenizer."
- "**Coconut** (Chain of Continuous Thought) feeds the model's last hidden state directly back as the next 'input embedding' instead of sampling a token, letting the model reason in continuous space. Achieves 97% on ProsQA via emergent BFS-via-superposition — capabilities discrete CoT cannot replicate at the same model depth — but its curriculum training causes catastrophic forgetting on instruction-tuned models."

Anti-patterns:

- More than ~4 sentences (it has stopped being a one-liner).
- No name or no mechanism (the reader can't tell what it is).
- Listing every result (that's what the Summary section is for).
- Editorializing about the paper's importance (let the reader judge).

## Adding a new source under this convention

When a new paper is ingested:

1. Create `wiki/sources/<category>/<slug>.md` as the narrative shell with full source frontmatter (`type: source`, `title`, `author`, `arxiv`, `tags`, `created`, etc.). Write the Summary, Mechanism, Results, and any other narrative sections inline.
2. Create `wiki/sources/<category>/<slug>/one-liner.md` with the partial frontmatter (`type: source-partial`, `parent: <slug>`, `partial: one-liner`) and the one-liner body underneath.
3. In the shell, add `## One-liner` as a heading between the H1 and `## Summary`, with `![[<slug>/one-liner]]` underneath.
4. Add the source page to any relevant MOC reading paths. If the new paper takes a slot in a comparison table that lives as a `moc-partial`, update the partial too.
5. Run `workflows/_shared/procedures/stale-count-sweep.md` if the new subdirectory changes any counts that appear in `wiki/index.md` or `README.md`.

Future revisions of a one-liner edit only the partial; the shell and every MOC consumer update automatically via transclusion.

## Invariants

- The parent shell file retains `## One-liner` as a heading even after extraction, so `[[<slug>#One-liner]]` anchor links keep working.
- Partial files always carry `type: source-partial` frontmatter. A file under `wiki/sources/.../<slug>/` without this frontmatter is either a mistake or a new partial type that needs to be documented here first.
- Never flatten a partial back into the shell file "because it is short" — the partial boundary is what makes reuse possible, and the cost of the frontmatter is negligible.
- Never extract narrative prose into a partial. Partials are short, structured, reusable atoms; long-form analysis stays in the shell where it can be edited in context.
- The partial subdirectory name must exactly equal the shell file's basename (minus `.md`). `wiki/sources/.../cipher-multiagent-debate-embeddings.md` ↔ `wiki/sources/.../cipher-multiagent-debate-embeddings/`.
- Partial slugs are lowercase-hyphenated (`one-liner`, not `OneLiner` or `one_liner`), matching the convention used by `entity-partial` files.

## Used by

- `workflows/create/ingest.md` — when an ingest creates a new source page, the one-liner partial is created in the same step.
- `workflows/audit/lint.md` — should check that every `wiki/sources/**/*.md` source shell has a matching `<slug>/one-liner.md` partial and a `## One-liner` heading with the embed underneath.

## Relationship to other partial types

This procedure defines `source-partial`. The vault has two other partial types with parallel conventions:

- `entity-partial` — see [`entity-partials.md`](entity-partials.md). Per-entity timeline and researcher lists.
- `moc-partial` — cross-cutting fragments that aggregate data from multiple sources or entities, living at `wiki/mocs/_partials/`. See [`wiki/mocs/_partials/README.md`](../../../wiki/mocs/_partials/README.md).
