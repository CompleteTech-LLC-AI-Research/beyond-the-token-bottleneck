Identifiability of latent variable models has been studied across several decades, with progressively weaker assumptions yielding progressively weaker (but more broadly applicable) guarantees:

| Approach | Assumptions | What's recovered | Recovery strength | Key references |
|----------|-------------|-----------------|-------------------|----------------|
| **Linear ICA** | Linear $f$, independent non-Gaussian sources | All sources | Up to permutation + scaling | Comon, 1994 |
| **Nonlinear ICA with auxiliary vars** | Access to auxiliary signals (time indices, class labels, domain info) | All sources | Up to elementwise transform | Hyvärinen & Morioka, 2016; Khemakhem et al., 2020 |
| **VAE with factorial prior** | Specific decoder architecture, factorial Gaussian prior | None in general | Not identifiable without additional constraints | Locatello et al., 2019 |
| **Causal representation learning** | Interventional data or temporal structure | Causal factors | Up to elementwise transform per mechanism | Brehmer et al., 2022; Liang et al., 2023 |
| **Structural constraints** | Specific function classes (polynomial, monotone) or sparse dependency graphs | All sources | Up to permutation | Zheng et al., 2022 |
| **ThoughtComm** | **Invertibility + $\ell_0$ Jacobian sparsity only** | **Pairwise shared/private thoughts + structure** | **Up to permutation** | **[[thought-communication-multiagent\|Zheng et al., 2025]]** |

[[thought-communication-multiagent|ThoughtComm]]'s contribution to this landscape: by targeting a **weaker goal** (pairwise shared/private recovery instead of full global recovery of all latents), it achieves identifiability under **much weaker assumptions** than prior work. No auxiliary variables, no parametric constraints on $f$, no independence assumptions — only invertibility and sparsity.
