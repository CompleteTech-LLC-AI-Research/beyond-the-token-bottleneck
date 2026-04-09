### The Invariance Construction

For any data point $x$ with embedding $e_x$ and a set of anchors $A = \{a_1, \ldots, a_{|A|}\}$:

> $$r_x = (\cos\text{sim}(e_x, e_{a_1}),\; \cos\text{sim}(e_x, e_{a_2}),\; \ldots,\; \cos\text{sim}(e_x, e_{a_{|A|}}))$$

Where $\cos\text{sim}(a,b) = \frac{a \cdot b}{\|a\| \|b\|} = \cos(\theta)$.

**Why this works**: Cosine similarity is invariant to any angle-preserving transformation $T$. If $T$ is applied to both vectors: $\cos\text{sim}(Te_x, Te_a) = \cos\text{sim}(e_x, e_a)$. Therefore two models trained with different seeds produce **identical relative representations** for the same input, regardless of the (near-isometric) transformation between their absolute latent spaces.

**Core assumption**: When training varies (different seeds, hyperparameters), the mapping between resulting latent spaces is approximately angle-preserving. This is empirically validated across diverse settings and theoretically motivated by shared inductive biases in deep networks.

### Anchor Types

| Strategy | Description | Quality |
|----------|------------|---------|
| Uniform random | Random training samples | Simplest; competitive |
| Farthest point sampling | Maximize coverage | Best Jaccard/MRR |
| K-means centroids | Cluster centers | Best cosine similarity |
| Top-K frequent | Most common samples | Slightly worse |
| OOD anchors | From out-of-distribution data | Works for domain adaptation |
| Parallel anchors | Corresponding samples across domains | Best for cross-lingual |

Even noisy anchors (Google Translate outputs) or OOD anchors (Wikipedia sentences for Amazon reviews) work well. Performance improves monotonically with anchor count when the encoder is frozen.
