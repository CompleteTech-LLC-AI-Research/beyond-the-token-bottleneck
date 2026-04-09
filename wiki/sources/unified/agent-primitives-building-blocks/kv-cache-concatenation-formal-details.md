### Input-Output Alignment Assumption (Equation 2)

The key assumption is that the Transformer decoder conditions future token generation exclusively on its accumulated key-value states, not the discrete token sequence:

> $$p(y \mid Z_A, x^B_{1:n_B}) \approx p(y \mid s_A, x^B_{1:n_B})$$

where $Z_A$ is the KV cache produced by agent A after processing sequence $s_A$. This approximation holds **when both agents share the same model parameters and positional encoding scheme**. The paper restricts all experiments to same-model configurations for this reason.

### Concatenation Mechanism

For agent A with KV cache $Z^A_{T_A}$ and agent B with system prompt KV cache $Z^B_{n_B}$, the combined cache at each layer $l$ is:

- $\tilde{K}^{B,l} = [K^{B,l}_{n_B};\; K^{A,l}_{T_A}]$
- $\tilde{V}^{B,l} = [V^{B,l}_{n_B};\; V^{A,l}_{T_A}]$

Agent B then decodes conditioned on this combined cache, without any natural language communication from A.

### RoPE Positional Re-encoding

Modern LLMs use **Rotary Positional Encoding (RoPE)** where positional information is encoded through position-dependent rotations: $\text{RoPE}(K_t) = R(t) \cdot K_t$, where $R(t)$ is a deterministic block-diagonal rotation operator with 2D rotation angles linear in $t$.

When KV caches are concatenated, the combined cache is treated as a single continuous sequence:
- Agent B's system prompt occupies positions $1$ to $n_B$
- Agent A's KV cache occupies positions $1$ to $T_A$

To preserve RoPE semantics, agent A's KV states are **re-indexed by offset $n_B$**: for each layer $l$ and position $t \in \{1,\ldots,T_A\}$, apply $\text{RoPE}(K^{A,l}_t) \to R(t + n_B) \cdot K^{A,l}_t$.

**Why LLaMA breaks without re-encoding**: LLaMA-based models are extremely sensitive to positional encoding misalignment. Without re-encoding, on DeepSeek-R1-Distill-Llama-70B the primitives-based MAS drops from 56.7% to 26.7% on AIME25, from 85.3% to 31.1% on HumanEval+, and from 81.9% to 36.6% on MedQA. Qwen3 models are more resilient — drops of only 1-13 pp — suggesting different architectural sensitivity to positional encoding consistency.
