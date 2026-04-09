In a transformer, each attention layer computes **keys (K)** and **values (V)** for every token in the context. During autoregressive generation, previously computed K and V vectors are cached to avoid redundant computation — this is the **KV-cache**.

The KV-cache has a specific structure:
- **Per layer**: Each of *L* transformer layers has its own KV-cache
- **Per head**: Within each layer, each of *H* attention heads has separate K and V vectors
- **Per position**: Each token position has a K-V pair per layer per head
- **Dimensionality**: Each token's full KV-cache is $2 \times L \times H \times d$ values ($d$ = head dimension)

For a 70B-parameter model (L=80, H=64, d=128), each token's full KV-cache is $2 \times 80 \times 64 \times 128 \approx 1.3\text{M}$ float values — orders of magnitude more information than the single embedding vector shared by [[cipher-multiagent-debate-embeddings|CIPHER]].
