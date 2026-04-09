The paper provides the strongest theoretical argument in this collection for why [[activation-communication]] should outperform [[embedding-space-communication]] and natural language:

1. **Activations are a strict superset of next-token predictions**: Late-layer activations encode the model's next-token prediction AND its belief distribution AND its enriched entity representations AND broader contextual knowledge. Token sampling keeps only the first; CIPHER keeps the first two; AC keeps everything.

2. **Final layers discard useful information**: Probe accuracy for various input properties rises through mid-layers, peaks around layer 20-26, then **drops** in final layers. The LM head is optimized for next-token prediction, not for preserving all contextual information. AC accesses the representations before this information is discarded.

3. **One-shot sufficiency**: Because activations encode "all of A's knowledge/beliefs about the prompt," there is no need for iterative rounds (unlike debate/CIPHER). One activation graft communicates everything. This is why AC is not iterative — and why it still loses to NLD on tasks where iterative refinement (not just knowledge transfer) is the key benefit.
