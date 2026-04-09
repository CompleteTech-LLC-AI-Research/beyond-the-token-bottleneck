---
type: source
title: "Towards Inference-time Scaling for Continuous Space Reasoning"
source_file: "[[raw/pdf/arxiv-2510.12167.pdf]]"
latex_source: "[[raw/latex/arxiv-2510.12167.tar.gz]]"
author: "Minghan Wang, Thuy-Trang Vu, Ehsan Shareghi, Gholamreza Haffari"
date_published: "2025-10-14"
date_ingested: "2026-04-08"
created: "2026-04-08"
updated: "2026-04-08"
venue: "arXiv preprint"
arxiv: "2510.12167"
institution: "Monash University"
tags: [latent-reasoning, inference-time-scaling, reward-modeling, prm, orm, geometric-analysis, diagnostic]
---

# Towards Inference-time Scaling for Continuous Space Reasoning

## One-liner

![[inference-time-scaling-continuous-reasoning/one-liner]]

## Summary

The first paper to ask whether the **inference-time scaling toolkit** of discrete reasoning — best-of-N sampling, self-consistency, Process Reward Models (PRM), Outcome Reward Models (ORM) — can be transplanted into [[latent-space-reasoning|continuous-space reasoning]]. Wang et al. operate on [[coconut-reasoning-latent-space|COCONUT]] (GPT-2 / GSM8K) and answer in three movements:

1. **Sampling works.** A surgically simple intervention — enabling dropout *only* during the latent reasoning loop, not during answer decoding — produces diverse continuous-thought trajectories. Pass@N rises from 31.08% (N=1) to **44.43% (N=32)**, surpassing both deterministic COCONUT and the text-CoT baseline. The number of unique answers grows logarithmically, suggesting reranking is computationally tractable.
2. **Reranking fails.** Adapting MATH-Shepherd's Monte Carlo annotation pipeline to continuous thoughts and training both PRM (hard + soft labels) and ORM yields only **+2.28 points** at best — a fraction of the +13.35-point Pass@N upper bound. Self-consistency and confidence reranking provide essentially zero gain.
3. **The diagnosis is geometric.** Continuous-thought representations exhibit extreme anisotropy (IsoScore $\approx$ 0.013) and modest sparsity (Hoyer $\approx$ 0.21), and — crucially — **correct and incorrect thoughts are indistinguishable** by every geometric and trajectory-dynamics metric tested (compactness, curvature, local smoothness, straightness). t-SNE shows complete intermixing. PRM/ORM classifiers achieve F1 scores barely above chance (54.09% / 51.59%) because there is no signal to learn.

This is the empirical companion to [[latent-reasoning-supervision-analysis|Cui et al. (2026)]]: where Cui et al. **identify** the Pass@100 / Maj@100 amplification gap, Wang et al. **operationalize** it with the most natural fix (train a reward model), show that the fix doesn't work, and explain *why*. Together the two papers reframe latent reasoning's central problem from "scale up Coconut" to "build geometric structure into continuous thought space so that correct and incorrect reasoning paths are *separable*."

## Why This Paper Matters

The wiki has been tracking a precise gap, formalized in [[contradictions]] #9 and [[frontier-research-directions]] #1: latent reasoning's correct-candidate pool is *larger* than CoT's (Pass@100 advantage of 20+ points), but its majority-vote accuracy is *lower* than CoT's by 3-4 points. [[latent-reasoning-supervision-analysis|Cui et al.]] identified this asymmetry and called for "a latent-aware reranker, learned aggregator, or alternative decoding strategy" to recover the diversity advantage. **Wang et al. tried it.** They built the reranker. They trained the PRM. They followed the discrete-space recipe. It didn't work, and they explain why with a battery of geometric and trajectory-dynamics measurements.

The paper therefore turns an open research direction into a *partially-resolved* one: the obvious approach is now empirically falsified at GPT-2 scale, and the analysis pinpoints the missing ingredient (inductive biases that promote geometric separability between correct and incorrect thoughts during *training*, not just at inference). Any future paper proposing a latent-aware decoder must engage with Wang et al.'s null result and explain why its approach overcomes the geometric homogeneity barrier.

## Method

