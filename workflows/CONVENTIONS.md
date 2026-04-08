---
type: workflow-doc
title: "Wiki Conventions"
created: "2026-04-08"
updated: "2026-04-08"
tags: [workflow, conventions, reference]
---

# Wiki Conventions

Canonical conventions for recurring structural elements across the wiki. When files drift from these conventions, run the normalization pass described in each section.

## Entity Contribution Timeline: Role vocabulary

Every file in `wiki/entities/` has a Contribution Timeline table with a `Role` column describing the entity's relationship to the paper. The canonical vocabulary is:

- **Lead** — The entity is the single institutional home of the paper's lead (first) author, and the paper is not a formal consortium. Use when the paper has one clear lead institution.
- **Co-lead** — Shared first authorship or co-lead institutional credit across two or more entities. Always annotate with the partner(s) in parentheses, e.g. `Co-lead (with CMU, MBZUAI)`.
- **Lead (multi-institution)** — The entity is the lead on a consortium paper with three or more institutional affiliations where this entity owns the direction but the work is explicitly multi-institutional. Annotate partners in parentheses where useful.
- **Contribution** — The entity is a co-author on the paper but not a lead. Use when the entity appears in the author list without first-author or lead-institution status.
- **Sole institution** — The entity is the only institutional affiliation on the paper. This extension exists for single-institution entities (e.g. Monash) where the `Lead` label would be ambiguous with "lead among several".

### Annotation format

- For `Co-lead` and `Lead (multi-institution)`, prefer listing partner entities in parentheses immediately after the role: `Co-lead (with Google Research)`, `Lead (multi-institution) (with CMU, Contextual AI, Georgia Tech)`. When the parenthetical would duplicate the multi-institution marker, collapse to a single parenthetical: `Lead (with CMU, Contextual AI, Georgia Tech)` is acceptable shorthand for `Lead (multi-institution)` when the partners are listed.

### Extending the vocabulary

If a new Role value is needed, add it here with a precise definition before using it in entity files. Do not introduce ad-hoc variants (e.g. `UIUC lead`, `Lead author`) in entity tables — normalize to the canonical set above.
