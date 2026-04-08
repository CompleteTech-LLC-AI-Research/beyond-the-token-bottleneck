---
type: source-partial
parent: coconut-reasoning-latent-space
partial: one-liner
created: "2026-04-08"
updated: "2026-04-08"
---

**Coconut** (Chain of Continuous Thought) feeds the model's last hidden state directly back as the next "input embedding" instead of sampling a token, letting the model reason in continuous space. Achieves 97% on ProsQA via emergent BFS-via-superposition — capabilities discrete CoT cannot replicate at the same model depth — but its curriculum training causes catastrophic forgetting on instruction-tuned models.
