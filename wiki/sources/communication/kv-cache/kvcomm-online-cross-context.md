---
type: source
title: "KVCOMM: Online Cross-context KV-cache Communication for Efficient LLM-based Multi-agent Systems"
source_file: "[[raw/pdf/arxiv-2510.12872.pdf]]"
latex_source: "[[raw/latex/arxiv-2510.12872.tar.gz]]"
venue_pdfs: ["[[raw/pdf/openreview-yGOytgjurF.pdf|OpenReview]]"]
author: "Hancheng Ye, Zhengqi Gao, Mingyuan Ma, Qinsi Wang, Yuzhe Fu, Ming-Yu Chung, Yueqian Lin, Zhijian Liu, Jianyi Zhang, Danyang Zhuo, Yiran Chen"
date_published: "2025-10-16"
date_ingested: "2026-04-06"
created: "2026-04-06"
venue: "NeurIPS 2025"
arxiv: "2510.12872"
institution: "Duke University, MIT, NVIDIA"
tags: [kv-cache, efficiency, cache-reuse, training-free, systems]
---

# KVCOMM: Online Cross-context KV-cache Communication for Efficient LLM-based Multi-agent Systems

## Summary

While [[kvcomm-selective-kv-sharing|KVComm]] and [[cache-to-cache-semantic-communication|C2C]] focus on **what** and **how** to communicate via KV-cache, this paper from Duke University, [[mit|MIT]], and NVIDIA tackles a different problem: **computational efficiency** of KV-cache operations in multi-agent systems. When multiple agents share overlapping context (e.g., the same user query, same retrieved documents), each agent redundantly recomputes KV-caches for the shared text under its own prefix context. KVCOMM eliminates this redundancy by **reusing KV-caches** across agents with different prefixes, estimating and correcting the context-dependent offsets introduced by different system prompts and conversation histories.

This is a **systems-level optimization** paper rather than a communication paradigm paper — it doesn't change what information is communicated, but makes the existing prefilling pipeline dramatically faster.

## The Problem: Multi-Context Redundancy

In a multi-agent system modeled as a directed graph, agents exchange messages. When Agent 2 receives a message from Agent 1, it must prefill its entire prompt — including Agent 1's message, which Agent 1 already computed KV-caches for. But Agent 2 has a different system prompt (prefix), so Agent 1's cached KVs cannot be directly reused: the same text produces different KV representations under different prefix contexts due to attention's context-dependence.

### Scaling Problem

If each of M agents receives messages from all peers, total prefilling complexity scales as **O(M²)** — each agent recomputes KV-caches for every peer's shared context. For a 5-agent system with 3K-token prompts on Llama-3.1-8B: 430ms × 25 = 10.75 seconds of redundant prefilling.

### The Offset-Variance Problem

The same shared text produces different KV-caches depending on what prefix precedes it. The key insight: this difference is a **context-dependent offset** — a relatively structured deviation that can be estimated from similar prior examples rather than recomputed from scratch.

## Key Insight: KV-Cache Offset Predictability

### Theoretical Foundation

Two propositions formalize why offset estimation works:

**Proposition 1 (KV Distance Between Tokens)**: The KV-cache distance between two different tokens at the same position under the same prefix is bounded by their embedding gap, scaled through transformer layers via Lipschitz constants. Tokens closer in embedding space have more similar KV-caches.

**Proposition 2 (Deviation Proximity Under Different Prefixes)**: The difference in KV-cache offsets (when switching from prefix A to prefix B) between two embedding-similar tokens is also bounded. This means: if you know how token X's KV-cache changes from prefix A to B, you can estimate how a similar token Y changes — **offsets are transferable between similar tokens**.

### Empirical Validation

- KV-cache proximity is **highly correlated** with token embedding distance (Spearman correlation)
- KV-cache offset proximity (under different prefixes) also correlates with embedding distance
- After RoPE positional de-rotation, Key cache offsets become much smaller and more predictable

### RoPE Positional Alignment

A critical technical detail: RoPE (Rotary Position Embedding) applies position-dependent rotations to Key vectors. When a token appears at position n in one prompt but n+δ in another, the raw Key difference is dominated by the rotational shift, which is orders of magnitude larger than the contextual offset. KVCOMM **always de-rotates Keys** before computing/applying offsets, isolating the true contextual deviation.

## The KVCOMM Framework

### Architecture

The system maintains an **anchor pool** — a collection of previously seen KV-cache samples along with their measured offsets under various prefix contexts.

**Workflow per agent per request:**

1. **Prefix precomputation**: Before any requests, agents precompute KV-caches for their fixed prompt template prefixes
2. **Shareability check**: When a request arrives, check if each placeholder's base KV-cache exists and whether anchors cover the current context
3. **If shareable**: Fetch matched anchors, estimate offsets via embedding-weighted interpolation, update KV-caches in parallel
4. **If not shareable**: Fall back to standard dense prefilling; store the new KV-caches as anchor entries for future reuse
5. **Decode**: Concatenate updated KV-caches, proceed with normal autoregressive decoding

### Anchor Pool Design

Each anchor stores:
- **Base KV-cache**: The KV-cache computed independently (without external context)
- **Placeholder offsets**: The difference between base and actual KV-cache within each agent's context
- **Prefix offsets**: Offsets of neighboring prefix segments (important due to position-dependent shifts)

### Anchor Matching

