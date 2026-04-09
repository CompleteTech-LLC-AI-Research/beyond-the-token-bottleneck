### Efficiency

Latent reasoning is **token-efficient** but not necessarily **compute-efficient**:
- **Token efficiency**: Coconut generates far fewer tokens than CoT (e.g., 14.2 vs 49.4 on ProsQA) because no fluency tokens are needed.
- **Compute per thought**: Each continuous thought requires a full forward pass through the transformer — the same compute as generating a token. But since there are fewer thoughts than tokens, total compute is often lower.
- **Parallelism limitation**: Continuous thoughts are inherently sequential (each depends on the previous). Unlike standard token generation (which can be parallelized across sequences in a batch), the sequential dependency limits training throughput.

### Scaling Properties

From Coconut's experiments:
- Increasing the hyperparameter $c$ (continuous thoughts per language step) from 0→1→2 steadily improves performance, suggesting that more latent computation scales reasoning ability.
- This parallels the finding that longer CoT chains improve accuracy — both are forms of **inference-time compute scaling**.
- Whether this scaling continues to frontier model sizes is an open question.
