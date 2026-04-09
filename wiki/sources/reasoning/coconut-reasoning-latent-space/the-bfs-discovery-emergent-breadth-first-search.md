The paper's most striking finding: continuous thoughts can **encode multiple alternative reasoning paths simultaneously**, enabling emergent breadth-first search (BFS).

### How It Works

In a [[latent-space-reasoning|latent reasoning]] step, the continuous thought is not committed to a single next token — it's a dense vector that can represent a **superposition** of possible continuations. When probed (by forcing the model to decode to language after intermediate latent thoughts), the model reveals:

1. **First continuous thought**: Probability mass is spread across multiple candidate next steps (e.g., 4 possible paths with probabilities 0.33, 0.28, 0.22, 0.17). The model is exploring broadly.
2. **Second continuous thought**: Probability mass concentrates — the model narrows to 1-2 strong candidates (e.g., one path at 0.87). The model has evaluated and pruned.
3. **Subsequent thoughts**: Further narrowing until a single path is selected.

This is in sharp contrast to CoT, which commits to one path at the first token and **cannot backtrack**. If CoT makes a wrong turn (e.g., follows a dead-end edge in a graph), it either hallucinates non-existent connections or reaches an irrelevant conclusion.

### The Height–Confidence Relationship

The paper provides a theoretical explanation for why BFS emerges: nodes **closer to the goal** (lower "height" in the reasoning graph) are inherently easier to evaluate. The model's value estimates are more accurate for near-terminal nodes than for early-stage nodes. Therefore, it's advantageous to **delay commitment** — keep multiple paths alive until they're close enough to the goal that the model can confidently distinguish correct from incorrect.

This is formalized by measuring the correlation between a node's height (shortest distance to any leaf) and the accuracy of the model's probability estimates. Nodes with lower height receive more accurate and decisive evaluations. Nodes with greater height show ambiguous probability distributions — exactly the positions where premature commitment (as in CoT) causes errors.

### Connection to Search Algorithms

| Property | CoT | Coconut |
|----------|-----|---------|
| Search strategy | Greedy / DFS (one path, no backtracking) | Emergent BFS (multiple paths, progressive narrowing) |
| Commitment | Immediate (first token locks in direction) | Deferred (continuous thoughts maintain options) |
| Error recovery | Cannot backtrack; hallucinates or fails | Prunes incorrect paths through evaluation |
| Representation | Discrete tokens (one choice per step) | Continuous vectors (superposition of choices) |

The paper notes that this BFS behavior is **not explicitly trained** — it emerges from the latent space's ability to represent superpositions. Prior work (Tree of Thoughts, etc.) required explicit search algorithms bolted on; Coconut achieves similar behavior implicitly.

### Empirical Critique by Cui et al. (2026)

[[latent-reasoning-supervision-analysis|Cui et al. (2026)]] subjected Coconut's BFS claim to the first systematic empirical test and **partially falsified it**. Their findings:

1. **Capacity confirmed**: Coconut's latent vectors do encode multiple candidate trajectories. Pass@100 over 100 stochastic latent–text rollouts is 69-82% on GPT-2, vs. 44-62% for explicit reasoning at the same prefix lengths — a 20+ point latent advantage.
2. **BFS expansion falsified**: When the number of latent prefix steps increases from 1 to 5, the average number of distinct next-step predictions **decreases** from 18.75 to 15.84. True BFS would *expand* the frontier; Coconut's process **prunes** it. The latent reasoning loop exhibits implicit pruning, not breadth-first exploration.
3. **Amplification fails**: Coconut's majority-vote accuracy (39-44%) is **3-4 points lower** than explicit reasoning's. The larger candidate pool is not being concentrated on the correct answer.
4. **Inference collapse**: Coconut's stage-wise curriculum produces a degenerate inference mode where reducing latent steps below the final-stage maximum causes the model to skip remaining textual reasoning entirely. This breaks any clean ablation of "use $k$ latent steps at inference."
5. **Improved Coconut**: Cui et al. propose a data-mixing fix to the stage-wise curriculum — at training stage $k$, sample from earlier stage $i$ ($i \leq k$) with proportion $(i+1)$. This restores stable behavior under varied inference latent lengths and improves GPT-2 GSM8K-Aug accuracy from **34.09% → 41.06%** (and GSM8K-Aug-NL from 24.90% → 33.48%) — the first published improvement to Coconut's training scheme.

The implication is significant: Coconut's most celebrated finding (emergent BFS) is **partially true and partially overstated**. The latent state has the *capacity* for multi-path exploration, but the iterative training dynamics produce *pruning*, not expansion. The [[frontier-research-directions|frontier-scale superposition reasoning agenda]] needs to factor this in: scaling Coconut alone will not produce BFS at frontier scale; the optimization process also has to be redesigned.
