KVComm and [[kv-cache-alignment-shared-space|KV Cache Alignment]] take complementary approaches to the cross-model problem:

| Dimension | KVComm | KV Cache Alignment |
|-----------|--------|-------------------|
| Cross-architecture | No — same architecture required | Yes — via shared KV-cache space |
| Training | None — calibration only | Required — adapters trained per model |
| Layer selection | Explicit — attention + Gaussian prior | Implicit — adapters learn which layers to emphasize |
| Efficiency mechanism | Transmit fewer layers | Transmit through shared space (all layers) |
| Self-improvement | Selective sharing sometimes exceeds skyline | Cyclic translation improves perplexity |
| Scalability | $O(1)$ per model pair (reusable scores) | $O(N)$ adapters for $N$ models |

A key open question is whether KVComm's layer selection could be **applied within** the KV Cache Alignment framework — selecting which layers to translate through the shared space rather than translating all layers. This could combine KVComm's bandwidth efficiency with KV Cache Alignment's cross-architecture compatibility.

### The "Exceeds Skyline" Phenomenon

On some datasets, KVComm at 70% of layers **outperforms** the Skyline (full context concatenation with all layers). This counterintuitive result suggests that selective sharing acts as **regularization**: by filtering out uninformative or noisy layers, the receiver gets cleaner signal than it would from the full unfiltered cache. This parallels [[cache-to-cache-semantic-communication|C2C]]'s effective rank increase finding and [[kv-cache-alignment-shared-space|KV Cache Alignment]]'s self-improvement effect — all three independently discover that latent-space mediation can improve over raw information transfer.
