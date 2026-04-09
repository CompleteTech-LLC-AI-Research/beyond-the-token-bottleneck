The advantage of continuous representation comes with a **compatibility cost**: continuous representations are tightly coupled to the architecture that produced them.

| Level | What's needed for compatibility |
|-------|-------------------------------|
| Natural language | Nothing — universal |
| Output embeddings ([[cipher-multiagent-debate-embeddings|CIPHER]]) | Shared tokenizer |
| KV-cache | Compatible architecture (layers, heads, dimensions) |
| Hidden states ([[coconut-reasoning-latent-space|Coconut]], [[activation-communication|activation communication]]) | Same or closely related model weights |

This creates a design tension: **richer communication requires tighter coupling**. However, two foundational results suggest the compatibility cost may be **lower than assumed**:

- **[[platonic-representation-hypothesis|Platonic Representation Hypothesis]]** ([[raw/pdf/arxiv-2405.07987.pdf|Huh et al. §3]]): Models converge to similar representations as they scale. Larger models should be **more** compatible, not less.
- **[[relative-representations-zero-shot|Relative Representations]]**: Well-trained models' latent spaces are related by approximately angle-preserving transforms — linear projections are the exact correct tool to align them. Zero-shot stitching works across architectures.

The optimal point on the trade-off depends on the system:
- **Open multi-agent systems** (heterogeneous models): Linear projections may suffice (supported by Platonic Rep + Relative Rep)
- **Homogeneous multi-agent systems** (same model): Can exploit deep latent communication with no alignment needed
- **Single-model reasoning**: Can use the deepest representations ([[coconut-reasoning-latent-space|Coconut]])
