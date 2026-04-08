---
type: source
title: "KVComm: Enabling Efficient LLM Communication through Selective KV Sharing"
source_file: "[[raw/pdf/arxiv-2510.03346.pdf]]"
latex_source: "[[raw/latex/arxiv-2510.03346.tar.gz]]"
author: "Xiangyu Shi, Marco Chiesa, Gerald Q. Maguire Jr., Dejan Kostić"
date_published: "2025-10-04"
date_ingested: "2026-04-06"
created: "2026-04-06"
venue: "ICLR 2026"
arxiv: "2510.03346"
institution: "KTH Royal Institute of Technology"
tags: [kv-cache, layer-selection, multi-agent, training-free]
---

# KVComm: Enabling Efficient LLM Communication through Selective KV Sharing

## Summary

This paper, from [[kth|KTH Royal Institute of Technology]], proposes **KVComm**, a training-free communication protocol where a sender model shares **selected layers' KV pairs** with a receiver model. The receiver concatenates the sender's KV pairs with its own at each selected layer, integrating the information through its native attention mechanism. The core contribution is a principled **layer selection strategy** that identifies which layers carry the most transferable semantic information, achieving near-upper-bound performance while transmitting as few as 30% of layers' KV pairs.

## Why KV Pairs Over Hidden States

The paper begins with a systematic analysis of why hidden states are a poor communication medium, directly challenging the [[activation-communication]] approach:

### Information Concentration Bias

Experiments reveal that in decoder-only LLMs, the **last token's hidden state** becomes increasingly dominant in later layers — it concentrates most of the information needed for the model's output. This creates a dilemma for hidden-state communication:
- **Transmitting only the last token's hidden state** (as in AC/Ramesh & Li, 2025): Loses all other positional information. Replacing the receiver's last token state with the sender's corrupts the receiver's own context.
- **Transmitting all tokens' hidden states**: Only effective if taken from early layers and prepended to early layers of the receiver. If taken from late layers (where most computation savings would come), performance drops sharply. If taken from early layers, the computation savings are minimal.

### Why KV Pairs Avoid This

KV pairs are the **attention-native** representation — the receiver integrates them through its standard attention mechanism, attending to the sender's cached representations alongside its own. This is non-destructive: the receiver's own hidden states are never replaced or corrupted. The receiver decides via attention how much weight to place on the sender's information at each position.

## Layer Selection Strategy

### Two Hypotheses

**H1 — Intermediate layers carry transferable knowledge**: Prior work (Jawahar et al., 2019; Geva et al., 2020) shows a layer hierarchy:
- **Early layers** (1-10): Surface patterns, syntactic features — too shallow for semantic transfer
- **Middle layers** (10-20): Semantic abstractions, relational information — most transferable
- **Late layers** (20+): Task-specific predictions — too specialized, may conflict with receiver's own late processing

**H2 — High-attention layers are more informative**: Layers where the attention mechanism allocates more weight to context tokens encode more salient contextual relations. Attention concentration serves as a proxy for the communication value of a KV subset.

### The Selection Score

For each layer $l$, the attention importance score is computed as the average attention weight assigned to context tokens across all heads and query positions:

> $$\hat{S}_{al} = \frac{1}{H|Q|} \sum_h \sum_q \sum_c a^l_{h,q,c}$$

This is normalized to $[0,1]$, then combined with a **Gaussian prior** centered at layer $\mu$ with standard deviation $\sigma$:

> $$S_l = \alpha \cdot S_{al} + (1-\alpha) \cdot P_l, \quad \text{where } P_l = \exp\!\left(-\frac{(l-\mu)^2}{2\sigma^2}\right)$$

The Gaussian prior encodes H1 (preference for intermediate layers). The attention score encodes H2 (preference for high-attention layers). The top $M$ layers by combined score are selected.

### Calibration Efficiency

A remarkable finding: **a single calibration sample** is sufficient to select layers that generalize to the entire test set. The selection is computed once per model pair and reused across all inputs.

### Non-Contiguous Selection

A key distinction from prior work: KVComm can select **non-contiguous layers** (e.g., layers 8, 12, 15, 19, 23 but not 9-11). This is important because the most informative layers are not necessarily adjacent.

## Communication Framework

The protocol is simple:

1. **Sender ($M_s$)** processes context $C$, runs one forward pass (prefill), generates KV pairs at all layers
2. **Selection**: Top $M$ layers chosen by the selection strategy
3. **Transmission**: Selected KV pairs $\{(k^s_{l_i}, v^s_{l_i})\}$ sent to receiver
4. **Receiver ($M_r$)** processes query $Q$. At each selected layer $l_i$, sender's KV pairs are concatenated with receiver's own: $k^r_l \leftarrow [k^s_{l_i}; k^r_l]$, $v^r_l \leftarrow [v^s_{l_i}; v^r_l]$
5. **Generation**: Receiver generates output attending to both its own and sender's cached context

