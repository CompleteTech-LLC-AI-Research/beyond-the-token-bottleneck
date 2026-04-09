### State Tracking (Qwen2.5-0.5B, OOD Length Generalization)

Models trained on sequences up to $N$ operations, evaluated on lengths $[N, 100]$:

| Method | Parity N=10 | Parity N=20 | Parity N=40 | Vars N=10 | Vars N=20 | Vars N=40 |
|--------|------------|------------|------------|-----------|-----------|-----------|
| No CoT | 54.67% | 57.50% | 59.60% | 2.15% | 2.17% | 2.19% |
| CoT | 12.35% | 38.12% | 64.38% | 6.78% | 35.45% | 87.75% |
| **Thinking States** | **98.37%** | **99.02%** | **100.00%** | **33.76%** | **87.23%** | **97.71%** |

Thinking States dramatically outperforms CoT on length generalization. At Parity N=10 (trained on up to 10 operations, tested on 10-100), CoT achieves only 12.35% while Thinking States reaches 98.37%. The recurrent state mechanism handles arbitrary-length sequences where CoT's greedy left-to-right generation fails to generalize. All models are trained to 100% in-distribution accuracy to isolate extrapolation from optimization effects.

### General Reasoning (Qwen2.5-1.5B)

| Method | GSM8K Acc | GSM8K Speedup | 2-Hop FK Acc | 2-Hop FK Speedup | 2-Hop PK Acc | 2-Hop PK Speedup |
|--------|----------|--------------|-------------|-----------------|-------------|-----------------|
| CoT | 60.50% | 1x | 54.79% | 1x | 43.07% | 1x |
| No CoT | 34.11% | 5.59x | 33.47% | 1.89x | 31.92% | 2.03x |
| **Thinking States** | **42.22%** | **2.66x** | **54.91%** | **1.19x** | **43.05%** | **1.23x** |
| Coconut | 32.65% | 3.14x | 33.71% | 1.14x | 32.60% | 1.21x |
| iCoT | 34.00% | 5.71x | 28.84% | 1.59x | 36.31% | 1.80x |

Key observations:
- **Matches CoT on 2-Hop QA**: 54.91% vs 54.79% on Full Knowledge variant, with 1.19x speedup
- **Beats Coconut by 21+ points** on 2-Hop FK (54.91% vs 33.71%) -- the largest gap among all methods
- **Beats all latent baselines** by ~8 points on GSM8K (42.22% vs 34.00/34.11/32.65%)
- **Lags CoT by 18 points on GSM8K** (42.22% vs 60.50%) -- the state ambiguity problem

Speedups are measured as wall-clock time on a single A100-80GB, not token counts, because thought generation through the lightweight Thinking Block is faster than standard autoregressive decoding.

### 2-Hop QA Variants

- **Full Knowledge (FK)**: Required facts appear in fine-tuning data. Tests whether methods can acquire and manipulate new knowledge.
- **Parametric Knowledge (PK)**: Examples filtered to reflect knowledge already in the base model. Tests whether methods improve retrieval and manipulation of existing knowledge.

Thinking States achieves parity with CoT on both variants, while Coconut and iCoT collapse to near-chance performance on FK (33.71% and 28.84% respectively). This suggests that **supervised thoughts** enable knowledge acquisition in ways that purely continuous latent methods cannot.
