C2C and [[kv-cache-alignment-shared-space|KV Cache Alignment]] address the same problem — cross-architecture KV-cache transfer — with fundamentally different strategies:

| Dimension | C2C (Pairwise Fuser) | KV Cache Alignment (Shared Space) |
|-----------|---------------------|-----------------------------------|
| Adapter count | $O(N^2)$ — one fuser per model pair | $O(N)$ — two adapters per model |
| Per-pair quality | Higher — fuser is specialized | Lower — shared space optimizes universality |
| Zero-shot extensibility | None — new pairs need training | Yes — untrained paths work via shared space |
| Self-improvement effect | Effective rank increase observed | Cyclic translation improves perplexity |
| Scale tested | 0.6B-14B, Qwen/LLaMA/Gemma | 100M-400M (smaller scale) |
| Module portability | No — fuser is pair-specific | Yes — soft prompts transfer across models |

The two approaches are potentially complementary: KV Cache Alignment's shared space could serve as an initialization for C2C's per-pair fusers, combining the scalability of the shared space with the per-pair specialization of learned fusers.
