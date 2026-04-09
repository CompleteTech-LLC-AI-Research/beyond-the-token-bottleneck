### Per-Layer Fuser Pipeline

At each layer $n$ of the Receiver, the fuser processes inputs through three sequential modules:

1. **Projection module**: Takes the concatenated tensor $[C_n(X); C^S_{G(n)}(X)]$ of shape $(2, T, d_h)$ where $T$ is the sequence length and $d_h$ is the head dimension. A learned projection layer maps from the concatenated space to a unified dimension, followed by a feature fusion layer that blends the two streams. This module handles the core representation space mismatch — the Sharer's keys/values live in a different learned manifold from the Receiver's, even when the models share similar architecture.

2. **Dynamic weighting module**: An input-aware layer that produces per-head modulation weights. For a model with $H$ attention heads, this generates $H$ scalar weights that reweight the projected information per head. The key insight is that different attention heads encode different types of information (syntactic, semantic, positional), so a fixed blending weight would be suboptimal. The dynamic weights are conditioned on the current input, adapting the fusion for each specific example.

3. **Learnable gate**: A per-layer gate using **Gumbel-sigmoid** with temperature annealing. During training, the gate outputs a continuous value in $(0, 1)$ controlled by temperature $\tau$: $g_n = \sigma((s_n + \text{Gumbel noise}) / \tau)$. As training progresses, $\tau$ is annealed toward 0, pushing the gate toward binary (0 or 1). At inference, the gate is fully binary — each layer either fuses or passes through unchanged. This directly implements the oracle finding that some layers benefit from enrichment while others are harmed.

### Token Alignment Details

Different tokenizers produce different token sequences for the same text. For example, "unbelievable" might be one token in the Receiver's tokenizer but three tokens ["un", "believ", "able"] in the Sharer's. C2C handles this with a **string coverage** heuristic:

1. Decode each Receiver token to its string form
2. Re-encode the string with the Sharer's tokenizer
3. For one-to-many mappings (one Receiver token maps to multiple Sharer tokens), select the Sharer token with **maximal string overlap**
4. For many-to-one mappings, the single Sharer token's cache is reused for all corresponding Receiver positions

This heuristic works well for languages with similar tokenization granularity but may lose information for morphologically complex languages or when tokenizers operate at very different granularities (byte-level vs. subword).

### Layer Alignment via Terminal Matching

For models of different depths (e.g., 32-layer Sharer → 24-layer Receiver), C2C uses **terminal alignment**: the final layers of both models are aligned first, then working backwards. If the mapping function is $G(n)$, then $G(N_R) = N_S$ (last layers align) and earlier layers are mapped proportionally. The assumption is that final layers in any transformer converge toward output-ready representations regardless of total depth, making them more comparable than early layers which may encode model-specific features.
