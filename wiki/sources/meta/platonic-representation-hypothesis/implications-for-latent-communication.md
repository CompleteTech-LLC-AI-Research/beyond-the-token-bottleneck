1. **Simple mappings suffice**: Merullo et al. (2022) showed a **single linear projection** stitches a vision model to an LLM. LLaVA achieves SOTA with a 2-layer MLP connector. This explains why [[activation-communication-harvard|AC]]'s cross-family results work without learned projections.

2. **Scale makes it easier**: The convergence strengthens with scale. Larger models should be **more** interchangeable. Future frontier models may need even simpler alignment.

3. **The "shared reality" as universal protocol**: Two sufficiently large models independently arrive at representations related by approximately linear transforms -- the shared reality acts as the universal communication protocol.

4. **Representation-conditioning > data-conditioning**: Li et al. (2023) found conditioning on representations for generation is easier than conditioning on raw data -- directly supporting activation/KV-cache communication over natural language.

5. **Cross-modal data sharing improves everything**: Training on images improves language and vice versa, because all modalities signal about the same $P(Z)$.
