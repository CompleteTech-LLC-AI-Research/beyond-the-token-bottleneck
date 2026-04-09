---
type: concept
title: "Catastrophic Forgetting"
created: "2026-04-06"
updated: "2026-04-09"
tags: [challenge, training, latent-reasoning]
---

# Catastrophic Forgetting

**Catastrophic forgetting** (also called catastrophic interference) is the phenomenon where fine-tuning a neural network on new data or objectives **destroys** previously learned capabilities. First identified by McCloskey & Cohen (1989) in connectionist models and extensively studied in the continual learning literature, the problem takes on particular urgency in the context of modern LLMs: instruction-tuned models represent millions of dollars of training investment across a complex pipeline (pretraining, supervised fine-tuning, RLHF/DPO), and any parameter modification risks degrading this carefully calibrated capability stack.

In the context of this wiki, catastrophic forgetting is the **critical barrier** preventing [[latent-space-reasoning]] methods from working on modern instruction-tuned models, and a key motivator for frozen-backbone architectures. It is one of two orthogonal training-time barriers that bound the latent reasoning design space — the second being the supervision-exploration trade-off identified by [[latent-reasoning-supervision-analysis|Cui et al. (2026)]]. Both are analyzed together in [[training-barriers-latent-reasoning]].

## Why Neural Networks Forget

![[catastrophic-forgetting/why-neural-networks-forget]]

## The Stability-Plasticity Dilemma

![[catastrophic-forgetting/the-stability-plasticity-dilemma]]

## Empirical Evidence: Latent Reasoning Breaks Instruction-Tuned Models

![[catastrophic-forgetting/empirical-evidence-latent-reasoning-breaks-instruction-tuned-models]]

## The Regime Boundary: Base vs. Instruction-Tuned Models

![[catastrophic-forgetting/the-regime-boundary-base-vs-instruction-tuned-models]]

## Classical Mitigation Strategies

![[catastrophic-forgetting/classical-mitigation-strategies]]

## Mitigation Strategies Applied to Latent Reasoning

![[catastrophic-forgetting/mitigation-strategies-applied-to-latent-reasoning]]

## The Second Barrier: The Supervision-Exploration Trade-Off

![[catastrophic-forgetting/the-second-barrier-the-supervision-exploration-trade-off]]

## The Alignment Tax

![[catastrophic-forgetting/the-alignment-tax]]

## Toward Modular Solutions

![[catastrophic-forgetting/toward-modular-solutions]]

## Open Questions

![[catastrophic-forgetting/open-questions]]

## Maps of Content

![[catastrophic-forgetting/maps-of-content]]

## See also

![[catastrophic-forgetting/see-also]]
