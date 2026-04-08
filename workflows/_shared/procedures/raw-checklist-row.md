# Raw Checklist Row

## Purpose

`raw/checklist.md` is the URL audit trail that runs parallel to `raw/index.md`'s asset map. Every arXiv paper listed in `raw/index.md`'s "Canonical PDFs" table must have exactly one corresponding row in `raw/checklist.md`. This fragment defines the eight-column row format and the per-column rules so callers append rows consistently and the bijection is never broken by ad-hoc formatting.

## When to run

- During an ingest, immediately after updating `raw/index.md` with the new PDF and LaTeX source.
- During a batch-ingest, once per ingested arXiv paper.
- Any time a new arXiv paper is added to `raw/index.md`'s Canonical PDFs table.

## Procedure

Append one row to `raw/checklist.md` with these eight columns:

```
Paper | Original refs from list | Canonical PDF download | Canonical LaTeX/source download | PDF present | Local PDF | LaTeX present | Local LaTeX/source
```

Fill each column as follows:

1. **Paper** — the paper title.
2. **Original refs from list** — `arXiv:XXXX.XXXXX` plus any venue-duplicate IDs (OpenReview, ACL, EMNLP, ICLR, NeurIPS, ICML) that appear in the "Duplicate PDFs (Venue Copies)" section of `raw/index.md` for this paper. Separate multiple refs with `;`. **Only include venue refs whose PDF is actually present in `raw/pdf/`** — verify each path with `Glob` before listing it, same constraint as the source page's `venue_pdfs:` frontmatter.
3. **Canonical PDF download** — `https://arxiv.org/pdf/{id}` (use the bare ID, no version suffix unless intentionally pinning).
4. **Canonical LaTeX/source download** — `https://arxiv.org/e-print/{id}`.
5. **PDF present** — `Yes` once the downloader has run and `raw/pdf/arxiv-{id}.pdf` exists on disk.
6. **Local PDF** — `raw/pdf/arxiv-XXXX.XXXXX.pdf`. **Do not use `reference/pdf/...`** — that is a stale historical path from a pre-move vault layout and has caused drift in the past.
7. **LaTeX present** — `Yes` once the downloader has run and the LaTeX source exists on disk in either form.
8. **Local LaTeX/source** — must match the actual on-disk format chosen in `raw/download_arxiv_papers.py`:
   - `raw/latex/arxiv-XXXX.XXXXX/` (trailing slash) for `extract`-mode papers whose source was unpacked into a directory.
   - `raw/latex/arxiv-XXXX.XXXXX.tar.gz` for `archive`-mode papers stored as a tarball.

## Invariants

- Every arXiv paper in `raw/index.md`'s "Canonical PDFs" table has exactly one row in `raw/checklist.md`. The bijection holds in both directions.
- Non-arXiv sources (e.g., the latentcompress GitHub project) are intentionally excluded from the checklist.
- `raw/pdf/...` and `raw/latex/...` are the only acceptable local-path prefixes. `reference/pdf/...` is a stale historical path that must never be reintroduced.
- Venue refs in column 2 are only listed when their PDF is on disk in `raw/pdf/`. Phantom venue refs propagate into `raw/index.md` and break lint passes weeks later.
- The `Local LaTeX/source` column format must match the actual download mode (`extract` → directory with trailing slash, `archive` → `.tar.gz` file). Mismatches break the asset bijection.

## After completion

Return to the calling workflow and proceed with its next numbered step. This fragment is a subroutine — it has no terminal action of its own, and its caller's remaining steps (analyses review, count sweep, log entry, commit, report) are not optional just because the row has been appended.

## Used by

- `workflows/ingest.md` (Procedure step 10)
- `workflows/batch-ingest.md` (once per ingested paper)
- `workflows/gap-analysis.md` (Phase 5 ingest substep)
