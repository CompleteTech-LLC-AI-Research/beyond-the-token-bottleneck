---
type: source
title: "Latent Reasoning with Supervised Thinking States"
source_file: "[[raw/pdf/arxiv-2602.08332.pdf]]"
latex_source: "[[raw/latex/arxiv-2602.08332.tar.gz]]"
author: "Ido Amos, Avi Caciularu, Mor Geva, Amir Globerson, Jonathan Herzig, Lior Shani, Idan Szpektor"
date_published: "2026-02-09"
date_ingested: "2026-04-06"
created: "2026-04-06"
updated: "2026-04-06"
venue: "arXiv preprint"
arxiv: "2602.08332"
institution: "Google Research, Hebrew University of Jerusalem, Tel Aviv University"
tags: [latent-reasoning, thinking-states, chunk-recurrence, supervised]
---

# Latent Reasoning with Supervised Thinking States

## One-liner

![[thinking-states-latent-reasoning/one-liner]]

## Summary

This paper introduces **Thinking States**, a method that combines the strengths of both discrete CoT (supervisable, interpretable) and continuous latent reasoning (compact, recurrent) by generating **natural language thoughts** at chunk boundaries during input processing, then **compressing** them into fixed-size continuous states that are injected back into the model at shallow layers. Unlike [[coconut-reasoning-latent-space|Coconut]], which requires BPTT (backpropagation through time), Thinking States uses teacher forcing for parallel training. Unlike [[softcot-efficient-reasoning|SoftCoT]], reasoning happens during input processing, not as a preamble. The method achieves competitive accuracy with CoT on 2-hop QA while being 1.19-2.66x faster, and dramatically outperforms all latent baselines.

## Core Architecture

Three lightweight modules augment a **frozen backbone LLM** (the backbone parameters are not updated):

### 1. Thinking Block (T)

A single-layer causal transformer decoder, initialized from the LLM's last layer. Autoregressively generates natural-language reasoning tokens from deep-layer representations. If no reasoning is needed for a given chunk, produces only an EOS token. The lightweight design ensures that thought generation is substantially faster than standard autoregressive decoding through the full backbone.

### 2. Compression Block (C)

A single-layer transformer encoder with a pooling layer, initialized from the LLM's first layer. Maps variable-length thought sequences into a fixed-size state $S \in \R^{c \times d}$, where $c$ is the chunk size and $d$ is the hidden dimension. The pooling operation ensures that thoughts of any length compress to the same-dimensional state, maintaining a fixed context size regardless of reasoning complexity.

### 3. Deep-to-Shallow Recurrence

The key architectural innovation. Thoughts are extracted from a **deep layer** (layer 26 of 28 in Qwen2.5-1.5B) and injected at a **shallow layer** (layer 1). This gives the compressed state maximum processing depth through the LLM backbone -- nearly all 27 layers process the reasoning state before the next chunk arrives. The design philosophy: let the heavyweight backbone do the computational work, while the lightweight modules handle thought generation and compression.

### Processing Loop (Diagram)

> [!diagram|left]
> ```mermaid
> graph LR
>     subgraph Input["Input Processing"]
>         X["Chunk tokens"]
>         S["State from previous chunk"]
>     end
> 
>     subgraph Processing["Backbone Forward Pass"]
>         INJ["1. Inject State<br>(additive, layer 1)"]
>         FWD["2. Forward Pass<br>(extract at layer 26)"]
>     end
> 
>     subgraph ThoughtGen["Thought Generation"]
>         THINK["3. Thinking Block<br>(NL thought tokens)"]
>         COMP["4. Compression Block<br>(fixed-size state)"]
>     end
> 
>     subgraph Output["Next Iteration"]
>         NEXT["5. Repeat for next chunk"]
>     end
> 
>     X --> INJ
>     S --> INJ
>     INJ --> FWD
>     FWD --> THINK
>     THINK --> COMP
>     COMP --> NEXT
>     NEXT -.->|"State feeds back"| S
> 
>     style Input fill:#dae8fc,stroke:#6c8ebf
>     style Processing fill:#fff2cc,stroke:#d6b656
>     style ThoughtGen fill:#d5e8d4,stroke:#82b366
>     style Output fill:#e1d5e7,stroke:#9673a6
> ```

