---
type: source
title: "Communicating Activations Between Language Model Agents"
source_file: "[[raw/pdf/arxiv-2501.14082.pdf]]"
latex_source: "[[raw/latex/arxiv-2501.14082.tar.gz]]"
author: "Vignav Ramesh, Kenneth Li"
date_published: "2025-01-24"
date_ingested: "2026-04-06"
created: "2026-04-06"
venue: "ICML 2025"
arxiv: "2501.14082"
institution: "Kempner Institute, Harvard University"
tags: [activation-communication, multi-agent, training-free, residual-stream]
---

# Communicating Activations Between Language Model Agents

## One-liner

![[activation-communication-harvard/one-liner]]

## Summary

**Activation Communication (AC)**, from the [[harvard|Kempner Institute at Harvard]], is a simple, training-free protocol: pause model B's computation at intermediate layer j, replace B's **last-token activation** with model A's activation from layer k, then continue B's forward pass. Despite its simplicity — just replacing one vector at one layer — AC outperforms natural language debate on 48/57 MMLU datasets, 6/7 reasoning benchmarks, and uses **less than ¼ the compute**.

## Core Mechanism

Given models A (sender with context/knowledge) and B (receiver generating the answer):

1. Run B's forward pass **up to layer $j$**, yielding post-layer activation $h_{B,j} \in \R^{t_B \times d_B}$
2. Run A's **partial** forward pass up to layer $k$, yielding $h_{A,k} \in \R^{t_A \times d_A}$
3. **Replace B's last-token activation only**: $(h_{B,j})_{t_B} \leftarrow f((h_{A,k})_{t_A}, (h_{B,j})_{t_B})$
4. Continue B's forward pass from layer j+1 through to decoding completion

### Combination Functions

Three non-learned options (assuming $d_A = d_B$):

| Function | Formula | Performance | Why |
|----------|---------|-------------|-----|
| **Replace** | $f(a,b) = a$ | **Best** | Output stays in B's activation space; B retains all context in other token positions |
| Mean | $f(a,b) = (a+b)/2$ | Moderate | Dilutes both signals |
| Sum | $f(a,b) = a+b$ | Worst | Roughly doubles activation norm, pushing out of distribution |

For cross-family models ($d_A \neq d_B$), a **task-agnostic linear mapping** $W \in \R^{d_B \times d_A}$ projects A's activations into B's space. $W$ is trained once per model pair on 3072 C4 sentences (MSE loss, 10 epochs, Adam lr=0.001). This introduces **zero task-specific parameters** — the same W is used across all benchmarks.

### Why Layer 26 (of 32)?

The paper provides a 2D contour plot scanning all $(k,j)$ pairs $\in \{1,\ldots,30\}^2$. The optimum at $k = j = 26$ corresponds to the "**enriched entity representation**" layers identified by Hernandez et al. (2024):

- **Early layers (1-12)**: Embeddings are still being contextualized. Not yet informative enough for communication.
- **Mid-late layers (~20-26)**: "Enriched entity representations" — entities in the prompt have been populated with additional facts about them from the model's weights. This is the **richest** representation of the input.
- **Final layers (27-32)**: Representations are optimized for next-token prediction — information not needed for that narrow objective is discarded. Richer contextual knowledge is "thrown away."

This layer-depth finding aligns with [[kvcomm-kth-selective|KVComm]]'s hypothesis H1 (intermediate layers encode the most transferable semantic knowledge), despite the two papers approaching the problem from different angles.

## Key Results

### Multi-Player Coordination Games (same model, A = B)

| Model | Game | Silent ($\emptyset$) | Skyline | NL | AC (replace) |
|-------|------|-----------|---------|-----|-------------|
| LLaMA-3.2-3B | Countries | 0.0% | 84.0% | 69.0% | **78.0%** |
| LLaMA-3.2-3B | Tip Sheets | 38.6% | 100.0% | 74.3% | **90.0%** |
| LLaMA-3.1-8B | Countries | 2.0% | 86.0% | 77.0% | **83.0%** |
| LLaMA-3.1-8B | Tip Sheets | 54.3% | 100.0% | 85.7% | **95.7%** |

AC nearly closes the gap between zero-communication and the single-agent skyline, substantially outperforming NL communication.

### Cross-Model Reasoning (LLaMA-3.2-3B → LLaMA-3.1-8B)