> [!diagram|left]
> ```mermaid
> graph TD
>     X["Question X"] --> S1["Latent step s_1<br>(dropout ON)"]
>     S1 --> S2["Latent step s_2<br>(dropout ON)"]
>     S2 --> S3["..."]
>     S3 --> ST["Latent step s_T"]
>     ST --> A["Answer decoding<br>(dropout OFF)"]
>     A --> R["Sampled answer a_n"]
>     R -->|"repeat N times"| X
>     R --> RM["PRM / ORM<br>reranker"]
>     RM --> FA["Final answer"]
>     style X fill:#dae8fc,stroke:#6c8ebf
>     style S1 fill:#fff2cc,stroke:#d6b656
>     style S2 fill:#fff2cc,stroke:#d6b656
>     style ST fill:#fff2cc,stroke:#d6b656
>     style A fill:#d5e8d4,stroke:#82b366
>     style RM fill:#ffe6cc,stroke:#d79b00
>     style FA fill:#e1d5e7,stroke:#9673a6
> ```

> [!notation|right]
> | Symbol | Meaning |
> |---|---|
> | $X$ | Input question prompt |
> | $\mathbf{s}_i \in \R^D$ | $i$-th continuous thought vector |
> | $T = c \cdot k$ | Total latent steps ($c=2$, $k=3$) |
> | $N$ | Number of stochastic samples per question |
> | $y^{HE}_{s_i}$ | Hard MC label for step $s_i$ |
> | $y^{SE}_{s_i}$ | Soft MC label for step $s_i$ |
> | $r^{OUT}$ | Outcome label for trajectory |

### Stochastic Sampling via Selective Dropout

COCONUT's reasoning is deterministic by construction — each latent step $\mathbf{s}_i = f_\theta(X, \mathbf{s}_{<i})$ is computed by a single forward pass with no sampling temperature, so applying temperature only at the answer-decoding stage cannot diversify the *trajectory*, only the *transcription* of a single trajectory.

The fix is minimal: enable dropout (at the same rate used during training) **only during the iterative hidden-state generation phase**, then disable it for the final-answer text generation. This confines stochasticity to the latent loop without compromising answer-decoding integrity. Each forward pass through the dropout-enabled COCONUT now produces a different continuous-thought trajectory, and Pass@N can be measured by drawing $N$ such trajectories and decoding each one's answer.

### MC Annotation for Continuous-Thought Reward Models

The reward modeling pipeline is a direct adaptation of MATH-Shepherd to continuous thoughts (Algo 1 in the paper). For each problem $X$ with ground-truth answer $a^*$:

1. Sample $M = 5$ continuous-thought trajectories via dropout, deduplicate by final answer (yielding $\sim$1.32 unique trajectories per problem).
2. For each step $\mathbf{s}_i$ in each unique trajectory, take the partial trajectory $\tau_{1:i}$ and Monte-Carlo sample $N = 10$ completions from it.
3. Compute step-wise labels:
   - **Hard estimation**: $y^{HE}_{s_i} = \mathbf{1}[\exists j: a_j = a^*]$ — does *any* completion from this prefix reach the correct answer?
   - **Soft estimation**: $y^{SE}_{s_i} = \frac{1}{N}\sum_{j=1}^{N} \mathbf{1}[a_j = a^*]$ — what *fraction* of completions reach it?
4. Compute trajectory-level outcome labels: $r^{OUT} = \mathbf{1}[\text{final answer correct}]$.

Annotation is run on the GSM8K training set, yielding 238K samples for PRM and 324K for ORM, balanced 1:1 between positive and negative. **Critical architectural constraint**: continuous thoughts are model-specific, so the reward model backbone *must* be COCONUT itself — a reward model trained on a different transformer cannot interpret COCONUT's latent representations. Wang et al. attach two-layer MLP heads (ReLU + sigmoid) to a COCONUT base for hard/soft PRM and ORM.

The PRM loss is the joint cross-entropy + MSE objective:

$$\mathcal{L}_{PRM} = \mathcal{L}_{CE}(y^{HE}_{s_i}, \hat{y}^{HE}_{s_i}) + \mathcal{L}_{MSE}(y^{SE}_{s_i}, \hat{y}^{SE}_{s_i})$$

ORM uses cross-entropy alone on the trajectory outcome.

## Experimental Setup

