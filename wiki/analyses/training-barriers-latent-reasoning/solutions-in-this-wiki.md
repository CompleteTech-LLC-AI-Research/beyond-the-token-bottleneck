Three distinct approaches to the forgetting problem have emerged, each representing a different point on the stability-plasticity trade-off:

### Approach 1: Frozen Backbone with External Reasoning ([[softcot-efficient-reasoning|SoftCoT]])

[[softcot-efficient-reasoning|SoftCoT]] completely separates reasoning from the backbone by externalizing continuous thought generation to a small assistant model. The backbone LLM is **never modified** — only a lightweight linear projection layer is trained. This is the most conservative approach: it guarantees zero forgetting by construction, at the cost of requiring a two-model architecture.

- **Forgetting avoidance**: Complete — no backbone parameters change
- **Reasoning capability**: Moderate — the external assistant provides reasoning cues via soft tokens, but cannot perform the deep recurrent reasoning that [[coconut-reasoning-latent-space|Coconut]] enables
- **Practical cost**: Low — projection training requires only a single A100-80G; assistant can be as small as 0.5B parameters with minimal performance impact ([[raw/pdf/arxiv-2502.12134.pdf|SoftCoT Table 4]])

### Approach 2: Multi-Stage Curriculum ([[coconut-reasoning-latent-space|Coconut]])

[[coconut-reasoning-latent-space|Coconut]] gradually transitions from language reasoning to latent reasoning through a curriculum that progressively replaces language steps with continuous thoughts, resetting the optimizer between stages. This attempts to minimize forgetting through **gradual distribution shift** — each stage is only slightly different from the previous one.

- **Forgetting avoidance**: Partial on base models; **insufficient** for instruction-tuned models
- **Reasoning capability**: High — the hidden-state feedback loop enables emergent BFS and deep multi-step reasoning ([[raw/pdf/arxiv-2412.06769.pdf|Coconut §4.3]])
- **Practical cost**: High — multi-stage training with optimizer resets, validated only on GPT-2

### Approach 3: Lightweight Modules with Supervised States ([[thinking-states-latent-reasoning|Thinking States]])

[[thinking-states-latent-reasoning|Thinking States]] adds three small modules (thinking block, compression block, deep-to-shallow recurrence) to a frozen backbone. Crucially, it uses **teacher forcing** with supervised ground-truth reasoning annotations, avoiding backpropagation through time entirely. This sidesteps the forgetting problem through architectural separation while preserving recurrent reasoning capability.

- **Forgetting avoidance**: High — backbone is frozen; only lightweight modules are trained (initialized from existing layers)
- **Reasoning capability**: High — chunk-recurrent processing with deep-to-shallow injection achieves near-CoT accuracy on 2-hop QA with 2.66x speedup; dramatically outperforms CoT on length generalization ([[raw/pdf/arxiv-2602.08332.pdf|Thinking States Table 1]])
- **Practical cost**: Moderate — requires supervised reasoning annotations for teacher forcing; tested only on Qwen2.5-Base (not instruction-tuned), so the instruction-tuned forgetting question remains **untested**

### Comparative Summary

| Property | [[softcot-efficient-reasoning|SoftCoT]] | [[coconut-reasoning-latent-space|Coconut]] Curriculum | [[thinking-states-latent-reasoning|Thinking States]] |
|----------|---------|-------------------|----------------|
| Backbone modification | None | Full (all parameters) | None (frozen) |
| Forgetting guarantee | Complete | None on instruction-tuned | Complete (but untested on instruction-tuned) |
| Reasoning depth | Single-pass (no recurrence) | Multi-step recurrence | Chunk-level recurrence |
| Supervision required | Reasoning annotations | CoT data for curriculum | Chunk-level reasoning annotations |
| Inference architecture | Two models + projection | Single model | Single model + lightweight modules |
| Scale validated | 7-8B instruction-tuned | GPT-2 base | 0.5-1.5B base |
