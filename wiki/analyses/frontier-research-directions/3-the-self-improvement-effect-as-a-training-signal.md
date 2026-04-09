**The signal**: Three independent papers find that passing representations through an intermediate space **improves** the original model:
- [[kv-cache-alignment-shared-space|KV Cache Alignment]]: Cyclic translation (A → Ω → A) improves model A's language modeling
- [[cache-to-cache-semantic-communication|C2C]]: Fused cache has higher effective rank than either individual model's cache
- [[kvcomm-kth-selective|KVComm]]: Selective sharing sometimes exceeds the Skyline (full context)

**The gap**: Nobody has explained *why* this happens or explored it as a deliberate training/inference strategy. The pattern suggests that latent-space mediation acts as a **beneficial regularizer** — distilling the most transferable features while filtering noise. But this is observed, not understood, and not exploited.

**Why this could be paradigm-shifting**: If the self-improvement effect is robust, you could build a **self-distillation loop**: model → shared space → back to model → shared space → ... Each cycle would sharpen representations. This could be a new form of inference-time compute scaling — instead of generating more tokens (CoT) or running more agents (debate), you run more cycles through the shared space. Entirely orthogonal to existing scaling approaches.

**Concrete next steps**:
- Characterize the self-improvement effect across model sizes and architectures (is it universal or specific to certain model families?)
- Measure whether iterating the cycle (A → Ω → A → Ω → A) produces monotonic improvement or saturates
- Compare the effective rank / representation quality metrics before and after each cycle
- Design a lightweight "self-distillation loop" at inference time and benchmark against CoT and self-consistency

---
