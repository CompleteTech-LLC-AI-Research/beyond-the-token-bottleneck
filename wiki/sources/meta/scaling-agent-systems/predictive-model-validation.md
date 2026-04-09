| Metric | Value |
|--------|-------|
| R^2_train | 0.613 |
| R^2_CV (5-fold) | **0.524** (+/- 0.033 SD) |
| MAE | 0.089 (+/- 0.011) |
| RMSE | 0.112 (+/- 0.014) |
| Train-CV gap | 0.076 |
| Correct architecture prediction | **87%** of held-out configs |
| Residual SE | 0.118 |
| Shapiro-Wilk p | 0.412 |
| Breusch-Pagan p | 0.298 |

Model comparison (R^2_CV): Intelligence only = 0.283, + tools/agents = 0.430, + architecture labels = 0.431, + coordination metrics = **0.524** (20% improvement over categorical labels).

Regularized alternatives: Lasso retained 16/20 predictors (R^2_CV = 0.506), Ridge (R^2_CV = 0.509). Full model retained for interpretability.

### GPT-5.2 Out-of-Sample Validation (released after study)

| Metric | Value | Status |
|--------|-------|--------|
| MAE | 0.071 | < 0.10 acceptable |
| MAPE | 15.8% | acceptable |
| Normalized MAE | 0.045 | |
| Qualitative findings validated | **4 of 5** | one partial |
| Kendall's tau (ranking) | 0.200 | weak |

GPT-5.2 Intelligence Index = 75. The one partially validated finding: architecture convergence at high capability means architecture distinctions narrow at frontier capability levels.
