### The Extra Computation Hypothesis

Each pause token at position $t$ provides $L$ additional attention operations (one per layer) that can attend to all preceding tokens. Unlike CoT tokens, which carry semantic content through the vocabulary bottleneck, pause tokens carry **no input-side information** — they contribute only through the learned embedding (shared across all positions). The model must learn to use the pause positions as **scratch space** within attention: pause keys and values are populated via the embedding and the attention mechanism, then subsequent query tokens can attend to these positions to retrieve intermediate computation results.

This is analogous to register allocation in computer architecture: pause tokens provide additional "registers" (KV-cache entries) that the model can write intermediate results to via the attention mechanism and read from in later layers. The SQuAD result (+19.5 EM) suggests that extractive QA particularly benefits from this pattern — the model uses pause positions to pre-compute query-passage alignments before committing to an extraction span.

### Connection to Coconut's Latent Reasoning

Pause tokens and [[coconut-reasoning-latent-space|Coconut]]'s continuous thoughts share the insight that transformers can exploit non-linguistic computation, but differ fundamentally in mechanism:

| Property | Pause Tokens | Coconut Continuous Thoughts |
|----------|-------------|---------------------------|
| Information content | Zero (shared embedding) | Rich (full hidden-state feedback) |
| Compute added | Width only ($M$ extra vectors per layer) | Width + depth ($K$ extra forward passes) |
| Recurrence | None — single forward pass | Yes — each thought is a full forward pass |
| Expressivity class | Still $\text{TC}^0$ (constant depth) | Breaks $\text{TC}^0$ barrier via depth extension |
| Superposition | Not possible (fixed embedding) | Enabled — continuous vectors support [[superposition-coconut-theory|BFS via superposition]] |

Coconut's ablation directly quantifies the gap: on GSM8K at GPT-2 scale, Coconut achieves 34.1% vs. pause-as-thought at 24.1%. The 10pp difference represents the **information carried by continuous thoughts beyond mere extra compute**. This gap is expected to widen on tasks requiring search or planning (ProsQA: Coconut 97.0% vs. pause baseline 75.9%), where the depth advantage becomes critical.

### Why the 1B Model Benefits More Than 130M

The scale-dependent benefit is counter-intuitive: one might expect smaller models to benefit more from extra compute. The paper hypothesizes that exploiting pause tokens requires **sufficient capacity** to learn the complex attention patterns needed to write useful intermediate results to pause positions and read them back in later layers. At 130M parameters (12 layers, 12 heads), the attention mechanism may lack the capacity to develop these patterns. At 1B (24 layers, 32 heads), the doubled depth and head count provide enough representational space for the model to learn multi-step scratch-space computation across pause positions.

This connects to [[cot-expressivity-theory|Feng et al.]]'s theoretical framework: even within the $\text{TC}^0$ class, the constant factor matters. More layers and heads allow the model to implement more complex constant-depth circuits, and pause tokens expand the effective width of each layer's computation, making previously infeasible circuits achievable.
