---
type: entity
title: "Monash University"
created: "2026-04-08"
updated: "2026-04-08"
aliases: [Monash, Monash University, Monash NLP]
tags: [organization, university, academic-lab]
---

# Monash University

Australian academic research group contributing the **first empirical study of inference-time scaling for continuous-space reasoning**. Like [[amazon|Amazon]]'s Cui et al., Monash's contribution is **diagnostic, not constructive**: rather than proposing a new latent reasoning method, it operationalizes the most natural fix to a known problem (build a reward model and rerank), shows that the fix doesn't work, and explains why with a battery of geometric and trajectory-dynamics measurements.

## Contribution Timeline

| Date | Paper | Role | Key Result |
|------|-------|------|------------|
| Oct 2025 | [[inference-time-scaling-continuous-reasoning\|Wang et al. (Inference-time Scaling for Continuous Reasoning)]] | Sole institution | Demonstrates dropout-based sampling unlocks Pass@32 of 44.43% on COCONUT (GPT-2/GSM8K) but PRM/ORM reranking recovers only 19.8% of the headroom; diagnoses geometric homogeneity (IsoScore$\star \approx 0.013$) as the root cause |

## Research Themes

Monash's single contribution to this collection sits at the **inference-time / diagnostic** end of latent reasoning research:

- **Dropout-based latent sampling**: A surgically minimal intervention — enable dropout *only* during the iterative continuous-thought generation, not during answer decoding — that produces diverse latent reasoning trajectories without modifying training. This is the cleanest published method for diversifying COCONUT inference, and it generalizes to any latent reasoning method that uses dropout in training.
- **Continuous-thought reward modeling**: First implementation of MATH-Shepherd-style Monte Carlo annotation adapted to continuous-thought vectors, training both PRM (hard + soft labels) and ORM with COCONUT itself as the backbone (necessary because continuous-thought representations are model-specific and only the originating model can interpret them).
- **Geometric diagnosis of discrimination failure**: Application of IsoScore$\star$ (Rudman & Eickhoff, 2024), Hoyer sparsity, and four trajectory-dynamics metrics (compactness, curvature, local smoothness, straightness) to continuous-thought representations. The headline finding — that correct and incorrect thoughts are **statistically indistinguishable by every metric tested** — is the strongest evidence to date that COCONUT's representation space lacks the inductive biases needed for inference-time scaling.
- **Perturbation-based shortcut detection**: Independent confirmation of [[latent-reasoning-supervision-analysis|Cui et al.]]'s shortcut finding via Gaussian noise injection at varying ratios; Pass@5 stays at 12.59% even at full noise (ratio 1.0).

## Collaboration Network

Wang et al. is a **single-institution paper** — all four authors are at Monash University's Faculty of Information Technology. Notable, given that most other papers in this wiki are multi-institution collaborations.

### Indirect Connections to Other Entities

- **[[fair-meta|FAIR at Meta]]**: Wang et al. uses [[coconut-reasoning-latent-space|COCONUT]] as its sole experimental backbone, faithfully reproducing the original training recipe (6 epochs initial stage, 3 epochs subsequent, $c=2$, $T=3 \times c$). The paper's null result on PRM/ORM reranking constrains the credibility of any claim that COCONUT's latent reasoning advantage can be exploited at inference time without further training innovation.
- **[[amazon|Amazon (via Cui et al.)]]**: Wang et al. and Cui et al. are direct conceptual companions, published four months apart and apparently without mutual awareness (Wang et al. October 2025; Cui et al. February 2026 — neither cites the other). Together they form the most complete decomposition to date of the Pass@N / Maj@N gap in latent reasoning. The wiki is the first place the two are explicitly synthesized.
- **CMU / UC Berkeley / UC San Diego (via Zhu et al.)**: Wang et al.'s extreme-anisotropy finding (IsoScore$\star \approx 0.013$) sits in tension with the theoretical prediction in [[superposition-coconut-theory|Zhu et al.]] that continuous thoughts encode uniform mixtures over reachable vertices (a near-isotropic state within a small subspace). Resolving the tension requires either (a) acknowledging that gradient training does not find the theoretical optimum, or (b) measuring isotropy *within* the active subspace rather than across the full hidden space.

### The Single-Institution Pattern

