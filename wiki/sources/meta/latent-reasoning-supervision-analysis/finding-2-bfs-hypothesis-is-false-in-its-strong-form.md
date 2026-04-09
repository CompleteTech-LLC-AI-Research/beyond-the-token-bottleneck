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
