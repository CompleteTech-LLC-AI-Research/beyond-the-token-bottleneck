---
type: overview
category: lens
title: "Cross-Architecture Compatibility"
created: "2026-04-06"
updated: "2026-04-06"
tags: [moc, cross-architecture, compatibility]
---

# Cross-Architecture Compatibility

The central tension in latent communication: **deeper channels carry more information but demand tighter architectural coupling**. Natural language works between any two models; raw activation sharing barely works between two training runs of the same architecture. This MOC traces how the field is trying to bend that curve — achieving deep, information-rich communication across heterogeneous model families.

## Reading Path

### 1. The Problem Statement

Start with the depth-compatibility trade-off laid out in [[embedding-space-communication]]. The spectrum table shows the cost clearly: [[cipher-multiagent-debate-embeddings|CIPHER]] requires a **shared tokenizer**, [[kvcomm-kth-selective|KVComm]] requires **identical architecture**, and [[state-delta-trajectory|SDE]] requires **identical weights**. Each step deeper in the transformer stack narrows the set of compatible partners. The [[open-questions|open questions]] frame cross-architecture compatibility as the field's major unsolved problem.

### 2. Why Cross-Model Communication Works at All

Two theoretical papers explain why independently trained models can share internal representations:

- **[[platonic-representation-hypothesis|The Platonic Representation Hypothesis]]** (Huh et al., ICML 2024) — Models across architectures, objectives, and modalities are **converging toward a shared statistical model of reality**. Higher-performing models align more tightly. The implication: cross-model communication should get *easier* with scale, not harder.

- **[[relative-representations-zero-shot|Relative Representations]]** (Moschella et al., ICLR 2023) — The practical complement. Well-trained models produce latent spaces related by approximately **angle-preserving transforms**. Representing data as cosine similarities to shared anchors makes representations invariant to rotations/reflections, enabling zero-shot stitching. The same underlying observation — that well-trained models differ by approximately orthogonal transforms — also explains why simple linear projections suffice for methods like AC and C2C. Cross-architecture stitching jumps from 6% to 80%+ accuracy.

Together they predict that a simple affine correction should bridge most model pairs — and the empirical results confirm it.

Note the counter-case: **[[latentmas-collaboration|LatentMAS]]** demonstrates what happens when you *don't* solve cross-architecture compatibility. Its training-free KV-cache transfer works well within homogeneous pools (Qwen-family), but catastrophically fails on LLaMA (-10.1% average), illustrating how same-architecture assumptions break down across families.

### 3. Shared Tokenizer Baseline (CIPHER)

![[cipher-multiagent-debate-embeddings/one-liner]]

**Cross-arch lens**: the shallowest cross-model method. Works between LLaMA2-70B ↔ LLaMA-65B because they share a tokenizer; out of reach for Falcon or MPT (though CIPHER works in same-model debate for both).

### 4. Learned Linear Mappings (AC)

![[activation-communication-harvard/one-liner]]

**Cross-arch lens**: breaks the tokenizer barrier. When explicit alignment helps, a single task-agnostic linear mapping $W$ trained on just 3,072 C4 sentences suffices — but the result that cross-family transfer works *without* $W$ is the strongest empirical evidence to date for the [[platonic-representation-hypothesis|Platonic Representation Hypothesis]].

### 5. Learned Pairwise Fusers (C2C)

![[cache-to-cache-semantic-communication/one-liner]]

**Cross-arch lens**: the first method to tackle cross-architecture at the KV-cache level. The $O(N^2)$ scaling cost is the price for cross-family + cross-size compatibility (Qwen ↔ LLaMA ↔ Gemma, 0.6B–14B).

### 6. Shared Latent Spaces (KV Cache Alignment)

![[kv-cache-alignment-shared-space/one-liner]]

**Cross-arch lens**: solves C2C's $O(N^2)$ scaling via the interlingua. Also enables **module portability** — soft prompts learned on one model transfer to another. Currently validated only at 100M–400M scale.

### 7. Architectural Bypass (Vision Wormhole)

![[vision-wormhole-heterogeneous/one-liner]]

**Cross-arch lens**: rather than *solving* the alignment problem like C2C/KV Alignment, this *bypasses* it — the visual pathway is already a continuous-vector input channel. Mid-sized models (4B–12B) show dramatic speedups (5.92×) but accuracy degrades, suggesting the fixed bandwidth bottleneck limits scaling.

## Compatibility Spectrum

![[compatibility-spectrum]]

## Connections

- **[[latent-communication]]** — The broader communication landscape; this MOC zooms in on the compatibility dimension
- **[[communication-depth-spectrum]]** — The 10-level depth walkthrough that defines the trade-off this MOC addresses
- **[[unified-frameworks]]** — Vision Wormhole and KV Cache Alignment appear there as systems combining reasoning + communication
- **[[open-questions]]** — The "Cross-Architecture Compatibility" section catalogs the unsolved problems
- **[[contradictions]]** — The "cross-arch compatibility varies by representation depth" tension is documented there
