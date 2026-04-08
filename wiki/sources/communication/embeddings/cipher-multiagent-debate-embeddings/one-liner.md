---
type: source-partial
parent: cipher-multiagent-debate-embeddings
partial: one-liner
created: "2026-04-08"
updated: "2026-04-08"
---

**CIPHER** replaces sampled tokens with the softmax-weighted average of vocabulary embeddings — a "soft token" that preserves the full distributional belief. Stays inside the vocabulary's convex hull so no architecture changes are needed; requires a shared tokenizer.
