---
type: source-partial
parent: kv-cache-alignment-shared-space
partial: one-liner
created: "2026-04-08"
updated: "2026-04-08"
---

**KV Cache Alignment** establishes a global shared KV-cache *interlingua* with two adapters per model (in/out), scaling **O(N)** with pool size. New models join by training two adapters; untrained paths work zero-shot. Exhibits a self-improvement effect where cyclic translation (A → shared → A) improves A's own performance, suggesting the shared space acts as a regularizer.
