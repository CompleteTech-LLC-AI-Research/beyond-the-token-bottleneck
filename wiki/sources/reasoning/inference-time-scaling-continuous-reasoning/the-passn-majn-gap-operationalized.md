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
