| Property | [[kvcomm-kth-selective\|KVComm]] | [[cache-to-cache-semantic-communication\|C2C]] | **This paper** |
|----------|---------|-----|------------|
| Training required | No | Per-pair fuser | Per-model adapters |
| Cross-architecture | No (same family only) | Yes (learned fuser) | Yes (shared space) |
| Scaling with N models | N/A | O(N²) fusers | **O(N) adapters** |
| Extensibility | N/A | Train new fuser per pair | Add 2 adapters, existing frozen |
| Module portability | No | No | **Yes (soft prompts transfer)** |
| Self-improvement | Via regularization effect | Via semantic enrichment | **Via shared space sharpening** |
| Experiment scale | 3B-8B models | 0.6B-14B models | 100M-400M models (smaller scale) |

### Comparison with KVComm's Selective Approach

[[kvcomm-kth-selective|KVComm]] and this paper represent fundamentally different philosophies for KV-cache communication. KVComm asks "**which** layers to share?" and uses a Gaussian-prior selection score to identify the most informative KV subset from a sender. This paper asks "**how** to translate?" and learns a universal representation that any model can read/write. The approaches are potentially complementary: one could apply KVComm's layer selection *before* translating into the shared space, transmitting only the most informative layers and reducing adapter input dimensionality.

A key architectural difference: KVComm operates **training-free** within the same model family (same architecture, same vocabulary), while this paper requires per-model adapter training but works **cross-architecture**. KVComm's layer selection assumes sender and receiver share the same layer semantics — layer 15 of Model A means roughly the same thing as layer 15 of Model B. The shared space approach makes no such assumption, which is why it handles the 4-layer ↔ 16-layer setting that KVComm cannot address.

### Cross-Architecture Implications

The successful 100M ↔ 400M communication (4 vs. 16 layers) is a proof of concept for cross-architecture KV-cache sharing, but it also reveals the challenges. The shared space must learn to abstract away not just different hidden dimensions but fundamentally different processing depths. The 4-layer model compresses all its computation into a shallow stack; the 16-layer model distributes processing across a deep hierarchy. The adapters must learn to "decompress" shallow representations into deep-format KV-caches and vice versa.

This connects to [[relative-representations-zero-shot|Moschella et al. (2022)]]'s finding that cross-architecture stitching degrades with architectural distance. The shared space approach handles this better than zero-shot stitching because the adapters are trained, but the training cost scales with architectural diversity in the pool. A pool containing only LLaMA variants would need simpler adapters than one spanning LLaMA, Gemma, and Qwen families.
