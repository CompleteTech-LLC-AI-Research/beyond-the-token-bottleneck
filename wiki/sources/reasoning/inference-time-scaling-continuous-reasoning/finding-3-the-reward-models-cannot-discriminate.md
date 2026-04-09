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
