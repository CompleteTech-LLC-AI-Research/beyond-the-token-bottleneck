---
type: source
title: "Relative Representations Enable Zero-Shot Latent Space Communication"
source_file: "[[raw/pdf/arxiv-2209.15430.pdf]]"
latex_source: "raw/latex/arxiv-2209.15430/"
author: "Luca Moschella, Valentino Maiorca, Marco Fumero, Antonio Norelli, Francesco Locatello, Emanuele Rodola"
date_published: "2022-09-30"
date_ingested: "2026-04-06"
created: "2026-04-06"
venue: "ICLR 2023"
arxiv: "2209.15430"
institution: "Sapienza University of Rome, AWS"
tags: [representation-alignment, zero-shot-stitching, cross-model, foundational]
---

# Relative Representations Enable Zero-Shot Latent Space Communication

## Summary

Establishes that well-trained neural networks produce latent spaces related by approximately **angle-preserving (isometric) transformations**. By representing each data point as a vector of cosine similarities to a fixed set of anchor samples, the representation becomes invariant to rotations/reflections — enabling **zero-shot model stitching** with no learned mapping. This is the practical foundation for why linear projections work in [[cache-to-cache-semantic-communication|C2C]], [[kv-cache-alignment-shared-space|KV Cache Alignment]], and [[activation-communication-harvard|AC]].

## Core Mechanism

### The Invariance Construction

For any data point $x$ with embedding $e_x$ and a set of anchors $A = \{a_1, \ldots, a_{|A|}\}$:

> $$r_x = (\cos\text{sim}(e_x, e_{a_1}),\; \cos\text{sim}(e_x, e_{a_2}),\; \ldots,\; \cos\text{sim}(e_x, e_{a_{|A|}}))$$

Where $\cos\text{sim}(a,b) = \frac{a \cdot b}{\|a\| \|b\|} = \cos(\theta)$.

**Why this works**: Cosine similarity is invariant to any angle-preserving transformation $T$. If $T$ is applied to both vectors: $\cos\text{sim}(Te_x, Te_a) = \cos\text{sim}(e_x, e_a)$. Therefore two models trained with different seeds produce **identical relative representations** for the same input, regardless of the (near-isometric) transformation between their absolute latent spaces.

**Core assumption**: When training varies (different seeds, hyperparameters), the mapping between resulting latent spaces is approximately angle-preserving. This is empirically validated across diverse settings and theoretically motivated by shared inductive biases in deep networks.

### Anchor Types

| Strategy | Description | Quality |
|----------|------------|---------|
| Uniform random | Random training samples | Simplest; competitive |
| Farthest point sampling | Maximize coverage | Best Jaccard/MRR |
| K-means centroids | Cluster centers | Best cosine similarity |
| Top-K frequent | Most common samples | Slightly worse |
| OOD anchors | From out-of-distribution data | Works for domain adaptation |
| Parallel anchors | Corresponding samples across domains | Best for cross-lingual |

Even noisy anchors (Google Translate outputs) or OOD anchors (Wikipedia sentences for Amazon reviews) work well. Performance improves monotonically with anchor count when the encoder is frozen.

## Key Results

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

## Training with Relative Representations

| Dataset | Absolute | Relative | $\Delta$ |
|---------|----------|----------|---|
| MNIST | 97.95 | 97.91 | -0.04 |
| Fashion-MNIST | 90.32 | 90.19 | -0.13 |
| CIFAR-10 | 87.85 | 87.70 | -0.15 |
| CIFAR-100 | 68.88 | **66.72** | **-2.16** |

Near-zero degradation on most tasks. CIFAR-100 shows a ~2-point drop — the only notable cost.

### End-to-End Training Instability

When training end-to-end (not frozen encoder): susceptible to model collapse. Increasing anchor count does NOT always help. Backpropagation does not pass through anchors (encourages smoother optimization but limits gradient information). Frozen-encoder usage is more stable and recommended.

### The Zero-Shot Transfer Mechanism in Detail

The zero-shot stitching result deserves careful analysis because it establishes the theoretical ceiling for training-free cross-model communication. The mechanism works in three steps:

1. **Anchor projection**: Both models compute embeddings for the same set of anchor inputs. These anchor embeddings define a coordinate system in each model's latent space.
2. **Relative encoding**: Any new input is represented not by its absolute embedding but by its similarity profile to the anchors — a vector in $\R^{|A|}$ where each coordinate is a cosine similarity.
3. **Space-invariant decoding**: Because cosine similarity is preserved under isometric transformations, the relative representation is (approximately) identical regardless of which model produced it.

