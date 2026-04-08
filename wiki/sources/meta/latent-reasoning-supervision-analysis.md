---
type: source
title: "How Do Latent Reasoning Methods Perform Under Weak and Strong Supervision?"
source_file: "[[raw/pdf/arxiv-2602.22441.pdf]]"
latex_source: "[[raw/latex/arxiv-2602.22441.tar.gz]]"
author: "Yingqian Cui, Zhenwei Dai, Bing He, Zhan Shi, Hui Liu, Rui Sun, Zhiji Liu, Yue Xing, Jiliang Tang, Benoit Dumoulin"
date_published: "2026-02-25"
date_ingested: "2026-04-08"
created: "2026-04-08"
updated: "2026-04-08"
venue: "arXiv preprint"
arxiv: "2602.22441"
institution: "Amazon, Michigan State University"
tags: [latent-reasoning, analysis, bfs, shortcut, supervision, foundational]
---

# How Do Latent Reasoning Methods Perform Under Weak and Strong Supervision?

## One-liner

![[latent-reasoning-supervision-analysis/one-liner]]

## Summary

The first comprehensive empirical analysis of the **internal mechanisms** of [[latent-space-reasoning|latent reasoning]] methods. Cui et al. test four representative latent reasoning approaches — [[coconut-reasoning-latent-space|Coconut]], CODI, SIM-CoT, and CoLaR — on GPT-2 and LLaMA-3.2-1B-Instruct against GSM8K-Aug and ProsQA, and report two findings that **directly challenge** the central narrative of the field:

1. **Pervasive shortcut behavior** — most latent methods retain non-trivial accuracy even when latent reasoning is *entirely disabled* (depth = 0) or *destroyed by Gaussian noise* ($\sigma = 100$, far above the embedding norm). They are not actually using their latent steps.
2. **The BFS hypothesis is false in its strong form** — while a single latent vector can encode multiple candidate trajectories (as [[superposition-coconut-theory|Zhu et al.]] proved theoretically), the *iterative* reasoning process exhibits **implicit pruning**, not parallel BFS expansion. Increasing latent depth *decreases* the diversity of next-step distributions, the opposite of true breadth-first search.

The paper introduces a **weak/strong supervision taxonomy**, identifies a fundamental **supervision–exploration trade-off** ([[catastrophic-forgetting|complementary to the alignment trade-off]]), and proposes an **Improved Coconut** training scheme that mixes earlier-stage data into later stages, raising GPT-2's GSM8K-Aug accuracy from 34.09% to 41.06%.

