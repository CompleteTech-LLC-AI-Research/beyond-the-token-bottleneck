### Multiplication (GPT-2 Small, 117M parameters)

| Task | No CoT | iCoT-KD | **iCoT-SI** | Explicit CoT | Speed ratio |
|------|--------|---------|-------------|-------------|-------------|
| 4×4 | 0.29 | 0.97 | **1.00** | 1.00 | 1.02× |
| 5×5 | 0.01 | 0.10 | **0.95** | 1.00 | 1.00× |
| 7×7 | 0.00 | — | **0.95** | 1.00 | 1.00× |
| 9×9 | 0.00 | — | **0.99** | 1.00 | 1.00× |

- Standard No-CoT cannot solve beyond 4×4 multiplication
- iCoT-SI solves **9×9 multiplication** with 99% accuracy and **11× faster** than explicit CoT (speed 1.00 vs 0.09, because explicit CoT for 9×9 requires 246 intermediate tokens)
- iCoT-KD (the prior knowledge distillation approach) caps at 10% on 5×5 — iCoT-SI is dramatically more effective

### GSM8K (All Model Sizes)

| Model | No CoT | iCoT-KD | **iCoT-SI** | Explicit CoT |
|-------|--------|---------|-------------|-------------|
| GPT-2 Small (117M) | 0.13 | 0.20 | **0.30** | 0.41 |
| GPT-2 Medium (355M) | 0.17 | 0.22 | **0.35** | 0.44 |
| Phi-3 (3.8B) | 0.28 | — | **0.31** | 0.74 |
| Mistral 7B | 0.38 | — | **0.51** | 0.68 |
| GPT-4 (5-shot, no FT) | — | — | — | 0.91 (CoT) / 0.44 (no CoT) |

- Mistral 7B with iCoT-SI: **51% on GSM8K without any visible reasoning** — surpasses GPT-4's 44% no-CoT baseline
- The accuracy gap vs explicit CoT narrows with model size: 11pp gap at 117M → 17pp at 7B (though Phi-3 shows a wider gap, suggesting architecture matters)

### CoT Token Statistics

| Task | Median CoT Tokens | Train Size |
|------|-------------------|------------|
| 4×4 mult | 46 | 808K |
| 5×5 mult | 74 | 808K |
| 7×7 mult | 148 | 808K |
| 9×9 mult | 246 | 808K |
| GSM8K | 19-24 | 378K |

The 246-token CoT for 9×9 multiplication being fully internalized into zero visible tokens is the paper's most impressive result.
