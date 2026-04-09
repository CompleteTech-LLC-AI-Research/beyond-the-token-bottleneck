All experiments on GSM8K dataset, 2-agent debate with 3 rounds. Approximate accuracies read from the bar chart (Figure 3):

| Model | Single Answer | NLD | CIPHER |
|---|---|---|---|
| WizardMath-70B | ~73% | ~75% | ~76% |
| LLaMA2-70B | ~60% | ~65% | ~66% |
| LLaMA2-Chat-70B | ~52% | ~55% | ~57% |
| LLaMA-65B | ~51% | ~52% | ~53% |
| Falcon-40B-Instruct | ~18% | ~20% | ~22% |
| MPT-30B | ~12% | ~15% | ~17% |

CIPHER provides an additional 0.5–3.5% boost over NLD across all models. Even weaker models (Falcon-40B, MPT-30B) benefit from CIPHER despite their low baseline accuracy.

**Optimal temperatures for different models on GSM8K (Table 5):**

| Model | Single Answer | NLD | CIPHER |
|---|---|---|---|
| LLaMA2-70B | 0.15 | (0.10, 0.20) | (0.22, 0.60) |
| LLaMA2-Chat-70B | 0.15 | (0.20, 0.40) | (0.25, 0.65) |
| LLaMA-65B | 0.20 | (0.10, 0.20) | (0.25, 0.85) |
| Falcon-40B-Instruct | 0.40 | (0.20, 0.40) | (0.25, 0.65) |
| MPT-30B | 0.45 | (0.35, 0.62) | (0.23, 0.64) |
| WizardMath-70B | 0.00 | (0.15, 0.35) | (0.26, 0.69) |
