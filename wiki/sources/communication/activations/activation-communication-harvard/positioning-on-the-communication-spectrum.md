AC introduces a critical distinction: **what matters is not just the depth of representation but the layer at which you extract it**. The [[embedding-space-communication]] spectrum should be understood not as "deeper = better" but as a two-dimensional space:

| Method | Representation depth | Extraction point | Information content |
|--------|---------------------|-----------------|-------------------|
| CIPHER | Output layer | After softmax | Next-token belief distribution |
| KVComm | Attention layer | Per-layer KV pairs | Layer-specific attention context |
| **AC** | **Residual stream** | **Mid-late layer (~26/32)** | **Enriched entity representations** |
| [[thought-communication-multiagent\|ThoughtComm]] | Latent factors | Autoencoder output | Disentangled thoughts |