This is the strongest piece of empirical evidence to date that the [[frontier-research-directions|#1 paradigm-shift direction]] (frontier-scale superposition reasoning) has a much harder problem than the field assumed: latent capacity exists, but **the optimization process actively destroys it**.

## Why This Paper Matters

The wiki's [[frontier-research-directions]] document identifies "superposition reasoning at frontier scale" and "disentangling superposed reasoning paths" as the two highest-potential research directions. Both rest on Coconut's empirical claim of **emergent BFS** ([[raw/pdf/arxiv-2412.06769.pdf|Coconut §4.2]]) and Zhu et al.'s theoretical proof that continuous thoughts can encode reachability frontiers ([[superposition-coconut-theory|Zhu et al. Theorem 1]]). Cui et al. **separate these two claims**:

- **Capacity** (a latent vector can encode multiple candidates) — confirmed via Pass@100 analysis: latent reasoning's Pass@100 (62–82%) consistently exceeds explicit reasoning's (44–62%) by 20+ points.
- **Use** (the model actually performs BFS-like exploration across iterations) — falsified. Diversity *decreases* with more latent steps; majority-vote accuracy stays *below* explicit reasoning by 3–4 points.

This is the cleanest decomposition yet of the gap between Coconut's theoretical promise and its empirical reality.

## Method Taxonomy

> [!diagram|left]
> ```mermaid
> graph TD
>     A["Latent Reasoning Methods"]
>     A --> WS["Weak Supervision<br>(outcome-level only)"]
>     A --> SS["Strong Supervision<br>(intermediate alignment)"]
>     WS --> CN["Coconut<br>(stage-wise CoT loss)"]
>     WS --> CD["CODI<br>(outcome + final-state distillation)"]
>     SS --> SC["SIM-CoT<br>(decoder reconstruction loss)"]
>     SS --> CL["CoLaR<br>(token-level compression alignment)"]
>     style A fill:#dae8fc,stroke:#6c8ebf
>     style WS fill:#fff2cc,stroke:#d6b656
>     style SS fill:#ffe6cc,stroke:#d79b00
>     style CN fill:#d5e8d4,stroke:#82b366
>     style CD fill:#d5e8d4,stroke:#82b366
>     style SC fill:#f8cecc,stroke:#b85450
>     style CL fill:#f8cecc,stroke:#b85450
> ```

> [!notation|right]
> | Class | Definition |
> |---|---|
> | Weak supervision | Latent state $c_t$ trained only via final answer loss or final latent alignment |
> | Strong supervision | Latent state $c_t$ trained against per-step textual or compressed targets |

The paper evaluates **four representative methods** spanning the supervision spectrum:

| Method | Supervision | Mechanism | Reference |
|---|---|---|---|
| **[[coconut-reasoning-latent-space\|Coconut]]** (Hao et al., 2024) | Weak | Stage-wise progressive replacement of CoT tokens with continuous thoughts; cross-entropy loss only on remaining textual predictions | arXiv 2412.06769 |
| **CODI** (Shen et al., 2025) | Weak | Unified training with outcome-level loss + teacher–student distillation aligning final latent states from a CoT teacher | arXiv 2502.21074 |
| **SIM-CoT** (Wei et al., 2025) | Strong | Decoder-based explanation loss: reconstructs the corresponding textual reasoning step from each intermediate latent state | arXiv 2509.20317 |
| **CoLaR** (Tan et al., 2025) | Strong | Token-level compression: averages every $c$ consecutive token representations, uses the average as the supervision target | arXiv 2505.16552 |

For all experiments, SIM-CoT is implemented on top of CODI (the better-performing variant) and CoLaR uses compression factor $c = 5$ to match the latent step count of other methods.

## Experimental Setup

- **Backbones**: GPT-2 (full fine-tuning) and LLaMA-3.2-1B-Instruct (LoRA fine-tuning)
- **Datasets**:
  - **GSM8K-Aug** ([[icot-internalize-cot|Deng et al., 2024]]): augmented grade-school math word problems with structured reasoning chains
  - **ProsQA** ([[coconut-reasoning-latent-space|Hao et al., 2024]]): multi-step first-order logical reasoning over compositional rules; harder than ProntoQA
- **Embedding norms** (used to calibrate noise interventions): GPT-2 latent embeddings have $\ell_2$ norm $\approx 24.42$ (768-dim); LLaMA-3.2-1B has $\approx 44.08$ (2048-dim)

## Finding 1: Pervasive Shortcut Behavior

### Latent Step Depth Ablation

The paper varies the number of latent steps at *inference* time, holding training fixed. Under a true BFS model, accuracy should collapse when latent depth is forced to zero. The actual results:

| Method | Backbone | GSM8K @ depth=0 | GSM8K @ default | ProsQA @ depth=0 | ProsQA @ default |
|---|---|---|---|---|---|
| Coconut | LLaMA | non-trivial | 36.97% | ~99% | 99.40% |
| **CODI** | LLaMA | **~30%** | 55.57% | ~100% | 100.00% |
| SIM-CoT | LLaMA | reduced | 56.03% | ~100% | 100.00% |
| **CoLaR** | LLaMA | **near-zero** | 25.23% | random (~50%) | 98.20% |

**Two patterns emerge**:
1. **GSM8K is shortcut-resistant for some methods**: accuracy correlates with latent depth, especially for CoLaR (the strongest-supervision method), which collapses to near-random when latent depth = 0.
2. **ProsQA is universally shortcut-prone**: every weakly-supervised method maintains its full ProsQA accuracy at depth = 0. ProsQA's compositional logic patterns are simple enough that input attention alone suffices.

### Noise Injection Validation

To rule out the hypothesis that depth-0 inference simply uses early latent representations, the paper injects strong Gaussian noise ($\Sigma = \sigma^2 \mathbf{I}$, $\sigma = 100$) into the latent embedding **after** the latent reasoning loop completes but **before** the final answer is generated. The injected noise is roughly $4\times$ the magnitude of the actual latent embeddings.

### Table 1: Clean vs. Noise (reproduced)

| Model | Setting | Coconut GSM8K | Coconut ProsQA | CODI GSM8K | CODI ProsQA | CoLaR GSM8K | CoLaR ProsQA | SIM-CoT GSM8K | SIM-CoT ProsQA | Std CoT GSM8K | Std CoT ProsQA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LLaMA | clean | 36.97% | 99.40% | 55.57% | 100.00% | 25.23% | 98.20% | 56.03% | 100.00% | 61.74% | 90.60% |
| LLaMA | noise | **20.61%** | **99.40%** | **27.45%** | 99.60% | **3.32%** | 60.92% | 10.08% | 97.60% | **0.03%** | 0.40% |
| GPT-2 | clean | 34.09% | 97.80% | 43.59% | 80.80% | 18.44% | 77.52% | 42.23% | 80.60% | 43.56% | 81.00% |
| GPT-2 | noise | **3.79%** | **89.00%** | 8.87% | 80.80% | 2.84% | 46.80% | 7.05% | 75.60% | 0.08% | 0.00% |

Standard CoT collapses to ~0% under the same noise — an essential control showing the perturbation is destructive. Latent methods retain 9–28% accuracy on GSM8K and 47–99% on ProsQA, **proving** they bypass their own latent representations.

### Attention-Based Diagnosis

Cui et al. visualize the top-10 attention weights from each output token during final-answer generation, excluding the universal "attention sink" token. The findings:

- **Coconut on ProsQA**: top-10 attended tokens for every output token come **entirely from the input question**, never from latent reasoning tokens. The latent state is bypassed.
- **Coconut on GSM8K**: top-10 attention shifts to latent tokens when generating final numerical answers (e.g., the answer token "18"), confirming that GSM8K does engage latent reasoning more.

This is the most direct mechanistic evidence yet that **shortcut behavior is task-specific**: it dominates when input patterns suffice for the answer, and recedes when they don't.

## Finding 2: BFS Hypothesis Is False (in Its Strong Form)

### The Coconut Collapse

Before testing BFS, Cui et al. discover a **degenerate inference mode** in Coconut: when fewer latent steps are provided at inference than during the final training stage, Coconut directly emits the final answer instead of resuming textual reasoning. This breaks any clean test of BFS, since reducing latent depth doesn't actually shorten reasoning — it just skips it.

**Hypothesized cause**: Coconut's stage-wise curriculum trains stage $k$ exclusively on data with $k$ latent steps. Later stages override the early-stage behavior of producing remaining textual steps after the `<|end-of-latent|>` marker. The model collapses to "encountering `<|end-of-latent|>` $\Rightarrow$ emit answer."

### Improved Coconut

To enable a clean BFS test, the paper introduces a **data-mixing variant** of Coconut's curriculum: at training stage $k$, the proportion of data sampled from earlier stage $i$ ($i \leq k$) is set to be proportional to $(i+1)$, ensuring continued exposure to short-latent-step examples throughout training.

**Empirical impact** (GPT-2):

| Variant | GSM8K-Aug | GSM8K-Aug-NL |
|---|---|---|
| Original Coconut | 34.09% | 24.90% |
| **Improved Coconut** | **41.06%** | **33.48%** |

The **+7 to +9 point gain** from a pure data-sampling change suggests that even Coconut's official numbers were depressed by the collapse phenomenon. This is a clean follow-up contribution: the entire downstream literature (Improved Coconut as a stronger baseline) inherits the fix.

### BFS Verification: Hybrid Latent–Text Rollouts

With the collapse mitigated, the paper tests the BFS hypothesis directly using **hybrid latent–text rollouts**:

1. Run a fixed prefix of $n$ latent reasoning steps.
2. Stochastically decode the remaining steps in text space at temperature $T = 1$, generating 100 independent rollouts per prefix.
3. Count the number of *distinct* next-step predictions and *distinct* final outcomes across the 100 samples.
4. Compare to a text-only baseline where the first $n$ steps are generated deterministically in text and only the remainder is sampled.

**Under true BFS**, increasing $n$ should produce *more* distinct outcomes (the latent state accumulates an expanding frontier of possibilities). The actual data:

### Table 2: Distribution of distinct possibilities (reproduced)

| # prefix steps | Latent next (avg) | Latent next (max) | Latent final (avg) | Explicit next (avg) | Explicit final (avg) |
|---|---|---|---|---|---|
| 1 | 18.75 | 87 | 28.35 | 3.68 | 9.32 |
| 2 | 20.38 | 89 | 25.50 | 3.31 | 6.59 |
| 3 | 20.00 | 97 | 21.82 | 2.73 | 4.17 |
| 4 | 17.22 | 92 | 17.74 | 2.01 | 2.42 |
| 5 | 15.84 | 91 | 15.84 | 1.27 | 1.37 |

**Three observations**:

1. **Latent diversity dramatically exceeds explicit diversity** (15–28 vs. 1–9 distinct candidates) — capacity confirmed.
2. **Latent diversity initially rises slightly, then *decreases*** with more latent steps — the opposite of BFS. The latent reasoning process is actively pruning, not expanding.
3. **Explicit diversity also decreases monotonically** with prefix length, as expected for autoregressive sampling, but it does so more steeply.

### Pass@100 vs. Majority Vote

If latent reasoning maintains more candidates, can we exploit that diversity at decode time? The paper measures **Pass@100** (any of 100 samples is correct) and **Maj@100** (majority-vote accuracy).

### Table 3: Implicit vs. explicit ensemble accuracy (Coconut, GPT-2, GSM8K)

| # prefix steps | Implicit Pass@100 | Implicit Maj@100 | Explicit Pass@100 | Explicit Maj@100 |
|---|---|---|---|---|
| 1 | 82.34% | 44.20% | 62.17% | 44.12% |
| 2 | 78.62% | 41.70% | 55.34% | 44.05% |
| 3 | 75.74% | 39.95% | 48.30% | 42.71% |
| 4 | 70.36% | 39.73% | 45.87% | 43.52% |
| 5 | 69.07% | 39.42% | 44.05% | 43.59% |

**Key implication**: latent reasoning preserves a **larger correct-candidate pool** (Pass@100 advantage of 20–25 points) but **fails to amplify the correct candidate** during the latent process (Maj@100 disadvantage of 3–4 points). The reasoning loop pruning is not selecting *for correctness* — it's selecting essentially at random.

This is the cleanest experimental statement to date of the gap between **representational capacity** and **algorithmic competence** in latent reasoning.

### Cross-Method Distribution Analysis

### Table 4: Distinct possibilities and accuracy across methods (GPT-2)

| Method | Distinct outcomes (avg) | Accuracy (greedy) | Pass@100 | Maj@100 |
|---|---|---|---|---|
| **Improved Coconut** | **15.84** | 34.09% | 69.07% | 39.42% |
| CODI | 12.96 | 43.59% | 70.43% | 42.23% |
| SIM-CoT | 13.57 | 42.23% | 69.60% | 43.21% |
| **CoLaR** | **3.21** | 18.44% | 23.28% | 18.42% |

### Table 5: Same analysis on LLaMA-3.2-1B-Instruct

| Method | Distinct outcomes (avg) | Accuracy (greedy) | Maj@100 | Pass@100 |
|---|---|---|---|---|
| Improved Coconut | 10.0 | 39.68% | 40.21% | 59.00% |
| CODI | 6.39 | 55.41% | 55.57% | 73.84% |
| SIM-CoT | 7.46 | 56.01% | 55.50% | 72.93% |
| CoLaR | 7.63 | 25.48% | 25.70% | 33.21% |

The cross-method ordering is striking:

- **Weak supervision** ⇒ **high diversity** (Coconut: 15.84 distinct outcomes), **low accuracy** (34.09% greedy), but **high Pass@100** (69.07%).
- **Strong supervision** ⇒ **low diversity** (CoLaR: 3.21 distinct outcomes), **low accuracy** (18.44% greedy), and **low Pass@100** (23.28%).
- **Hybrid CODI/SIM-CoT** sit in between, with the highest accuracy and Pass@100 but moderate diversity.

CoLaR's collapse to 3.21 distinct outcomes confirms the symmetric problem: rigid supervision destroys the very property (latent capacity) that makes latent reasoning interesting.

## The Supervision–Exploration Trade-Off

The paper's central conceptual contribution is identifying a **fundamental supervision-strength trade-off**:

| Supervision strength | Shortcut behavior | Latent diversity | Pass@100 ceiling | Practical accuracy |
|---|---|---|---|---|
| Weak (Coconut, CODI) | Severe (especially on simple tasks) | High | High | Limited by inability to amplify correct candidate |
| Strong (SIM-CoT, CoLaR) | Reduced or eliminated | Low | Low | Limited by loss of capacity |

This is **distinct from but complementary to** the [[catastrophic-forgetting|alignment trade-off]] identified by [[softcot-efficient-reasoning|SoftCoT]]:

| Trade-off | Tension | Mitigation in literature |
|---|---|---|
| Alignment trade-off | Backbone modification damages instruction-tuning | Frozen-backbone designs ([[softcot-efficient-reasoning|SoftCoT]], [[thinking-states-latent-reasoning|Thinking States]], [[latentmas-collaboration|LatentMAS]]) |
| **Supervision–exploration trade-off** | **Stronger supervision destroys latent capacity** | **None — open problem** |

Together, these two trade-offs **bound** the latent reasoning design space from both sides: too little supervision and the model takes shortcuts or fails to exploit its own representations; too much supervision and the latent state collapses to a deterministic compression of CoT.

## Limitations

1. **Scale ceiling**: All experiments use GPT-2 (117M) and LLaMA-3.2-1B. The findings join [[coconut-reasoning-latent-space|Coconut]] and [[icot-internalize-cot|iCoT]] in the [[benchmark-overlap|"<2B latent reasoning" cluster]] — none of the conclusions are validated at the 7B+ scale where superposition might emerge differently.
2. **Two-task ceiling**: Only GSM8K-Aug and ProsQA. The shortcut behavior may differ on harder math (MATH, AIME) or non-math reasoning (GPQA, ARC).
3. **No counterfactual training fix**: The paper diagnoses but does not solve the supervision–exploration trade-off. Improved Coconut helps with the collapse issue, not with the deeper amplification failure.
4. **No SoftCoT/LatentMAS coverage**: The four methods are all single-model latent reasoning. The paper does not test [[softcot-efficient-reasoning|SoftCoT]]'s externalized variant, [[thinking-states-latent-reasoning|Thinking States]]' chunk-recurrent variant, or [[latentmas-collaboration|LatentMAS]]'s training-free transfer — exactly the methods that the [[catastrophic-forgetting|catastrophic forgetting]] literature suggests are most likely to scale.
5. **Pass@100 / Maj@100 asymmetry is not explained mechanistically**: We learn that latent reasoning fails to amplify the correct candidate, but not *why*. Is it an optimization failure, a model-capacity ceiling, or a fundamental property of the autoregressive latent loop?
6. **No comparison to inference-time scaling baselines**: The Pass@100 numbers should be benchmarked against best-of-N CoT and self-consistency to determine whether latent reasoning's diversity is genuinely *better* or just *bigger*.

## Connection to Existing Wiki Pages

### Direct experimental tests

- **[[coconut-reasoning-latent-space|Coconut (Hao et al., 2024)]]**: Cui et al. test the *same model* on the *same datasets*. The Improved Coconut variant (+7pp on GSM8K-Aug) is a direct follow-up. The shortcut analysis is the strongest mechanistic critique of Coconut to date.
- **[[superposition-coconut-theory|Superposition Theory (Zhu et al., 2025)]]**: Cui et al. **partially confirm** the theory (latent vectors do encode multiple candidates) but **falsify the iterative-BFS extension** (the process exhibits implicit pruning, not breadth-first expansion). The theoretical bound is achievable in capacity but not in dynamics.
- **[[icot-internalize-cot|iCoT]]**: Same GPT-2 backbone, related stage-wise curriculum. The collapse-mitigation insight (mix earlier-stage data) plausibly transfers to iCoT's progressive removal schedule.

### Concept page updates

- **[[latent-space-reasoning]]**: The "Emergent BFS" section needs a major caveat — capacity ≠ use. The "Three Solutions to the Training Challenge" table should add a fourth row for the supervision–exploration trade-off as an orthogonal failure mode.
- **[[catastrophic-forgetting]]**: Add the supervision–exploration trade-off as a *complementary* training-time barrier. The two trade-offs together explain why the latent reasoning design space is so constrained.
- **[[continuous-vs-discrete-representation]]**: The Pass@100 / Maj@100 gap is a quantitative instance of the discrete bottleneck — discrete tokens can't represent the multi-candidate state, but the multi-candidate state alone is insufficient.

### Analysis page updates

- **[[contradictions]]**: New tension #9 — "BFS as faithful structured search vs. implicit pruning" (Coconut/Zhu et al. vs. Cui et al.). Status: **partially resolved by Cui et al.** — capacity confirmed, dynamics falsified.
- **[[frontier-research-directions]]**: Direction #1 (superposition reasoning at frontier scale) and #2 (disentangling superposed paths) need a new "blockers" subsection — Cui et al. show the optimization process actively destroys the property both directions try to exploit.
- **[[benchmark-overlap]]**: Add to the "<2B latent reasoning cluster" and the GSM8K table.
- **[[open-questions]]**: Add the supervision–exploration trade-off as an open question; add the Pass@100 / Maj@100 amplification gap.

### MOC updates

- **[[latent-reasoning]]**: Add as a "critical empirical analysis" entry following Coconut and Superposition Theory.
- **[[theoretical-foundations]]**: Add as the empirical counterpoint to Zhu et al.'s superposition proof — together they bracket what is and isn't true about parallel BFS in latent space.
- **[[safety-interpretability]]**: The shortcut and noise-injection findings are directly relevant — latent reasoning that bypasses its own reasoning is a safety concern (you cannot audit a process that isn't being used).

## Open Questions Raised

1. **Can the amplification gap be closed?** Latent reasoning's Pass@100 advantage suggests the correct candidate is *somewhere* in the latent state. Is there a decoding strategy (rerankers, latent-aware best-of-N, learned aggregation) that recovers this?
2. **Does the supervision–exploration trade-off scale with model size?** At GPT-2 scale, weak supervision allows ~16 distinct outcomes. Would a 7B model maintain proportionally more, or does the trade-off flatten?
3. **Is implicit pruning learnable or innate?** Does Coconut prune because the gradient signal pushes it to commit, or because the transformer architecture lacks the inductive bias to maintain multiple hypotheses across iterations?
4. **Can [[thought-communication-multiagent|ThoughtComm]]-style disentanglement break the trade-off?** If a sparse autoencoder can separate distinct candidate trajectories from a single latent vector (as ThoughtComm does for inter-agent thoughts), the iterative pruning could be bypassed entirely — each latent step would route through the disentangled space.
5. **Do cross-architectural latent methods escape the trade-off?** [[softcot-efficient-reasoning|SoftCoT]]'s externalized assistant and [[latentmas-collaboration|LatentMAS]]'s training-free alignment both avoid the supervision dilemma by not training the backbone at all. Their performance vs. the Pass@100/Maj@100 gap is an open empirical question.

## Source Materials

- [[raw/pdf/arxiv-2602.22441.pdf|PDF]] ([[raw/latex/arxiv-2602.22441.tar.gz|LaTeX source]])
