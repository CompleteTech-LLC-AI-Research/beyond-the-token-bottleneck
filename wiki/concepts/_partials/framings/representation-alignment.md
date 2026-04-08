---
type: concept-partial
partial: representation-alignment
created: "2026-04-08"
updated: "2026-04-08"
---

**Representation alignment** is the empirical finding that independently trained neural models converge on similar internal representational geometries — and the family of techniques that exploits this convergence to bridge different models' latent spaces. It is the *enabling condition* for the deep end of the [[depth-spectrum]]: without it, sharing KV entries, activations, or embeddings across models would be noise.

The core observation comes from the [[platonic-representation-hypothesis|Platonic Representation Hypothesis]]: models across architectures, training objectives, and even modalities appear to be converging toward a shared statistical model of reality, with higher-performing models more aligned with each other. If independently trained networks arrive at approximately the same internal representations, then cross-model latent communication should get *easier* with scale, not harder.

Two complementary techniques turn this observation into a usable bridge:

- **[[relative-representations-zero-shot|Relative Representations]]** re-encode each vector as its similarities to a shared set of anchor samples. Because the resulting coordinates depend only on geometric relationships — not on the absolute basis any particular model happened to learn — representations become invariant to the rotations and reflections that separate well-trained latent spaces. This enables zero-shot model stitching with no learned mapping.
- **[[linearity-relation-decoding|Linear relational embeddings]]** show that the mapping from one concept to a related concept is approximately an affine transform inside a model's representation space. Because structure-preserving relations are *linear*, the transform between two models' spaces can often be recovered by a small linear map fit on a handful of paired examples.

Together these say: the geometry is shared, the residual transform is approximately orthogonal, and a linear projection is the exact correct tool for crossing between models. Every deep-stage latent communication method — KV-cache transfer, activation sharing, embedding-space exchange — ultimately rests on this, whether it aligns spaces explicitly (learned projections, ridge-regression alignment matrices) or implicitly assumes the spaces are already close enough to graft without one.

## Used by

- [[activation-communication]]
