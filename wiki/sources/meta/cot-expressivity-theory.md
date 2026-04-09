---
type: source
title: "Towards Revealing the Mystery behind Chain of Thought: A Theoretical Perspective"
source_file: "[[raw/pdf/arxiv-2305.15408.pdf]]"
latex_source: "[[raw/latex/arxiv-2305.15408/]]"
author: "Guhao Feng, Bohang Zhang, Yuntian Gu, Haotian Ye, Di He, Liwei Wang"
date_published: "2023-05-24"
date_ingested: "2026-04-06"
created: "2026-04-06"
updated: "2026-04-06"
venue: "NeurIPS 2023"
arxiv: "2305.15408"
institution: "Peking University, Pazhou Lab"
tags: [theoretical, cot-expressivity, circuit-complexity, foundational]
---

# Towards Revealing the Mystery behind Chain of Thought: A Theoretical Perspective

## One-liner

![[cot-expressivity-theory/one-liner]]

## Summary

The first rigorous theoretical explanation of **why Chain-of-Thought works** in transformers, using circuit complexity theory. Proves that bounded-depth transformers **cannot** solve basic arithmetic or linear equations without CoT (assuming $\text{TC}^0 \neq \text{NC}^1$), but **constant-size** transformers **can** solve them with CoT. The key insight: **CoT increases the effective circuit depth** by looping outputs back as inputs, breaking through the $\text{TC}^0$ barrier. This paper provides the theoretical backbone for all latent reasoning work -- any mechanism that adds effective depth (CoT tokens, pause tokens, continuous thoughts, recurrence) should yield similar expressivity gains.

## Circuit Complexity Background

The paper frames transformer expressivity through the lens of **circuit complexity classes**, which classify Boolean functions by the resources required by families of circuits:

| Complexity Class | Definition | Relevant Computation |
|-----------------|-----------|---------------------|
| **$\text{TC}^0$** | Constant-depth, polynomial-size circuits with threshold gates | What bounded-depth log-precision transformers can compute |
| **$\text{NC}^1$** | $O(\log n)$-depth, polynomial-size circuits with bounded fan-in | Arithmetic expression evaluation, linear equation solving |
| **$\text{P}$** | Polynomial-time Turing machines (equivalent to polynomial-depth circuits) | General dynamic programming, CFG membership testing |

The key separation assumption is $\text{TC}^0 \neq \text{NC}^1$, widely believed since Yao (1989). This means constant-depth threshold circuits (and hence bounded-depth transformers) cannot simulate logarithmic-depth computations. The **log-precision transformer** model used throughout the paper restricts internal neurons to $O(\log n)$ bit precision, matching practical implementations where machine precision (16 or 32 bits) is much smaller than input length.

## Core Theoretical Results

### Impossibility Without CoT (Theorems 3.1 and 3.2)

**Theorem 3.1 (Arithmetic).** Assume $\text{TC}^0 \neq \text{NC}^1$. For any prime $p$, any integer depth $L$, and any polynomial $Q$, there exists a problem size $n$ such that no log-precision autoregressive transformer with depth $L$ and hidden dimension $d \leq Q(n)$ can solve $\text{Arithmetic}(n, p)$.

**Theorem 3.2 (Equations).** Under the same assumption, for any prime $p$, depth $L$, and polynomial $Q$, there exists $m$ such that no log-precision transformer with depth $L$ and $d \leq Q(m)$ can solve $\text{Equation}(m, p)$.

**Proof strategy.** The proofs establish that both problems are $\text{NC}^1$-hard via reductions from known $\text{NC}^1$-complete problems. Merrill & Sabharwal (2023) showed that bounded-depth log-precision transformers of polynomial size can be simulated by $\text{TC}^0$ circuits. Since $\text{TC}^0 \subsetneq \text{NC}^1$ (under the assumption), the transformers provably lack the circuit depth to solve these problems. The bottleneck is fundamentally **parallel complexity** -- these tasks require $\Omega(\log n)$ sequential computational steps that cannot be parallelized into constant depth, regardless of how wide the model is.

