### Two Hypotheses

**H1 — Intermediate layers carry transferable knowledge**: Prior work (Jawahar et al., 2019; Geva et al., 2020) shows a layer hierarchy:
- **Early layers** (1-10): Surface patterns, syntactic features — too shallow for semantic transfer
- **Middle layers** (10-20): Semantic abstractions, relational information — most transferable
- **Late layers** (20+): Task-specific predictions — too specialized, may conflict with receiver's own late processing

**H2 — High-attention layers are more informative**: Layers where the attention mechanism allocates more weight to context tokens encode more salient contextual relations. Attention concentration serves as a proxy for the communication value of a KV subset.

### The Selection Score

For each layer $l$, the attention importance score is computed as the average attention weight assigned to context tokens across all heads and query positions:

> $$\hat{S}_{al} = \frac{1}{H|Q|} \sum_h \sum_q \sum_c a^l_{h,q,c}$$

This is normalized to $[0,1]$, then combined with a **Gaussian prior** centered at layer $\mu$ with standard deviation $\sigma$:

> $$S_l = \alpha \cdot S_{al} + (1-\alpha) \cdot P_l, \quad \text{where } P_l = \exp\!\left(-\frac{(l-\mu)^2}{2\sigma^2}\right)$$

The Gaussian prior encodes H1 (preference for intermediate layers). The attention score encodes H2 (preference for high-attention layers). The top $M$ layers by combined score are selected.

### Calibration Efficiency

A remarkable finding: **a single calibration sample** is sufficient to select layers that generalize to the entire test set. The selection is computed once per model pair and reused across all inputs.

### Non-Contiguous Selection

A key distinction from prior work: KVComm can select **non-contiguous layers** (e.g., layers 8, 12, 15, 19, 23 but not 9-11). This is important because the most informative layers are not necessarily adjacent.