> [!notation|right]
> | Step | Notation |
> |---|---|
> | Chunk tokens | $X_i$ ($c$ tokens) |
> | State from previous chunk | $S_i$ |
> | Inject State | $\tilde{X}_i = X_i + S_i$ |
> | Forward Pass | $H_i = M_\theta(\tilde{X}_i)$ |
> | Thinking Block | $Z_{i+1} = T(H_i)$ |
> | Compression Block | $S_{i+1} = C(Z_{i+1})$ |
> | Next chunk | $X_{i+1}$ |
> | State feedback | $S_{i+1}$ feeds back |

### Processing Loop (Formal)

Input is partitioned into $K$ non-overlapping chunks of size $c$ (e.g., 8 tokens): $X_1, \ldots, X_K$ where each $X_i \in \R^{c \times d}$.

At each step $i$:

1. **Inject state**: $\tilde{X}_i = X_i + S_i$ (additive injection at layer $L^{in} = 1$)
2. **Forward pass**: $H_i^{out} = M_\theta(\tilde{X}_i | \tilde{X}_{<i})$ (extract representations at layer $L^{out} = 26$, past chunks accessed via KV-cache)
3. **Generate thought**: $Z_{i+1} = T(H_i^{out})$ (Thinking Block produces variable-length NL thought)
4. **Compress thought**: $S_{i+1} = C(Z_{i+1}) \in \R^{c \times d}$ (Compression Block maps to fixed-size state)
5. Repeat for next chunk. Initial state: $S_1 = \mathbf{0}$.

Since the thought tokens are never appended to the backbone's context window, the **context length remains fixed** -- no context extension occurs regardless of how many reasoning steps are generated.

## Training with Teacher Forcing

### Parallel Training

Because ground-truth reasoning annotations $Z_i^*$ are available for each chunk, gold states $S_i^* = C(Z_i^*)$ can be **precomputed** for all chunks simultaneously. All chunks can then be processed in a **single parallel forward pass** through $M_\theta$:

$$\tilde{X}_i = X_i + S_i^*, \quad \forall i$$

This eliminates sequential dependencies during training entirely. The Thinking Block is then trained to predict $Z_i^*$ via standard next-token prediction, in parallel over all chunks. Each $H_i^{out}$ is computed under the gold state history $S_1^*, \ldots, S_i^*$, so predicting $Z_{i+1}$ is implicitly conditioned on all prior gold reasoning steps.

### Training Objective

$$\Loss = \Loss_{\text{LM}} + \sum_{i=1}^{K} \Loss_T(Z_i, Z_i^*)$$

where $\Loss_{\text{LM}}$ is the standard language modeling loss and $\Loss_T$ is cross-entropy over thinking sequences.

### Training Cost Comparison

The paper directly measures wall-clock time for forward + backward passes:

| Recurrent Steps | BPTT (Coconut) | Teacher Forcing (Thinking States) |
|----------------|---------------|----------------------------------|
| 1 | ~1x | ~1x |
| 5 | ~5x | ~1.1x |
| 10 | ~10x | ~1.1x |
| 20 | ~20x | ~1.1x |

BPTT cost grows **linearly** with recurrence depth. Thinking States maintains **approximately constant** training time regardless of reasoning depth. At 10 steps, BPTT incurs a **~10x cost penalty**.

### Fast Prefill with Speculative Thinking

While training is fully parallel, naive inference is sequential across chunks. The paper introduces an exact prefill algorithm exploiting the observation that most chunks produce **trivial states** (EOS-only thoughts):

1. Perform parallel forward pass over all chunks, speculating all states are trivial
2. Generate thinking states for each chunk using T and C
3. Identify earliest chunk $i_1$ with non-trivial state -- all chunks before $i_1$ are correctly computed
4. Cache positions up to $i_1$ and repeat from step 1 for remaining chunks