**Problem formulations.** Both tasks operate over finite fields $\mathbb{F}_p$ (integers modulo a prime $p$), which simplifies the analysis by ensuring all numbers are tokens in a bounded dictionary. $\text{Arithmetic}(n, p)$ asks the model to evaluate arithmetic expressions (with $+, -, \times, \div$ and brackets) of input length up to $n$. $\text{Equation}(m, p)$ asks the model to solve systems of $m$ linear equations in $m$ variables.

### Sufficiency With CoT (Theorems 3.3 and 3.4)

**Theorem 3.3 (Arithmetic with CoT).** Fix any prime $p$. For any $n > 0$, there exists an autoregressive transformer with constant hidden size $d = O(\text{poly}(p))$ (independent of $n$), depth $L = 5$, and 5 heads per layer that generates the CoT solution for all inputs in $\text{Arithmetic}(n, p)$. All parameter values are bounded by $O(\text{poly}(n))$.

**Theorem 3.4 (Equations with CoT).** Fix any prime $p$. For any $m > 0$, there exists an autoregressive transformer with constant hidden size $d$ (independent of $m$), depth $L = 4$, and 5 heads per layer that generates the CoT solution for all inputs in $\text{Equation}(m, p)$.

The polynomial parameter bound ensures these constructions are implementable in log-precision without loss of accuracy.

### Construction Details for the Depth-5 Arithmetic Transformer

The constructive proof of Theorem 3.3 is the paper's most technically detailed result. It builds on a set of fundamental operations implementable by transformer components:

**Attention-level primitives:**
- **Conditional COPY** (Lemma B.1): A softmax attention head can extract the content of the unique previous position satisfying certain conditions. Achieved by constructing $Q, K, V$ matrices so that the dot-product score is zero for exactly the target position and negative elsewhere.
- **Conditional MEAN** (Lemma B.2): A softmax attention head can average values over all positions satisfying a condition -- a "scatter" operation in parallel computing.

**MLP-level primitives:**
- **Multiplication** (Lemma B.3): A 2-layer MLP with GeLU activation and hidden dimension 4 approximates scalar multiplication $f(a,b) \approx ab$ within error $\epsilon$, with weights bounded by $O(\text{poly}(M, 1/\epsilon))$. The construction uses the identity $ab = \frac{1}{4}[(a+b)^2 - (a-b)^2]$, approximated via GeLU's Taylor expansion.
- **Conditional selection** (Lemma B.4): A 2-layer MLP selects between two values based on a threshold condition.
- **Lookup table** (Lemma B.5): A 2-layer MLP with $d^k$ hidden units implements any $k$-dimensional lookup table over a discrete domain of size $d$.

**Layer-by-layer construction:**

| Layer | Purpose | Mechanism |
|-------|---------|-----------|
| **Layer 1** | Count equal signs, find position of last `=`, compute $i^2$ | MEAN head counts `=` frequency; COPY head retrieves last `=` position; MLP computes products |
| **Layer 2** | Compute distances to nearest/last `=`, count strictly-previous `=`, compute squared quantities | COPY from position $i-1$; MLP computes $(n^=)^2$, $(d^=)^2$ |
| **Layer 3** | Extract 5 context tokens from previous CoT step; determine if calculation needed | 5 parallel COPY heads with dot-product scores $-(n^= - \hat{n}^= - 1)^2 - (d^= - \hat{d}^= + t)^2$ ensuring unique retrieval; MLP implements arithmetic lookup table |
| **Layer 4-5** | Generate output: copy token, perform calculation, or emit result | Conditional selection between copy/compute modes; final lookup table for $+, -, \times, \div$ |

The key insight is that the CoT format reduces each generation step to examining a **fixed-size context window** (5 tokens from the previous derivation step), enabling a constant-size model to handle arbitrarily long expressions.

### Generalization to Dynamic Programming (Theorem 4.7)