- **Backbone**: GPT-2 (117M) trained as in [[coconut-reasoning-latent-space|the original Coconut paper]] — 6 epochs in the initial stage, 3 epochs in each of 3 subsequent stages.
- **Latent budget**: $T = 3 \times c$ with $c = 2$, i.e. 6 continuous-thought vectors per trajectory.
- **Sampling sizes**: $N \in \{1, 2, 4, 8, 16, 32\}$.
- **Dataset**: GSM8K — training set used for RM data construction; test set used for BoN evaluation.
- **Reward model training**: 10 epochs, learning rate 1e-4 with 500 warmup steps, batch size 128, single A100 GPU.
- **Evaluation dataset for analysis**: A 3,014-sample subset of GSM8K test, with $M = 10$ trajectories per problem (2.29 unique on average) and $N = 20$ MC completions for label reliability. Natural distribution preserved (18.48% correct answers, 28.21% correct reasoning steps).
- **Baselines**: text CoT, deterministic COCONUT, confidence-based reranking (answer-probability scoring), self-consistency (majority voting).

## Finding 1: Sampling Unlocks a Pass@N Advantage

### Pass@N vs. Baselines

The headline result on GSM8K (N=32):

| Method | GSM8K Acc. |
|---|---|
| Deterministic COCONUT | 31.08% |
| Text CoT (GPT-2) | $\sim$42.9% |
| Dropout-sampled COCONUT, Pass@1 | $<$31.08% (slight degradation) |
| Dropout-sampled COCONUT, **Pass@32** | **44.43%** |

Pass@1 is *slightly* below deterministic COCONUT — enabling dropout during inference imposes a small per-sample cost — but Pass@N rapidly surpasses both COCONUT and text CoT as $N$ grows. The Pass@32 number (44.43%) **exceeds the GPT-2 text CoT baseline**, which is the cleanest demonstration to date that COCONUT's latent state really does contain a richer correct-answer pool than its single deterministic decoding can recover.

### Logarithmic Growth of Unique Answers

| N | # Unique answers (avg) | # Correct (avg) | # Major incorrect (avg) | Pass@N |
|---|---|---|---|---|
| 1 | 1.00 | 0.31 | 0.69 | 31.08 |
| 2 | 1.33 | 0.62 | 1.14 | 35.10 |
| 4 | 1.72 | 1.24 | 2.11 | 38.67 |
| 8 | 2.16 | 2.45 | 4.09 | 41.02 |
| 16 | 2.62 | 4.95 | 8.02 | 42.61 |
| 32 | 3.17 | 9.84 | 15.88 | 44.43 |

Two patterns are diagnostic of the central problem:

1. **Unique answers grow logarithmically** in $N$ (1.00 → 3.17 from N=1 to N=32), so the candidate pool stays small and reranking remains tractable. This is *good news for the reranker hypothesis*.
2. **Major incorrect answers vastly outnumber correct ones** at every $N$ (15.88 vs. 9.84 at N=32). The dominant mode of the candidate distribution is *wrong*. Naive majority voting cannot work.

The second pattern is the death blow for self-consistency: the latent process not only fails to amplify the correct answer, it actively concentrates probability mass on a *wrong* one. This agrees with [[latent-reasoning-supervision-analysis|Cui et al.]]'s finding that Coconut's Maj@100 sits below explicit reasoning's even though its Pass@100 exceeds it.

## Finding 2: PRM and ORM Reranking Yields Only Marginal Gains

### Best-of-N Across Reranking Methods (Table 1, GSM8K)

| N | Pass@N | Confidence | Self-Consistency | PRM-HE | PRM-SE | ORM |
|---|---|---|---|---|---|---|
| 1 | 31.08 | 31.08 | 31.08 | 31.08 | 31.08 | 31.08 |
| 2 | 35.10 | 31.08 | 31.01 | 31.69 | 30.86 | 31.61 |
| 4 | 38.67 | 30.48 | 31.61 | 32.45 | 32.37 | 32.15 |
| 8 | 41.02 | 29.87 | 31.24 | **33.06** | 32.52 | 31.46 |
| 16 | 42.61 | 31.39 | 32.15 | **33.36** | 32.37 | 32.37 |
| 32 | 44.43 | 30.71 | 32.15 | 32.83 | **33.28** | 31.39 |

**The gap is brutal**:
- Pass@N upper bound at N=16: **42.61%** (theoretical ceiling for this candidate pool)
- Best reranker (PRM-HE) at N=16: **33.36%** (+2.28pp over baseline)
- Realized fraction of the upper bound: **(33.36 − 31.08) / (42.61 − 31.08) = 19.8%**

