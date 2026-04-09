A striking finding across multiple papers: passing KV-caches through an intermediate representation **improves** performance beyond the original model:
- [[kv-cache-alignment-shared-space|KV Cache Alignment]]: Cyclic translation (A → Ω → A) improves model A's language modeling
- [[cache-to-cache-semantic-communication|C2C]]: Fused cache has higher effective rank than either individual model's cache
- [[kvcomm-kth-selective|KVComm]]: Selective sharing sometimes exceeds the Skyline (full context concatenation)

This suggests that latent-space mediation — whether through a learned shared space, a neural fuser, or even simple layer selection — acts as a form of **beneficial regularization**, distilling the most transferable and task-relevant features while filtering noise. The parallels to how [[coconut-reasoning-latent-space|Coconut]]'s continuous thoughts learn more efficient representations than language CoT are notable.
