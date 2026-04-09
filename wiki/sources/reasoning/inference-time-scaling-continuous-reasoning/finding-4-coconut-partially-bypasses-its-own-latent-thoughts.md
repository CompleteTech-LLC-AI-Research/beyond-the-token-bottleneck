### Perturbation Test (Table 6)

To probe whether continuous thoughts contain semantic information at all, Wang et al. inject Gaussian noise into the latent thoughts at varying ratios — $\text{ratio} \times \text{noise} + (1-\text{ratio}) \times \text{thought}$ — and measure Pass@5 on GSM8K:

| Noise Ratio | # Unique answers | Pass@5 | # Correct (avg) | % Majority answer unchanged |
|---|---|---|---|---|
| 0.0 | 1.86 | 39.20 | 1.55 | 100.00 |
| 0.2 | 1.92 | 38.67 | 1.50 | 76.35 |
| 0.4 | 2.22 | 34.80 | 1.24 | 67.32 |
| 0.6 | 2.56 | 20.32 | 0.55 | 44.73 |
| 0.8 | 2.62 | 15.62 | 0.37 | 49.43 |
| 1.0 | 2.49 | **12.59** | 0.32 | 53.83 |

**Two observations**:

1. **Robustness at low noise** (ratio 0.0–0.2): Pass@5 barely moves (39.20 → 38.67), 76% of majority answers unchanged. Consistent with the high-anisotropy finding — most dimensions are inert, so noise mostly perturbs irrelevant subspaces.
2. **Non-zero accuracy at full corruption** (ratio = 1.0): Pass@5 stays at **12.59%** even when latent thoughts are *replaced entirely* with Gaussian noise. For a non-trivial fraction of problems, COCONUT can produce correct answers without using its own continuous thoughts at all.

This is closely related to [[latent-reasoning-supervision-analysis|Cui et al.]]'s shortcut analysis (which used similar noise-injection tests on Coconut/CODI/SIM-CoT/CoLaR and found 3.79% accuracy at $\sigma=100$ on GPT-2 GSM8K). Wang et al.'s 12.59% Pass@5 number is *higher* than Cui et al.'s 3.79% greedy accuracy because Pass@5 is a softer metric (it counts a problem as correct if any of 5 stochastic decodings is right). The two papers triangulate the same phenomenon from different angles.
