### The Cache Fuser

At each layer $n$, the fuser takes the Receiver's KV-cache $C_n(X)$ and the corresponding Sharer's KV-cache $C^S_{G(n)}(X)$ and produces a fused cache with residual connection:

> $$C_F = C_n(X) + F_n(C_n(X), C^S_{G(n)}(X))$$

Three modules within the fuser:

1. **Projection module**: Concatenates Receiver and Sharer KV-caches, processes through a projection layer + feature fusion layer. This handles the representation space mismatch between models.

2. **Dynamic weighting module**: An input-aware head modulation layer that dynamically reweights the projected information per attention head. Different heads encode different types of information; the dynamic weights adapt to each input.

3. **Learnable gate**: A per-layer trainable gate using **Gumbel-sigmoid with temperature annealing** — differentiable during training, binary at inference. This learns which layers benefit from cache fusion and which should be left alone (addressing the layer-wise variation finding from the oracle experiments).

### Cross-Model Alignment

Two alignment challenges for cross-architecture communication:

**Token alignment**: Different tokenizers produce different token sequences for the same input. C2C aligns by decoding each Receiver token to its string form, re-encoding with the Sharer's tokenizer, and selecting the Sharer token with maximal string coverage for one-to-many mappings.

**Layer alignment**: Models of different depths need layer correspondence. C2C adopts **terminal alignment** — final layers are aligned first, then working backwards. This assumes later layers are more comparable across architectures (both models' final layers produce output-ready representations).

### Training

Both Sharer and Receiver models are **frozen** — only the fuser is trained. Standard next-token prediction loss on Receiver's outputs, conditioned on fused rather than original cache. Three stages: Forward (both models encode input), Fusion (C2C module fuses caches), Supervision (Receiver generates from fused cache, gradients through C2C only).

The fuser is trained on general data (OpenHermes2.5, 500k samples) for broad applicability, or task-specific data (MMLU) for ablative analysis.
