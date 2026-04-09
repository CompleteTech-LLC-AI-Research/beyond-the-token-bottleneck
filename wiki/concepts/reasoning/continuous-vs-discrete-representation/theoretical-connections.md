### Information Theory

The discrete bottleneck is a lossy compression step. For a vocabulary of size $V$:
- **Maximum information per token**: $\log_2(V) \approx 15$ bits (for $V = 32{,}000$)
- **Information in the model's belief**: The full softmax distribution — up to $V \times 32$ bits (float32) = ~128 KB of raw probability data, or more practically, the effective information content of the distribution

The gap between these is enormous. Even if most of the distribution's mass is concentrated on a few tokens, the tail carries real information — particularly about what the model considered but rejected. This "rejected alternative" information is exactly what enables BFS in [[coconut-reasoning-latent-space|Coconut]] and richer communication in [[cipher-multiagent-debate-embeddings|CIPHER]].

More precisely, the information loss at the bottleneck can be quantified as the **KL divergence** between the model's full distribution and the degenerate distribution obtained after sampling:

$$D_\text{KL}(p \| \delta_{\hat{v}}) = -\sum_v p(v) \log \frac{\delta_{\hat{v}}(v)}{p(v)} = -\log p(\hat{v}) + H(p)$$

where $\hat{v}$ is the sampled token and $H(p)$ is the entropy of the original distribution. When the model is confident ($H(p) \approx 0$, $p(\hat{v}) \approx 1$), almost no information is lost. When the model is uncertain ($H(p)$ is large), the loss is dramatic — precisely the regime where [[temperature-diversity]] and [[latent-space-reasoning]] provide the most benefit.

### The Expected SARSA Analogy

[[cipher-multiagent-debate-embeddings|CIPHER]] draws an explicit analogy to reinforcement learning: Expected SARSA (using expected Q-values) outperforms vanilla SARSA (using sampled Q-values) because expectations are lower-variance estimates. The same principle applies:
- **Sampled token** (vanilla SARSA): High variance, information-lossy
- **Expected embedding** (Expected SARSA): Low variance, information-preserving

### Superposition and Quantum Analogy

![[superposition]]

[[superposition-coconut-theory|Zhu et al. (NeurIPS 2025)]] provide a **rigorous formalization** of this mechanism ([[raw/pdf/arxiv-2505.12514.pdf|Zhu et al. Theorem 1]]): each continuous thought is provably the normalized uniform mixture of all vertices reachable within $c$ BFS steps, so a 2-layer transformer with $D$ continuous thoughts solves graph reachability in $D$ steps vs. $O(n^2)$ for discrete CoT — a potentially **quadratic-to-linear speedup**. The quantum mechanics analogy is made mathematically precise: continuous thoughts are superposition states (weighted sums over multiple vertex embeddings), token sampling is measurement/collapse, and the answer token is a measurement that projects the superposition onto the correct candidate. The formalization proves this isn't just an analogy — it's the actual computational mechanism, and it ties superposition directly to the bandwidth-gap argument above: the rejected-alternative information the KL divergence quantifies is precisely the mixture weights that parallel BFS depends on.

### The Depth Bottleneck (Feng et al., NeurIPS 2023)

[[cot-expressivity-theory|Feng et al.]] prove that the discrete bottleneck isn't just about information density — it's about **computational expressivity** ([[raw/pdf/arxiv-2305.15408.pdf|Feng et al. Theorem 3.3]]). Bounded-depth transformers are limited to $\text{TC}^0$ (constant-depth threshold circuits). CoT breaks this barrier by adding effective depth. Continuous CoT breaks it further by adding superposition. The discrete-to-continuous shift is not incremental — it's a complexity-class transition.

### Connection to Distributed Representations

The continuous vs. discrete tension in LLM systems echoes the classic **localist vs. distributed** representation debate in neural network research (Hinton, 1986; Smolensky, 1988). Distributed representations (patterns of activation across many dimensions) are more expressive than localist representations (one unit per concept). LLMs operating in natural language are, in a sense, reverting to localist representation (one token per position) despite having rich distributed representations internally.
