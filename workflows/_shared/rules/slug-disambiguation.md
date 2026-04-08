# Rule: Slug Disambiguation

## Statement

Source page slugs MUST disambiguate by default. Before creating a new source page, check whether the leading hyphen-token of the candidate slug already exists in the same `wiki/sources/**/` directory. If it does, use the hybrid form `<technique>-<institution>-<distinguisher>.md` so collisions never accumulate.

## Hybrid form

`<technique>-<institution>-<distinguisher>.md`

Examples (from past KVComm collisions that prompted this rule):

- `kvcomm-kth-selective.md` — KVComm technique, KTH lead, "selective" as the distinguishing approach.
- `kvcomm-duke-online-reuse.md` — KVComm technique, Duke lead, "online reuse" as the distinguishing approach.
- `coconut-meta-reasoning.md` — Coconut technique, Meta (FAIR) lead, "reasoning" as the use-case distinguisher.

## Procedure (during ingest)

1. **Glob** `wiki/sources/**/*.md` and inspect the leading hyphen-token of every existing slug in the target subdirectory.
2. If your candidate slug's leading token (e.g. `kvcomm-`, `coconut-`) is already present in another file from a different paper, switch to the hybrid form before creating the new file.
3. The institution component should match the lead author's primary affiliation. If the lead has shared institutional credit, pick the institution most closely associated with the technique's prior work.
4. The distinguisher should be a short phrase (1–2 words) that captures the paper's most distinctive contribution relative to the colliding slug — its mechanism, its application, its dataset, etc.

## Rationale

When two source pages share a leading filename token, readers cannot disambiguate them without opening both files. In a vault with thousands of cross-references, this regularly produces wrong-page navigation: clicking `[[kvcomm-...]]` lands on the alphabetically-first match rather than the intended paper.

The hybrid form solves this at file creation time, which is cheaper than retroactive disambiguation via the [bulk source-page rename](../procedures/bulk-source-rename.md) procedure (which requires updating every backlink in the vault). The KVComm collision in early 2026 forced two retroactive renames; codifying the rule prevents the third.

The "in the same `wiki/sources/**/` directory" qualifier matters because cross-directory collisions are rarer (the directory itself usually disambiguates) and adding institution + distinguisher to every slug would inflate filenames unnecessarily. The trigger is a same-directory leading-token collision specifically.

## How violations are caught

- `workflows/lint.md` Redundancy & Dead-Reference Audit, section C — slug-collision detection. Groups basenames by their first hyphenated token within each `wiki/sources/**/` directory and flags clusters of size ≥ 2 from different papers.
- The fix is `workflows/_shared/procedures/bulk-source-rename.md` for retroactive disambiguation.

## Used by

- `workflows/ingest.md` (expected, PR 2b — Procedure step 3, "Pick a slug")
- `workflows/batch-ingest.md` (expected, PR 2b — applies to every paper in the batch)
- `workflows/lint.md` (expected, PR 2b — Redundancy & Dead-Reference Audit, section C)
- `workflows/_shared/procedures/bulk-source-rename.md` — the retroactive fix when this rule was violated