The algorithm completes in $|R| + 1$ rounds, where $|R|$ is the number of chunks with non-trivial states. When $|R| \ll K$ (typical regime), prefill latency is substantially reduced.

## Data Construction

Ground-truth thinking sequences are synthesized by aligning existing CoT annotations with input chunks. For each task:

- **State tracking (Parity, Vars)**: Reasoning annotations correspond naturally to state updates at each operation
- **GSM8K**: CoT steps are parsed and mapped to the input chunks where the relevant quantities first appear (~400K problems)
- **2-Hop QA**: Intermediate reasoning steps are mapped to chunks containing the relevant facts

The process uses existing CoT data without requiring new annotation -- the key innovation is the **chunk-to-thought mapping** that determines which reasoning should occur at which input position.

## Key Results

### State Tracking (Qwen2.5-0.5B, OOD Length Generalization)

Models trained on sequences up to $N$ operations, evaluated on lengths $[N, 100]$:

| Method | Parity N=10 | Parity N=20 | Parity N=40 | Vars N=10 | Vars N=20 | Vars N=40 |
|--------|------------|------------|------------|-----------|-----------|-----------|
| No CoT | 54.67% | 57.50% | 59.60% | 2.15% | 2.17% | 2.19% |
| CoT | 12.35% | 38.12% | 64.38% | 6.78% | 35.45% | 87.75% |
| **Thinking States** | **98.37%** | **99.02%** | **100.00%** | **33.76%** | **87.23%** | **97.71%** |

Thinking States dramatically outperforms CoT on length generalization. At Parity N=10 (trained on up to 10 operations, tested on 10-100), CoT achieves only 12.35% while Thinking States reaches 98.37%. The recurrent state mechanism handles arbitrary-length sequences where CoT's greedy left-to-right generation fails to generalize. All models are trained to 100% in-distribution accuracy to isolate extrapolation from optimization effects.

### General Reasoning (Qwen2.5-1.5B)

| Method | GSM8K Acc | GSM8K Speedup | 2-Hop FK Acc | 2-Hop FK Speedup | 2-Hop PK Acc | 2-Hop PK Speedup |
|--------|----------|--------------|-------------|-----------------|-------------|-----------------|
| CoT | 60.50% | 1x | 54.79% | 1x | 43.07% | 1x |
| No CoT | 34.11% | 5.59x | 33.47% | 1.89x | 31.92% | 2.03x |
| **Thinking States** | **42.22%** | **2.66x** | **54.91%** | **1.19x** | **43.05%** | **1.23x** |
| Coconut | 32.65% | 3.14x | 33.71% | 1.14x | 32.60% | 1.21x |
| iCoT | 34.00% | 5.71x | 28.84% | 1.59x | 36.31% | 1.80x |

Key observations:
- **Matches CoT on 2-Hop QA**: 54.91% vs 54.79% on Full Knowledge variant, with 1.19x speedup
- **Beats Coconut by 21+ points** on 2-Hop FK (54.91% vs 33.71%) -- the largest gap among all methods
- **Beats all latent baselines** by ~8 points on GSM8K (42.22% vs 34.00/34.11/32.65%)
- **Lags CoT by 18 points on GSM8K** (42.22% vs 60.50%) -- the state ambiguity problem

Speedups are measured as wall-clock time on a single A100-80GB, not token counts, because thought generation through the lightweight Thinking Block is faster than standard autoregressive decoding.

### 2-Hop QA Variants

- **Full Knowledge (FK)**: Required facts appear in fine-tuning data. Tests whether methods can acquire and manipulate new knowledge.
- **Parametric Knowledge (PK)**: Examples filtered to reflect knowledge already in the base model. Tests whether methods improve retrieval and manipulation of existing knowledge.

Thinking States achieves parity with CoT on both variants, while Coconut and iCoT collapse to near-chance performance on FK (33.71% and 28.84% respectively). This suggests that **supervised thoughts** enable knowledge acquisition in ways that purely continuous latent methods cannot.

