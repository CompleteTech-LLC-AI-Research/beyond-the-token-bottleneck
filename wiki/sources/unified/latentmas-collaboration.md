---
type: source
title: "Latent Collaboration in Multi-Agent Systems"
source_file: "[[raw/pdf/arxiv-2511.20639.pdf]]"
latex_source: "[[raw/latex/arxiv-2511.20639.tar.gz]]"
author: "Jiaru Zou, Xiyuan Yang, Ruizhong Qiu, Gaotang Li, Katherine Tieu, Pan Lu, Ke Shen, Hanghang Tong, Yejin Choi, Jingrui He, James Zou, Mengdi Wang, Ling Yang"
date_published: "2025-11-28"
date_ingested: "2026-04-06"
created: "2026-04-06"
updated: "2026-04-06"
venue: "arXiv preprint"
arxiv: "2511.20639"
institution: "Princeton, UIUC, Stanford"
tags: [latent-communication, kv-cache, training-free, multi-agent]
---

# Latent Collaboration in Multi-Agent Systems (LatentMAS)

## Summary

**LatentMAS** unifies [[latent-space-reasoning]] and latent communication in a single **training-free** framework. Each agent generates "latent thoughts" by feeding hidden states back as input embeddings (like [[coconut-reasoning-latent-space|Coconut]]), then transfers its full **layer-wise KV caches** (including the latent thoughts) to the next agent. Only the final agent decodes to text. No adapters, no training, no learned projections. Evaluated across 9 benchmarks, 3 model scales (Qwen3-4B/8B/14B), and 2 MAS topologies (sequential, hierarchical).

## Core Mechanism: Detailed Pipeline

> [!diagram|left]
> ```mermaid
> graph LR
>     subgraph AgentI["Current Agent (e.g. Planner)"]
>         FWD["**Forward Pass**<br>Input through N layers<br>to last-layer hidden state"]
>         ALN["**Alignment**<br>Ridge regression<br>d×d matrix"]
>         LAT["**Latent Thoughts**<br>K steps (40-80)<br>Feed aligned state back<br>No decoding/softmax"]
>     end
>     KV["**Extract Working Memory**<br>All N layers: KV caches<br>T input + K latent positions"]
>     subgraph AgentNext["Next Agent (e.g. Critic)"]
>         PRE["**KV Prepend**<br>Prepend predecessor caches<br>at every layer<br>via past_key_values"]
>         GEN["**Generate**<br>Latent thoughts<br>or final text"]
>     end
> 
>     FWD -->|"hidden state"| ALN -->|"aligned state"| LAT -->|"KV caches"| KV -->|"working memory"| PRE --> GEN
>     LAT -.->|"repeat K times"| FWD
> 
>     style AgentI fill:#dae8fc,stroke:#6c8ebf
>     style AgentNext fill:#f5f5f5,stroke:#666666
>     style KV fill:#ffe6cc,stroke:#d79b00
> ```

> [!notation|right]
> | Step | Notation |
> |---|---|
> | Current Agent | $A_i$ |
> | Next Agent | $A_{i+1}$ |
> | Last-layer hidden state | $h_T$ |
> | Alignment matrix | $M$ |
> | Aligned hidden state | $h'_T = M \cdot h_T$ |
> | Working memory of agent | $\M_i$ |
> | KV caches at layer $l$ | $(K_\text{cache}^{(l)}, V_\text{cache}^{(l)})$ |

### Step 1 — Latent Thought Generation

Each agent generates K latent steps via auto-regressive hidden-state recurrence:

1. **Forward pass**: Given input embeddings $X = [x_1, \ldots, x_T]$, the agent runs all $N$ transformer layers to produce last-layer hidden state $h_T$.
2. **Alignment**: Apply the alignment matrix $M$ to produce $h'_T = M h_T$, mapping the output-space vector back into a valid input-space embedding.
3. **Feedback loop**: Insert $h'_T$ as the input embedding for position $T+1$ (replacing normal token-embedding lookup). No decoding, no softmax, no vocabulary projection.
4. **Repeat**: Run the full transformer forward pass again with the extended sequence $[x_1, \ldots, x_T, h'_T]$ to produce $h_{T+1}$. Apply $M$, feed back. Repeat for $K$ total latent steps.
5. **Result**: A sequence of $K$ new hidden states $\Theta = [h_{T+1}, h_{T+2}, \ldots, h_{T+K}]$ — the agent's "latent thoughts."

The number of latent steps $K$ is a hyperparameter drawn from $\{0, 10, 20, 40, 80\}$. No stopping condition is learned — $K$ is fixed per run.

### Step 2 — Input-Output Alignment Matrix M

Since last-layer hidden states live in the output embedding space (high-level, abstract) and input embeddings live in the token embedding space (shallow, distributional), directly feeding $h$ back as input causes **out-of-distribution activations**. $M$ bridges this gap.

**Formula**: $M$ approximates the pseudo-inverse mapping from output to input space:

> $M \approx W_\text{out}^{-1} W_\text{in}$

Since $W_\text{out}$ is non-square ($d \times |V|$), the true inverse does not exist. In practice $M$ is computed via **ridge regression**:

> $M = (W_\text{out}^\top W_\text{out} + \lambda I)^{-1} W_\text{out}^\top W_\text{in}$

This solves: $\min_M \{ \|W_\text{out} M - W_\text{in}\|_F^2 + \lambda\|M\|_F^2 \}$

**Key properties**:
- $M$ is a **$d \times d$ matrix** (e.g., $d=1024$ for Qwen3-0.6B). Small and cheap.
- Computed **once per model** and reused for all latent steps and all queries.
- $\lambda > 0$ is a small regularization hyperparameter for numerical stability (exact value not specified in paper).
- Computational cost: polynomial in $d$ — negligible relative to inference.

**Theoretical justification** (Theorem A.1): For any non-singular $M$, the Wasserstein distance between the aligned embedding distribution and the true token embedding distribution is upper-bounded by $\|W_\text{out} M - W_\text{in}\|_F$. The ridge regression solution minimizes this upper bound.

### Step 3 — Working Memory Transfer (KV-Cache Concatenation)

After agent $A_i$ completes $K$ latent steps, its working memory is extracted and passed to $A_{i+1}$:

1. **Extract**: Collect KV caches from **all $N$ transformer layers** of $A_i$. For layer $l$, this gives $K_\text{cache}^{(l)}$ and $V_\text{cache}^{(l)}$, each containing $T+K$ column vectors ($T$ from original input, $K$ from latent thoughts).
2. **Define working memory**: $\M_i = \{(K_\text{cache}^{(l)}, V_\text{cache}^{(l)}) \mid l = 1, 2, \ldots, N\}$. This captures both the original input context AND the generated latent thoughts — unlike [[cache-to-cache-semantic-communication|C2C]] and [[kvcomm-selective-kv-sharing|KVComm]] which share only input-derived KV caches.
3. **Prepend**: For each layer $l$ of agent $A_{i+1}$, prepend $A_i$'s $K_\text{cache}^{(l)}$ and $V_\text{cache}^{(l)}$ to $A_{i+1}$'s own caches. This is done via the `past_key_values` interface in HuggingFace Transformers.
4. **Conditioning**: When $A_{i+1}$ now generates (either latent thoughts or final text), its attention at every layer attends over both the predecessor's full working memory and its own representations.

**Positional encodings**: The paper does not explicitly discuss positional encoding adjustment during KV-cache concatenation. The prepending operation places predecessor KV entries before the successor's own entries in the sequence dimension, implying the predecessor's positional encodings are preserved as-is from their original computation.

**Information preservation** (Theorem 3.3): The outputs of an agent receiving latent working memory via KV-cache transfer are provably equivalent to what it would produce if the predecessor's full output were directly re-encoded as input. Proof is by induction over transformer layers — if keys and values are identical, attention outputs are identical, so the full forward pass is identical.

## MAS Topologies

**Sequential MAS** (4 agents): Planner → Critic → Refiner → Solver. Each agent receives the previous agent's latent working memory via KV-cache prepending. Only the Solver decodes text.

**Hierarchical MAS** (4 agents): Math Agent, Science Agent, and Code Agent operate in parallel on the same question. A Summarizer agent then receives all three agents' latent working memories (concatenated) and produces the final text answer.

## Full Results: All 9 Benchmarks

### Sequential MAS

| Benchmark | Metric | Qwen3-4B ||| Qwen3-8B ||| Qwen3-14B |||
|---|---|---|---|---|---|---|---|---|---|---|
| | | Single | TextMAS | LatentMAS | Single | TextMAS | LatentMAS | Single | TextMAS | LatentMAS |
| **ARC-E** | Acc | 95.4 | 96.4 | **98.6** | 95.6 | 99.1 | **98.8** | 97.2 | 99.0 | **99.4** |
| | Token | 724 | 2420 | 581 | 656 | 2085 | 490 | 608 | 1670 | 224 |
| | Speed | 369 | 2874 | 512 | 404 | 3702 | 1759 | 551 | 9171 | 2124 |
| **ARC-C** | Acc | 89.2 | 90.0 | **92.3** | 91.0 | 94.6 | **94.4** | 92.6 | 95.9 | **95.6** |
| | Token | 913 | 2678 | 718 | 846 | 2252 | 529 | 773 | 2985 | 426 |
| | Speed | 97 | 1579 | 260 | 266 | 2059 | 703 | 338 | 5125 | 1136 |
| **GSM8K** | Acc | 82.4 | 89.8 | **88.2** | 81.1 | 92.3 | **93.8** | 83.7 | 93.8 | **95.2** |
| | Token | 1136 | 3172 | 607 | 1280 | 2324 | 860 | 1118 | 3324 | 644 |
| | Speed | 469 | 1970 | 375 | 449 | 1739 | 543 | 536 | 3729 | 1952 |
| **MedQA** | Acc | 47.7 | 65.3 | **66.3** | 53.0 | 75.0 | **75.3** | 64.7 | 80.3 | **80.7** |
| | Token | 2134 | 3962 | 1685 | 2098 | 4260 | 1555 | 1746 | 3444 | 1841 |
| | Speed | 236 | 1267 | 438 | 476 | 1923 | 928 | 1360 | 4142 | 1420 |
| **MBPP+** | Acc | 63.5 | 69.8 | **73.5** | 64.8 | 69.5 | **74.6** | 68.5 | 72.8 | **75.7** |
| | Token | 1634 | 4420 | 1339 | 2053 | 3695 | 1164 | 1858 | 4971 | 1621 |
| | Speed | 523 | 2148 | 577 | 1064 | 3628 | 1275 | 2410 | 8728 | 2400 |
| **HumanEval+** | Acc | 75.0 | 79.7 | **79.9** | 74.4 | 80.5 | **80.5** | 76.8 | 81.1 | **86.5** |
| | Token | 2380 | 5987 | 1775 | 2507 | 4593 | 1866 | 2366 | 5934 | 2042 |
| | Speed | 274 | 1044 | 350 | 502 | 1619 | 497 | 1084 | 4062 | 1285 |

Token = total output tokens per run. Speed = end-to-end time (seconds) per run.

**Sequential MAS improvements over TextMAS** (Qwen3-14B): Token reduction 46.5%-86.6%. Speed improvement 1.9×-4.5×.

### Hierarchical MAS

| Benchmark | Metric | Qwen3-4B ||| Qwen3-8B ||| Qwen3-14B |||
|---|---|---|---|---|---|---|---|---|---|---|
| | | Single | TextMAS | LatentMAS | Single | TextMAS | LatentMAS | Single | TextMAS | LatentMAS |
| **ARC-E** | Acc | 95.4 | 97.1 | **96.8** | 95.6 | 98.2 | **98.3** | 97.2 | 98.3 | **98.7** |
| | Token | 724 | 2054 | 363 | 656 | 2237 | 308 | 608 | 2752 | 619 |
| | Speed | 369 | 2239 | 591 | 404 | 3619 | 1779 | 551 | 7102 | 1884 |
| **ARC-C** | Acc | 89.2 | 92.5 | **91.7** | 91.0 | 93.3 | **93.9** | 92.6 | 95.3 | **95.5** |
| | Token | 913 | 2674 | 447 | 846 | 2854 | 344 | 773 | 2167 | 295 |
| | Speed | 97 | 1275 | 299 | 266 | 2034 | 714 | 338 | 4283 | 1090 |
| **GSM8K** | Acc | 82.4 | 89.4 | **88.4** | 81.1 | 90.4 | **89.5** | 83.7 | 90.8 | **91.6** |
| | Token | 1136 | 3098 | 555 | 1280 | 2370 | 353 | 1118 | 3021 | 495 |
| | Speed | 469 | 1878 | 360 | 449 | 1365 | 702 | 536 | 3675 | 1631 |
| **MedQA** | Acc | 47.7 | 65.0 | **67.3** | 53.0 | 76.3 | **77.0** | 64.7 | 78.0 | **78.3** |
| | Token | 2134 | 6702 | 1015 | 2098 | 6893 | 1007 | 1746 | 5473 | 899 |
| | Speed | 236 | 1495 | 557 | 476 | 3387 | 964 | 1360 | 7591 | 1250 |
| **MBPP+** | Acc | 63.5 | 69.3 | **70.6** | 64.8 | 71.9 | **72.2** | 68.5 | 73.0 | **73.8** |
| | Token | 1634 | 6782 | 1339 | 2053 | 7703 | 1264 | 1858 | 7458 | 1187 |
| | Speed | 523 | 1766 | 489 | 1064 | 3898 | 1387 | 2410 | 9162 | 2507 |
| **HumanEval+** | Acc | 75.0 | 76.2 | **79.3** | 74.4 | 76.8 | **78.0** | 76.8 | 84.1 | **86.6** |
| | Token | 2380 | 8127 | 1373 | 2507 | 8768 | 1274 | 2366 | 8114 | 1512 |
| | Speed | 274 | 931 | 333 | 502 | 1809 | 439 | 1084 | 3988 | 1188 |

**Hierarchical MAS improvements over TextMAS** (Qwen3-14B): Token reduction 77.5%-86.4%. Speed improvement 2.3×-6.1×.

### Reasoning-Intensive Tasks (Qwen3-8B and 14B only)

| Benchmark | Setting | Qwen3-8B ||| Qwen3-14B |||
|---|---|---|---|---|---|---|---|
| | | Single | TextMAS | LatentMAS | Single | TextMAS | LatentMAS |
| **AIME24** | Seq | 50.0 | 53.3 | **56.7** | 50.0 | 63.3 | **66.7** |
| | Hier | 50.0 | 53.3 | **53.3** | 50.0 | 63.3 | **73.3** |
| **AIME25** | Seq | 46.7 | 53.3 | **53.3** | 46.7 | 56.7 | **63.3** |
| | Hier | 46.7 | 50.0 | **50.0** | 46.7 | 60.0 | **66.7** |
| **GPQA-Diamond** | Seq | 39.9 | 43.4 | **45.5** | 39.9 | 48.5 | **52.0** |
| | Hier | 39.9 | 43.0 | **46.9** | 39.9 | 51.5 | **53.0** |

AIME24/25 token and speed data (Qwen3-14B, Sequential):
- AIME24: TextMAS 32,092 tokens / 4,554s → LatentMAS 10,593 tokens / 1,149s (67.0% fewer tokens, 4.0× faster)
- AIME25: TextMAS 44,618 tokens / 5,184s → LatentMAS 11,402 tokens / 1,473s (74.4% fewer tokens, 3.5× faster)
- GPQA-Diamond: TextMAS 12,676 tokens / 9,714s → LatentMAS 5,454 tokens / 1,475s (57.0% fewer tokens, 6.6× faster)

## Aggregate Efficiency Metrics

**Sequential MAS averages**:
- Accuracy: +14.6% over single, +2.8% over TextMAS
- Token reduction: 70.8% fewer than TextMAS
- Speed: 4.0× faster (range 2.6×-7.0×)

**Hierarchical MAS averages**:
- Accuracy: +13.3% over single, +4.6% over TextMAS
- Token reduction: 83.7% fewer than TextMAS
- Speed: 4.3× faster (range 2.0×-7.7×)

LatentMAS also uses **15.0%-60.3% fewer tokens than single agents** because it distributes the question across agents, with only the final agent decoding a short answer.

Per-benchmark speedup factors (Hierarchical, Qwen3-14B): ARC-E 3.8×, ARC-C 3.9×, GSM8K 2.3×, MedQA 6.1×, MBPP+ 3.7×, HumanEval+ 3.4×, AIME24 4.0×, AIME25 5.7×, GPQA 6.3×.

## Theoretical Analysis

### Theorem 3.1 — Expressiveness of Latent Thoughts

**Assumption** (Linear Representation Hypothesis): Hidden embeddings $h$ are linear combinations of an underlying semantic basis $\{e_1, \ldots, e_d\}$ with ternary coefficients $\alpha_i \in \{0, +1, -1\}$, where $d$ is the hidden dimension.

**Statement**: If a length-$K$ sequence of latent thoughts can be expressed losslessly through text-based reasoning, then the required text length (in tokens) is at least $Kd / \log|V|$, where $|V|$ is the vocabulary size.

**Derivation sketch**: Under the ternary coefficient assumption, each hidden embedding can encode one of $3^d$ distinct states. A length-$K$ sequence of latent thoughts can represent $(3^d)^K = 3^{Kd}$ distinct sequences. To represent this losslessly with text tokens from vocabulary $V$, you need at least $L$ tokens where $|V|^L \geq 3^{Kd}$, giving $L \geq Kd \cdot \log(3) / \log|V| \geq Kd / \log|V|$.

**Concrete numbers**: For Qwen3 models with typical vocabulary size ~152K:
- Qwen3-4B ($d=3584$): $3584 / \log_2(152000) \approx$ **235.7x** more efficient
- Qwen3-8B ($d=4096$): $4096 / \log_2(152000) \approx$ **377.1x** more efficient (note: paper states this but $d$ values may differ)
- Qwen3-14B ($d=5120$): $5120 / \log_2(152000) \approx$ **471.4x** more efficient

### Theorem 3.3 — Lossless Information Preservation

KV-cache transfer produces outputs identical to directly re-encoding the predecessor's full output as input text. Proved by induction: if keys and values are the same at layer $l-1$, then the attention output at layer $l$ is the same, so the full forward pass is the same through all $N$ layers.

### Theorem 3.4 — Complexity Comparison

**LatentMAS per-agent complexity**: $O((T^2 K + K^2 + Kd) \cdot N)$, where $T$ = input length, $K$ = latent steps, $d$ = hidden dimension, $N$ = number of layers.

**TextMAS per-agent complexity** (to match expressiveness): $O((T^3 Kd / \log|V| + K^3 d^2 / \log^2|V| + K^2 d / \log|V|) \cdot N + K^2 d |V| / \log|V|)$. The extra $|V|$ factor comes from the softmax decoding step required at every text token.

## Ablation Results

### Alignment Matrix M Removal

On MedQA (Qwen3-14B Sequential), removing $M$ causes:
- ARC-C: **+5.3%** accuracy gain from using $M$ (from ~89.6% to ~94.9%)
- ARC-E: **+2.3%** accuracy gain
- GSM8K: **+3.6%** accuracy gain

Visualizations (Figure 6) show that without $M$, output embeddings $h_t$ drift significantly from the input embedding distribution. After applying $M$, the aligned vector $h'_{t+1}$ realigns with the original input embedding distribution in both density and geometric structure.

### Latent Step Depth Sweep (Qwen3-14B, Sequential)

| K (latent steps) | ARC-C | ARC-E | GSM8K |
|---|---|---|---|
| 0 | 91.3 | 94.7 | 85.6 |
| 10 | 93.4 | 98.9 | 90.3 |
| 20 | 93.4 | 98.9 | 90.9 |
| 40 | **94.9** | **99.4** | 91.4 |
| 80 | 94.8 | 99.6 | **92.0** |
| 160 | 93.7 | 98.3 | 91.9 |

Peak performance at $K=40$–$80$ steps. Beyond $K=160$, performance plateaus or slightly declines — excessive latent steps may introduce redundant or less useful information. In practice, a moderate budget of 40-80 steps provides the best accuracy-efficiency trade-off.

### t-SNE Visualization (Figure 5)

Conducted on 300 MedQA questions using Qwen3-4B/8B/14B. Compared the distribution of last-layer embeddings from LatentMAS (40 latent steps) against token embeddings from TextMAS (4096 max tokens). Two findings:
1. LatentMAS embeddings occupy **the same region** of embedding space as TextMAS token embeddings — semantic consistency.
2. LatentMAS embeddings **cover a broader area** than TextMAS embeddings — greater diversity and expressive capacity than discrete tokens.

## Case Study: GSM8K Bee Problem (Qwen3-14B Sequential)

**Problem**: Track bees leaving/returning a hive across four 6-hour periods. Correct answer: 75 bees return in the final period (15 remaining from Period 1 + 60 from Period 3).

**TextMAS failure**: The Planner correctly identifies all four periods and computes intermediate values. The Critic provides feedback but introduces confusion by repeatedly questioning straightforward interpretations. The Refiner produces a correct plan. However, the **Solver re-derives everything from scratch** through text, gets confused about "bees that left before that," and outputs **15** (wrong — forgot the 60 bees from Period 3).

**LatentMAS success**: Agents communicate via latent working memory rather than verbose text. The final Solver agent receives rich continuous representations of the refined reasoning and correctly computes **15 + 60 = 75**. The key difference: latent transfer avoids the **error compounding** problem where early misinterpretations propagate through brittle text and constrain later agents' search space.

## Implementation Details

- **Backend**: PyTorch + HuggingFace Transformers, optional vLLM backend for prefix caching and tensor parallelism.
- **Temperature**: 0.6, top-p: 0.95 for all agents and baselines.
- **Max output lengths**: 2048 tokens (ARC-E, ARC-C, GSM8K), 4096 tokens (MedQA, MBPP+, HumanEval+), 8192 tokens (GPQA), 20000 tokens (AIME24/25).
- **Hardware**: 8× NVIDIA A100-80G GPUs.
- **Evaluation**: Mean over 3 independent runs with hyperparameter tuning.
- **KV transfer**: Via HuggingFace `past_key_values` interface for direct concatenation.

## Limitations

- **Homogeneous architecture required**: All agents must share the same model family and layer structure. Heterogeneous agents would need trainable adapters for layer mapping.
- Only tested on Qwen3 (4B/8B/14B).
- Requires open-weight models (needs KV cache access).
- $\lambda$ regularization value for ridge regression not specified — unclear sensitivity.
- Fixed $K$ latent steps per agent (no adaptive stopping).

## Connections

- **[[latent-space-reasoning]]**: LatentMAS is the first to combine Coconut-style latent reasoning with multi-agent KV-cache transfer in a training-free system.
- **[[kv-cache-communication]]**: Extends prior KV-cache methods by sharing caches that include generated latent thoughts, not just processed input.
- **[[agent-primitives-building-blocks|Agent Primitives]]**: Agent Primitives also use KV-cache concatenation but with structured primitives (Review, Voting, Planning) rather than free-form latent generation.
- **[[superposition-coconut-theory|Superposition/Coconut theory]]**: The expressiveness theorem (Theorem 3.1) relies on the same Linear Representation Hypothesis foundation — ternary coefficients over a semantic basis.
- **[[continuous-vs-discrete-representation]]**: The $d/\log|V|$ bound is the core quantification of why continuous beats discrete for reasoning expressiveness.

## Source Materials

- [[raw/pdf/arxiv-2511.20639.pdf|PDF]] ([[raw/latex/arxiv-2511.20639.tar.gz|LaTeX source]])
