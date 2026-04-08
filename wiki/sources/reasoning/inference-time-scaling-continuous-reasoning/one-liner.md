---
type: source-partial
parent: inference-time-scaling-continuous-reasoning
partial: one-liner
created: "2026-04-08"
updated: "2026-04-08"
---

**Wang et al. (2025)** ask whether the inference-time scaling toolkit (sampling, PRM, ORM) transplants into continuous reasoning. **Sampling works** — dropout in the latent loop pushes COCONUT Pass@N from 31.08% to 44.43%. **Reranking fails** — PRM/ORM trained via MATH-Shepherd MC annotation recovers only 19.8% of the available headroom. The diagnosis is **geometric**: continuous-thought representations are statistically indistinguishable for correct vs. incorrect thoughts (IsoScore$\star \approx 0.013$), reframing the field's central problem as "produce geometrically discriminable latent thoughts."