## Ablation Studies

### Deep-to-Shallow Recurrence Depth

Varying the extraction layer for the Thinking Block while keeping injection fixed at layer 1 (Qwen2.5-1.5B, 28 hidden layers, GSM8K):

| Extraction Layer | # Layers in Loop | Approximate Accuracy | Speedup |
|-----------------|-----------------|---------------------|---------|
| Layer 4 | 4 | ~24% | ~4.5x |
| Layer 8 | 8 | ~28% | ~3.8x |
| Layer 12 | 12 | ~31% | ~3.3x |
| Layer 16 | 16 | ~34% | ~2.9x |
| Layer 20 | 20 | ~37% | ~2.8x |
| Layer 24 | 24 | ~39% | ~2.7x |
| Layer 26 | 26 | ~42% | ~2.66x |

Performance increases **monotonically** with the number of layers in the recurrent loop, with a ~20% absolute gap between shallowest and deepest configurations. This confirms that maximizing computational capacity for processing thinking states is critical. There is also an inherent accuracy-latency tradeoff: fewer layers in the loop means more layers run only during prefill, yielding higher speedups.

### Chunk Size

Peak performance at $c = 8$ tokens (GSM8K):

| Chunk Size | Approximate Accuracy | Approximate Speedup |
|-----------|---------------------|---------------------|
| $c = 2$ | ~34% | ~1.8x |
| $c = 4$ | ~38% | ~2.2x |
| **$c = 8$** | **~42%** | **~2.66x** |
| $c = 16$ | ~40% | ~3.2x |
| $c = 32$ | ~38% | ~4.0x |
| $c = 48$ | ~36% | ~4.5x |

The tradeoff: too small ($c = 2$) -- insufficient computational capacity per state, too many iterations. Too large ($c = 48$) -- must compress too many reasoning steps into one state update, undermining the deep-to-shallow recurrence since consecutive steps within the same chunk cannot access the full recurrent loop.

### Coconut Scaling

Increasing Coconut's latent tokens from 6 to 21 does **not** improve accuracy (stays ~32-33% on GSM8K) while reducing speedup from ~3.14x to ~1.5x. This demonstrates that Coconut's bottleneck is **optimization difficulty** (BPTT training instability), not insufficient compute -- confirming the advantage of supervised thoughts.

## Error Analysis

### Where Thinking States Wins Over CoT

Approximately **12% of queries** correctly solved by Thinking States are *not* solved by CoT. Two representative failure modes of CoT:

**Hallucinated steps:** CoT generates an additional spurious reasoning step (e.g., "10*12=120, 120*2=240, 240*30=7200, 7200*6=43200" -- the final step is hallucinated). Thinking States produces the correct 3-step trajectory.

**Over-complex computation:** CoT attempts multiple operations in a single step and errs (e.g., "60-17-34=8" instead of computing each subtraction separately). Thinking States decomposes into atomic operations: "17*2=34", "17+34=51", "60-51=9".

Both models are fine-tuned from the same base model on identical training data, so these differences reflect the method's structural properties, not data advantages.

### The State Ambiguity Problem

The 18-point GSM8K gap is partly explained by **state ambiguity**: the question (what to compute) appears at the end of the input, but Thinking States processes left-to-right. The model may commit to reasoning about the wrong quantity before seeing the question.

**Example:** "Richard lives in a building with 15 floors. Each floor contains 8 units. [T: 15*8=120] Three quarters of the units are occupied. [T: (3/4)*120=90] What's the number of unoccupied units on **each floor**? [T: 120-90=30]" -- The model computes total unoccupied (30) rather than per-floor (2) because it cannot anticipate "on each floor" until the final clause.

**Disambiguation test:** Prepending the question to the start of the prompt ("What's the number of unoccupied units on each floor? Richard lives in a building...") improves accuracy from **42.22% to 48.65%** -- a 6.43-point gain. This is a zero-shot intervention (no retraining), confirming the hypothesis. Notably, this limitation stems from combining chunk-recurrence with a **causal autoregressive backbone**; bidirectional processing could identify the target quantity from the full input before committing to states.

