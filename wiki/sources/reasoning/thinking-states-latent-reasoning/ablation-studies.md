### Deep-to-Shallow Recurrence Depth

Varying the extraction layer for the Thinking Block while keeping injection fixed at layer 1 (Qwen2.5-1.5B, 28 hidden layers, GSM8K):

| Extraction Layer | # Layers in Loop | Approximate Accuracy | Speedup |
|-----------------|-----------------|---------------------|---------|
| Layer 4 | 4 | ~24% | ~4.5x |
| Layer 8 | 8 | ~28% | ~3.8x |
| Layer 12 | 12 | ~31% | ~3.3x |
| Layer 16 | 16 | ~34% | ~2.9x |
| Layer 20 | 20 | ~37% | ~2.8x |
| Layer 24 | 24 | ~39% | ~2.7x |
| Layer 26 | 26 | ~42% | ~2.66x |

Performance increases **monotonically** with the number of layers in the recurrent loop, with a ~20% absolute gap between shallowest and deepest configurations. This confirms that maximizing computational capacity for processing thinking states is critical. There is also an inherent accuracy-latency tradeoff: fewer layers in the loop means more layers run only during prefill, yielding higher speedups.

### Chunk Size

Peak performance at $c = 8$ tokens (GSM8K):

| Chunk Size | Approximate Accuracy | Approximate Speedup |
|-----------|---------------------|---------------------|
| $c = 2$ | ~34% | ~1.8x |
| $c = 4$ | ~38% | ~2.2x |
| **$c = 8$** | **~42%** | **~2.66x** |
| $c = 16$ | ~40% | ~3.2x |
| $c = 32$ | ~38% | ~4.0x |
| $c = 48$ | ~36% | ~4.5x |

The tradeoff: too small ($c = 2$) -- insufficient computational capacity per state, too many iterations. Too large ($c = 48$) -- must compress too many reasoning steps into one state update, undermining the deep-to-shallow recurrence since consecutive steps within the same chunk cannot access the full recurrent loop.

### Coconut Scaling

Increasing Coconut's latent tokens from 6 to 21 does **not** improve accuracy (stays ~32-33% on GSM8K) while reducing speedup from ~3.14x to ~1.5x. This demonstrates that Coconut's bottleneck is **optimization difficulty** (BPTT training instability), not insufficient compute -- confirming the advantage of supervised thoughts.