PRM-HE is the best of the trained methods but recovers less than a quarter of the available headroom. **Confidence-based reranking is *worse* than the baseline at most $N$**, indicating that COCONUT's answer probabilities are completely uncalibrated. Self-consistency provides essentially zero gain — confirming directly that the majority answer is *systematically wrong*.

### Score Aggregation Strategies (Table 2)

To rule out the possibility that the issue is simple aggregation choice, Wang et al. compare last-step / min / max / mean aggregation following [Zhang et al., 2025]:

| N | Hard last | Hard min | Hard max | Hard mean | Soft last | Soft min | Soft max | Soft mean |
|---|---|---|---|---|---|---|---|---|
| 1 | 31.08 | 31.08 | 31.08 | 31.08 | 31.08 | 31.08 | 31.08 | 31.08 |
| 8 | 33.06 | 32.98 | 31.69 | 33.06 | 32.52 | 31.46 | 32.22 | 33.06 |
| 16 | 33.36 | 33.13 | 32.37 | 33.13 | 32.37 | 31.61 | 31.77 | 32.52 |
| 32 | 32.83 | 32.52 | 31.84 | 32.90 | 33.28 | 32.60 | 32.75 | 33.06 |

Aggregation choice changes results by less than 1pp. The bottleneck is *not* in how scores are combined — it is in the reward model's ability to assign meaningful scores in the first place.

## Finding 3: The Reward Models Cannot Discriminate

### Classification Performance (Table 3)

On the held-out 3,014-sample test set, with threshold 0.5:

| Model | Accuracy | Precision | Recall | F1 | Specificity |
|---|---|---|---|---|---|
| PRM | 62.98 | **41.60** | 77.28 | **54.09** | 57.36 |
| ORM | 73.72 | **39.11** | 75.76 | **51.59** | 73.26 |

**Both reward models fail at the classification task they were trained for**. F1 scores hover around chance. Precision is in the 39-42% range, meaning a "correct" prediction from either model is wrong more often than right. PRM emits 5,535 false positives versus only 3,943 true positives — it labels incorrect reasoning steps as correct *more often than it labels them correctly*.

The ORM achieves higher overall accuracy (73.72%) only because the test set is class-imbalanced (18.48% correct) and ORM defaults to predicting "incorrect" — the high specificity (73.26%) reflects this class skew, not real discriminative ability.

The implication is decisive: **the bottleneck is not the reward model architecture or training recipe — it is the absence of any learnable signal in the input representations.** No amount of MLP-head depth, training data, or aggregation cleverness can extract a discriminative signal that isn't there.

### Why? Geometric Homogeneity (Table 4)

Wang et al. measure two geometric properties of continuous thought vectors:

- **IsoScore$\star$** (Rudman & Eickhoff, 2024): a rotation-invariant, mean-agnostic measure of representational isotropy. 1 = perfectly isotropic; 0 = maximally anisotropic.
- **Hoyer sparsity** (Hurley & Rickard, 2009): higher = sparser activation, fewer dominant dimensions.

Computed across three sample groups (entire test set, PRM-correctly-predicted, PRM-incorrectly-predicted), separating "correct" and "incorrect" reasoning steps within each:

| Group | IsoScore$\star$ Correct | IsoScore$\star$ Incorrect | Hoyer Correct | Hoyer Incorrect |
|---|---|---|---|---|
| Entire set | 0.0134 | 0.0130 | 0.21 ± 0.01 | 0.22 ± 0.01 |
| PRM+ | 0.0137 | 0.0131 | 0.21 ± 0.01 | 0.22 ± 0.01 |
| PRM− | 0.0126 | 0.0132 | 0.22 ± 0.01 | 0.21 ± 0.01 |

**Two findings, both decisive**:

1. **Continuous thoughts are extremely anisotropic** (IsoScore$\star \approx 0.013$, on a 0-1 scale where 1 is isotropic). They occupy a very low-dimensional subspace of the 768-dim hidden space. Sparsity is moderate ($\sim$0.21 Hoyer).
2. **Correct and incorrect thoughts are statistically indistinguishable** by either metric. Differences are within 0.0008 IsoScore and 0.01 Hoyer — well within noise.

A t-SNE visualization (Figure 3 in the paper) confirms the same picture: correct and incorrect thoughts intermix completely. The two visible clusters in the t-SNE correspond to the two thought-positions per reasoning step ($c=2$), not to any correctness signal.

