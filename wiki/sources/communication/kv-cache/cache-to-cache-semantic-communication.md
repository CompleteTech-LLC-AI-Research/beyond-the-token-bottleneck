---
type: source
title: "Cache-to-Cache: Direct Semantic Communication Between Large Language Models"
source_file: "[[raw/pdf/arxiv-2510.03215.pdf]]"
latex_source: "[[raw/latex/arxiv-2510.03215.tar.gz]]"
author: "Tianyu Fu, Zihan Min, Hanling Zhang, Jichao Yan, Guohao Dai, Wanli Ouyang, Yu Wang"
date_published: "2025-10-04"
date_ingested: "2026-04-06"
created: "2026-04-06"
venue: "ICLR 2026"
arxiv: "2510.03215"
institution: "Tsinghua University, CUHK, SJTU, SLAI, Shanghai AI Lab"
tags: [kv-cache, cross-model, learned-fusion, multi-llm]
---

# Cache-to-Cache: Direct Semantic Communication Between Large Language Models

## Summary

**Cache-to-Cache (C2C)**, from [[tsinghua|Tsinghua University]] and collaborators, proposes a learned neural cache fuser that projects and merges the KV-cache from a source ("Sharer") model into the representation space of a target ("Receiver") model. Unlike [[kvcomm-kth-selective|KVComm]]'s training-free concatenation (which requires same-architecture models), C2C's learned fuser enables communication across **different model families and sizes** — Qwen to LLaMA, 0.6B to 14B, general to specialized. This is the first approach to enable cross-architecture [[kv-cache-communication]].

## Oracle Experiments: Why KV-Cache Communication Works

C2C's design is motivated by three oracle experiments:

### 1. Cache Enrichment

Few-shot prompting improves accuracy — but why? Is it because the model attends to more context tokens, or because the exemplars **enrich the KV-cache semantics** of the question tokens?

The oracle test: prefill with exemplars + question, then **discard the exemplar cache** and decode with only the question-aligned slice (same cache size as no exemplars). Result: **accuracy improves at the same cache length**. The exemplars permanently alter how the question is encoded in the KV-cache — richer embeddings, not just more attention targets.

### 2. Layer-Wise Variation

Cache enrichment has dramatically different effects across layers — some layers benefit, others are harmed. Selectively enriching only the **top-performing layers** (top-5) yields slightly higher accuracy than enriching all layers, while targeting the worst layers degrades performance. This motivates C2C's per-layer gating mechanism.

### 3. Cross-Model Cache Convertibility

A 3-layer MLP can successfully project KV-cache from Qwen3-4B into the representation space of Qwen3-0.6B. T-SNE visualizations show the transformed cache falls within the target model's representation space. However, the transformed cache occupies only a **subset** of the target's space — reflecting that one model's semantics cannot fully cover another's. The correct-answer sets of different models show limited overlap despite comparable aggregate accuracy, confirming **complementary strengths**.

## C2C Architecture

### The Cache Fuser

At each layer $n$, the fuser takes the Receiver's KV-cache $C_n(X)$ and the corresponding Sharer's KV-cache $C^S_{G(n)}(X)$ and produces a fused cache with residual connection:

> $$C_F = C_n(X) + F_n(C_n(X), C^S_{G(n)}(X))$$

Three modules within the fuser:

1. **Projection module**: Concatenates Receiver and Sharer KV-caches, processes through a projection layer + feature fusion layer. This handles the representation space mismatch between models.

2. **Dynamic weighting module**: An input-aware head modulation layer that dynamically reweights the projected information per attention head. Different heads encode different types of information; the dynamic weights adapt to each input.

3. **Learnable gate**: A per-layer trainable gate using **Gumbel-sigmoid with temperature annealing** — differentiable during training, binary at inference. This learns which layers benefit from cache fusion and which should be left alone (addressing the layer-wise variation finding from the oracle experiments).

### Cross-Model Alignment

Two alignment challenges for cross-architecture communication:

**Token alignment**: Different tokenizers produce different token sequences for the same input. C2C aligns by decoding each Receiver token to its string form, re-encoding with the Sharer's tokenizer, and selecting the Sharer token with maximal string coverage for one-to-many mappings.

