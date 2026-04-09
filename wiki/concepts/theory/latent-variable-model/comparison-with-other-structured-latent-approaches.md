| Approach | Latent structure | How structure is imposed | Identifiability guarantee | Practical overhead |
|----------|-----------------|-------------------------|--------------------------|-------------------|
| **ThoughtComm autoencoder** | Shared/private thoughts with agreement routing | $\ell_1$ Jacobian sparsity | Theorems 1-3 (pairwise, up to permutation) | Autoencoder training (500 examples) |
| **$\beta$-VAE** | Factorial (independent) latent dimensions | KL divergence penalty on prior | None (Locatello et al., 2019) | Standard VAE training |
| **Sparse autoencoders (SAEs)** | Sparse activations (many zeros per input) | $\ell_1$ on activations (not Jacobian) | None formal; empirically interpretable | SAE training on activations |
| **Dictionary learning** | Sparse codes over learned dictionary | $\ell_0$/$\ell_1$ on codes | Unique under RIP conditions | Optimization per input |
| **[[cipher-multiagent-debate-embeddings|CIPHER]] (unstructured)** | None — raw embedding vectors | None | None | Zero (inference-time only) |

A key distinction: ThoughtComm regularizes the **Jacobian** (the mapping's derivative), not the **activations** (the latent values themselves). This is a deeper form of structural constraint — it controls how the latent-to-observed mapping works, not just what specific values the latents take. Two inputs could produce dense latent activations while still having a sparse Jacobian, meaning the underlying generative process is sparse even when any particular instantiation is not.
