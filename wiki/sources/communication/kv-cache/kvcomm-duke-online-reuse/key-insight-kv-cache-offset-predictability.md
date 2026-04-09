### Theoretical Foundation

Two propositions formalize why offset estimation works:

**Proposition 1 (KV Distance Between Tokens)**: The KV-cache distance between two different tokens at the same position under the same prefix is bounded by their embedding gap, scaled through transformer layers via Lipschitz constants. Tokens closer in embedding space have more similar KV-caches.

**Proposition 2 (Deviation Proximity Under Different Prefixes)**: The difference in KV-cache offsets (when switching from prefix A to prefix B) between two embedding-similar tokens is also bounded. This means: if you know how token X's KV-cache changes from prefix A to B, you can estimate how a similar token Y changes — **offsets are transferable between similar tokens**.

### Empirical Validation

- KV-cache proximity is **highly correlated** with token embedding distance (Spearman correlation)
- KV-cache offset proximity (under different prefixes) also correlates with embedding distance
- After RoPE positional de-rotation, Key cache offsets become much smaller and more predictable

### RoPE Positional Alignment

A critical technical detail: RoPE (Rotary Position Embedding) applies position-dependent rotations to Key vectors. When a token appears at position n in one prompt but n+δ in another, the raw Key difference is dominated by the rotational shift, which is orders of magnitude larger than the contextual offset. KVCOMM **always de-rotates Keys** before computing/applying offsets, isolating the true contextual deviation.
