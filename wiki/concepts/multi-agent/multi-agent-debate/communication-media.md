The debate framework is agnostic to the communication medium. This is a crucial architectural insight — the *protocol* (initial round → debate rounds → aggregation) is separable from the *representation* used for inter-agent messages.

| Medium | Information per message | Compatibility | Interpretability | Source |
|--------|----------------------|---------------|------------------|--------|
| Natural language | Low (discrete tokens) | Universal | Full | Du et al., 2023 |
| Embedding vectors | Medium (soft tokens) | Shared tokenizer | Via NN decoding | [[cipher-multiagent-debate-embeddings|CIPHER]] |
| Disentangled thoughts | Medium-High (structured latent factors) | Trained autoencoder | Via structure + decoding | [[thought-communication-multiagent|ThoughtComm]] |
| KV-cache (same arch.) | High (layer-specific repr.) | Same model family | Low | [[kvcomm-kth-selective|KVComm]] |
| KV-cache (cross arch.) | High (projected + fused) | Learned fuser | Low | [[cache-to-cache-semantic-communication|C2C]] |
| Hidden activations | Highest | Near-identical arch. | Minimal | [[activation-communication]] |
