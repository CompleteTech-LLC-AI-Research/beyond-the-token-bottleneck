### Adapter architecture matters
| Architecture | Parameters | Performance |
|-------------|-----------|-------------|
| Identity mapping (no learned params) | 0 | Poor — even same-architecture models can't share KV directly |
| Linear mapping | 269M-806M | Matches base model (supports the "approximately linear" latent space hypothesis) |
| Cross-attention translator | 238M-645M | Exceeds base model, scales consistently with size |

The linear mapping result aligns with Moschella et al. (2022) — latent spaces of models trained on similar distributions are approximately related by linear transformations. But the cross-attention architecture is more parameter-efficient and scales better.

### Training paths
Not all pairwise paths need to be seen during training. Even training on 1 of 9 possible paths (in a 3-model pool) produces reasonable zero-shot generalization to unseen paths. Some stochasticity in path selection is beneficial for generalization.
