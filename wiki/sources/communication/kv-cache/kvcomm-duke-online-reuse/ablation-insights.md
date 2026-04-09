### Anchor Pool Size

The anchor pool capacity $V$ governs the trade-off between approximation quality and GPU memory consumption. With a small pool, matched anchors may be distant in embedding space from the current input, producing larger offset estimation errors. As the pool grows, the likelihood of finding a close embedding-space neighbor increases, tightening the approximation bound from Proposition 2. The reuse rate (>70% across workloads) indicates that the pool reaches sufficient coverage quickly — most real-world queries fall within embedding neighborhoods of previously seen inputs. The LFU (least-frequently-used) pruning strategy ensures the pool adapts to the actual input distribution, retaining anchors that cover high-traffic regions of the embedding space while discarding rare outliers. A pool that is too large wastes GPU memory storing anchors that are rarely matched; a pool that is too small forces frequent fallback to dense recomputation, reducing the effective speedup.

### Offset Estimation Variants

The offset estimation relies on three key design choices, each of which affects quality:

1. **RoPE de-rotation**: Without removing the position-dependent rotational component from Key vectors, the raw KV-cache difference is dominated by positional shift artifacts that are orders of magnitude larger than the true contextual offset. De-rotation isolates the semantic deviation, making offsets small and predictable. This step is critical — without it, the interpolation-based approximation would fail because the positional component varies non-smoothly with position differences.

2. **Embedding-weighted interpolation**: Offsets from matched anchors are combined via softmax weights derived from embedding distances. This prioritizes anchors that are semantically closest to the current input, consistent with the theoretical bound that offset transferability scales inversely with embedding distance. Alternative schemes (uniform averaging, nearest-single-anchor) would lose the smooth interpolation property that makes the approximation robust when no single anchor is a close match.

3. **Separate Key/Value handling**: Keys require de-rotation before offset application and re-rotation after, while Values are offset-corrected directly (no positional encoding). This asymmetry reflects the architectural difference: RoPE is applied only to Keys in standard transformer implementations. Treating Keys and Values identically would introduce spurious rotational artifacts in the Value cache.
