The paper provides the conceptual framework (informal, not a formal theorem) that positions pause tokens relative to CoT and latent reasoning:

| Method | Computational expansion | Extra operations |
|--------|------------------------|-----------------|
| **Pause tokens** | **Width only**: $K+M$ vectors per layer | $M \times L$ additive (parallel per layer) |
| Chain-of-thought | **Width + depth**: $M$ tokens $\times$ $L$ layers | $M \times L$ multiplicative (sequential) |
| [[coconut-reasoning-latent-space\|Coconut]] | **Width + depth + continuous**: $K$ latent steps $\times$ $L$ layers | $K \times L$ multiplicative + superposition |

CoT's computational depth is larger by a **multiplicative factor $M$** vs pause tokens' **additive width gain**. This is why CoT produces much larger reasoning improvements — it adds effective depth ([[cot-expressivity-theory|Feng et al. prove this is the key bottleneck]]). Pause tokens add only width, which provides extra computation per layer but cannot break the $\text{TC}^0$ expressivity barrier.