The critical insight is that this works **without any paired data** between models. Unlike [[kv-cache-alignment-shared-space|KV Cache Alignment]], which requires training on shared text to learn adapter parameters, relative representations need only a shared set of anchor inputs. The anchors serve as a "Rosetta Stone" — they don't need labels, just consistent inputs across models. This is why even OOD anchors work: the relative geometry is preserved even when the anchors themselves are poorly represented.

### Cross-Architecture Compatibility Implications

The cross-architecture results (BERT ↔ ELECTRA ↔ RoBERTa, ViT ↔ RexNet) are particularly significant for the broader [[latent-space-reasoning]] and [[kv-cache-communication]] research. They demonstrate that the isometric assumption holds across fundamentally different architectures (not just different seeds or hyperparameters of the same architecture). This provides empirical grounding for the [[platonic-representation-hypothesis|Platonic Representation Hypothesis]]: if different architectures trained on similar data converge to approximately isometric representations, then cross-model communication is theoretically possible without architecture-specific engineering.

However, the quality of zero-shot stitching degrades with architectural distance. Same-architecture stitching (BERT encoder ↔ BERT decoder) preserves ~95% of within-model accuracy, while cross-architecture stitching (ViT encoder ↔ RexNet decoder) preserves ~83%. This gap quantifies the degree to which the isometric assumption breaks down as models diverge — and motivates the learned projections used by [[cache-to-cache-semantic-communication|C2C]] and [[activation-communication-harvard|AC]] when higher fidelity is needed.

## Why This Matters for Latent Communication

### Linear maps are theoretically justified

If the transformation between latent spaces is approximately orthogonal (rotation/reflection + scaling), then a linear projection is the **exact correct tool**. You don't need nonlinear transformations. This directly explains why:
- [[cache-to-cache-semantic-communication|C2C]]'s projection module works with linear layers
- [[kv-cache-alignment-shared-space|KV Cache Alignment]]'s affine adapters suffice
- [[activation-communication-harvard|AC]]'s mapping matrix W (trained on 3072 C4 sentences) achieves SOTA

### Anchor-based alignment is O(N)

Each model needs anchor similarities computed once. Cross-model alignment is a fixed-cost post-processing step. This echoes KV Cache Alignment's $O(N)$ scaling and Vision Wormhole's affine alignment.

### Diagnostic tool

The 0.955 Pearson correlation means you can predict whether two models' latent spaces are compatible **before** attempting communication — no task-specific evaluation needed.

## Connections

- **[[platonic-representation-hypothesis|Platonic Representation Hypothesis]]**: PRH explains *why* representations converge (shared statistical model of reality). Relative representations provide *how* to exploit this convergence in practice.
- **[[activation-communication-harvard|AC]]**: AC's cross-family results without W are consistent with the isometric assumption — cosine similarities in activation space should be approximately preserved.
- **[[kv-cache-alignment-shared-space|KV Cache Alignment]]**: The ablation showing linear maps work but cross-attention scales better mirrors Moschella et al.'s finding that cosine alignment is good but nonlinear methods can do better.
- **[[vision-wormhole-heterogeneous|Vision Wormhole]]**: Affine alignment with ridge regression on anchor texts is a direct application of the relative representation principle.

## Limitations

- **Isometry assumption scope**: Assumes angle-preserving transforms between latent spaces. This holds well when models share training distributions but may break for models trained on very different data (e.g., code-only vs. natural language). The degree of isometry is empirically correlated with training distribution overlap.
- **Slight degradation on harder tasks**: CIFAR-100 shows a ~2.16-point drop, suggesting that fine-grained classification with many categories strains the relative representation's capacity. The anchor-based projection introduces a dimensionality bottleneck: $|A|$ anchors can only distinguish $|A|$ directions in representation space.
- **End-to-end training less stable** than frozen-encoder usage due to model collapse risk.
- **Single-layer stitching only**: Multi-layer stitching (e.g., aligning intermediate representations at multiple depths) is unexplored. This is relevant because [[linearity-relation-decoding|Hernandez et al. (2023)]] show that different layers encode qualitatively different information — single-layer stitching necessarily loses the depth-dependent structure.
- **Anchor count vs. dimensionality trade-off**: More anchors improve alignment monotonically (with frozen encoders), but each anchor adds a dimension to the relative representation. For large anchor sets, the relative representation may become higher-dimensional than the original embedding, negating efficiency benefits.
- **Static anchors**: The anchor set is fixed at alignment time. If the deployment distribution shifts significantly from the anchor distribution, alignment quality degrades. Adaptive anchor selection strategies are not explored.

## Source Materials

- [[raw/pdf/arxiv-2209.15430.pdf|PDF]] (`raw/latex/arxiv-2209.15430/`)
