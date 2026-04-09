### NormMatch Components

NormMatch rescaling ($\text{NormMatch}(h) = \mu_i \cdot h / (\|h\|_2 + \varepsilon)$) is critical for preventing norm drift during latent rollout. Without NormMatch, rollout hidden states diverge from the embedding manifold within ~50 steps, causing generation collapse. The per-model calibration constant $\mu_i = \E[\|E_i(w)\|_2]$ must be computed over the full vocabulary — approximating with a subset degrades rollout stability.

### Resampler Configuration

The Perceiver-style resampler uses 6 Transformer layers with 8 attention heads and dropout 0.10. Reducing to 3 layers drops accuracy by ~3-4pp on math benchmarks. Increasing to 12 layers shows diminishing returns (<1pp gain) while doubling codec parameter count. The L=6 configuration represents the efficiency sweet spot at ~0.05B parameters per codec.

### Alignment Anchor Count

Default: **3,000 anchors** (1,000 each from CoS-E, OpenCodeReasoning, PRM800K). The weakly supervised variant uses only **90 anchors** (30 per source) yet achieves comparable or better results (+6.5pp accuracy, 2.67x speedup vs +6.3pp, 1.87x for full supervision). This remarkable data efficiency suggests that affine alignment via ridge regression is well-conditioned: the cross-model mismatch is low-rank enough that ~90 paired observations suffice to estimate the affine transform. However, the weakly supervised variant shows higher variance across benchmark pairs — reliability improves with more anchors even if average performance does not.

### Visual Token Budget

The default **256 image injection tokens** ($K_\text{img}$) suffice for small models (1.6B-4B) but become a bottleneck for mid-sized models (4B-12B). The accuracy degradation on complex tasks (AIME 2024: -33.3pp for 8B+12B config) is attributed to this fixed bandwidth. The paper notes this is not a hard limit: stacking multiple images (4x 224x224 for ~1024 tokens) or using higher-resolution images (1008px Qwen-style) can increase the visual token budget proportionally. No systematic ablation of $K_\text{img} \in \{64, 128, 256, 512, 1024\}$ is provided — this is a key gap for understanding the bandwidth-accuracy trade-off curve.
