### Word Embeddings (FastText ↔ Word2Vec, 20K words, 300 anchors)

| Metric | Absolute | Relative |
|--------|----------|----------|
| Jaccard | 0.00 | **0.34-0.39** |
| MRR | 0.00 | **0.94-0.98** |
| Cosine | 0.01 | **0.86** |

Absolute representations are **completely incompatible** (zero alignment). Relative representations recover near-perfect correspondence.

### Cross-Lingual Text Classification (Amazon Reviews, English decoder)

| Encoder Language | Absolute F1 | Relative (Translated anchors) F1 |
|-----------------|-------------|----------------------------------|
| English | 91.54 | 90.06 |
| Spanish | 43.67 | **82.78** |
| French | 54.41 | **78.49** |
| Japanese | 48.72 | **65.72** |

Using language-specific RoBERTa models. Relative representations close most of the cross-lingual gap — Spanish jumps from 43.67 to 82.78 with zero retraining.

### Cross-Architecture Text Stitching (BERT/ELECTRA/RoBERTa)

| Dataset | Absolute Stitch | **Relative Stitch** |
|---------|----------------|---------------------|
| TREC | 21.49 | **75.89** |
| DBpedia | 6.96 | **80.47** |
| Amazon Reviews | 49.58 | **72.37** |

### Cross-Architecture Image Stitching (ViT + RexNet, CIFAR-100)

ViT-base encoder + RexNet decoder: Absolute = 6.21, **Relative = 81.42** — two orders of magnitude improvement.

### Zero-Shot Image Reconstruction (MSE)

Relative AE stitching: ~2.78 MSE vs absolute: ~100.56 — **$36\times$ better**.

### Performance Proxy (No Labels Needed)

On Cora graph classification across ~2000 models with varied hyperparameters: Pearson correlation between relative-space similarity and model accuracy = $0.955$. This metric is differentiable and requires no labeled data — usable as a training signal.