## Position in the Latent Reasoning Spectrum

| Method | Reasoning Format | Supervision | Recurrence | Training Cost | Interpretability |
|--------|-----------------|-------------|------------|---------------|-----------------|
| CoT | NL tokens (appended) | Direct | Sequential generation | Constant | Full |
| [[coconut-reasoning-latent-space\|Coconut]] | Continuous embeddings | None (indirect) | Hidden-state feedback | Linear (BPTT) | None |
| [[softcot-efficient-reasoning\|SoftCoT]] | External soft tokens | Indirect (projection) | None (single pass) | Constant | Via decoding |
| **Thinking States** | **NL $\to$ compressed states** | **Direct (teacher forcing)** | **Chunk-recurrent** | **Constant** | **Full (NL thoughts)** |

Thinking States uniquely combines recurrent conditioning, direct supervision, no context extension, AND interpretability -- properties previously mutually exclusive in the latent reasoning literature.

## Limitations

- **Small model scale**: All experiments use Qwen2.5-0.5B and Qwen2.5-1.5B. Whether Thinking States' advantages persist at frontier scale (7B+, 70B+) is untested, and the [[google-research|Google Research]] team acknowledges this as a key open question.
- **Limited benchmark diversity**: Evaluated only on state tracking (Parity, Vars), GSM8K, and 2-hop QA. Tasks requiring search, planning, code generation, or open-ended reasoning are not covered.
- **No multi-agent evaluation**: Thinking States is evaluated purely as a single-model method. Whether compressed thinking states could serve as inter-agent communication tokens (analogous to how [[coconut-reasoning-latent-space|Coconut]]'s continuous thoughts relate to [[embedding-space-communication]]) is unexplored.
- **State ambiguity concerns**: The 18-point GSM8K gap vs. CoT is partially attributed to the causal left-to-right processing order, where the model commits to reasoning states before seeing the question. While the disambiguation test (prepending the question) recovers 6.43 points, the fundamental tension between causal processing and chunk-recurrent reasoning remains unresolved.

## Future Directions Identified

1. **Extension to decoding phase**: Currently thoughts are generated only during input processing (prefill). Extending to the decoding phase could enable dynamic compute allocation during generation.

2. **RL warm-starting**: The supervised model could serve as initialization for reinforcement learning, allowing the model to optimize its thinking process beyond human-generated CoT traces. Starting from a model that already compresses reasoning into states could stabilize RL training.

3. **Bidirectional processing**: The state ambiguity problem would be resolved if the model could process the full input before committing to intermediate states. This motivates encoder-decoder or bidirectional variants.

## Connections

- **[[latent-space-reasoning]]**: A new point on the spectrum between fully discrete CoT and fully continuous Coconut. Generates discrete thoughts but compresses them into continuous states.
- **[[catastrophic-forgetting]]**: Uses Qwen2.5-Base (not instruction-tuned), avoiding the forgetting problem [[softcot-efficient-reasoning|SoftCoT]] identified. Whether it would work on instruction-tuned models is untested.
- **[[continuous-vs-discrete-representation]]**: Bridges the divide -- thoughts are discrete (supervisable) but their influence on future processing is continuous (compact, rich).
- **[[cot-expressivity-theory|Feng et al.]]**: The deep-to-shallow recurrence directly addresses the depth bottleneck identified theoretically. Each chunk-to-chunk iteration adds effective depth proportional to the number of layers in the loop.
- **[[superposition-coconut-theory|Zhu et al.]]**: An open question is whether Thinking States' compressed states exhibit superposition-like properties. If the compression block preserves frontier information, the method might combine the benefits of supervised reasoning with parallel search.

## Source Materials

- [[raw/pdf/arxiv-2602.08332.pdf|PDF]] ([[raw/latex/arxiv-2602.08332.tar.gz|LaTeX source]])
