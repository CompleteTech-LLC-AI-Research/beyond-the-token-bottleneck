### Complexity Theory

The **depth bottleneck** is the foundational result. Feng et al. establish the $\text{TC}^0$ limitation; Zhu et al. show continuous CoT breaks it more efficiently than discrete CoT. Together they prove that the discrete-to-continuous shift is not an optimization — it is a change in what is **computable** at fixed model depth.

### Representation Geometry

Three papers converge on the same conclusion from different angles: neural network representations have **linear geometric structure** that is approximately preserved across models.

| Paper | Finding | Implication |
|-------|---------|-------------|
| [[linearity-relation-decoding\|Hernandez et al.]] | 48% of tested relation types decoded by affine transforms | Linear projections are theoretically justified |
| [[relative-representations-zero-shot\|Moschella et al.]] | Latent spaces related by angle-preserving maps | Zero-shot stitching via cosine anchors |
| [[platonic-representation-hypothesis\|Huh et al.]] | Representations converge to shared PMI kernel | Cross-model alignment improves with scale |

### Convergence Hypotheses

The **Platonic Representation Hypothesis** is the strongest claim: models converge on a single representation of reality. The **relative representations** framework is the weaker, more practical version: models are related by near-isometric transforms regardless of whether they converge to an absolute target. Both predict that cross-model latent communication should work — and get easier — as models improve.
