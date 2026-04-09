---
type: moc
category: thread
title: "Latent Reasoning"
created: "2026-04-06"
updated: "2026-04-08"
tags: [moc, latent-reasoning]
---

# Latent Reasoning

How individual models reason in continuous hidden-state space rather than discrete tokens. The core insight: standard chain-of-thought forces models to "think out loud," imposing a discretization bottleneck, a fluency tax, and an irreversible commitment to each generated token. Latent reasoning removes all three constraints.

## Reading Path

Start with the theoretical motivation, then the breakthrough result, then the refinements:

1. **[[continuous-vs-discrete-representation]]** — Why continuous representations carry 4× to 2600× more information than discrete tokens. The theoretical foundation everything else builds on.
2. **[[cot-expressivity-theory]]** — Feng et al.'s proof that CoT increases effective transformer depth ($\text{TC}^0 \to \text{NC}^1$). Establishes *why* extra reasoning steps help at all.
3. **[[coconut-reasoning-latent-space]]** — The breakthrough: Coconut's hidden-state feedback loop, emergent BFS via superposition, and the proof that continuous reasoning enables capabilities discrete tokens cannot.
4. **[[superposition-coconut-theory]]** — Rigorous theoretical backing: continuous CoT implements parallel BFS in $D$ steps vs $O(n^2)$ for discrete.
5. **[[icot-internalize-cot]]** — iCoT: the direct precursor to Coconut. Progressive CoT token removal curriculum.
6. **[[pause-tokens]]** — Minimal baseline: pause tokens as existence proof that transformers use non-linguistic computation.
7. **[[latent-reasoning-supervision-analysis]]** — The empirical reckoning: Cui et al. (2026) test the BFS hypothesis directly. Capacity is real (Pass@100 advantage of 20+ points), but the iterative process exhibits *implicit pruning*, not BFS expansion. Identifies the supervision–exploration trade-off as a second training-time barrier complementary to catastrophic forgetting. Read this **after** Coconut and Superposition Theory to understand what is and isn't true about parallel BFS in latent space.
8. **[[inference-time-scaling-continuous-reasoning]]** — The decoding-side companion: Wang et al. (2025) implement the most natural fix to Cui et al.'s Pass@N gap — train a PRM/ORM via MATH-Shepherd MC annotation on dropout-sampled COCONUT trajectories — and find it recovers only 19.8% of the available headroom. The diagnosis is geometric: continuous-thought representations exhibit IsoScore$\star \approx 0.013$ and produce statistically indistinguishable values across compactness, curvature, local smoothness, and straightness for correct vs. incorrect thoughts. Read this **immediately after** Cui et al.: together, they form a complete decomposition of the Pass@N gap and reframe the field's central problem from "scale up Coconut" or "build a better reranker" to "build training-time inductive biases that produce geometrically discriminable continuous thoughts."

## The Catastrophic Forgetting Barrier

Coconut's curriculum training damages instruction-tuned models (LLaMA-3.1-8B drops 79.61% → 76.12% on GSM8K). This is the central unsolved tension — see **[[catastrophic-forgetting]]**. Three solutions have been proposed:

| Solution | Paper | Approach | Trade-off |
|----------|-------|----------|-----------|
| Frozen backbone | [[softcot-efficient-reasoning\|SoftCoT]] | External assistant generates soft thoughts; only a projection layer is trained | Requires two models at inference |
| Teacher forcing | [[thinking-states-latent-reasoning\|Thinking States]] | NL thoughts → compressed states with deep-to-shallow recurrence | Needs teacher-generated thoughts for training |
| Training-free | [[latentmas-collaboration\|LatentMAS]] | Ridge regression alignment, no fine-tuning at all | Requires homogeneous architecture |

## Core Concept Page

**[[latent-space-reasoning]]** — The full synthesis: 8-method comparison spectrum, superposition property, height-confidence principle, training challenges, and open questions.

## Key Entities

- **[[fair-meta]]** — Coconut, the founding result
- **[[google-research]]** — Thinking States, pushing toward production viability

## Connections

- Latent reasoning *within* agents combines with latent communication *between* agents in the [[unified-frameworks|unified frameworks]]
- The same [[continuous-vs-discrete-representation]] bottleneck motivates both this line and [[latent-communication|latent communication]]
- [[frontier-research-directions]] identifies superposition at frontier scale as the #1 open bet