### Trajectory Dynamics Are Equally Indistinguishable (Table 5)

Treating the 6-step continuous-thought sequence as a trajectory in $\R^{768}$, Wang et al. compute four trajectory metrics:

- **Compactness** (radius of gyration): $\sqrt{\frac{1}{T}\sum_i \|\mathbf{s}_i - \bar{\mathbf{s}}\|_2^2}$
- **Curvature** (total angular bending): $\sum_{i=2}^{T-1} \arccos\left(\frac{\Delta_{i-1} \cdot \Delta_i}{\|\Delta_{i-1}\| \|\Delta_i\|}\right)$
- **Local smoothness** (average cosine between consecutive thoughts)
- **Straightness** (net displacement / total path length)

| Subset | Metric | Correct | Incorrect | $p$ | Cohen's $d$ |
|---|---|---|---|---|---|
| Entire set | Compactness | 19.81 ± 2.53 | 19.39 ± 2.48 | 0.023* | 0.17 |
| Entire set | Curvature | 9.32 ± 0.52 | 9.38 ± 0.53 | 0.161 | −0.10 |
| Entire set | Local smoothness | 0.43 ± 0.11 | 0.44 ± 0.11 | 0.074 | −0.13 |
| Entire set | Straightness | 0.22 ± 0.04 | 0.21 ± 0.04 | 0.637 | 0.04 |
| PRM+ | Compactness | 20.72 ± 1.97 | 18.55 ± 1.83 | 0.022* | 1.14 |
| PRM+ | Local smoothness | 0.39 ± 0.09 | 0.48 ± 0.10 | 0.049* | −0.97 |

The only statistically significant differences appear *within the PRM+ subset* — the small subgroup the reward model already classifies correctly. Even there, only compactness and local smoothness reach significance, and only with effect sizes that reverse direction (correct trajectories are *more* compact and *less* smooth). On the entire set, no metric achieves a Cohen's $d$ above 0.17.

**Conclusion**: trajectory dynamics carry essentially no information about reasoning correctness. The continuous-thought process produces the same kinds of curves regardless of whether it eventually arrives at the right answer.

## Finding 4: Coconut Partially Bypasses Its Own Latent Thoughts

### Perturbation Test (Table 6)

To probe whether continuous thoughts contain semantic information at all, Wang et al. inject Gaussian noise into the latent thoughts at varying ratios — $\text{ratio} \times \text{noise} + (1-\text{ratio}) \times \text{thought}$ — and measure Pass@5 on GSM8K:

| Noise Ratio | # Unique answers | Pass@5 | # Correct (avg) | % Majority answer unchanged |
|---|---|---|---|---|
| 0.0 | 1.86 | 39.20 | 1.55 | 100.00 |
| 0.2 | 1.92 | 38.67 | 1.50 | 76.35 |
| 0.4 | 2.22 | 34.80 | 1.24 | 67.32 |
| 0.6 | 2.56 | 20.32 | 0.55 | 44.73 |
| 0.8 | 2.62 | 15.62 | 0.37 | 49.43 |
| 1.0 | 2.49 | **12.59** | 0.32 | 53.83 |

**Two observations**:

1. **Robustness at low noise** (ratio 0.0–0.2): Pass@5 barely moves (39.20 → 38.67), 76% of majority answers unchanged. Consistent with the high-anisotropy finding — most dimensions are inert, so noise mostly perturbs irrelevant subspaces.
2. **Non-zero accuracy at full corruption** (ratio = 1.0): Pass@5 stays at **12.59%** even when latent thoughts are *replaced entirely* with Gaussian noise. For a non-trivial fraction of problems, COCONUT can produce correct answers without using its own continuous thoughts at all.

This is closely related to [[latent-reasoning-supervision-analysis|Cui et al.]]'s shortcut analysis (which used similar noise-injection tests on Coconut/CODI/SIM-CoT/CoLaR and found 3.79% accuracy at $\sigma=100$ on GPT-2 GSM8K). Wang et al.'s 12.59% Pass@5 number is *higher* than Cui et al.'s 3.79% greedy accuracy because Pass@5 is a softer metric (it counts a problem as correct if any of 5 stochastic decodings is right). The two papers triangulate the same phenomenon from different angles.

## The Diagnosis: Missing Inductive Biases