| Benchmark | 3B alone | 8B alone | NLD | AC | AC(W) |
|-----------|----------|----------|-----|-----|-------|
| Biographies | 79.4% | 83.9% | 80.2% | **84.6%** | **86.8%** |
| GSM8k | 58.0% | 60.0% | **75.0%** | 64.0% | 66.0% |
| HS Psychology | 30.0% | 65.0% | 83.0% | **85.0%** | 70.0% |
| Formal Logic | 16.0% | 42.0% | 37.0% | **47.0%** | 35.0% |
| College Biology | 11.0% | 50.0% | 71.0% | **78.0%** | **79.0%** |
| Professional Law | 0.0% | 20.0% | **30.0%** | **30.0%** | **45.0%** |
| Public Relations | 26.0% | 53.0% | 63.0% | **74.0%** | 63.0% |

AC outperforms NLD on **6 of 7 benchmarks**, with up to **27.0% improvement** (Public Relations: 63%→74%; College Biology: 71%→78%). The learned mapping $W$ provides further gains on 4/7 datasets.

**Exception: GSM8K** — NLD (75%) beats AC (64%). Multi-step mathematical reasoning benefits from **iterative refinement** across debate rounds; single-shot activation grafting communicates knowledge but doesn't enable the back-and-forth error correction that debate provides. This highlights that AC and debate serve complementary functions.

### Full MMLU
AC matches or outperforms NLD on **48 of 57 MMLU datasets**. Average: AC 62.7% vs NLD 60.7%.

### Cross-Family Communication (no learned mapping W)

| Model Pair (A → B) | NLD (Bio/GSM) | AC (Bio/GSM) |
|---------------------|---------------|--------------|
| LLaMA-3.2-3B → LLaMA-3.1-8B | 80.2/75.0 | **84.6/64.0** |
| Qwen-2.5-1.5B → Qwen-2.5-3B | 63.2/65.0 | **89.6/70.0** |
| Gemma-2-2B → Gemma-2-9B | 70.3/70.0 | **88.1/90.0** |
| Qwen-2.5-1.5B → LLaMA-3.2-3B | 75.4/75.0 | **79.5/75.0** |
| LLaMA-3.2-3B → Gemma-2-2B | 62.5/55.0 | **84.0/60.0** |

AC works across LLaMA, Qwen-2.5, and Gemma-2 families **without** learned projections.  This is remarkable — these models have different tokenizers, vocabularies, training data, and architectures. The authors cite this as possible evidence for the **[[platonic-representation-hypothesis|Platonic Representation Hypothesis]]** (Huh et al., 2024): independently trained models may converge to similar internal representations of the same concepts.

### Compute Efficiency

Formal analysis shows AC requires:
- **A**: 1 partial forward pass (k/L of a full pass)
- **B**: 1 full forward pass
- **Total**: < ¼ the compute of NLD (which requires M full forward passes of A for an M-token message, plus T forward passes of B on the extended prompt)

The **performance-per-FLOP ratio** (slope of accuracy vs. compute) is consistently steeper for AC than NLD across model scales — AC achieves greater improvement per additional unit of compute.

### Directionality

Swapping A and B (smaller model does full forward pass) yields lower accuracy but still beats both single-model baselines and sometimes NLD. This is more compute-efficient since the smaller model does the full pass.

## Theoretical Insight: Why Activations Beat Tokens

The paper provides the strongest theoretical argument in this collection for why [[activation-communication]] should outperform [[embedding-space-communication]] and natural language:

1. **Activations are a strict superset of next-token predictions**: Late-layer activations encode the model's next-token prediction AND its belief distribution AND its enriched entity representations AND broader contextual knowledge. Token sampling keeps only the first; CIPHER keeps the first two; AC keeps everything.

2. **Final layers discard useful information**: Probe accuracy for various input properties rises through mid-layers, peaks around layer 20-26, then **drops** in final layers. The LM head is optimized for next-token prediction, not for preserving all contextual information. AC accesses the representations before this information is discarded.

3. **One-shot sufficiency**: Because activations encode "all of A's knowledge/beliefs about the prompt," there is no need for iterative rounds (unlike debate/CIPHER). One activation graft communicates everything. This is why AC is not iterative — and why it still loses to NLD on tasks where iterative refinement (not just knowledge transfer) is the key benefit.

## Ablation Insights

### Layer Choice Effects

The 2D contour plot scanning all $(k, j)$ pairs reveals that performance is sharply non-monotonic: the optimum at layer 26 (of 32) lies in the narrow "enriched entity representation" window. Early layers (1-12) produce activations that are too shallow for meaningful knowledge transfer — the sender's representations have not yet been contextualized with factual knowledge from model weights. Final layers (27-32) are too specialized for next-token prediction, discarding contextual information that isn't needed for the immediate decoding step. The drop-off on either side of the optimum is steep, with layers outside the 20-28 range yielding negligible improvement over no communication. This sensitivity to extraction depth is a critical design parameter that must be calibrated per model architecture.