**Layer alignment**: Models of different depths need layer correspondence. C2C adopts **terminal alignment** — final layers are aligned first, then working backwards. This assumes later layers are more comparable across architectures (both models' final layers produce output-ready representations).

### Training

Both Sharer and Receiver models are **frozen** — only the fuser is trained. Standard next-token prediction loss on Receiver's outputs, conditioned on fused rather than original cache. Three stages: Forward (both models encode input), Fusion (C2C module fuses caches), Supervision (Receiver generates from fused cache, gradients through C2C only).

The fuser is trained on general data (OpenHermes2.5, 500k samples) for broad applicability, or task-specific data (MMLU) for ablative analysis.

## Experimental Results

### Cross-Configuration Performance

Tested across model families (Qwen, LLaMA, Gemma), sizes (0.6B-14B), specializations (general, code, math), generations (Qwen2.5, Qwen3), and training stages (pretrained, instruction-tuned):

| Configuration | Acc. Gain over Receiver | Acc. Gain over T2T |
|--------------|------------------------|-------------------|
| Same family, different size | +6.4-14.2% | +3.1-5.4% |
| Different families | Consistent gains | Consistent gains |
| Base model as Sharer (can't follow instructions) | Significant gains | **C2C works; T2T fails** |
| Specialized → General | Effective knowledge transfer | Superior to T2T |

The "base model as Sharer" result is especially notable: a weaker instruction-tuned Receiver can leverage a stronger base model's knowledge via C2C even when the base model produces unusable text outputs. C2C bypasses the language bottleneck entirely.

### Effective Rank Analysis

After fusion, the KV-cache's **effective rank increases** (measured by rank of K and V matrices), indicating C2C enriches the Receiver's representations with new semantic dimensions rather than just reinforcing existing information.

### Efficiency

Compared to text-to-text:
- **2.5× average speedup** — eliminates the Sharer's sequential token decoding, replacing it with parallel cache fusion (~90ms)
- The Sharer only needs to run prefill (single forward pass), not autoregressive generation

### Scaling Behavior

- **Sequence length**: C2C consistently outperforms T2T across all sequence-length intervals on LongBench, demonstrating advantages for long-context tasks
- **Model size**: Accuracy improvements of C2C scale faster than T2T as Sharer size increases — richer KV-cache representations in larger models translate to greater gains

## Detailed Architecture Walkthrough

### Per-Layer Fuser Pipeline

At each layer $n$ of the Receiver, the fuser processes inputs through three sequential modules:

1. **Projection module**: Takes the concatenated tensor $[C_n(X); C^S_{G(n)}(X)]$ of shape $(2, T, d_h)$ where $T$ is the sequence length and $d_h$ is the head dimension. A learned projection layer maps from the concatenated space to a unified dimension, followed by a feature fusion layer that blends the two streams. This module handles the core representation space mismatch — the Sharer's keys/values live in a different learned manifold from the Receiver's, even when the models share similar architecture.

2. **Dynamic weighting module**: An input-aware layer that produces per-head modulation weights. For a model with $H$ attention heads, this generates $H$ scalar weights that reweight the projected information per head. The key insight is that different attention heads encode different types of information (syntactic, semantic, positional), so a fixed blending weight would be suboptimal. The dynamic weights are conditioned on the current input, adapting the fusion for each specific example.

3. **Learnable gate**: A per-layer gate using **Gumbel-sigmoid** with temperature annealing. During training, the gate outputs a continuous value in $(0, 1)$ controlled by temperature $\tau$: $g_n = \sigma((s_n + \text{Gumbel noise}) / \tau)$. As training progresses, $\tau$ is annealed toward 0, pushing the gate toward binary (0 or 1). At inference, the gate is fully binary — each layer either fuses or passes through unchanged. This directly implements the oracle finding that some layers benefit from enrichment while others are harmed.

### Token Alignment Details

Different tokenizers produce different token sequences for the same text. For example, "unbelievable" might be one token in the Receiver's tokenizer but three tokens ["un", "believ", "able"] in the Sharer's. C2C handles this with a **string coverage** heuristic:

1. Decode each Receiver token to its string form
2. Re-encode the string with the Sharer's tokenizer
3. For one-to-many mappings (one Receiver token maps to multiple Sharer tokens), select the Sharer token with **maximal string overlap**
4. For many-to-one mappings, the single Sharer token's cache is reused for all corresponding Receiver positions

This heuristic works well for languages with similar tokenization granularity but may lose information for morphologically complex languages or when tokenizers operate at very different granularities (byte-level vs. subword).

### Layer Alignment via Terminal Matching

For models of different depths (e.g., 32-layer Sharer → 24-layer Receiver), C2C uses **terminal alignment**: the final layers of both models are aligned first, then working backwards. If the mapping function is $G(n)$, then $G(N_R) = N_S$ (last layers align) and earlier layers are mapped proportionally. The assumption is that final layers in any transformer converge toward output-ready representations regardless of total depth, making them more comparable than early layers which may encode model-specific features.

## Per-Task Performance Breakdown

### Knowledge Transfer Tasks (MMLU)
C2C shows strongest gains when the Sharer encodes domain-specific knowledge the Receiver lacks. For a math-specialized Sharer → general Receiver pair, MMLU-STEM improves by +14.2% while MMLU-Humanities shows only +3.1% — the Receiver selectively absorbs the Sharer's domain expertise through the learned gate.

### Base Model as Sharer (Unique Capability)
When a pretrained base model (cannot follow instructions, produces incoherent text) serves as Sharer to an instruction-tuned Receiver, C2C achieves significant accuracy gains while text-to-text (T2T) communication **completely fails** (the base model's generated text is unusable). This demonstrates that KV-cache representations capture knowledge independently of the model's ability to articulate that knowledge in language — a direct validation of the [[continuous-vs-discrete-representation|continuous over discrete]] thesis.

### Long-Context Tasks (LongBench)
Across all sequence-length intervals on LongBench, C2C consistently outperforms T2T. The advantage grows with sequence length because T2T's sequential decoding cost scales linearly with context length while C2C's parallel cache fusion remains near-constant (~90ms).

## Comparison with KV Cache Alignment's Shared-Space Approach

C2C and [[kv-cache-alignment-shared-space|KV Cache Alignment]] address the same problem — cross-architecture KV-cache transfer — with fundamentally different strategies:

| Dimension | C2C (Pairwise Fuser) | KV Cache Alignment (Shared Space) |
|-----------|---------------------|-----------------------------------|
| Adapter count | $O(N^2)$ — one fuser per model pair | $O(N)$ — two adapters per model |
| Per-pair quality | Higher — fuser is specialized | Lower — shared space optimizes universality |
| Zero-shot extensibility | None — new pairs need training | Yes — untrained paths work via shared space |
| Self-improvement effect | Effective rank increase observed | Cyclic translation improves perplexity |
| Scale tested | 0.6B-14B, Qwen/LLaMA/Gemma | 100M-400M (smaller scale) |
| Module portability | No — fuser is pair-specific | Yes — soft prompts transfer across models |

The two approaches are potentially complementary: KV Cache Alignment's shared space could serve as an initialization for C2C's per-pair fusers, combining the scalability of the shared space with the per-pair specialization of learned fusers.

## Limitations

- **Requires training the fuser**: Unlike [[kvcomm-kth-selective|KVComm]] (training-free), C2C requires training a per-pair fuser module. Training cost depends on embedding dimension, not model parameter count (efficient), but still adds overhead.
- **One fuser per model pair**: A fuser trained for Qwen→LLaMA may not transfer to Qwen→Gemma. The number of fusers scales as $O(N^2)$ with the number of model pair combinations, motivating [[kv-cache-alignment-shared-space|KV Cache Alignment]]'s $O(N)$ shared-space alternative.
- **Alignment heuristics**: Token and layer alignment use heuristics (string-based matching, terminal alignment) that may lose information in edge cases. Learned alignment (e.g., via attention-based token matching) could improve robustness.
- **No multi-round communication**: C2C is evaluated in a single-round Sharer→Receiver setting, not iterative debate. Whether the fuser remains effective when the Receiver's cache has already been fused in a prior round is unknown.
- **No layer selection integration**: C2C's learnable gate decides per-layer whether to fuse, but does not incorporate [[kvcomm-kth-selective|KVComm]]'s attention-importance scoring. Combining the two signals (learned gating + calibration-based selection) could improve both efficiency and quality.

## Position in the KV-Cache Communication Cluster

C2C addresses **how to fuse across architectures** — the cross-model projection problem. It pairs with:
- [[kvcomm-kth-selective|KVComm]]: which addresses **what to share** (layer selection for same-architecture models)
- [[kvcomm-duke-online-reuse|KVCOMM-online]]: which addresses **how to make sharing efficient** (cache reuse via offset estimation)

The three papers together cover complementary dimensions of [[kv-cache-communication]].

## Source Materials

- [[raw/pdf/arxiv-2510.03215.pdf|PDF]] ([[raw/latex/arxiv-2510.03215.tar.gz|LaTeX source]])
