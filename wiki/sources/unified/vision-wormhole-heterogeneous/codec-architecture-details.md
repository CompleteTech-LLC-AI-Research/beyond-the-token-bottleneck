| Parameter | Value |
|---|---|
| Universal token dimension $D$ | 512 |
| Number of universal tokens $K_u$ | 1024 |
| Image injection tokens $K_\text{img}$ | 256 |
| Transformer layers | 6 |
| Attention heads | 8 |
| Dropout | 0.10 |
| Latent rollout length $T$ | 1024 |
| Training steps | 400 |
| Batch size | 2 |
| Optimizer | AdamW, lr = $2 \times 10^{-4}$ |
| Codec parameter count | ~0.05B |
| Effective dataset coverage (default) | ~0.27× (800 draws / 3000 anchors) |
| Effective dataset coverage (weak) | ~8.9× (800 draws / 90 anchors) |
