In a multi-agent system modeled as a directed graph, agents exchange messages. When Agent 2 receives a message from Agent 1, it must prefill its entire prompt — including Agent 1's message, which Agent 1 already computed KV-caches for. But Agent 2 has a different system prompt (prefix), so Agent 1's cached KVs cannot be directly reused: the same text produces different KV representations under different prefix contexts due to attention's context-dependence.

### Scaling Problem

If each of M agents receives messages from all peers, total prefilling complexity scales as **O(M²)** — each agent recomputes KV-caches for every peer's shared context. For a 5-agent system with 3K-token prompts on Llama-3.1-8B: 430ms × 25 = 10.75 seconds of redundant prefilling.

### The Offset-Variance Problem

The same shared text produces different KV-caches depending on what prefix precedes it. The key insight: this difference is a **context-dependent offset** — a relatively structured deviation that can be estimated from similar prior examples rather than recomputed from scratch.
