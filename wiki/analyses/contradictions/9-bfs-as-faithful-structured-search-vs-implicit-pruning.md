**Claim A**: Coconut's continuous thoughts implement **emergent breadth-first search** — each latent step expands a frontier of candidate reasoning paths, with weaker candidates pruned only as the model approaches a confident answer. Theoretically formalized by Zhu et al. (2025), who prove that a 2-layer transformer can encode the full reachable-vertex set as a normalized superposition.
— [[coconut-reasoning-latent-space|Coconut (Hao et al., 2024)]], [[superposition-coconut-theory|Zhu et al. (2025)]]

**Claim B**: Latent reasoning *can* encode multiple candidates (Pass@100 over 100 stochastic rollouts is 20+ points higher than explicit reasoning), but the *iterative* process exhibits **implicit pruning**, not BFS expansion. Distinct outcomes *decrease* monotonically with latent depth (avg. 18.75 → 15.84 from 1 to 5 latent steps), the opposite of true BFS. Majority-vote accuracy is *lower* than explicit reasoning by 3-4 points, meaning the larger candidate pool is not being concentrated on the correct answer.
— [[latent-reasoning-supervision-analysis|Cui et al. (2026)]]

**Claim C**: Even when the diverse candidates are externally available (dropout-sampled COCONUT trajectories yield Pass@32 = 44.43% on GPT-2 GSM8K, exceeding both deterministic COCONUT and text CoT), no standard reranker can recover the headroom. PRM (hard + soft, MATH-Shepherd-style) and ORM achieve only +2.28pp out of +13.35pp available, with PRM/ORM classification F1 hovering near chance (54%/52%). The diagnosis is geometric: continuous-thought representations exhibit IsoScore$\star \approx 0.013$ and produce statistically indistinguishable values across compactness, curvature, local smoothness, and straightness metrics for correct vs. incorrect thoughts.
— [[inference-time-scaling-continuous-reasoning|Wang et al. (2025)]]

**Status**: **Substantially resolved by Cui et al. + Wang et al. — capacity confirmed, dynamics falsified, naive reranking falsified, geometric structure absent**. The cleanest decomposition to date of five claims that the literature conflated:

| Sub-claim | Status | Evidence |
|---|---|---|
| Latent vectors can encode multiple candidates | Confirmed | Zhu et al. theoretical construction; Cui et al. Pass@100 advantage; Wang et al. Pass@32 = 44.43% |
| The iterative process expands the frontier | **Falsified** | Cui et al. distinct-outcome counts decrease with depth |
| The process amplifies the correct candidate | **Falsified** | Cui et al. majority-vote below explicit reasoning |
| Standard reranking (PRM/ORM/self-consistency) closes the gap | **Falsified** | [[inference-time-scaling-continuous-reasoning\|Wang et al.]] PRM-HE recovers only 19.8% of Pass@N headroom |
| The remaining diversity has discriminable geometric structure | **Falsified** | Wang et al. IsoScore$\star \approx 0.013$; correct/incorrect thoughts intermixed in t-SNE; F1 ≈ 54%/52% |

**Implication for the field**: Zhu et al.'s theoretical bound is achievable in *capacity* but not in *dynamics*, and the residual capacity is *geometrically structureless* — there is no signal a verifier can extract. Practical methods (Coconut, CODI, SIM-CoT, CoLaR) prune their own diversity during the latent loop, and the surviving thoughts produce statistically indistinguishable IsoScore$\star$, Hoyer sparsity, compactness, curvature, local smoothness, and straightness measurements regardless of correctness. The [[frontier-research-directions|frontier-scale superposition reasoning agenda]] must redirect from "scale up Coconut" or "build a better reranker" to **"build training-time inductive biases (isotropy regularization, contrastive losses, trajectory-diversity objectives) that produce continuous thoughts which are *structurally* discriminable from incorrect ones."** Wang et al. propose this trio of mitigations but test none of them; both the training-time and the inference-time gaps remain open.

**Resolution status**: The controlled comparison of best-of-N CoT, self-consistency CoT, and latent-aware best-of-N decoding is now done at GPT-2 scale ([[inference-time-scaling-continuous-reasoning|Wang et al.]]) and the latent-aware variants do *not* close the gap. The BFS hypothesis is therefore rescued in only its *weakest* form: capacity is real, but exploitation requires not just external machinery but also training-time intervention to make the latent state discriminable. Whether the geometric homogeneity finding persists at LLaMA-1B / Qwen-7B scale, and whether stronger-supervision methods (CODI, SIM-CoT, CoLaR) produce more discriminable representations, are the next two open questions.

---
