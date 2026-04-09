### The Enriched Entity Representation Argument

[[activation-communication-harvard|AC (Ramesh & Li, 2025)]] provides the theoretical foundation: by around the halfway point of an LLM's computation (~layer 26 of 32), the model has developed **enriched entity representations** ([[raw/pdf/arxiv-2501.14082.pdf|AC §3.2, Figure 2]]) — entities in the prompt are populated with additional facts from the model's weights. But by the final layers, these rich representations are **compressed** into next-token predictions, discarding information not needed for that narrow objective.

This creates a layer-depth hierarchy for communication value:

| Layer range | Content | Communication value |
|-------------|---------|-------------------|
| Early (1-12) | Embeddings being contextualized | Low — not yet informative |
| **Mid-late (20-26)** | **Enriched entity representations** | **Highest — broadest contextual knowledge** |
| Final (27-32) | Next-token prediction optimized | Declining — useful info discarded |

[[activation-communication-harvard|AC]] validates this empirically: $k = j = 26$ is optimal across all benchmarks (scanned via 2D contour over all $(k,j) \in \{1,\ldots,30\}^2$).

### The Depth Spectrum

![[depth-spectrum]]

Activations sit at the deep end of this spectrum: a **strict superset** of what tokens, output embeddings, or KV-cache entries transmit, carrying the full computational state — predictions, beliefs, enriched entities, and contextual knowledge — at the cost of requiring a receiver that understands the sender's internal geometry.
