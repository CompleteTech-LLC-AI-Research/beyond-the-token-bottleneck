| Dataset | Absolute | Relative | $\Delta$ |
|---------|----------|----------|---|
| MNIST | 97.95 | 97.91 | -0.04 |
| Fashion-MNIST | 90.32 | 90.19 | -0.13 |
| CIFAR-10 | 87.85 | 87.70 | -0.15 |
| CIFAR-100 | 68.88 | **66.72** | **-2.16** |

Near-zero degradation on most tasks. CIFAR-100 shows a ~2-point drop — the only notable cost.

### End-to-End Training Instability

When training end-to-end (not frozen encoder): susceptible to model collapse. Increasing anchor count does NOT always help. Backpropagation does not pass through anchors (encourages smoother optimization but limits gradient information). Frozen-encoder usage is more stable and recommended.

### The Zero-Shot Transfer Mechanism in Detail

The zero-shot stitching result deserves careful analysis because it establishes the theoretical ceiling for training-free cross-model communication. The mechanism works in three steps:

1. **Anchor projection**: Both models compute embeddings for the same set of anchor inputs. These anchor embeddings define a coordinate system in each model's latent space.
2. **Relative encoding**: Any new input is represented not by its absolute embedding but by its similarity profile to the anchors — a vector in $\R^{|A|}$ where each coordinate is a cosine similarity.
3. **Space-invariant decoding**: Because cosine similarity is preserved under isometric transformations, the relative representation is (approximately) identical regardless of which model produced it.

The critical insight is that this works **without any paired data** between models. Unlike [[kv-cache-alignment-shared-space|KV Cache Alignment]], which requires training on shared text to learn adapter parameters, relative representations need only a shared set of anchor inputs. The anchors serve as a "Rosetta Stone" — they don't need labels, just consistent inputs across models. This is why even OOD anchors work: the relative geometry is preserved even when the anchors themselves are poorly represented.

### Cross-Architecture Compatibility Implications

The cross-architecture results (BERT ↔ ELECTRA ↔ RoBERTa, ViT ↔ RexNet) are particularly significant for the broader [[latent-space-reasoning]] and [[kv-cache-communication]] research. They demonstrate that the isometric assumption holds across fundamentally different architectures (not just different seeds or hyperparameters of the same architecture). This provides empirical grounding for the [[platonic-representation-hypothesis|Platonic Representation Hypothesis]]: if different architectures trained on similar data converge to approximately isometric representations, then cross-model communication is theoretically possible without architecture-specific engineering.

However, the quality of zero-shot stitching degrades with architectural distance. Same-architecture stitching (BERT encoder ↔ BERT decoder) preserves ~95% of within-model accuracy, while cross-architecture stitching (ViT encoder ↔ RexNet decoder) preserves ~83%. This gap quantifies the degree to which the isometric assumption breaks down as models diverge — and motivates the learned projections used by [[cache-to-cache-semantic-communication|C2C]] and [[activation-communication-harvard|AC]] when higher fidelity is needed.
