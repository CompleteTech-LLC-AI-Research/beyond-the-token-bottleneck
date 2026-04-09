### Alignment Measurement

The paper uses a **mutual nearest-neighbor (mutual k-NN) metric** to measure representational alignment, rather than CKA or SVCCA. The metric measures the mean intersection of the $k$-nearest neighbor sets induced by two kernels $K_1$ and $K_2$, normalized by $k$. This is a variant of metrics from Park et al. (2024), Klabunde et al. (2023), and Oron et al. (2017).

Key definitions:
- **Representation**: A function $f: \mathcal{X} \to \R^n$ mapping inputs to feature vectors
- **Kernel**: $K(x_i, x_j) = \langle f(x_i), f(x_j) \rangle$ -- the similarity structure induced by a representation
- **Kernel alignment metric**: $m: \mathcal{K} \times \mathcal{K} \to \R$ -- similarity between two kernels

The mutual k-NN metric was chosen over CKA because it captures **neighborhood structure** rather than global linear correlation. The authors argue that for cross-modal alignment, what matters is whether nearby points in one representation are also nearby in another, not whether the exact distances match. The metric uses $k = 10$ in all experiments.

### Cross-Modal Alignment Measurement

For vision-language alignment, the paper uses the **Wikipedia captions dataset (WIT)** -- paired images $(x_i)$ and captions $(y_i)$. Two kernels are constructed:
$$K_{\text{img}}(i, j) = \langle f_{\text{img}}(x_i), f_{\text{img}}(x_j) \rangle$$
$$K_{\text{text}}(i, j) = \langle f_{\text{text}}(y_i), f_{\text{text}}(y_j) \rangle$$

The mutual k-NN metric is then computed between $K_{\text{img}}$ and $K_{\text{text}}$. Embeddings are extracted from vision models as class tokens and from language models as average-pooled tokens, selecting the layer that maximizes alignment.
