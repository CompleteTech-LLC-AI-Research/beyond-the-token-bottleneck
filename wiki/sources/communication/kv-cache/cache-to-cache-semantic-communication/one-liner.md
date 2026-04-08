---
type: source-partial
parent: cache-to-cache-semantic-communication
partial: one-liner
created: "2026-04-08"
updated: "2026-04-08"
---

**Cache-to-Cache (C2C)** uses a learned neural cache fuser with per-layer gating to project the sender's KV-cache into the receiver's representation space across model families and sizes (Qwen ↔ LLaMA ↔ Gemma, 0.6B–14B). Scales $O(N^2)$ — one fuser per model pair — but bypasses the language interface entirely, so even base models that produce unusable text can serve as knowledge sources.
