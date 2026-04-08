---
type: source-partial
parent: superposition-coconut-theory
partial: one-liner
created: "2026-04-08"
updated: "2026-04-08"
---

**Zhu et al.** prove that continuous CoT implements **parallel BFS via superposition** — each latent vector encodes a normalized uniform mixture of all graph vertices reachable within $c$ steps. A 2-layer transformer with continuous CoT solves directed graph reachability in **$D$ steps** (graph diameter) vs. **$O(n^2)$** for discrete CoT. The theoretical backbone for why Coconut outperforms discrete reasoning on planning tasks.
