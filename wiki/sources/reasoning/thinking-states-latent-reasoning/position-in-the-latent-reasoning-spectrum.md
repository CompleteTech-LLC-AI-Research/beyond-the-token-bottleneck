| Method | Reasoning Format | Supervision | Recurrence | Training Cost | Interpretability |
|--------|-----------------|-------------|------------|---------------|-----------------|
| CoT | NL tokens (appended) | Direct | Sequential generation | Constant | Full |
| [[coconut-reasoning-latent-space\|Coconut]] | Continuous embeddings | None (indirect) | Hidden-state feedback | Linear (BPTT) | None |
| [[softcot-efficient-reasoning\|SoftCoT]] | External soft tokens | Indirect (projection) | None (single pass) | Constant | Via decoding |
| **Thinking States** | **NL $\to$ compressed states** | **Direct (teacher forcing)** | **Chunk-recurrent** | **Constant** | **Full (NL thoughts)** |

Thinking States uniquely combines recurrent conditioning, direct supervision, no context extension, AND interpretability -- properties previously mutually exclusive in the latent reasoning literature.
