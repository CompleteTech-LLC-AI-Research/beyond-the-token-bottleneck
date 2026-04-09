### Main Results

All experiments use standard transformers ($d = 256$, $H = 4$, various depths), trained with AdamW ($\beta_1 = 0.9$, $\beta_2 = 0.999$, lr $= 10^{-4}$, weight decay $= 0.01$), dropout 0.1, on 4 V100 GPUs for 100 epochs. Training data: 1M samples per task; test: 0.1M samples (no overlap).

| Task | Difficulty | CoT (3-layer) | Direct (3-layer) | Direct (4-layer) | Direct (5-layer) |
|------|-----------|--------------|-----------------|-----------------|-----------------|
| **Arithmetic** | 4 ops | ~100% | ~58% | ~60% | ~55% |
| **Arithmetic** | 5 ops | ~100% | ~52% | ~55% | ~50% |
| **Arithmetic** | 6 ops | ~100% | ~48% | ~50% | ~45% |
| **Equation** | 3 vars | ~100% | ~55% | ~60% | ~68% |
| **Equation** | 4 vars | ~100% | ~20% | ~30% | ~40% |
| **Equation** | 5 vars | ~100% | ~5% | ~10% | ~15% |
| **LIS** | len 50 | ~100% | ~55% | ~58% | ~60% |
| **ED** | len 12 | ~100% | ~50% | ~55% | ~58% |

3-layer transformers with CoT achieve **near-perfect accuracy** across all tasks and difficulty levels. Direct prediction consistently fails, especially as problem size grows. Notably, the 5-variable Equation task requires generating CoT sequences of ~500 tokens perfectly, yet the 3-layer model achieves this.

### Robustness to Data Quality

On the arithmetic task with 10 operators:

| Corruption Rate ($\gamma$) | 0 | 0.1 | 0.2 | 0.3 |
|----------------------------|------|------|------|------|
| **Accuracy** | 100.0% | 98.5% | 97.6% | 95.8% |

Where $\gamma = 0.1$ means 10% of intermediate steps are omitted and 10% of remaining steps have a single-token corruption. The model remains above **95% even with 30% corruption**, demonstrating remarkable robustness of CoT training to low-quality supervision.

### Length Extrapolation

A 3-layer model trained on arithmetic expressions with 1-15 operators was tested on longer expressions:

| # Operators | 15 (in-dist) | 16 | 17 | 18 |
|------------|-------------|-----|-----|-----|
| **Accuracy** | 99.9% | 97.6% | 82.4% | 45.5% |

The model generalizes well to 16 operators (2 beyond training) and degrades gracefully, suggesting it has learned algorithmic rules rather than memorizing input-output distributions.
