![[superposition]]

In the latent-reasoning setting specifically, [[superposition-coconut-theory|Zhu et al. (2025)]] gave this capacity a sharp formal expression: for directed graph reachability, the $c$-th continuous thought in a 2-layer transformer is provably the normalized uniform mixture of all vertex embeddings reachable within $c$ steps, $[t_c] = \frac{1}{|V_c|} \sum_{v \in V_c} u_v$. The quantum-mechanics analogy is thus exact — continuous thoughts are superposition states, token sampling is measurement/collapse, and the final answer token projects the superposition onto a single candidate. This is also directly analogous to how [[embedding-space-communication]] improves over discrete tokens: the weighted average embedding in [[cipher-multiagent-debate-embeddings|CIPHER]] encodes uncertainty across multiple tokens, and Coconut extends the same principle from communication to reasoning.

### Emergent BFS — and Why It Doesn't Quite Work

On the strength of Zhu et al.'s theorem, the superposition property was initially read as giving rise to what Coconut described as **emergent breadth-first search** (BFS):

1. **Step 1**: The continuous thought maintains probability mass on all immediate next steps (broad exploration).
2. **Step 2**: Paths are evaluated and weaker candidates are pruned (narrowing).
3. **Steps 3+**: Continued evaluation until a single path dominates (commitment).

This contrasts with CoT's inherent **depth-first / greedy** strategy — commit to one path immediately, follow it to the end, hope it's right.

The BFS behavior is **not explicitly trained** ([[raw/pdf/arxiv-2412.06769.pdf|Coconut §4.2, Figure 3]]). It emerges naturally from the interaction between:
- The continuous representation's ability to encode superpositions
- The training objective's pressure to predict the correct final answer
- The gradient-based optimization finding that maintaining multiple paths improves expected accuracy

#### The Capacity vs. Use Distinction (Cui et al., 2026)

[[latent-reasoning-supervision-analysis|Cui et al. (2026)]] conducted the first systematic empirical test of whether the iterative latent process actually performs BFS. Their hybrid latent–text rollout protocol (run $n$ latent prefix steps, then sample 100 stochastic text continuations at $T = 1$) **partially confirms and partially falsifies** the claim:

- **Capacity is real**: Latent reasoning's Pass@100 (~70-82%) consistently exceeds explicit reasoning's (~44-62%) by 20+ points across all prefix lengths. A single latent vector *does* encode multiple correct candidates, exactly as [[superposition-coconut-theory|Zhu et al.]] proved theoretically.
- **Iterative BFS is false**: Increasing latent prefix length **decreases** the diversity of next-step distributions (avg. 18.75 → 15.84 distinct outcomes from 1 to 5 latent steps). True BFS would *expand* the frontier, not contract it. The latent process exhibits **implicit pruning**, not breadth-first exploration.
- **Amplification fails**: Latent reasoning's majority-vote accuracy is **3-4 points lower** than explicit reasoning's, despite the larger correct-candidate pool. The reasoning loop preserves diversity but fails to concentrate probability mass on the correct candidate.

This is the cleanest experimental separation to date of three distinct claims:

| Claim | Status | Evidence |
|---|---|---|
| Latent vectors *can* encode multiple candidates | Confirmed | Zhu et al. theory; Cui et al. Pass@100 advantage; Wang et al. Pass@32 = 44.43% |
| The iterative process *does* expand the frontier | **Falsified** | Cui et al. distinct-outcome counts decrease with depth |
| The process *amplifies* the correct candidate | **Falsified** | Cui et al. majority-vote accuracy below explicit reasoning |
| Standard reranking (PRM/ORM/self-consistency) closes the gap | **Falsified** | [[inference-time-scaling-continuous-reasoning\|Wang et al.]] PRM-HE recovers only 19.8% of Pass@N headroom |
| The remaining diversity has discriminable geometric structure | **Falsified** | Wang et al. IsoScore$\star \approx 0.013$; correct/incorrect thoughts intermixed in t-SNE |

The implication: **the latent reasoning loop is not failing for lack of representational capacity — it is failing because the optimization process prunes its own diversity, and the surviving diversity is geometrically structureless**. This redirects the [[frontier-research-directions|frontier-scale superposition reasoning agenda]] from "scale up Coconut" to "build training-time inductive biases that produce geometrically separable continuous thoughts." [[inference-time-scaling-continuous-reasoning|Wang et al. (2025)]] is the empirical companion to Cui et al.: where Cui et al. *suggest* a latent-aware reranker as the missing decoding-side fix, Wang et al. *implement* it (PRM hard, PRM soft, ORM, MATH-Shepherd MC annotation) and show that the obvious approach yields only +2.28pp out of +13.35pp of available headroom because COCONUT's continuous-thought representations lack any discriminative signal — correct and incorrect thoughts produce statistically identical IsoScore$\star$, Hoyer sparsity, compactness, curvature, local smoothness, and straightness measurements.

### The Height–Confidence Principle

Coconut's analysis reveals a fundamental principle about reasoning under uncertainty: **nodes closer to the goal are easier to evaluate accurately**. The model's value estimates improve as paths approach terminal states. Therefore, the optimal strategy is:

- **Early in reasoning**: Maintain many candidate paths (high uncertainty, evaluation is unreliable).
- **Later in reasoning**: Narrow to the best path (low uncertainty, evaluation is reliable).

This is why BFS outperforms DFS/greedy for planning tasks — it delays commitment to when the model can make reliable decisions. CoT is forced to commit early, when evaluation is least reliable.