### Number of Tokens Transferred

AC transfers exactly **one token's activation** — the last-token hidden state. This is sufficient because in decoder-only transformers, the last token position aggregates information from all prior positions via causal attention. The paper argues that multi-token transfer would be redundant (the receiver retains its own representations at all other positions) and potentially harmful (replacing non-final positions would corrupt the receiver's contextualization of its own prompt). The success of single-token transfer validates the information concentration hypothesis: late-layer last-token activations encode a compressed summary of the full input.

### Mapping Matrix W vs Raw Transfer

When sender and receiver share the same embedding dimension ($d_A = d_B$), raw replacement (no learned projection) works well, sometimes outperforming the learned mapping $W$. When dimensions differ, $W \in \R^{d_B \times d_A}$ is essential. Notably, $W$ is trained task-agnostically on 3072 C4 sentences with MSE loss — a generic corpus unrelated to any evaluation benchmark. Despite this, $W$ provides further gains on 4/7 cross-model benchmarks, suggesting that the mapping captures general structural correspondence between latent spaces rather than task-specific alignment. On 3/7 benchmarks $W$ slightly hurts performance compared to raw transfer, indicating that the MSE-optimal linear mapping does not always preserve the task-relevant subspace of the activation manifold. The trade-off between raw and projected transfer depends on how closely the models' representation geometries align — models from the same family benefit less from $W$ than cross-family pairs.

## Positioning on the Communication Spectrum

AC introduces a critical distinction: **what matters is not just the depth of representation but the layer at which you extract it**. The [[embedding-space-communication]] spectrum should be understood not as "deeper = better" but as a two-dimensional space:

| Method | Representation depth | Extraction point | Information content |
|--------|---------------------|-----------------|-------------------|
| CIPHER | Output layer | After softmax | Next-token belief distribution |
| KVComm | Attention layer | Per-layer KV pairs | Layer-specific attention context |
| **AC** | **Residual stream** | **Mid-late layer (~26/32)** | **Enriched entity representations** |
| [[thought-communication-multiagent\|ThoughtComm]] | Latent factors | Autoencoder output | Disentangled thoughts |

## Limitations

- **Requires aligned embedding spaces** (when not using W). Less restrictive than CIPHER's shared-tokenizer requirement, but still limits applicability. Relaxed by learned W.
- **Requires access to model internals** — incompatible with black-box API models.
- **Limited interpretability** — activations are not human-readable. The authors suggest a future direction: "translating" activations by observing the beliefs they induce in receiving agents.
- **GSM8K underperformance** — multi-step math reasoning benefits from iterative refinement, not single-shot knowledge transfer.
- **W training domain sensitivity** — the mapping matrix trained on C4 data has variable effectiveness depending on test domain similarity.

## Connections

- **[[activation-communication]]**: This is the **definitive empirical paper** for the concept. It validates that raw activation transfer works, identifies the optimal layer depth (mid-late), establishes the enriched entity representation theory, and demonstrates cross-family communication without learned projections.
- **[[cipher-multiagent-debate-embeddings|CIPHER]]**: AC communicates a "strict superset" of CIPHER's information. CIPHER uses probability-weighted output embeddings; AC uses intermediate activations that encode richer information. AC also saves compute (partial forward pass vs. CIPHER's full sequential generation).
- **[[kvcomm-kth-selective|KVComm]]**: Both find that intermediate layers are most informative for communication. KVComm found hidden states suffer from information concentration bias on the last token; AC confirms this but argues replace-at-one-layer is sufficient because B retains its own representations at other positions. KVComm advocates for KV pairs (attention-native integration); AC advocates for residual-stream activations (richer per position, but more invasive replacement).
- **[[state-delta-trajectory|SDE]]**: SDE refines AC's approach for same-model settings by using **deltas** (inter-token differences) instead of raw states, avoiding context contamination. AC works cross-model; SDE works same-model only.
- **[[interlat-latent-space-agents|Interlat]]**: Extends AC from single-vector replacement to full-sequence hidden-state transmission with a learned communication adapter.
- **[[continuous-vs-discrete-representation]]**: AC provides the clearest empirical case that continuous activations beat discrete text at a fraction of the compute.
- **[[platonic-representation-hypothesis|Platonic Representation Hypothesis]]**: Cross-family AC results without learned mappings suggest independently trained models develop similar internal representations — a profound implication for the universality of latent communication.

## Source Materials

- [[raw/pdf/arxiv-2501.14082.pdf|PDF]] ([[raw/latex/arxiv-2501.14082.tar.gz|LaTeX source]])
