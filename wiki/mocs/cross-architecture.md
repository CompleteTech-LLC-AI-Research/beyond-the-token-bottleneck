---
type: overview
title: "Cross-Architecture Compatibility"
created: "2026-04-06"
updated: "2026-04-06"
tags: [moc, cross-architecture, compatibility]
---

# Cross-Architecture Compatibility

The central tension in latent communication: **deeper channels carry more information but demand tighter architectural coupling**. Natural language works between any two models; raw activation sharing barely works between two training runs of the same architecture. This MOC traces how the field is trying to bend that curve — achieving deep, information-rich communication across heterogeneous model families.

## Reading Path

### 1. The Problem Statement

Start with the depth-compatibility trade-off laid out in [[embedding-space-communication]]. The spectrum table shows the cost clearly: [[cipher-multiagent-debate-embeddings|CIPHER]] requires a **shared tokenizer**, [[kvcomm-selective-kv-sharing|KVComm]] requires **identical architecture**, and [[state-delta-trajectory|SDE]] requires **identical weights**. Each step deeper in the transformer stack narrows the set of compatible partners. The [[open-questions|open questions]] frame cross-architecture compatibility as the field's major unsolved problem.

### 2. Why Cross-Model Communication Works at All

Two theoretical papers explain why independently trained models can share internal representations:

- **[[platonic-representation-hypothesis|The Platonic Representation Hypothesis]]** (Huh et al., ICML 2024) — Models across architectures, objectives, and modalities are **converging toward a shared statistical model of reality**. Higher-performing models align more tightly. The implication: cross-model communication should get *easier* with scale, not harder.

- **[[relative-representations-zero-shot|Relative Representations]]** (Moschella et al., ICLR 2023) — The practical complement. Well-trained models produce latent spaces related by approximately **angle-preserving transforms**. Representing data as cosine similarities to shared anchors makes representations invariant to rotations/reflections, enabling zero-shot stitching. The same underlying observation — that well-trained models differ by approximately orthogonal transforms — also explains why simple linear projections suffice for methods like AC and C2C. Cross-architecture stitching jumps from 6% to 80%+ accuracy.

Together they predict that a simple affine correction should bridge most model pairs — and the empirical results confirm it.

Note the counter-case: **[[latentmas-collaboration|LatentMAS]]** demonstrates what happens when you *don't* solve cross-architecture compatibility. Its training-free KV-cache transfer works well within homogeneous pools (Qwen-family), but catastrophically fails on LLaMA (-10.1% average), illustrating how same-architecture assumptions break down across families.

### 3. Shared Tokenizer Baseline (CIPHER)

**[[cipher-multiagent-debate-embeddings|CIPHER]]** is the shallowest cross-model method. By transmitting probability-weighted embedding averages, it avoids the sampling bottleneck while staying within the vocabulary's convex hull. But it requires a **shared tokenizer** — models must segment text identically and share an embedding matrix. Cross-model debate between LLaMA2-70B and LLaMA-65B works because they share a tokenizer; cross-model debate with Falcon or MPT is out of reach (though CIPHER works in same-model debate for both).

### 4. Learned Linear Mappings (AC)

**[[activation-communication-harvard|Activation Communication]]** breaks the tokenizer barrier. A single **task-agnostic linear mapping** W, trained on 3,072 C4 sentences, projects activations between model families. Cross-family results (LLaMA, Qwen, Gemma) work even **without** W — raw activation replacement transfers knowledge across families with zero learned parameters. This is the strongest empirical evidence for the [[platonic-representation-hypothesis|Platonic Representation Hypothesis]].

### 5. Learned Pairwise Fusers (C2C)

**[[cache-to-cache-semantic-communication|Cache-to-Cache]]** tackles cross-architecture at the KV-cache level. A learned **neural cache fuser** projects the sender's KV-cache into the receiver's representation space with per-layer gating. Works across Qwen, LLaMA, and Gemma families at 0.6B-14B scale. The cost: one fuser per model pair, scaling $O(N^2)$ with pool size. The payoff: even base models that produce unusable text can serve as knowledge sources, bypassing the language interface entirely.

### 6. Shared Latent Spaces (KV Cache Alignment)

**[[kv-cache-alignment-shared-space|KV Cache Alignment]]** solves C2C's quadratic scaling via an **interlingua** architecture. Each model gets two adapters (into and out of a global shared KV-cache space), scaling **O(N)** with pool size. New models join by training two adapters; untrained paths work zero-shot. The shared space also enables **module portability** — soft prompts learned on one model transfer to another. Current limitation: validated only at 100M-400M scale.

### 7. Architectural Bypass (Vision Wormhole)

**[[vision-wormhole-heterogeneous|Vision Wormhole]]** sidesteps the representation alignment problem entirely. Instead of projecting between incompatible hidden-state spaces, it routes communication through the **visual input pathway** of VLMs — a channel explicitly designed to accept dense continuous vectors. A hub-and-spoke affine alignment (ridge regression on anchor texts) maps between model-specific universal tokens, scaling O(N). Achieves +6.3pp accuracy and 1.87x speedup over text-based MAS at the small-model scale (1.6B-4B) across fully heterogeneous pools (Gemma, Qwen, SmolVLM, LFM). Mid-sized models (4B-12B) show dramatic speedups (5.92x) but accuracy degrades, suggesting the fixed bandwidth bottleneck limits scaling.

## Compatibility Spectrum

Methods ranked by cross-architecture support, from most restrictive to most general:

| Method | Cross-Arch Support | Alignment Cost | Scaling | Key Limitation |
|--------|-------------------|----------------|---------|----------------|
| [[state-delta-trajectory\|SDE]] | Same weights only | None | N/A | Deltas only meaningful in shared weight space |
| [[kvcomm-selective-kv-sharing\|KVComm]] | Same architecture | None (training-free) | N/A | Requires identical layer structure |
| [[cipher-multiagent-debate-embeddings\|CIPHER]] | Shared tokenizer | None | N/A | Different tokenizers produce incompatible embeddings |
| [[activation-communication-harvard\|AC (no W)]] | Cross-family | None | N/A | Assumes roughly aligned activation spaces |
| [[activation-communication-harvard\|AC (with W)]] | Cross-family | 1 linear map per pair | $O(N^2)$ | 3,072 calibration sentences per pair |
| [[interlat-latent-space-agents\|Interlat]] | Cross-family | 1 adapter per model | O(N) | Requires adapter training (curriculum learning) |
| [[cache-to-cache-semantic-communication\|C2C]] | Cross-family + cross-size | 1 neural fuser per pair | $O(N^2)$ | Fuser training overhead |
| [[kv-cache-alignment-shared-space\|KV Cache Alignment]] | Cross-family + cross-size | 2 adapters per model | **O(N)** | Validated at small scale only |
| [[vision-wormhole-heterogeneous\|Vision Wormhole]] | Fully heterogeneous VLMs | 1 codec per model + ridge regression | **O(N)** | Requires VLM receivers |

## Connections

- **[[latent-communication]]** — The broader communication landscape; this MOC zooms in on the compatibility dimension
- **[[communication-depth-spectrum]]** — The 10-level depth walkthrough that defines the trade-off this MOC addresses
- **[[unified-frameworks]]** — Vision Wormhole and KV Cache Alignment appear there as systems combining reasoning + communication
- **[[open-questions]]** — The "Cross-Architecture Compatibility" section catalogs the unsolved problems
- **[[contradictions]]** — The "cross-arch compatibility varies by representation depth" tension is documented there
