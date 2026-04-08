---
type: concept-partial
partial: depth-spectrum
created: "2026-04-08"
updated: "2026-04-08"
---

Latent communication methods form a **spectrum of depth**: a continuum over *where in the transformer stack* information is tapped from the sender and injected into the receiver. Shallower taps are closer to the discrete token interface; deeper taps are closer to raw weights. The stages, ordered from shallowest to deepest:

1. **Natural-language tokens** — discrete samples from the output distribution. ~15 bits per position, universally compatible, but collapses the sender's full belief state at every step.
2. **Output embeddings** — weighted averages over the vocabulary embedding table (e.g. [[cipher-multiagent-debate-embeddings|CIPHER]]). Stays in the convex hull of real token embeddings, so any receiver sharing the tokenizer can process them unchanged.
3. **KV-cache entries** — per-layer key/value pairs injected through the receiver's attention mechanism (see [[kv-cache-communication]]). Non-destructive: the receiver *attends to* the sender's context rather than overwriting its own state.
4. **Hidden-state activations** — intermediate residual-stream vectors from within the transformer stack (see [[activation-communication]]). A strict superset of what shallower methods transmit, including enriched entity representations that later layers compress away.
5. **Weights** — the theoretical deepest point: sharing the model itself. Almost never used for communication (it's fine-tuning or merging), but it anchors the axis.

As you move deeper along this axis, **bandwidth rises**, **information density rises**, **decoder requirements tighten** (the receiver must understand the sender's internal geometry), **cross-architecture compatibility falls**, and **human interpretability falls**. This is the core depth–compatibility trade-off.

This framing matters across multiple communication concepts because individual methods only make sense relative to their neighbours on the axis: [[cipher-multiagent-debate-embeddings|CIPHER]] sits one step deeper than tokens, KV-cache methods sit one step deeper than that, and activation-sharing sits one step deeper still. Orthogonal axes — cross-model compatibility, structure vs. raw transfer, and same-model vs. cross-family alignment — are layered on top of this depth spine in each consuming concept.

## Used by

- [[activation-communication]]
- [[embedding-space-communication]]
- [[kv-cache-communication]]
