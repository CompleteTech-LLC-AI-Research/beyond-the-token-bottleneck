**Claim A**: Cross-family [[activation-communication|activation communication]] works **without learned projections**. LLaMA ↔ Qwen ↔ Gemma activation transfer succeeds zero-shot.
— [[activation-communication-harvard|AC (Ramesh & Li, 2025)]]

**Claim B**: Cross-architecture [[kv-cache-communication|KV-cache communication]] requires **learned fusers** or a **shared representation space**. Direct KV transfer across architectures fails.
— [[cache-to-cache-semantic-communication|C2C]], [[kv-cache-alignment-shared-space|KV Alignment]]

**Status**: **Complementary, different representation depths**. Activations (single-layer residual stream) may converge across models per the [[platonic-representation-hypothesis|Platonic Representation Hypothesis]], but KV-caches (per-layer, per-head attention memory) have more architecture-specific structure. The contradiction highlights that **representation convergence varies by layer/component** — final-layer activations converge; attention-specific KV pairs do not.

**Resolution needed**: Systematic measurement of cross-model representation similarity at different transformer components (embeddings, layer-wise activations, KV-cache entries, attention patterns) to map where convergence holds and where it breaks.

---