No learned projections, no training. Pure concatenation + attention.

## Experimental Results

Evaluated on 9 model pairs across 8 datasets (Countries, Tipsheets, HotpotQA, QASPER, MuSiQuest, MultiFieldQA-en, 2WikiMQA, TMATH).

### Key Comparisons

| Method | Complex task performance (HotpotQA F1) | Layers transmitted |
|--------|---------------------------------------|-------------------|
| Baseline (no communication) | 0.23 | 0 |
| NLD (natural language debate) | 0.43 | N/A (full decode) |
| CIPHER (embedding communication) | 0.50 | N/A (full decode) |
| AC — replace (hidden state replacement) | 0.05 | 1 layer |
| AC — mean (hidden state averaging) | 0.25 | 1 layer |
| **KVComm (30% layers)** | **0.46** | **~10 layers** |
| **KVComm (50% layers)** | **0.57** | **~16 layers** |
| **KVComm (70% layers)** | **0.65** | **~22 layers** |
| Skyline (full context concat) | 0.73 | All (upper bound) |

Critical observations:
- **KVComm at 70% matches or approaches Skyline** across most datasets — near-optimal communication with 30% less data transmitted
- **KVComm at 30% already outperforms NLD, CIPHER, and AC** — even minimal KV sharing beats full natural language or embedding communication
- NLD and CIPHER perform well on simple datasets (Countries, Tipsheets) where only small, salient information needs transfer, but **fail on complex long-context tasks** where the sender has context the receiver needs
- **KVComm sometimes exceeds Skyline** — selective KV sharing can act as regularization, filtering noise

### Efficiency

Compared to NLD, KVComm eliminates all decode steps for the sender — only a single prefill pass is needed. The computation margin is $O(L(T_s + T_r + |Q|)^2 d)$ where $T_s, T_r$ are debate token counts.

## Deeper Layer Selection Analysis

### Why Non-Contiguous Selection Outperforms Contiguous Blocks

KVComm's selection strategy can pick layers like {8, 12, 15, 19, 23} rather than a contiguous block like {10, 11, 12, 13, 14}. This outperforms contiguous selection because the **most informative layers are scattered** across the network. The Gaussian prior centers the selection around intermediate layers, but the attention-importance score overrides this when specific early or late layers carry unusually high semantic content for a given model.

The non-contiguous finding aligns with C2C's learnable gate results: when C2C's Gumbel-sigmoid gates converge to binary values, the "on" layers are typically non-contiguous, confirming that the beneficial fusion layers do not cluster.

### The Attention Importance Score in Practice

The selection score $\hat{S}_{al}$ measures how much each layer's attention mechanism focuses on context tokens (as opposed to self-attention on the query). Layers with high $\hat{S}_{al}$ are those where the model is actively retrieving and integrating contextual information — these are precisely the layers whose KV-cache carries the most transferable semantic content.

The Gaussian prior $P_l$ serves as a **regularizer**: without it, selection based purely on attention scores can produce unstable results (different calibration samples may yield very different layer sets). The prior smooths the selection toward the theoretically motivated intermediate layer range, and the mixing weight $\alpha$ controls the balance between data-driven and prior-driven selection.

### Single-Sample Calibration: Why It Works

The finding that **one calibration sample** generalizes to the full test set is surprising and important for practical deployment. The explanation: layer-level attention patterns are a property of the **model architecture and weights**, not of individual inputs. While per-input attention distributions vary, the **average** attention importance across layers is remarkably stable. A single sufficiently diverse input activates enough of the model's attention patterns to produce a representative layer ranking.

This contrasts sharply with C2C's approach, where the learnable gate must be trained on hundreds of thousands of samples (OpenHermes2.5, 500K samples) to learn per-layer fusion decisions. The difference is that KVComm's selection is a simple ranking over a fixed model property, while C2C's gating must learn input-dependent behavior.

## Ablation Insights

### Random vs Importance-Based Layer Selection

The paper's selection strategy combines an attention-importance score $\hat{S}_{al}$ with a Gaussian prior $P_l$. Compared to baselines:

- **Random layer selection** at the same budget (e.g., 30% of layers chosen uniformly at random) performs significantly worse than importance-based selection, often falling below NLD on complex tasks. This confirms that the information content of KV-caches varies dramatically across layers — not all layers carry transferable semantic knowledge, and including uninformative layers can inject noise that degrades the receiver's processing.
- **Attention-only selection** (no Gaussian prior, $\alpha = 1$) produces unstable results: different calibration samples may yield very different layer sets because per-input attention distributions are noisy. The Gaussian prior smooths this instability by biasing selection toward the theoretically motivated intermediate layer range.
- **Prior-only selection** (no attention score, $\alpha = 0$) performs reasonably on average but misses model-specific deviations — some models have unusually informative early or late layers that the fixed Gaussian cannot capture.

