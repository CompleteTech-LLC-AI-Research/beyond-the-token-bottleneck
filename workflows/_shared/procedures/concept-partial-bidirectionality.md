# Concept-Partial Bidirectionality Check

## Purpose

Every fragment under `wiki/concepts/_partials/framings/` (and `wiki/concepts/_partials/definitions/`, once populated) ends with a `## Used by` footer listing the consuming concept notes as `[[basename]]` wikilinks. The contract is bidirectional: each listed consumer must actually contain an `![[<fragment-basename>]]` embed, and no fragment may be orphaned (zero consumers). This fragment catches three regression classes:

1. A consumer's embed was deleted but the fragment's footer was not updated.
2. A fragment's footer names a consumer that does not exist on disk (phantom).
3. A fragment was created but never consumed (orphan).

## When to run

- As part of the lint workflow's content integrity pass.
- After any change under `wiki/concepts/_partials/` or to the `![[...]]` embeds inside `wiki/concepts/*.md`.

## Procedure

1. **Enumerate fragments.** List every `*.md` file under `wiki/concepts/_partials/framings/` and `wiki/concepts/_partials/definitions/`, excluding `README.md` and any `.gitkeep`. Use:

   ```bash
   ls wiki/concepts/_partials/framings/*.md wiki/concepts/_partials/definitions/*.md 2>/dev/null \
     | grep -v '/README\.md$'
   ```

2. **Forward check — consumer existence.** For each fragment, extract the `[[basename]]` wikilinks from its `## Used by` section and confirm every listed consumer resolves to a real `wiki/concepts/<basename>.md` file. Any `## Used by` entry whose target file is missing is a phantom and must be flagged.

   ```bash
   for fragment in wiki/concepts/_partials/framings/*.md wiki/concepts/_partials/definitions/*.md; do
     [ -f "$fragment" ] || continue
     [ "$(basename "$fragment")" = "README.md" ] && continue
     # Extract consumers from the ## Used by section (everything after the heading to EOF).
     consumers=$(awk '/^## Used by/{flag=1; next} flag' "$fragment" \
       | grep -oE '\[\[[^]]+\]\]' | sed 's/\[\[//; s/\]\]//')
     for c in $consumers; do
       [ -f "wiki/concepts/${c}.md" ] || echo "PHANTOM: $fragment lists [[${c}]] but wiki/concepts/${c}.md does not exist"
     done
   done
   ```

3. **Backward check — embed presence.** For each (fragment, consumer) pair claimed by the fragment's `## Used by` footer, grep the consumer's concept file for `![[<fragment-basename>]]`. If the embed is absent, the footer is lying — flag it.

   ```bash
   for fragment in wiki/concepts/_partials/framings/*.md wiki/concepts/_partials/definitions/*.md; do
     [ -f "$fragment" ] || continue
     [ "$(basename "$fragment")" = "README.md" ] && continue
     base=$(basename "$fragment" .md)
     consumers=$(awk '/^## Used by/{flag=1; next} flag' "$fragment" \
       | grep -oE '\[\[[^]]+\]\]' | sed 's/\[\[//; s/\]\]//')
     for c in $consumers; do
       target="wiki/concepts/${c}.md"
       [ -f "$target" ] || continue
       grep -qF "![[${base}]]" "$target" \
         || echo "BROKEN FOOTER: $fragment claims ${c} consumes it, but ${target} has no ![[${base}]] embed"
     done
   done
   ```

4. **Orphan check — no zero-consumer fragments.** For every fragment file, confirm that `![[<fragment-basename>]]` appears in at least one `wiki/concepts/*.md`. Zero matches = orphan = flag.

   ```bash
   for fragment in wiki/concepts/_partials/framings/*.md wiki/concepts/_partials/definitions/*.md; do
     [ -f "$fragment" ] || continue
     [ "$(basename "$fragment")" = "README.md" ] && continue
     base=$(basename "$fragment" .md)
     if ! grep -lF "![[${base}]]" wiki/concepts/*.md >/dev/null 2>&1; then
       echo "ORPHAN: $fragment is not embedded by any wiki/concepts/*.md"
     fi
   done
   ```

5. **Report.** Roll any `PHANTOM`, `BROKEN FOOTER`, or `ORPHAN` lines into the lint findings under a dedicated "Concept-partial bidirectionality" subheading. Do not auto-fix — footer edits and embed restoration both require judgement about which side is authoritative.

## Invariants

- A fragment's `## Used by` footer is authoritative only in the sense that it claims a set of consumers — the consumer's embed is what actually materializes the transclusion. Both must agree.
- `README.md` under `_partials/` and its subdirectories is never a fragment and must be excluded from all three checks.
- The check runs against on-disk state only. Do not infer consumers from prior logs or memory.

## After completion

Return to the calling workflow and proceed with its next numbered step. This fragment is a subroutine — it has no terminal action of its own, and its caller's remaining steps (report findings, seek approval, log entry, commit) are not optional just because the bidirectionality check is done.

## Used by

- `workflows/audit/lint.md` (Procedure — concept-partial bidirectionality check).