Most diagnostic / analytical work in this collection comes from large industrial labs ([[amazon|Amazon]], [[google-deepmind|Google DeepMind]], [[google-research|Google Research]]). Wang et al. is unusual in being a small academic group producing a methodologically dense critical paper without industrial affiliation. The closest analogue in the collection is [[harvard|Harvard]]'s work on AC and iCoT (also academic, also methodologically dense), but Harvard's contributions are primarily constructive whereas Monash's is purely diagnostic.

## Strategic Position

Wang et al.'s findings define **two open problems** that Monash is well-positioned to address in follow-up work:

1. **Training-time inductive biases for continuous-thought discrimination**: The paper proposes isotropy regularization, trajectory diversity objectives, and contrastive losses but tests none of them. A natural follow-up — fine-tune COCONUT briefly with an IsoScore$\star$ penalty, then re-run the PRM training to test whether geometric separability is now learnable — is a small, well-defined experiment that the same group could execute on the same infrastructure.
2. **Cross-method geometric analysis**: The paper tests only COCONUT. Repeating the IsoScore$\star$ / trajectory-dynamics measurements on CODI, SIM-CoT, and CoLaR (the other methods analyzed by [[latent-reasoning-supervision-analysis|Cui et al.]]) would establish whether stronger supervision produces more discriminable representations, directly testing whether the supervision–exploration trade-off has a corresponding geometric signature.

Wang et al.'s findings also directly inform the [[frontier-research-directions|frontier directions analysis]]: direction #1 (superposition reasoning at frontier scale) now has a third blocker (geometric homogeneity) layered on top of catastrophic forgetting (SoftCoT) and implicit pruning (Cui et al.), and the resolution must address all three simultaneously.

## Research Trajectory

Monash is a new entity in this collection. Natural next steps for the same group:

1. **Scale the geometric analysis to LLaMA-1B / Qwen-7B**: The current analysis is GPT-2 only. Whether extreme anisotropy persists at larger scales determines whether Wang et al.'s finding is a property of GPT-2 specifically or of latent reasoning generally.
2. **Test isotropy regularization end-to-end**: The paper's most concrete proposed mitigation. A single regularization term added to COCONUT's training loss, followed by retraining and re-running the PRM evaluation, would convert a diagnostic paper into a constructive one.
3. **Apply the geometric framework to inter-agent latent communication**: The IsoScore$\star$ / trajectory analysis could be applied to [[activation-communication-harvard|AC]], [[state-delta-trajectory|SDE]], or [[interlat-latent-space-agents|Interlat]] to test whether their shared continuous representations exhibit the same homogeneity. This would extend the framework from latent *reasoning* to latent *communication*.
4. **Build a learned latent-space verifier**: Wang et al.'s reward model emits a scalar score per step. A verifier that operates *in* the latent space — e.g., a transformer that ingests a trajectory and outputs a corrected one — bypasses the discrimination problem entirely.

## Key Researchers

- **Minghan Wang** (first author, Monash): Designed the dropout-sampling protocol and the PRM/ORM training pipeline. Also the first author on follow-up work in continuous-space reasoning expected from this group.
- **Thuy-Trang Vu** (Monash): Co-author on the experimental design and the geometric-properties analysis.
- **Ehsan Shareghi** (Monash): Senior co-author. Research interests in NLP and language model evaluation.
- **Gholamreza Haffari** (Monash): Senior advisor. Long-standing research interest in machine translation and structured prediction, which informs the trajectory-dynamics methodology.

## Why This Entity Matters

Monash's contribution is rare in three ways. First, it is **purely diagnostic** — the paper makes no claim to a new method, only to a new measurement framework and a null result. Second, it is the **first paper to attempt a latent-aware inference-time scaling toolkit** for COCONUT, completing a natural research arc that the rest of the field had not yet taken. Third, the geometric measurement framework (IsoScore$\star$ + trajectory dynamics + perturbation tests) is a **reusable methodological contribution** that any future paper proposing a latent-space reasoning method should adopt as a sanity check before claiming inference-time scaling potential.

The lack of a Monash–Amazon collaboration on the joint Pass@N / Maj@N problem (as of April 2026) is itself notable: the two groups have produced the most complete decomposition of the gap, in opposite hemispheres, without coordination. The natural follow-up — a joint paper combining Cui et al.'s training-time interventions with Wang et al.'s inference-time measurement framework — is open for any group to execute.