Wang et al.'s discussion section pinpoints a single root cause: **COCONUT's training objective applies supervision only to the final text answer**, not to the latent thoughts themselves. The continuous-thought representations are therefore optimized solely for end-task accuracy, with no pressure to develop *structural* properties that would let an external verifier discriminate correct from incorrect reasoning.

Three concrete mitigations are proposed but not tested:

1. **Isotropy regularization** during training to spread latent representations across more dimensions, breaking the geometric homogeneity that prevents discrimination.
2. **Trajectory diversity objectives** that encourage geometrically varied reasoning paths for different problem types.
3. **Contrastive losses** that explicitly teach the model to produce *different* latent representations for correct versus incorrect reasoning patterns.

The general principle: **inference-time scaling cannot be retrofitted onto a representation that was never trained to support discrimination.** The solution must be in training, not decoding.

## The Pass@N / Maj@N Gap, Operationalized

This paper is the empirical mirror of [[latent-reasoning-supervision-analysis|Cui et al. (2026)]]. The two papers approach the same gap from opposite directions:

| Aspect | [[latent-reasoning-supervision-analysis\|Cui et al. (2026)]] | **Wang et al. (2025)** |
|---|---|---|
| Discovery of the gap | Identifies Pass@100 advantage and Maj@100 deficit (20+ points vs. −3 points) | Reproduces the gap independently in a Pass@N → BoN frame (Pass@32 = 44.43% vs. Best Reranker = 33.36%) |
| Diversity hypothesis | "Iterative latent reasoning exhibits implicit pruning, not BFS expansion" — distinct outcomes decrease 18.75 → 15.84 with depth | "Dropout-sampled latent trajectories produce diverse Pass@N candidates" — unique answers grow 1.00 → 3.17 with N |
| Proposed remedies | "Latent-aware reranker, learned aggregator, alternative decoding" — *suggested but not implemented* | **Implemented** (PRM hard, PRM soft, ORM, confidence, self-consistency); all fail to reach the upper bound |
| Mechanism diagnosis | Implicit pruning attributed to weak supervision and the supervision–exploration trade-off | Geometric homogeneity attributed to absence of inductive biases during training |
| Constructive output | "Improved Coconut" — a curriculum mixing fix, +7pp on GPT-2 GSM8K-Aug | None — paper is purely diagnostic |

Together, the two papers form a complete decomposition:

1. **Capacity is real** (Cui et al. Pass@100 = 70-82%; Wang et al. Pass@32 = 44.43%).
2. **Iterative dynamics prune diversity** (Cui et al.: 18.75 → 15.84 distinct outcomes with depth).
3. **The remaining diversity is geometrically structureless** (Wang et al.: IsoScore$\star \approx 0.013$, no correct/incorrect separation).
4. **Therefore reward models trained on standard recipes cannot discriminate** (Wang et al.: F1 ≈ 54%, BoN gain ≈ 19.8% of upper bound).
5. **And therefore the obvious decoding-side fix to the Pass@N gap does not work** (Wang et al.: best reranker is +2.28pp out of +13.35pp available).

The frontier-scale latent reasoning agenda that the [[frontier-research-directions|wiki has been tracking]] now has **two known blockers** at the training stage and **one known blocker** at the inference stage — and the inference-stage blocker cannot be removed without first addressing one of the training-stage ones.

## Limitations

1. **Single model, single dataset, single scale.** GPT-2 (117M) on GSM8K only. Whether the geometric homogeneity finding persists at LLaMA-1B or Qwen-7B scale is the immediate next question. [[latent-reasoning-supervision-analysis|Cui et al.]] tested at LLaMA-3.2-1B as well as GPT-2 and found the supervision–exploration trade-off in both — the geometric analysis here would need to be repeated on the larger backbone to know whether the analogous geometric finding holds.
2. **Single latent reasoning method.** Only COCONUT is tested. CODI's distillation alignment loss might already produce more discriminable representations; SIM-CoT's reconstruction loss enforces decoder-side semantic alignment, which could plausibly yield richer geometric structure. Wang et al. explicitly acknowledge this: their findings are about COCONUT specifically, though their discussion suggests the absence of latent-state supervision is a general pathology.
3. **PRM training architecture is forced.** The model-specificity of continuous thoughts means the reward model *must* use the COCONUT backbone. This limits architectural exploration — whether a custom verifier architecture (e.g. a small transformer trained only to score thoughts, or a contrastive head added during pretraining) could outperform the MLP-head approach is untested.
4. **No alternative training proposals are validated.** The paper proposes isotropy regularization, trajectory diversity objectives, and contrastive losses but tests none of them. The constructive follow-up is left entirely to future work.
5. **No comparison to alternative decoding strategies.** Tree search, beam search, or learned latent-space rerankers (rather than scalar PRM/ORM scores) could plausibly do better than scoring + selection. Wang et al. only test variants of the scoring + selection family.
6. **The 12.59% Pass@5 noise number is under-explained.** Why is COCONUT robust to *complete* latent corruption on a non-trivial fraction of GSM8K problems? Is this overlap with the easy-question subset, or does the model genuinely have a parallel "shortcut path" through the input attention? The paper raises the question but does not separate these explanations.

