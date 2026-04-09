### Architecture

The system maintains an **anchor pool** — a collection of previously seen KV-cache samples along with their measured offsets under various prefix contexts.

**Workflow per agent per request:**

1. **Prefix precomputation**: Before any requests, agents precompute KV-caches for their fixed prompt template prefixes
2. **Shareability check**: When a request arrives, check if each placeholder's base KV-cache exists and whether anchors cover the current context
3. **If shareable**: Fetch matched anchors, estimate offsets via embedding-weighted interpolation, update KV-caches in parallel
4. **If not shareable**: Fall back to standard dense prefilling; store the new KV-caches as anchor entries for future reuse
5. **Decode**: Concatenate updated KV-caches, proceed with normal autoregressive decoding

### Anchor Pool Design

Each anchor stores:
- **Base KV-cache**: The KV-cache computed independently (without external context)
- **Placeholder offsets**: The difference between base and actual KV-cache within each agent's context
- **Prefix offsets**: Offsets of neighboring prefix segments (important due to position-dependent shifts)

### Anchor Matching

Matching uses two criteria:
- **Embedding proximity**: New samples must be close to existing anchors in embedding space (validated by Proposition 2)
- **Length compatibility**: Sequence lengths must be compatible for correct positional alignment

### Offset Approximation

For matched anchors, the KV-cache for a new prefix context is estimated as:

> **Key update**: De-rotate stored Key to correct position, add interpolated offset, re-rotate
> **Value update**: Add interpolated offset directly (no positional information in Values)

Offsets are interpolated from matched anchors weighted by embedding-distance-based softmax weights.

### Online Adaptation

The anchor pool is maintained and updated dynamically:
- New unmatched samples become new anchors
- Least-frequently-accessed anchors are pruned when pool exceeds capacity V
- The pool adapts to the input distribution over time
