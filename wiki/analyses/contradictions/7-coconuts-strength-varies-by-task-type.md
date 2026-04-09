**Claim A**: Coconut achieves 97.0% on ProsQA (planning/search) — dramatically outperforming CoT's 77.5%.
— [[coconut-reasoning-latent-space|Coconut]]

**Claim B**: Coconut achieves only 34.1% on GSM8K (math) — **underperforming** CoT's 42.9%.
— [[coconut-reasoning-latent-space|Coconut]] (same paper)

**Status**: **Internally consistent, task-dependent**. Superposition-based BFS excels at search/planning (where exploring multiple paths matters) but struggles with linear sequential math (where commitment to one calculation path is fine). The contradiction is within a single paper and is acknowledged.

**Implication**: Latent reasoning is not a universal improvement. It's specifically powerful for tasks requiring **search** or **parallel hypothesis evaluation**. For sequential computation, CoT may remain superior. This has implications for which tasks to target in future latent reasoning research.

---
