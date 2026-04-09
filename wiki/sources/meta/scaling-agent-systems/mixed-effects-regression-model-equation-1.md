Twenty parameters, all predictors standardized (mu = 0, sigma = 1). Log transformations applied to right-skewed variables (Delta%: 0-515%; t_tools: 4-16; n: 1-4; alpha: 1.0-17.2).

$$S = \beta_0 + \beta_1(I - \bar{I}) + \beta_2(I - \bar{I})^2 + \beta_3 \log(1+t) + \beta_4 \log(1+n) + \beta_5 \log(1+\Delta\%) + \beta_6 \eta + \beta_7 \mu + \beta_8 \rho + \beta_9 \log(1+\alpha) + \beta_{10} S_{\text{SA}} + \beta_{11}(S_{\text{SA}} \cdot \log(1+n)) + \beta_{12}(\eta \cdot t) + \beta_{13}(\Delta\% \cdot t) + \beta_{14}(\alpha \cdot t) + \beta_{15}(\rho \cdot n) + \beta_{16}(\alpha \cdot S_{\text{SA}}) + \beta_{17}(\mu \cdot I) + \beta_{18}(I \cdot \log(1+t)) + \beta_{19}(\eta \cdot \alpha) + \epsilon$$

### Independent Variables (4 categories)
1. **Base model capability**: Intelligence Index (I), centered at I_bar = 56.9
2. **System configuration**: agent count (n)
3. **Task properties**: tool count (t), single-agent baseline (S_SA)
4. **Coordination metrics**: efficiency (eta), overhead (Delta%), error amplification (alpha), message density (mu), redundancy (rho)

### Full Coefficient Table (Table 4)

| Predictor | beta_hat | 95% CI | p-value | Interpretation |
|-----------|----------|--------|---------|----------------|
| **Main Effects** | | | | |
| Intercept (beta_0) | 0.453 | [0.433, 0.472] | <0.001 | Baseline performance |
| Intelligence (I - I_bar) | 0.171 | [0.070, 0.272] | 0.001 | Linear capability effect |
| Intelligence^2 | 0.007 | [-0.013, 0.026] | 0.509 | Quadratic: NOT significant |
| log(1+t) tools | 0.411 | [0.291, 0.531] | <0.001 | Tool diversity benefit |
| log(1+n) agents | 0.052 | [-0.061, 0.166] | 0.367 | Agent count: NOT significant |
| S_SA baseline | 0.315 | [0.185, 0.445] | <0.001 | Task difficulty proxy |
| **Coordination** | | | | |
| log(1+Delta%) overhead | 0.034 | [0.011, 0.057] | 0.005 | Direct overhead cost |
| mu message density | -0.057 | [-0.110, -0.003] | 0.039 | Communication intensity |
| rho redundancy | -0.007 | [-0.052, 0.037] | 0.748 | NOT significant alone |
| eta efficiency | -0.043 | [-0.078, -0.007] | 0.021 | Coordination efficiency |
| log(1+alpha) error amp | -0.022 | [-0.077, 0.034] | 0.441 | NOT significant alone |
| **Critical Interactions** | | | | |
| S_SA * log(1+n) | **-0.404** | [-0.557, -0.252] | <0.001 | **Baseline paradox** |
| eta * t | **-0.267** | [-0.355, -0.178] | <0.001 | **Efficiency-tools trade-off** |
| Delta% * t | **-0.162** | [-0.241, -0.083] | <0.001 | **Overhead scales with complexity** |
| alpha * t | -0.019 | [-0.075, 0.037] | 0.506 | Not significant |
| rho * n | 0.047 | [0.019, 0.075] | 0.001 | Redundancy benefit with scale |
| alpha * S_SA | -0.022 | [-0.075, 0.030] | 0.404 | Not significant |
| mu * I | -0.065 | [-0.146, 0.015] | 0.114 | Not significant |
| I * log(1+t) | -0.011 | [-0.057, 0.034] | 0.626 | Not significant |
| eta * alpha | -0.069 | [-0.138, 0.000] | 0.053 | Borderline |

### Three Dominant Effects

1. **Baseline paradox** (beta = -0.404, p < 0.001): When S_SA > ~45%, coordination yields diminishing or negative returns. Decision boundary: S_SA = -beta_4/beta_17 = 0.052/0.404 = 0.129 standardized units, ~0.45 raw.
2. **Efficiency-tools trade-off** (beta = -0.267, p < 0.001): Tool-heavy tasks suffer disproportionately. For 16-tool tasks, penalty = -0.267 * eta * t, yielding -1.99 for SAS vs. -0.32 for MAS — single-agent paradoxically more effective.
3. **Overhead-complexity interaction** (beta = -0.162, p < 0.001): Critical threshold Delta%_max = (0.034/0.162) * log(1+Delta%) ~ 150% for t=16, ruling out all MAS except possibly decentralized.
