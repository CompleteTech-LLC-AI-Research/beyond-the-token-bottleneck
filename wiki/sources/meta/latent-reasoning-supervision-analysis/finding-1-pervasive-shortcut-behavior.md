### Latent Step Depth Ablation

The paper varies the number of latent steps at *inference* time, holding training fixed. Under a true BFS model, accuracy should collapse when latent depth is forced to zero. The actual results:

| Method | Backbone | GSM8K @ depth=0 | GSM8K @ default | ProsQA @ depth=0 | ProsQA @ default |
|---|---|---|---|---|---|
| Coconut | LLaMA | non-trivial | 36.97% | ~99% | 99.40% |
| **CODI** | LLaMA | **~30%** | 55.57% | ~100% | 100.00% |
| SIM-CoT | LLaMA | reduced | 56.03% | ~100% | 100.00% |
| **CoLaR** | LLaMA | **near-zero** | 25.23% | random (~50%) | 98.20% |

**Two patterns emerge**:
1. **GSM8K is shortcut-resistant for some methods**: accuracy correlates with latent depth, especially for CoLaR (the strongest-supervision method), which collapses to near-random when latent depth = 0.
2. **ProsQA is universally shortcut-prone**: every weakly-supervised method maintains its full ProsQA accuracy at depth = 0. ProsQA's compositional logic patterns are simple enough that input attention alone suffices.

### Noise Injection Validation

To rule out the hypothesis that depth-0 inference simply uses early latent representations, the paper injects strong Gaussian noise ($\Sigma = \sigma^2 \mathbf{I}$, $\sigma = 100$) into the latent embedding **after** the latent reasoning loop completes but **before** the final answer is generated. The injected noise is roughly $4\times$ the magnitude of the actual latent embeddings.

### Table 1: Clean vs. Noise (reproduced)

| Model | Setting | Coconut GSM8K | Coconut ProsQA | CODI GSM8K | CODI ProsQA | CoLaR GSM8K | CoLaR ProsQA | SIM-CoT GSM8K | SIM-CoT ProsQA | Std CoT GSM8K | Std CoT ProsQA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LLaMA | clean | 36.97% | 99.40% | 55.57% | 100.00% | 25.23% | 98.20% | 56.03% | 100.00% | 61.74% | 90.60% |
| LLaMA | noise | **20.61%** | **99.40%** | **27.45%** | 99.60% | **3.32%** | 60.92% | 10.08% | 97.60% | **0.03%** | 0.40% |
| GPT-2 | clean | 34.09% | 97.80% | 43.59% | 80.80% | 18.44% | 77.52% | 42.23% | 80.60% | 43.56% | 81.00% |
| GPT-2 | noise | **3.79%** | **89.00%** | 8.87% | 80.80% | 2.84% | 46.80% | 7.05% | 75.60% | 0.08% | 0.00% |

Standard CoT collapses to ~0% under the same noise — an essential control showing the perturbation is destructive. Latent methods retain 9–28% accuracy on GSM8K and 47–99% on ProsQA, **proving** they bypass their own latent representations.

### Attention-Based Diagnosis

Cui et al. visualize the top-10 attention weights from each output token during final-answer generation, excluding the universal "attention sink" token. The findings:

- **Coconut on ProsQA**: top-10 attended tokens for every output token come **entirely from the input question**, never from latent reasoning tokens. The latent state is bypassed.
- **Coconut on GSM8K**: top-10 attention shifts to latent tokens when generating final numerical answers (e.g., the answer token "18"), confirming that GSM8K does engage latent reasoning more.

This is the most direct mechanistic evidence yet that **shortcut behavior is task-specific**: it dominates when input patterns suffice for the answer, and recedes when they don't.
