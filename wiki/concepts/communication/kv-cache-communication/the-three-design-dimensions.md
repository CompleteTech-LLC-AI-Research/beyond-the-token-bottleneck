### Dimension 1: What to Share (Layer Selection)

Not all layers are equally informative. [[kvcomm-kth-selective|KVComm]]'s analysis reveals a **layer hierarchy** for communication:

| Layer depth | Content | Communication value |
|-------------|---------|-------------------|
| Early (1-10) | Surface patterns, syntactic features | Low — too shallow for semantic transfer |
| Middle (10-20) | Semantic abstractions, relational knowledge | **Highest** — most transferable |
| Late (20+) | Task-specific predictions | Medium — may conflict with receiver's specialization |

KVComm's selection strategy combines two signals:
1. **Attention importance scores**: Average attention weight assigned to context tokens per layer — layers where the model attends more heavily to context encode more salient relations
2. **Gaussian prior**: Centered on intermediate layers, encoding the prior that middle layers are most transferable

Result: **30% of layers** already outperforms full natural language debate and embedding communication ([[raw/pdf/arxiv-2510.03346.pdf|KVComm §4.2, Figure 3]]). **70% of layers** matches the upper bound (full context concatenation).

A remarkable finding: **non-contiguous layer selection** outperforms contiguous blocks — the most informative layers are scattered across the network, not clustered.

### Dimension 2: Cross-Architecture Fusion

[[kvcomm-kth-selective|KVComm]] requires sender and receiver to be the same model or fine-tuned variants (identical architecture). [[cache-to-cache-semantic-communication|C2C]] breaks this constraint with a **learned neural cache fuser** ([[raw/pdf/arxiv-2510.03215.pdf|C2C §3]]):

**The fuser pipeline**:
1. **Projection**: Maps sender KV-cache into receiver's representation space (handles different dimensions, different learned representations)
2. **Dynamic weighting**: Per-head modulation — different attention heads get different blending weights, adaptive to each input
3. **Learnable gating**: Per-layer Gumbel-sigmoid gate that learns which layers benefit from fusion (binary at inference)
4. **Residual integration**: Fused cache is **added** to receiver's cache, not replacing it — preserves receiver's own information

**Cross-model results**: Works across Qwen ↔ LLaMA ↔ Gemma, 0.6B ↔ 14B, general ↔ specialized models. Even enables a base model (can't follow instructions) to serve as Sharer to an instruction-tuned Receiver — bypassing the language interface entirely.

**Key oracle finding**: KV-cache enrichment improves accuracy at **constant cache size** — proving the benefit comes from richer semantics, not just more attention targets. Different models encode genuinely complementary information (limited overlap in correct-answer sets).

### Dimension 2b: Scalable Cross-Model via Shared Space

[[kv-cache-alignment-shared-space|KV Cache Alignment (Google DeepMind)]] takes a fundamentally different approach from [[cache-to-cache-semantic-communication|C2C]]'s pairwise fusers: learn a **global shared KV-cache representation space** (an "interlingua") with per-model adapters.

**Architecture**: Each model gets two cross-attention-based adapters (~¼ model size each):
- T[α→Ω]: Translate from model α's KV-cache into the shared space
- T[Ω→α]: Translate from the shared space into model α's KV-cache

**Key advantages over pairwise approaches**:
- **$O(N)$ adapters** instead of $O(N^2)$ fusers — linear scaling with pool size
- **Zero-shot extensibility**: Add a new model by training 2 adapters; untrained paths to/from existing models work zero-shot
- **Module portability**: Soft prompts learned on one model transfer to another via the shared space — a capability no other approach provides

**The self-improvement effect**: Passing a model's KV-cache through the shared space and back (cyclic: A → Ω → A) actually **improves** that model's performance ([[raw/pdf/arxiv-2601.06123.pdf|KV Alignment §4.3]]). The shared space acts as a feature sharpener — distilling the most transferable representations. This parallels C2C's effective rank increase and KVComm's finding that selective sharing can exceed the skyline.

**Trade-off vs. C2C**: The shared space may lose pair-specific fine-grained structure (it optimizes for universality, not pair-specific performance). C2C's per-pair fusers can capture richer pair-specific relationships. Current scale is also smaller (100M-400M vs. C2C's 0.6B-14B).

### Dimension 3: Efficiency (Cache Reuse)

[[kvcomm-duke-online-reuse|KVCOMM-online]] tackles the **$O(M^2)$ redundant prefilling** problem in multi-agent systems. When agents share overlapping text under different system prompts, the same text produces different KV-caches due to context dependence. KVCOMM estimates these **context-dependent offsets** rather than recomputing from scratch.

**Theoretical foundation**: Two propositions show that KV-cache offsets between embedding-similar tokens under different prefixes are **bounded and predictable**. If you know how token X shifts from prefix A to prefix B, you can estimate how similar token Y shifts.

**Anchor pool mechanism**:
- Stores representative offset patterns from prior examples
- At inference: matches new requests to anchors by embedding similarity, interpolates offsets
- Updated online — adapts to changing input distributions
- Handles RoPE positional shifts via de-rotation/re-rotation

**Results**: 70%+ cache reuse rate, up to **7.8× prefill speedup** in 5-agent settings ([[raw/pdf/arxiv-2510.12872.pdf|KVCOMM-online Table 3]]), <2.5% accuracy degradation.