Matching uses two criteria:
- **Embedding proximity**: New samples must be close to existing anchors in embedding space (validated by Proposition 2)
- **Length compatibility**: Sequence lengths must be compatible for correct positional alignment

### Offset Approximation

For matched anchors, the KV-cache for a new prefix context is estimated as:

> **Key update**: De-rotate stored Key to correct position, add interpolated offset, re-rotate
> **Value update**: Add interpolated offset directly (no positional information in Values)

Offsets are interpolated from matched anchors weighted by embedding-distance-based softmax weights.

### Online Adaptation

The anchor pool is maintained and updated dynamically:
- New unmatched samples become new anchors
- Least-frequently-accessed anchors are pruned when pool exceeds capacity V
- The pool adapts to the input distribution over time

## Experimental Results

### Efficiency Gains

| Setting | Prefill Speedup | Reuse Rate |
|---------|----------------|------------|
| 2 agents, GSM8K | 2.5× | 95% |
| 3 agents, GSM8K | 4.2× | 95% |
| 4 agents, GSM8K | 6.1× | 95% |
| 5 agents, GSM8K (512 prefix, 1K input) | **7.8×** | 95% |
| Average across workloads | **6.7×** | **70%+** |

TTFT (Time to First Token) drops from 430ms to 55ms in the 5-agent setting.

### Quality Preservation

| Dataset | Original Accuracy | KVCOMM Accuracy | Drop |
|---------|------------------|-----------------|------|
| MMLU (5 agents) | 69.9% | 69.9% | 0.0% |
| GSM8K (4 agents) | 68.0% | 66.6% | <2.5% |
| HumanEval (3 agents) | Pass@1 maintained | Comparable | Minimal |

KVCOMM achieves **>70% reuse rate** across diverse workloads (RAG, math reasoning, collaborative coding) with negligible quality degradation.

### Comparison to CacheBlend

CacheBlend (selective recomputation baseline) achieves similar reuse rates but uses a fixed acceleration policy that doesn't adapt to varying prefix contexts. KVCOMM's online anchor-based approach adapts dynamically, maintaining quality across diverse prefix variations.

## Ablation Insights

### Anchor Pool Size

The anchor pool capacity $V$ governs the trade-off between approximation quality and GPU memory consumption. With a small pool, matched anchors may be distant in embedding space from the current input, producing larger offset estimation errors. As the pool grows, the likelihood of finding a close embedding-space neighbor increases, tightening the approximation bound from Proposition 2. The reuse rate (>70% across workloads) indicates that the pool reaches sufficient coverage quickly — most real-world queries fall within embedding neighborhoods of previously seen inputs. The LFU (least-frequently-used) pruning strategy ensures the pool adapts to the actual input distribution, retaining anchors that cover high-traffic regions of the embedding space while discarding rare outliers. A pool that is too large wastes GPU memory storing anchors that are rarely matched; a pool that is too small forces frequent fallback to dense recomputation, reducing the effective speedup.

### Offset Estimation Variants

The offset estimation relies on three key design choices, each of which affects quality:

1. **RoPE de-rotation**: Without removing the position-dependent rotational component from Key vectors, the raw KV-cache difference is dominated by positional shift artifacts that are orders of magnitude larger than the true contextual offset. De-rotation isolates the semantic deviation, making offsets small and predictable. This step is critical — without it, the interpolation-based approximation would fail because the positional component varies non-smoothly with position differences.

2. **Embedding-weighted interpolation**: Offsets from matched anchors are combined via softmax weights derived from embedding distances. This prioritizes anchors that are semantically closest to the current input, consistent with the theoretical bound that offset transferability scales inversely with embedding distance. Alternative schemes (uniform averaging, nearest-single-anchor) would lose the smooth interpolation property that makes the approximation robust when no single anchor is a close match.

3. **Separate Key/Value handling**: Keys require de-rotation before offset application and re-rotation after, while Values are offset-corrected directly (no positional encoding). This asymmetry reflects the architectural difference: RoPE is applied only to Keys in standard transformer implementations. Treating Keys and Values identically would introduce spurious rotational artifacts in the Value cache.

## Limitations

- **Same model only**: All agents must run the same model checkpoint (same architecture, same weights). No cross-model communication.
- **Efficiency focus, not quality**: KVCOMM doesn't improve communication quality (unlike [[kvcomm-selective-kv-sharing|KVComm]] or [[cache-to-cache-semantic-communication|C2C]]). It makes existing multi-agent pipelines faster without changing what's communicated.
- **Anchor pool memory**: Storing base KV-caches and offsets for multiple anchors consumes GPU memory. The pruning strategy mitigates this but adds complexity.
- **Approximation errors accumulate**: In deep agent graphs with many hops, offset approximation errors could potentially compound.

## Position in the KV-Cache Communication Cluster

KVCOMM-online addresses **how to make KV operations efficient** — the systems optimization dimension. It's orthogonal to and composable with:
- [[kvcomm-selective-kv-sharing|KVComm]]: Could select layers first, then apply offset-based reuse for selected layers
- [[cache-to-cache-semantic-communication|C2C]]: Could apply offset estimation to reduce the fuser's input computation

See [[kv-cache-communication]] for the unified concept page.

## Source Materials

- [[raw/pdf/arxiv-2510.12872.pdf|PDF]] ([[raw/latex/arxiv-2510.12872.tar.gz|LaTeX source]])
