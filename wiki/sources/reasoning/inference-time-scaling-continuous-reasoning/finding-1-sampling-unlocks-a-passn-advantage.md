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
