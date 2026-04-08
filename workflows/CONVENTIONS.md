---
type: workflow-doc
title: "Workflow & Wiki Conventions"
created: "2026-04-08"
updated: "2026-04-08"
tags: [workflow, conventions, reference]
---

# Workflow & Wiki Conventions

## Purpose

This document defines the structural and terminological conventions that all files in `workflows/` must follow, plus the canonical vocabularies used by recurring structural elements elsewhere in the wiki (currently: entity Contribution Timeline roles). Workflows that drift from this template should be flagged by the lint workflow; wiki files that drift from the vocabularies in the trailing sections should be normalized in their respective audit passes.

## Standard workflow structure

Every workflow file MUST use the following heading order. Sections marked optional may be omitted only with explicit justification in a comment; all others are mandatory.

1. `# <Workflow Name>` — H1 title, human-readable (e.g. `# Ingest Workflow`, `# Lint (Health Check)`). Exactly one per file.
2. *(optional)* **Mermaid diagram** — a `graph TD` or phase-subgraph block placed immediately after the H1. Required for any workflow with more than six procedure steps; encouraged otherwise.
3. `## Purpose` — one to three sentences stating what the workflow does and what outcome it produces. No procedure details here.
4. `## When To Use` — one or two paragraphs (or a short bullet list) describing the scope where this workflow is the right tool. Answers "given a task, should I pick this workflow?"
5. `## Trigger Phrases` — bullet list of literal user phrases that should invoke the workflow (e.g. `` `lint` ``, `` `ingest a paper` ``). Use inline-code ticks for each phrase.
6. `## Do Not Use When` — bullet list of scenarios that belong to a *different* workflow. Every bullet MUST cross-reference the correct workflow by relative path (e.g. `` Use `workflows/query.md`. ``).
7. `## Required Context` — bullet list of files, MCPs, or pieces of information the workflow depends on before the procedure can start.
8. `## Procedure` — the executable body. Use a single numbered list when there are six or fewer steps; use `### Phase N: <Name>` subheadings with numbered steps inside each phase when the workflow has more than six steps or more than one distinct stage.
9. `## Completion Checklist` — bullet list of post-conditions a reviewer (human or agent) can tick off to confirm the workflow finished cleanly. Each bullet should be independently verifiable.
10. `## Related Workflows` — three to four cross-references to adjacent workflows, no more. Keep it curated; longer lists become stale and dilute signal.

Optional trailing sections (such as `## Notes for Future Refinement`) may appear after `## Related Workflows` but must not displace any of the required sections above.

## Terminology glossary (seed)

Canonical names for concepts that have drifted across existing workflows. This seed will be expanded in PR 2's `_shared/glossary.md`.

| Canonical term | Deprecated / drift variants | Notes |
| --- | --- | --- |
| living analyses | gap-tracking analysis pages; analysis pages in `wiki/analyses/` | The six+ files under `wiki/analyses/` that must be checked on every ingest. `gap-analysis.md` uses "gap-tracking analysis pages"; `ingest.md` uses "living analysis". Prefer "living analyses". |
| source page | source summary page; source file page | A markdown page under `wiki/sources/**/` that summarizes a single paper. `ingest.md` mixes "source summary page" and "source page". Prefer "source page". |
| reading path | reading path outline; MOC reading path | The ordered traversal baked into a MOC. `ingest.md` uses "reading path"; older drafts used "reading path outline". Prefer "reading path". |
| coordinator-only files | shared files; off-limits for agents; do-not-touch files | Files that only the coordinator (human or orchestrator agent) may edit. Prefer "coordinator-only files"; avoid "shared" (ambiguous with `_shared/` fragments). |

## Meta-rules

- Never reference a file path without verifying it exists on disk. Phantom references propagate into indexes and break lint passes weeks later.
- Log entries in `wiki/log.md` are point-in-time records — never backdate, never rewrite, never sweep counts inside them.
- Workflow file changes go via feature branch + PR, never directly to `master` (see `ingest.md:123` and `gap-analysis.md` Phase 6).
- Mermaid node labels use `<br>` for line breaks, not `\n` (which renders literally in Obsidian).
- Fragment links use relative paths from the workflow file's location (e.g. `_shared/procedures/stale-count-sweep.md`, not `/workflows/_shared/...`).

## Fragment reference style

Workflows reference shared procedure fragments under `_shared/` with a standard markdown link, not an Obsidian transclude. Links render in every reader; transcludes only render in Obsidian, and these workflows are also read directly on GitHub and by non-Obsidian agents.

Example, as it should appear inside a numbered procedure step:

```
11. **Mandatory:** Run the [stale-count sweep](_shared/procedures/stale-count-sweep.md).
```

Do not use `![[...]]` transclude syntax for fragments. Do not inline the fragment body into the workflow; the whole point of `_shared/` is to keep one copy.

## Fragment chaining contract

Fragments under `_shared/procedures/` are subroutines, not standalone workflows. Both the caller (a workflow) and the callee (the fragment) must follow this contract so an agent executing step-by-step never loses its place across the boundary.

**Caller side — every fragment reference inside a numbered step MUST tell the agent to come back.** Use the explicit return-step phrasing:

```
11. **<Action label>:** Run the [<fragment name>](_shared/procedures/<file>.md) in full, then return here and continue with step 12. <Optional load-bearing invariant kept inline.>
```

The "then return here and continue with step N+1" tail is mandatory, not stylistic. When two fragment calls are adjacent (e.g., ingest.md steps 11→12), each call still gets its own explicit return cue — back-to-back fragments are the spot most likely to skip the next step (log append, commit) if an agent loses its stack.

Load-bearing invariants (rules whose violation breaks downstream state) MAY be repeated inline at the call site even though they also live in the fragment. This is a deliberate, narrow exception to the no-duplication rule: the invariant must travel with any workflow that touches the procedure, because losing it in delegation is worse than repeating it.

**Callee side — every fragment MUST end with an `## After completion` section** placed immediately above `## Used by`:

```markdown
## After completion

Return to the calling workflow and proceed with its next numbered step. This fragment is a subroutine — it has no terminal action of its own, and its caller's remaining steps (<list the remaining caller steps generically: log entry, commit, report>) are not optional just because <this procedure> is done.
```

The "After completion" text is caller-agnostic: it must not name specific caller workflows or specific step numbers, because step numbers shift and listing callers creates a maintenance burden every time a workflow renumbers. The `## Used by` footer below it is the place for caller enumeration; `## After completion` is the place for the return contract.

**What not to do:**

- Do not omit the return cue at the call site, assuming the agent will "obviously" come back. Two consecutive fragment calls (the most failure-prone shape) need both cues.
- Do not put step numbers in `## After completion` ("return to step 12 of ingest.md"). Renumbering any caller would require updating every fragment that references it.
- Do not let a fragment have its own terminal action (e.g., "commit and push"). Fragments are subroutines; terminal actions belong to the calling workflow.
- Do not inline the fragment body "for safety" because the chain feels fragile. Tighten the chaining cues instead — that is the whole purpose of this contract.

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