**Theorem 4.7.** Consider any DP problem satisfying Assumptions 4.1-4.4. For any integer $n$, there exists an autoregressive transformer with constant depth $L$, hidden dimension $d$, and attention heads $H$ (all independent of $n$) that correctly generates the CoT solution for all input sequences of length up to $n$.

The DP framework is characterized by three ingredients:
- **State space** $\mathcal{I}_n \subset \mathcal{I}$: The finite set of subproblems, with a partial order (DAG) defining dependencies.
- **Transition function** $T$: $\text{dp}(i) = f(n, i, s_{g(n,i)}, \text{dp}(h(n,i)))$ -- each state depends on a constant number of input tokens ($J$) and previous states ($K$).
- **Aggregation function** $A$: Combines results, e.g., $\min$, $\max$, $\sum$ over a subset of states.

**Assumptions** (all verified for LIS, ED, and CFG problems):
1. $|\mathcal{I}_n| = O(\text{poly}(|s|))$ -- polynomial state space
2. Functions $f, g, h, u$ are approximable by constant-size GeLU MLPs with polynomial efficiency
3. The topological ordering function is similarly approximable
4. The aggregation indicator function is similarly approximable

**Impossibility complement (Theorem 4.8).** Context-Free Grammar (CFG) Membership Testing -- a $\text{P}$-complete DP problem -- cannot be solved by bounded-depth polynomial-size transformers without CoT (under $\text{TC}^0 \neq \text{NC}^1$). This establishes that CoT enables transformers to solve problems up to $\text{P}$-completeness, a dramatic jump from $\text{TC}^0$.

**DP examples analyzed:**

| Problem | State Space | Transition | Aggregation |
|---------|-------------|-----------|-------------|
| **LIS** (Longest Increasing Subsequence) | $(j, k)$ for $j \in [n], k \in \{0, \ldots, j-1\}$ | $\text{dp}(j,k) = \max(\text{dp}(j,k-1), \text{dp}(k,k-1) \cdot \mathbb{I}[s_j > s_k] + 1)$ | $\max_i \text{dp}(i, i-1)$ |
| **ED** (Edit Distance) | $(j, k) \in \{0,\ldots,n_1\} \times \{0,\ldots,n_2\}$ | $\min(\text{dp}(j,k-1)+a, \text{dp}(j-1,k)+b, \text{dp}(j-1,k-1)+c\mathbb{I}[s^{(1)}_j \neq s^{(2)}_k])$ | $\text{dp}(n_1, n_2)$ |

### RNN Impossibility

An important negative result: **constant-size RNNs cannot solve** any of these tasks with CoT, even given the same CoT format. The bottleneck is that RNNs lack attention's ability to **selectively retrieve** arbitrary previous intermediate results. The hidden state of an RNN can only carry a constant amount of information, while attention can access any position in the context. This distinction is critical for latent reasoning architectures.

## Experimental Validation

### Main Results

All experiments use standard transformers ($d = 256$, $H = 4$, various depths), trained with AdamW ($\beta_1 = 0.9$, $\beta_2 = 0.999$, lr $= 10^{-4}$, weight decay $= 0.01$), dropout 0.1, on 4 V100 GPUs for 100 epochs. Training data: 1M samples per task; test: 0.1M samples (no overlap).

| Task | Difficulty | CoT (3-layer) | Direct (3-layer) | Direct (4-layer) | Direct (5-layer) |
|------|-----------|--------------|-----------------|-----------------|-----------------|
| **Arithmetic** | 4 ops | ~100% | ~58% | ~60% | ~55% |
| **Arithmetic** | 5 ops | ~100% | ~52% | ~55% | ~50% |
| **Arithmetic** | 6 ops | ~100% | ~48% | ~50% | ~45% |
| **Equation** | 3 vars | ~100% | ~55% | ~60% | ~68% |
| **Equation** | 4 vars | ~100% | ~20% | ~30% | ~40% |
| **Equation** | 5 vars | ~100% | ~5% | ~10% | ~15% |
| **LIS** | len 50 | ~100% | ~55% | ~58% | ~60% |
| **ED** | len 12 | ~100% | ~50% | ~55% | ~58% |

