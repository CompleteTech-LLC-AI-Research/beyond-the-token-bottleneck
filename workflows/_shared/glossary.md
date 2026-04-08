# Glossary

Canonical names for concepts that have drifted across existing workflows. Workflows MUST use the canonical term in new prose. The lint workflow's terminology check flags drift variants for normalization.

This glossary is the single source of truth for canonical terminology — `workflows/CONVENTIONS.md` points here and contains no inline glossary. When you encounter a term that drifts, add it here.

## Terms

### living analyses

**Drift variants:** "gap-tracking analysis pages", "analysis pages", "synthesis pages"

**Definition:** The 6+ files under `wiki/analyses/` that must be checked on every ingest because they synthesize claims across multiple papers. New papers regularly update individual numbered tensions, directions, or rows inside these files, so they require per-item review (see [`procedures/living-analyses-review.md`](procedures/living-analyses-review.md)).

**Notes:** "synthesis pages" is too broad — it would also include `wiki/overview-state-of-field.md`, which is not a living analysis. Always use "living analyses" when you specifically mean the per-item-review enumeration.

### source page

**Drift variants:** "source summary page", "source file page"

**Definition:** A markdown page under `wiki/sources/**/` that summarizes a single paper. Has frontmatter `type: source` and the per-source schema in [`rules/frontmatter-schema.md`](rules/frontmatter-schema.md).

**Notes:** `ingest.md` historically mixed "source summary page" and "source page" in the same procedure. Standardize on "source page".

### MOC

**Drift variants:** none — but commonly conflated with "reading path"

**Definition:** A *Map of Content* file at `wiki/mocs/<theme>.md`. Each MOC defines a curated traversal of the wiki for a specific theme.

**Important:** "MOC" is the **file**. "Reading path" (see next term) is the **ordered traversal baked into the MOC's body**. They are not synonyms — the MOC has metadata and prose around its reading path, and a single MOC has exactly one reading path. Conflating the two leads to ambiguous procedure language ("update the MOC" vs "update the reading path") that has caused real bugs.

### reading path

**Drift variants:** "reading path outline", "MOC reading path", and (incorrectly) "MOC"

**Definition:** The ordered sequence of pages baked into a MOC's body. The order matters — each MOC declares an ordering principle (chronological, conceptual progression, mechanism-first, etc.) in its header, and entries are inserted in the position the principle dictates, not appended at the end.

**Notes:** When you say "update the MOC", be explicit about whether you mean the file as a whole (prose, header, ordering principle) or the reading path inside it.

### coordinator-only files

**Drift variants:** "shared files", "off-limits for agents", "do-not-touch files"

**Definition:** The set of files that subagents launched in parallel from a workflow MUST NOT edit. The canonical enumeration lives in [`rules/shared-file-off-limits.md`](rules/shared-file-off-limits.md).

**Notes:** Avoid "shared files" because it is ambiguous with the `_shared/` fragment directory. "Coordinator-only" is unambiguous and signals the underlying rule (the coordinator is the only allowed writer).

### thin pages / below depth standard

**Drift variants:** "shallow pages", "stub pages", "pages needing expansion"

**Definition:** Pages whose content falls below the depth standard for their type. The depth standard is documented per-type in `AGENTS.md` (and the upcoming `_shared/checklists/base.md` in PR 2b).

**Notes:** Both "thin pages" and "below depth standard" are acceptable — they differ in register, not meaning. Prefer "thin pages" in procedure step language for brevity, and "below depth standard" in checklist and audit contexts where precision matters.

### phantom assets / phantom paths

**Drift variants:** "stale paths", "dead references" (when applied to file paths specifically)

**Definition:** A file path written into the wiki (in frontmatter, body wiki-links, indexes, or checklists) that does not actually point to a file on disk. See [`rules/path-discipline.md`](rules/path-discipline.md) for the rule that forbids these.

**Notes:** "phantom" is the canonical term and is well-named — it captures both that the path looks valid and that the underlying file is absent. Use "phantom" rather than "stale" or "dead", which have other meanings (stale = outdated, dead = orphaned).

### stale claim

**Drift variants:** "outdated claim", "superseded claim"

**Definition:** A factual claim in a wiki page that newer evidence has invalidated or refined. The lint workflow's content-integrity scan looks for these.

**Notes:** A stale claim is *content* that has been superseded; a phantom path is a *file reference* that does not resolve. They are different regression classes and should not be conflated.

### orphan page

**Drift variants:** "unlinked page", "isolated page"

**Definition:** A page with no inbound wiki-links from any other page in the vault. Lint flags these because they are unreachable through navigation even though they exist in `wiki/index.md`.

**Notes:** A page that is referenced only from `wiki/index.md`'s directory tree counts as an orphan. The directory tree is an inventory, not a navigation surface.

### red link

**Drift variants:** "broken link", "missing page link"

**Definition:** A `[[wiki-link]]` whose target file does not exist. Lint flags these as part of the content-integrity scan.

**Notes:** "Red link" is borrowed from MediaWiki convention and is unambiguous. Avoid "broken link" (which can also mean a malformed URL) and "missing page link" (clumsy).

## How this glossary is enforced

- **Authoring time:** Workflows reference this glossary when introducing new prose. Use the canonical term, not a drift variant.
- **Lint time:** The lint workflow's terminology check greps for drift variants and flags them for normalization.
- **Review time:** The review workflow surfaces drift variants in its findings list.

## Used by

- `workflows/CONVENTIONS.md` (one-line pointer; CONVENTIONS.md no longer carries a seed glossary)
- `workflows/lint.md` (terminology drift scan, Procedure step 6)
- `workflows/review.md` (terminology drift scan, Procedure step 9)
- All workflow files (every workflow that uses any term in this glossary should use the canonical form)
