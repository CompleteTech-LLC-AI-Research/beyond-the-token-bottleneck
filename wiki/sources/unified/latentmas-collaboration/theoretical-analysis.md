### Theorem 3.1 — Expressiveness of Latent Thoughts

**Assumption** (Linear Representation Hypothesis): Hidden embeddings $h$ are linear combinations of an underlying semantic basis $\{e_1, \ldots, e_d\}$ with ternary coefficients $\alpha_i \in \{0, +1, -1\}$, where $d$ is the hidden dimension.

**Statement**: If a length-$K$ sequence of latent thoughts can be expressed losslessly through text-based reasoning, then the required text length (in tokens) is at least $Kd / \log|V|$, where $|V|$ is the vocabulary size.

**Derivation sketch**: Under the ternary coefficient assumption, each hidden embedding can encode one of $3^d$ distinct states. A length-$K$ sequence of latent thoughts can represent $(3^d)^K = 3^{Kd}$ distinct sequences. To represent this losslessly with text tokens from vocabulary $V$, you need at least $L$ tokens where $|V|^L \geq 3^{Kd}$, giving $L \geq Kd \cdot \log(3) / \log|V| \geq Kd / \log|V|$.

**Concrete numbers**: For Qwen3 models with typical vocabulary size ~152K:
- Qwen3-4B ($d=3584$): $3584 / \log_2(152000) \approx$ **235.7x** more efficient
- Qwen3-8B ($d=4096$): $4096 / \log_2(152000) \approx$ **377.1x** more efficient (note: paper states this but $d$ values may differ)
- Qwen3-14B ($d=5120$): $5120 / \log_2(152000) \approx$ **471.4x** more efficient

### Theorem 3.3 — Lossless Information Preservation

KV-cache transfer produces outputs identical to directly re-encoding the predecessor's full output as input text. Proved by induction: if keys and values are the same at layer $l-1$, then the attention output at layer $l$ is the same, so the full forward pass is the same through all $N$ layers.

### Theorem 3.4 — Complexity Comparison

**LatentMAS per-agent complexity**: $O((T^2 K + K^2 + Kd) \cdot N)$, where $T$ = input length, $K$ = latent steps, $d$ = hidden dimension, $N$ = number of layers.

**TextMAS per-agent complexity** (to match expressiveness): $O((T^3 Kd / \log|V| + K^3 d^2 / \log^2|V| + K^2 d / \log|V|) \cdot N + K^2 d |V| / \log|V|)$. The extra $|V|$ factor comes from the softmax decoding step required at every text token.
