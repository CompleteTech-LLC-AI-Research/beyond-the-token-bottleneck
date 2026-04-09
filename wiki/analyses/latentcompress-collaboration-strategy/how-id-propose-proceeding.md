### Option A: Join Their Project With Our Unique Contributions

If you want to collaborate with them, our analysis provides **differentiation** they can't get elsewhere. Specifically:

**Contribution 1 — The superposition-disentanglement hypothesis**: Propose testing whether their 4 slots correspond to distinct reasoning paths (using [[coconut-reasoning-latent-space|Coconut]]'s probing methodology). This is a one-experiment test that could produce a landmark finding. If slot-attention naturally disentangles superposed paths, it connects compression research to the deepest theoretical finding in the field.

> [!warning] Caveat: Geometric Homogeneity Barrier
> [[inference-time-scaling-continuous-reasoning|Wang et al. (2025)]] found that COCONUT's continuous thought space exhibits extreme geometric homogeneity — IsoScore $\approx$ 0.013 (near-zero isotropy), and correct vs. incorrect reasoning trajectories are **geometrically indistinguishable** by every metric tested (compactness, curvature, local smoothness, straightness). PRM/ORM rerankers trained on these representations achieve F1 scores barely above chance. This is a potential blocker for Contribution 1: if the latent representations lack geometric structure to begin with, slot-attention may not find meaningful subspaces to disentangle. The hypothesis survives — compression *could* impose structure that the raw space lacks — but it should be framed as "does compression *create* separability?" rather than "does compression *reveal* separability?" Any experimental test must measure whether slots produce geometrically distinguishable representations (e.g., per-slot IsoScore, inter-slot cosine distance) rather than assuming the input space already supports disentanglement.

**Contribution 2 — Delta compression**: Propose compressing state deltas instead of raw hidden states. Based on [[state-delta-trajectory|SDE]]'s results, this should require less bandwidth for the same information content (deltas are already context-agnostic). Simple swap in their pipeline, potentially large improvement.

**Contribution 3 — The comprehensive literature map**: They reference 3 papers. We have 16. Our wiki provides the context they're missing — especially the [[kvcomm-kth-selective|KVComm]] layer selection work, [[activation-communication-harvard|AC]]'s enriched entity representation finding, [[thought-communication-multiagent|ThoughtComm]]'s identifiability framework, and the [[catastrophic-forgetting|catastrophic forgetting]] barrier.

**Interest area for their application**: Direction 1 (compressor training) + Direction 2 (native pretraining), with a focus on whether compression naturally disentangles superposed reasoning.

### Option B: Independent Research Informed by Their Results

If you want to pursue your own research, their results validate several of our directions and suggest a specific experimental program:

**Phase 1 — Validate superposition survival under compression** (1-2 weeks):
Use their slot-attention architecture (or reimplement) on Coconut's ProsQA task. Generate continuous thoughts, compress to slots, probe each slot for distinct reasoning paths. This is the highest-leverage experiment — if it works, it's a new paper.

**Phase 2 — Delta compression** (1-2 weeks):
Replace their raw hidden-state input with [[state-delta-trajectory|SDE]]-style inter-token deltas. Measure bandwidth-accuracy curves and compare. If deltas achieve the same accuracy at lower bandwidth, that's a direct improvement on their core result.

**Phase 3 — Self-improvement cycling** (1 week):
Test whether their compressor (or any latent mediator) improves solo model performance through cyclic translation. If the self-improvement effect is robust and iterable, it's a new inference-time scaling paradigm.

### Option C: Hybrid — Collaborate on Their Infrastructure, Pursue Our Unique Directions

Join their project for access to their codebase and compute, but focus on the directions they haven't identified:

1. **Superposition disentanglement via compression** (our direction #2, using their slots)
2. **Delta-based compression** (our direction #4, applied to their pipeline)
3. **Self-improvement cycling** (our direction #3, testable with their compressor)

These are all **complementary** to their stated directions — they'd get novel research directions, you'd get working infrastructure.
