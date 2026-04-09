### Alignment Matrix M Removal

On MedQA (Qwen3-14B Sequential), removing $M$ causes:
- ARC-C: **+5.3%** accuracy gain from using $M$ (from ~89.6% to ~94.9%)
- ARC-E: **+2.3%** accuracy gain
- GSM8K: **+3.6%** accuracy gain

Visualizations (Figure 6) show that without $M$, output embeddings $h_t$ drift significantly from the input embedding distribution. After applying $M$, the aligned vector $h'_{t+1}$ realigns with the original input embedding distribution in both density and geometric structure.

### Latent Step Depth Sweep (Qwen3-14B, Sequential)

| K (latent steps) | ARC-C | ARC-E | GSM8K |
|---|---|---|---|
| 0 | 91.3 | 94.7 | 85.6 |
| 10 | 93.4 | 98.9 | 90.3 |
| 20 | 93.4 | 98.9 | 90.9 |
| 40 | **94.9** | **99.4** | 91.4 |
| 80 | 94.8 | 99.6 | **92.0** |
| 160 | 93.7 | 98.3 | 91.9 |

Peak performance at $K=40$–$80$ steps. Beyond $K=160$, performance plateaus or slightly declines — excessive latent steps may introduce redundant or less useful information. In practice, a moderate budget of 40-80 steps provides the best accuracy-efficiency trade-off.

### t-SNE Visualization (Figure 5)

Conducted on 300 MedQA questions using Qwen3-4B/8B/14B. Compared the distribution of last-layer embeddings from LatentMAS (40 latent steps) against token embeddings from TextMAS (4096 max tokens). Two findings:
1. LatentMAS embeddings occupy **the same region** of embedding space as TextMAS token embeddings — semantic consistency.
2. LatentMAS embeddings **cover a broader area** than TextMAS embeddings — greater diversity and expressive capacity than discrete tokens.
