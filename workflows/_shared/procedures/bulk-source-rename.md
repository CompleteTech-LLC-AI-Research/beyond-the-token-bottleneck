# Bulk Source-Page Rename

## Purpose

When a source page slug changes (e.g., to disambiguate after a slug-collision audit), every backlink in the wiki must be updated atomically. The surface area of backlinks is large enough that editing one file at a time virtually guarantees a missed link, and a single missed link breaks navigation. This fragment defines the exact sequence — including the one place in the wiki where `sed` is the blessed tool — so renames stay consistent and history-preserving.

## When to run

- After a slug-collision audit triggers a rename (`workflows/lint.md` Redundancy & Dead-Reference Audit, section C).
- Any time a source page's filename slug needs to change for any reason.
- Never as a one-off shortcut for a content change — this is rename-only; if the page itself needs revision, do that as a separate edit.

## Procedure

1. **Enumerate references first**: `Grep '\[\[<old-slug>' .` — confirm the count and the files affected. This is the inventory you will verify against in step 4.
2. **Move the file with `git mv`** so history is preserved. Never use `Write` to create a new file alongside the old; that orphans the rename from git history and forces a manual fix later.
3. **Bulk-rewrite all references**. The blessed tool for this single case is `sed` (the only place in the project where `sed` overrides the "use Edit, not sed" default), because (a) the slug is unique enough that collateral damage is impossible to introduce, and (b) the alternative is 30+ Read+Edit pairs:

   ```bash
   find wiki raw -name "*.md" -print0 | xargs -0 sed -i 's/<old-slug>/<new-slug>/g'
   ```

4. **Verify**: re-run `Grep '<old-slug>' .` — must return zero matches. Any non-zero result means the inventory step missed a file, and the rewrite must be extended to cover it.
5. **Update `raw/index.md`** if the source page is also referenced there (the sed pass usually handles this — confirm by inspection).
6. **Log it** in `wiki/log.md` with action `lint` or `update`, listing both the old and new slugs so the rename is auditable later.

## Invariants

- `git mv`, never `Write`. History preservation is non-negotiable.
- `sed` is the blessed tool for this single rename pattern — and only this pattern. Anywhere else in the project, the "use Edit, not sed" default applies.
- The post-rewrite `Grep '<old-slug>' .` must return zero matches before the procedure is considered complete. Any non-zero result is a regression, not a "good enough" outcome.
- Both the old slug and the new slug must appear in the `wiki/log.md` entry so future audits can trace the rename.
- This procedure is rename-only. Do not bundle it with content edits to the renamed page; mixing the two makes the diff unreadable and the history confusing.

## After completion

Return to the calling workflow and proceed with its next numbered step. This fragment is a subroutine — it has no terminal action of its own, and its caller's remaining steps (any further audit findings, fixes, log entry, report) are not optional just because the rename is complete.

## Used by

- `workflows/lint.md` (Redundancy & Dead-Reference Audit, section C, replacing the inlined "Bulk source-page rename" section)
- `workflows/enrich.md` (when a slug change is part of the pass)
