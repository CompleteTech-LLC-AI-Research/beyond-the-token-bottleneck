---
type: index
title: "Raw Asset Index"
created: "2026-04-06"
---

# Raw Asset Index

Maps every file in `raw/pdf/` and `raw/latex/` to its corresponding wiki source page. Files are grouped by type and role (canonical source vs. venue duplicate).

See also: [[checklist]] — Paper download checklist mapping URLs to local files.

## Naming Conventions

- **`arxiv-XXXX.XXXXX.pdf`** — canonical arXiv PDFs
- **`arxiv-XXXX.XXXXX/`** — extracted arXiv LaTeX source directories
- **`arxiv-XXXX.XXXXX.tar.gz`** — compressed arXiv source archives

If venue copies (OpenReview, ACL Anthology, etc.) are added in the future, name them `openreview-XXXXXXXX.pdf` or `acl-YYYY.venue-type.NNNN.pdf` and list them under a "Duplicate PDFs" section.

---

## Canonical PDFs

Each PDF below is the primary copy used for ingestion. The wiki source page was written from this file.

| PDF | Wiki Source Page |
|-----|-----------------|
| `raw/pdf/arxiv-2412.06769.pdf` | [[wiki/sources/reasoning/coconut-reasoning-latent-space]] |
| `raw/pdf/arxiv-2502.12134.pdf` | [[wiki/sources/reasoning/softcot-efficient-reasoning]] |
| `raw/pdf/arxiv-2602.08332.pdf` | [[wiki/sources/reasoning/thinking-states-latent-reasoning]] |
| `raw/pdf/arxiv-2405.14838.pdf` | [[wiki/sources/reasoning/icot-internalize-cot]] |
| `raw/pdf/arxiv-2310.02226.pdf` | [[wiki/sources/reasoning/pause-tokens]] |
| `raw/pdf/arxiv-2505.12514.pdf` | [[wiki/sources/reasoning/superposition-coconut-theory]] |
| `raw/pdf/arxiv-2310.06272.pdf` | [[wiki/sources/communication/embeddings/cipher-multiagent-debate-embeddings]] |
| `raw/pdf/arxiv-2506.19209.pdf` | [[wiki/sources/communication/embeddings/state-delta-trajectory]] |
| `raw/pdf/arxiv-2501.14082.pdf` | [[wiki/sources/communication/activations/activation-communication-harvard]] |
| `raw/pdf/arxiv-2511.09149.pdf` | [[wiki/sources/communication/activations/interlat-latent-space-agents]] |
| `raw/pdf/arxiv-2510.03346.pdf` | [[wiki/sources/communication/kv-cache/kvcomm-selective-kv-sharing]] |
| `raw/pdf/arxiv-2510.03215.pdf` | [[wiki/sources/communication/kv-cache/cache-to-cache-semantic-communication]] |
| `raw/pdf/arxiv-2510.12167.pdf` | [[wiki/sources/reasoning/inference-time-scaling-continuous-reasoning]] |
| `raw/pdf/arxiv-2601.06123.pdf` | [[wiki/sources/communication/kv-cache/kv-cache-alignment-shared-space]] |
| `raw/pdf/arxiv-2510.12872.pdf` | [[wiki/sources/communication/kv-cache/kvcomm-online-cross-context]] |
| `raw/pdf/arxiv-2510.20733.pdf` | [[wiki/sources/communication/structured/thought-communication-multiagent]] |
| `raw/pdf/arxiv-2511.20639.pdf` | [[wiki/sources/unified/latentmas-collaboration]] |
| `raw/pdf/arxiv-2602.15382.pdf` | [[wiki/sources/unified/vision-wormhole-heterogeneous]] |
| `raw/pdf/arxiv-2602.03695.pdf` | [[wiki/sources/unified/agent-primitives-building-blocks]] |
| `raw/pdf/arxiv-2512.08296.pdf` | [[wiki/sources/meta/scaling-agent-systems]] |
| `raw/pdf/arxiv-2305.15408.pdf` | [[wiki/sources/meta/cot-expressivity-theory]] |
| `raw/pdf/arxiv-2405.07987.pdf` | [[wiki/sources/meta/platonic-representation-hypothesis]] |
| `raw/pdf/arxiv-2209.15430.pdf` | [[wiki/sources/meta/relative-representations-zero-shot]] |
| `raw/pdf/arxiv-2308.09124.pdf` | [[wiki/sources/meta/linearity-relation-decoding]] |
| `raw/pdf/arxiv-2305.14325.pdf` | [[wiki/sources/meta/multiagent-debate-du-et-al]] |
| `raw/pdf/arxiv-2602.22441.pdf` | [[wiki/sources/meta/latent-reasoning-supervision-analysis]] |

## Non-PDF Source

| Source | Wiki Source Page |
|--------|-----------------|
| GitHub repository (no PDF) | [[wiki/sources/meta/latentcompress-open-call]] |

---

## LaTeX Sources

Each LaTeX source corresponds 1:1 to the PDF with the same arXiv ID. Some papers are stored as extracted directories; newer ones remain as `.tar.gz` archives.

### Extracted Directories (9)

