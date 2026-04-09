Three specific mechanisms explain why latent reasoning training causes forgetting in instruction-tuned models:

1. **Distribution shift**: Latent reasoning training data contains continuous thoughts replacing language steps — a representation the model has never seen during its instruction-tuning pipeline. The model's input distribution shifts from well-formed natural language tokens to arbitrary continuous vectors, forcing adaptation of early-layer representations.

2. **Objective conflict**: The latent reasoning objective (predict future tokens from continuous hidden states) optimizes for a different capability than the instruction-following objective (generate helpful, harmless, format-compliant responses). The gradient directions for these two objectives may be **anti-correlated** in large parts of parameter space.

3. **Representation drift**: Even LoRA's low-rank updates (which modify only a small subspace of each weight matrix) alter the model's internal representations enough to cascade through the network. A small change in layer 3's output distribution becomes amplified through subsequent layers, producing large behavioral shifts at the output.

4. **Optimizer state mismatch**: Coconut's multi-stage curriculum resets the optimizer state between stages ([[raw/pdf/arxiv-2412.06769.pdf|Coconut §3.2]]), which helps on base models but may be insufficient for instruction-tuned models where the loss landscape has been reshaped by RLHF.
