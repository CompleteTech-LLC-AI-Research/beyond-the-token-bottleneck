Three foundational papers establish **why** latent reasoning works, forming a theoretical stack:

### 1. CoT Increases Effective Depth (Feng et al., NeurIPS 2023)

[[cot-expressivity-theory|Feng et al.]] prove via circuit complexity theory that bounded-depth transformers are limited to $\text{TC}^0$ — they **cannot** solve basic arithmetic or linear equations ($\text{NC}^1$ problems) without CoT. With CoT, constant-size transformers solve all these problems because autoregressive generation increases effective depth proportionally to generation length. This establishes the **depth bottleneck** as the core constraint that any latent reasoning method must address.

**Implication**: Any mechanism that adds effective depth — CoT tokens, pause tokens, continuous thoughts, chunk recurrence — should yield expressivity gains. The key question becomes: which mechanism adds depth most efficiently?

### 2. Continuous CoT Adds Superposition (Zhu et al., NeurIPS 2025)

[[superposition-coconut-theory|Zhu et al.]] extend Feng et al.'s framework to prove that continuous CoT is **provably more efficient** than discrete CoT. A 2-layer transformer with $D$ continuous thought steps solves directed graph reachability ($D$ = diameter), vs. $O(n^2)$ for the best known discrete CoT result ([[raw/pdf/arxiv-2505.12514.pdf|Zhu et al. Theorem 1]]). The mechanism: each continuous thought is a **superposition state** encoding the complete BFS frontier.

### 3. Enriched Entity Representations Peak at Mid-Layers (Hernandez et al., ICLR 2024)

[[linearity-relation-decoding|Hernandez et al.]] show that transformers encode relational knowledge as linear embeddings at intermediate layers (~layer 20-26 of 32), then **compress** this information for next-token prediction in later layers. This explains why Coconut's hidden-state feedback (which captures mid-computation representations) is richer than discrete tokens (which only capture the output-layer prediction).

### The Unified Picture

> [!diagram|left]
> ```mermaid
> graph TD
>     A["Feng et al.: CoT works because<br>it adds effective depth"] --> B["Zhu et al.: Continuous CoT is better<br>because it adds superposition"]
>     B --> C["Hernandez et al.: Mid-layer representations<br>are richer than output representations"]
>     C --> D["Combined: Latent reasoning = more depth<br>+ superposition + richer representations"]
> ```

> [!notation|right]
> | Claim | Notation |
> |---|---|
> | Depth gain | TC0 → NC1 |
> | Superposition gain | $D$ steps vs $O(n^2)$ |