3-layer transformers with CoT achieve **near-perfect accuracy** across all tasks and difficulty levels. Direct prediction consistently fails, especially as problem size grows. Notably, the 5-variable Equation task requires generating CoT sequences of ~500 tokens perfectly, yet the 3-layer model achieves this.

### Robustness to Data Quality

On the arithmetic task with 10 operators:

| Corruption Rate ($\gamma$) | 0 | 0.1 | 0.2 | 0.3 |
|----------------------------|------|------|------|------|
| **Accuracy** | 100.0% | 98.5% | 97.6% | 95.8% |

Where $\gamma = 0.1$ means 10% of intermediate steps are omitted and 10% of remaining steps have a single-token corruption. The model remains above **95% even with 30% corruption**, demonstrating remarkable robustness of CoT training to low-quality supervision.

### Length Extrapolation

A 3-layer model trained on arithmetic expressions with 1-15 operators was tested on longer expressions:

| # Operators | 15 (in-dist) | 16 | 17 | 18 |
|------------|-------------|-----|-----|-----|
| **Accuracy** | 99.9% | 97.6% | 82.4% | 45.5% |

The model generalizes well to 16 operators (2 beyond training) and degrades gracefully, suggesting it has learned algorithmic rules rather than memorizing input-output distributions.

## Why This Matters for Latent Reasoning

1. **The depth bottleneck is the core insight**: Transformers are limited by parallel depth ($\text{TC}^0$). Any mechanism that increases effective depth -- CoT tokens, [[pause-tokens|pause tokens]], [[coconut-reasoning-latent-space|Coconut]]'s continuous thoughts, [[thinking-states-latent-reasoning|Thinking States]]' chunk recurrence -- should yield similar expressivity gains.

2. **Constant-size sufficiency**: A fixed-size model can solve arbitrarily large problems via CoT. The reasoning capacity is in the *process* (generation steps), not the *model* (parameters). This motivates latent approaches that provide more "thinking steps" rather than more parameters.

3. **RNNs cannot substitute**: Constant-size RNNs fail where transformers with CoT succeed -- attention's selective retrieval of previous intermediate results is essential. Latent reasoning architectures need analogous retrieval mechanisms.

4. **The construction reveals essential components**: The proof identifies specific roles for softmax attention (conditional copy/mean), multi-head parallelism (extracting multiple context tokens simultaneously), FFNs (arithmetic lookup tables), and residual connections (maintaining information across layers). These are not interchangeable with simpler alternatives.

5. **[[superposition-coconut-theory|Superposition theory]]** extends this: Feng et al. prove CoT adds depth; Zhu et al. prove continuous CoT additionally exploits **width** (superposition). Together they explain why continuous thoughts outperform discrete CoT on planning tasks.

6. **DP generalization bridges to real tasks**: Many practical reasoning problems (planning, multi-hop QA, code execution) can be cast as DP, meaning the theoretical sufficiency result applies broadly. The $\text{P}$-completeness of CFG membership testing shows CoT-equipped transformers can, in principle, solve anything in polynomial time.

## Limitations

- **Constructive, not learned**: The proofs show existence of weight configurations, not that gradient descent finds them. The experimental results suggest learning is possible but do not prove it theoretically.
- **Finite field simplification**: Operating over $\mathbb{F}_p$ avoids floating-point precision issues present in real arithmetic.
- **Constant-size is relative**: The hidden dimension $d = O(\text{poly}(p))$ can be large for large primes, though it is independent of input length $n$.
- **CoT format dependency**: The specific CoT format (step-by-step reduction) is chosen to enable the construction; other formats might not yield the same guarantees.

## Source Materials

- [[raw/pdf/arxiv-2305.15408.pdf|PDF]] (`raw/latex/arxiv-2305.15408/`)