| Directory | Corresponding PDF | Wiki Source Page |
|-----------|-------------------|-----------------|
| `raw/latex/arxiv-2209.15430/` | `arxiv-2209.15430.pdf` | [[wiki/sources/meta/relative-representations-zero-shot]] |
| `raw/latex/arxiv-2305.14325/` | `arxiv-2305.14325.pdf` | [[wiki/sources/meta/multiagent-debate-du-et-al]] |
| `raw/latex/arxiv-2305.15408/` | `arxiv-2305.15408.pdf` | [[wiki/sources/meta/cot-expressivity-theory]] |
| `raw/latex/arxiv-2308.09124/` | `arxiv-2308.09124.pdf` | [[wiki/sources/meta/linearity-relation-decoding]] |
| `raw/latex/arxiv-2310.02226/` | `arxiv-2310.02226.pdf` | [[wiki/sources/reasoning/pause-tokens]] |
| `raw/latex/arxiv-2405.07987/` | `arxiv-2405.07987.pdf` | [[wiki/sources/meta/platonic-representation-hypothesis]] |
| `raw/latex/arxiv-2405.14838/` | `arxiv-2405.14838.pdf` | [[wiki/sources/reasoning/icot-internalize-cot]] |
| `raw/latex/arxiv-2505.12514/` | `arxiv-2505.12514.pdf` | [[wiki/sources/reasoning/superposition-coconut-theory]] |
| `raw/latex/arxiv-2602.08332/` | `arxiv-2602.08332.pdf` | [[wiki/sources/reasoning/thinking-states-latent-reasoning]] |

### Compressed Archives (16)

| Archive | Corresponding PDF | Wiki Source Page |
|---------|-------------------|-----------------|
| `raw/latex/arxiv-2310.06272.tar.gz` | `arxiv-2310.06272.pdf` | [[wiki/sources/communication/embeddings/cipher-multiagent-debate-embeddings]] |
| `raw/latex/arxiv-2412.06769.tar.gz` | `arxiv-2412.06769.pdf` | [[wiki/sources/reasoning/coconut-reasoning-latent-space]] |
| `raw/latex/arxiv-2501.14082.tar.gz` | `arxiv-2501.14082.pdf` | [[wiki/sources/communication/activations/activation-communication-harvard]] |
| `raw/latex/arxiv-2502.12134.tar.gz` | `arxiv-2502.12134.pdf` | [[wiki/sources/reasoning/softcot-efficient-reasoning]] |
| `raw/latex/arxiv-2506.19209.tar.gz` | `arxiv-2506.19209.pdf` | [[wiki/sources/communication/embeddings/state-delta-trajectory]] |
| `raw/latex/arxiv-2510.03215.tar.gz` | `arxiv-2510.03215.pdf` | [[wiki/sources/communication/kv-cache/cache-to-cache-semantic-communication]] |
| `raw/latex/arxiv-2510.03346.tar.gz` | `arxiv-2510.03346.pdf` | [[wiki/sources/communication/kv-cache/kvcomm-selective-kv-sharing]] |
| `raw/latex/arxiv-2510.12167.tar.gz` | `arxiv-2510.12167.pdf` | [[wiki/sources/reasoning/inference-time-scaling-continuous-reasoning]] |
| `raw/latex/arxiv-2510.12872.tar.gz` | `arxiv-2510.12872.pdf` | [[wiki/sources/communication/kv-cache/kvcomm-online-cross-context]] |
| `raw/latex/arxiv-2510.20733.tar.gz` | `arxiv-2510.20733.pdf` | [[wiki/sources/communication/structured/thought-communication-multiagent]] |
| `raw/latex/arxiv-2511.09149.tar.gz` | `arxiv-2511.09149.pdf` | [[wiki/sources/communication/activations/interlat-latent-space-agents]] |
| `raw/latex/arxiv-2511.20639.tar.gz` | `arxiv-2511.20639.pdf` | [[wiki/sources/unified/latentmas-collaboration]] |
| `raw/latex/arxiv-2512.08296.tar.gz` | `arxiv-2512.08296.pdf` | [[wiki/sources/meta/scaling-agent-systems]] |
| `raw/latex/arxiv-2601.06123.tar.gz` | `arxiv-2601.06123.pdf` | [[wiki/sources/communication/kv-cache/kv-cache-alignment-shared-space]] |
| `raw/latex/arxiv-2602.03695.tar.gz` | `arxiv-2602.03695.pdf` | [[wiki/sources/unified/agent-primitives-building-blocks]] |
| `raw/latex/arxiv-2602.08332.tar.gz` | `arxiv-2602.08332.pdf` | [[wiki/sources/reasoning/thinking-states-latent-reasoning]] |
| `raw/latex/arxiv-2602.15382.tar.gz` | `arxiv-2602.15382.pdf` | [[wiki/sources/unified/vision-wormhole-heterogeneous]] |
| `raw/latex/arxiv-2602.22441.tar.gz` | `arxiv-2602.22441.pdf` | [[wiki/sources/meta/latent-reasoning-supervision-analysis]] |

---

## Summary

| Category | Count |
|----------|-------|
| Canonical PDFs | 26 |
| Non-PDF sources | 1 (GitHub) |
| **Total PDFs** | **26** |
| LaTeX directories | 9 |
| LaTeX archives | 18 |
| **Total LaTeX** | **27** |
| **Unique wiki source pages** | **27** |