## Connection to Existing Wiki Pages

### Direct experimental tests

- **[[coconut-reasoning-latent-space|COCONUT (Hao et al., 2024)]]**: Wang et al. reproduce the original paper's training recipe exactly (6 epochs initial stage, 3 epochs subsequent, $c=2$, $T=3 \times c$) and report that deterministic COCONUT achieves 31.08% on GSM8K — consistent with the 34.1% in the original paper (small difference attributable to random seeds and minor reproduction details). The dropout-sampling protocol is a clean addition to COCONUT's inference-time toolkit; it should generalize to any subsequent method that uses dropout in training.
- **[[latent-reasoning-supervision-analysis|Cui et al. (2026)]]**: Direct conceptual companion. Both papers run the same model on the same dataset and converge on the same gap (large Pass@N pool, weak Maj@N concentration). Wang et al. operationalize the decoding-side question Cui et al. raise; Cui et al. operationalize the training-side question Wang et al. invoke. **Neither paper cites the other** — they are concurrent (Wang et al. October 2025, Cui et al. February 2026), so the wiki is the first place the two are explicitly synthesized.
- **[[superposition-coconut-theory|Zhu et al. (2025)]]**: Wang et al.'s geometric finding (extreme anisotropy, IsoScore$\star \approx 0.013$) is in tension with Zhu et al.'s theoretical construction, where continuous thoughts are *uniform mixtures* of reachable vertex embeddings (a maximally isotropic state in a small subspace). The discrepancy may be that (i) Zhu et al.'s construction is a theoretical optimum that gradient training does not actually find, or (ii) the IsoScore$\star$ metric measures global anisotropy across the full hidden space, while Zhu et al.'s claim is about isotropy *within the subspace of reachable vertices* — a much smaller submanifold. Either way, the gap between theoretical superposition and empirical geometric homogeneity is a target for follow-up work.

### Concept page updates

- **[[latent-space-reasoning]]**: The "Capacity vs. Use Distinction" subsection should add Wang et al. as the empirical confirmation that the gap is *not* closeable by standard reranking. The "Open Questions" section's "Closing the Pass@100 / Maj@100 gap" entry needs a status update: *partially answered — direct PRM/ORM reranking does not work; the bottleneck is geometric homogeneity, not reranker design.*
- **[[catastrophic-forgetting]]**: The "Second Barrier" section (supervision–exploration trade-off) gains a third entry: even at inference time, the absence of training-time inductive biases prevents discrimination. The trade-off bounds the design space *and* the inference-time mitigation space.
- **[[continuous-vs-discrete-representation]]**: The discrete-token bottleneck section should note that continuous representations carry *more* information but, without explicit structural constraints, may not carry information that downstream consumers can *extract*.

### Analysis page updates

- **[[contradictions]]** #9 ("BFS as faithful structured search vs. implicit pruning"): Wang et al. is a third pillar alongside Coconut/Zhu et al. and Cui et al. The "Resolution needed" section's call for a controlled comparison of best-of-N CoT, self-consistency CoT, and latent-aware best-of-N decoding is now *partially answered* — Wang et al. ran exactly this comparison on COCONUT/GSM8K and the latent-aware variants did not close the gap. Status update: *capacity confirmed (Cui, Wang); iterative dynamics prune diversity (Cui); remaining diversity lacks geometric structure for discrimination (Wang); standard reranking cannot recover the gap (Wang).*
- **[[frontier-research-directions]]** #1 (Superposition reasoning at frontier scale): Wang et al.'s geometric homogeneity finding is a third blocker on the agenda alongside Cui et al.'s implicit pruning and SoftCoT's catastrophic forgetting. Update the "Blockers" subsection.
- **[[open-questions]]**: The "Closing the Pass@100 / Maj@100 gap" entry should be updated with Wang et al.'s null result and the new question: *can training-time inductive biases (isotropy regularization, contrastive losses, trajectory-diversity objectives) restore geometric separability?*
- **[[benchmark-overlap]]**: Add Wang et al. to the GSM8K table (deterministic 31.08%, Pass@32 44.43%, Best Reranker 33.36%). Note that its scale (GPT-2) places it firmly in the "<2B latent reasoning" cluster.
- **[[paper-timeline]]**: Insert at October 2025, between [[kvcomm-kth-selective|KVComm]] (October 2025) and [[kvcomm-duke-online-reuse|KVCOMM-online]] (October 2025).
- **[[method-comparison]]**: Wang et al. is diagnostic, not a new method, but the dropout-sampling protocol could be added as an inference-time augmentation row.

