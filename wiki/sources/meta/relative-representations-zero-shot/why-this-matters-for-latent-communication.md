### Linear maps are theoretically justified

If the transformation between latent spaces is approximately orthogonal (rotation/reflection + scaling), then a linear projection is the **exact correct tool**. You don't need nonlinear transformations. This directly explains why:
- [[cache-to-cache-semantic-communication|C2C]]'s projection module works with linear layers
- [[kv-cache-alignment-shared-space|KV Cache Alignment]]'s affine adapters suffice
- [[activation-communication-harvard|AC]]'s mapping matrix W (trained on 3072 C4 sentences) achieves SOTA

### Anchor-based alignment is O(N)

Each model needs anchor similarities computed once. Cross-model alignment is a fixed-cost post-processing step. This echoes KV Cache Alignment's $O(N)$ scaling and Vision Wormhole's affine alignment.

### Diagnostic tool

The 0.955 Pearson correlation means you can predict whether two models' latent spaces are compatible **before** attempting communication — no task-specific evaluation needed.
