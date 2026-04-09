### Experiment 1: Extreme Compression (GSM8K, ARC-C, GPQA)

| Method | Message size | GSM8K | ARC-C | GPQA-Diamond |
|--------|-------------|-------|-------|-------------|
| Single agent | 0 | 91% | 92% | 8.1% |
| [[latentmas-collaboration\|LatentMAS]] (full KV) | ~MB | **95%** | 93% | **26.8%** |
| SlotMAS (trained) | **512 B** | **91%** | — | 19.1% |

Critical finding: **512 bytes matches baseline on GSM8K** but GPQA needs MB-scale bandwidth. Task-dependent bandwidth requirements are the key variable.

### Experiment 2: Hidden Profile (forced communication)
16-byte bottleneck raises communication-dependent accuracy from **12% → 57-65%**. Full mean pool (10 KB) reaches 80.7%.

### Experiment 3: Long Document QA (QASPER)
Carefully selected 1.35 KB text (4.5% of full) achieves **54%** vs. 33% for full text — models are **drowned by long context**. Latent high-bandwidth (2 KB) only reaches 31%.

### Experiment 4: Information Bottleneck + Style Adversarial
4× compression with IB + adversarial training: 99.95% accuracy, style leakage drops from 35.2% → 13.5%.