The combined score with $\alpha$ balancing data-driven and prior-driven components gives the most robust performance across model pairs and tasks, which is why a single calibration sample suffices for generalization.

### Contiguous vs Non-Contiguous Layer Patterns

A key finding: constraining selection to **contiguous blocks** (e.g., layers 10-19) consistently underperforms the unconstrained non-contiguous selection (e.g., layers 8, 12, 15, 19, 23) at the same budget. The most informative layers are scattered across the network rather than clustered in a single block. For example, a model may have high attention importance at layers 8 and 23 alongside the expected intermediate-layer peaks — a contiguous block centered at layer 15 would miss both.

This non-contiguity finding is independently corroborated by [[cache-to-cache-semantic-communication|C2C]]'s learnable Gumbel-sigmoid gates, which converge to binary "on/off" decisions at non-contiguous layers. The convergence across two very different selection mechanisms (calibration-based ranking vs. gradient-trained gating) strengthens the conclusion that the beneficial fusion layers do not cluster.

The practical implication: any KV-cache sharing protocol that imposes contiguous-block constraints (e.g., "share the middle third of layers") leaves significant performance on the table compared to a principled non-contiguous selection strategy.

## Comparison with KV Cache Alignment's Shared-Space Approach

KVComm and [[kv-cache-alignment-shared-space|KV Cache Alignment]] take complementary approaches to the cross-model problem:

| Dimension | KVComm | KV Cache Alignment |
|-----------|--------|-------------------|
| Cross-architecture | No — same architecture required | Yes — via shared KV-cache space |
| Training | None — calibration only | Required — adapters trained per model |
| Layer selection | Explicit — attention + Gaussian prior | Implicit — adapters learn which layers to emphasize |
| Efficiency mechanism | Transmit fewer layers | Transmit through shared space (all layers) |
| Self-improvement | Selective sharing sometimes exceeds skyline | Cyclic translation improves perplexity |
| Scalability | $O(1)$ per model pair (reusable scores) | $O(N)$ adapters for $N$ models |

A key open question is whether KVComm's layer selection could be **applied within** the KV Cache Alignment framework — selecting which layers to translate through the shared space rather than translating all layers. This could combine KVComm's bandwidth efficiency with KV Cache Alignment's cross-architecture compatibility.

### The "Exceeds Skyline" Phenomenon

On some datasets, KVComm at 70% of layers **outperforms** the Skyline (full context concatenation with all layers). This counterintuitive result suggests that selective sharing acts as **regularization**: by filtering out uninformative or noisy layers, the receiver gets cleaner signal than it would from the full unfiltered cache. This parallels [[cache-to-cache-semantic-communication|C2C]]'s effective rank increase finding and [[kv-cache-alignment-shared-space|KV Cache Alignment]]'s self-improvement effect — all three independently discover that latent-space mediation can improve over raw information transfer.

## Constraints and Limitations

- **Same architecture required**: Sender and receiver must be the same model or fine-tuned from the same base (identical layer count, head dimensions). No cross-family communication — for that, see [[cache-to-cache-semantic-communication|C2C]]'s learned fuser or [[kv-cache-alignment-shared-space|KV Cache Alignment]]'s shared space.
- **Same-layer matching**: Layer indices are 1-to-1 matched between models. Cannot handle models of different depths. C2C addresses this with terminal alignment; KV Cache Alignment handles it through per-model adapters.
- **Context/query split**: The sender processes context only; the receiver processes query only. This is a specific multi-model inference setup, not general multi-agent debate. [[latentmas-collaboration|LatentMAS]] demonstrates full KV-cache sharing in a general multi-agent topology.
- **No training, but calibration needed**: One calibration sample per model pair to compute layer selection scores. While minimal, this still requires access to a representative input.
- **No token-level selection**: KVComm selects which layers to share but transmits **all token positions** within selected layers. Token-level selection (which positions' KVs are most informative) remains an open direction that could further reduce bandwidth.

## Position in the KV-Cache Communication Cluster

KVComm addresses **what to share** — the layer selection problem. It pairs naturally with:
- [[cache-to-cache-semantic-communication|C2C]]: which addresses **how to fuse across architectures** (learned projection for cross-family/cross-size communication)
- [[kvcomm-duke-online-reuse|KVCOMM-online]]: which addresses **how to make sharing efficient** (cache reuse via offset estimation)

See [[kv-cache-communication]] for the unified concept page.

## Source Materials

- [[raw/pdf/arxiv-2510.03346.pdf|PDF]] ([[raw/latex/arxiv-2510.03346.tar.gz|LaTeX source]])