### MOC updates

- **[[latent-reasoning]]**: Add as a "diagnostic / inference-time scaling" entry following Cui et al. The two papers should be read together as the empirical reckoning with COCONUT's promised capabilities.
- **[[theoretical-foundations]]**: The geometric-properties analysis (IsoScore$\star$, Hoyer sparsity, trajectory dynamics) is a methodological contribution that complements [[platonic-representation-hypothesis|Platonic Rep]] and [[linearity-relation-decoding|Hernandez et al.]] — all three measure properties of internal representations, but Wang et al. is the first to ask whether these properties carry *task-relevant* information.
- **[[safety-interpretability]]**: The geometric-homogeneity finding has direct safety implications. If correct and incorrect latent reasoning paths are indistinguishable to a verifier, then *no audit mechanism applied at the latent level can detect bad reasoning*. The shortcut behavior (12.59% Pass@5 under full noise) compounds this: COCONUT can produce correct answers without using its latent thoughts, so even the existence of well-formed latent thoughts is not evidence that they were used.

## Open Questions Raised

1. **Does geometric homogeneity persist at scale?** Cui et al. tested GPT-2 *and* LLaMA-3.2-1B and found the supervision–exploration trade-off in both. Wang et al. tested only GPT-2. Repeating the IsoScore$\star$ / trajectory-dynamics analysis on a 1B+ COCONUT variant would establish whether the finding generalizes.
2. **Do CODI / SIM-CoT / CoLaR produce more discriminable representations?** Strong-supervision methods (SIM-CoT's decoder reconstruction loss, CoLaR's token-level alignment) plausibly inject more geometric structure into the latent space. Repeating the PRM-training experiment on these methods would test whether the supervision–exploration trade-off has a corresponding geometric signature.
3. **Can isotropy regularization be added post-hoc?** Wang et al. propose IsoScore$\star$ regularization as a future training objective. A small experiment — fine-tune COCONUT briefly with an IsoScore$\star$ penalty, then re-run the PRM training — could quickly test whether this specific intervention is sufficient.
4. **Is the geometric homogeneity finding specific to dropout-based sampling?** Sampling COCONUT trajectories via *temperature-perturbed* hidden-state injection (or other diversification strategies) might produce a different representational landscape. Wang et al.'s geometric analysis is on dropout-sampled trajectories; the picture for other diversification strategies is unknown.
5. **Could a learned latent-space verifier (rather than a scalar PRM) work?** Wang et al.'s reward model emits a scalar score per step. A verifier that operates *in* the latent space — e.g., a transformer that takes the trajectory as input and outputs a corrected trajectory — bypasses the discrimination problem entirely by replacing scoring with regeneration.
6. **What is the relationship between the geometric homogeneity here and the implicit-pruning finding in Cui et al.?** If the iterative process prunes diversity (Cui), are the surviving trajectories homogenized into a single attractor (Wang)? Tracking IsoScore$\star$ across the latent prefix length should reveal whether geometric collapse follows diversity collapse step by step.
7. **Could the dropout-sampling protocol be applied to instruction-tuned methods?** [[softcot-efficient-reasoning|SoftCoT]] and [[latentmas-collaboration|LatentMAS]] do not modify the backbone, but dropout could still be enabled in the projection layer or alignment matrix. This would extend the Pass@N analysis beyond GPT-2.

## Source Materials

- [[raw/pdf/arxiv-2510.12167.pdf|PDF]] ([[raw/latex/arxiv-2510.12167.tar.gz|LaTeX source]])
