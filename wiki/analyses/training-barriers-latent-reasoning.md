---
type: analysis
title: "Training Barriers for Latent Reasoning"
created: "2026-04-08"
updated: "2026-04-08"
tags: [synthesis, training, latent-reasoning, barriers]
---

# Training Barriers for Latent Reasoning

Two orthogonal training-time barriers bound the latent reasoning design space from both sides. This analysis tracks the wiki-specific synthesis: which papers have hit each barrier, what mitigations have been tried, and what the boundaries imply for the field. For the textbook definition of the underlying phenomenon — what catastrophic forgetting is and why neural networks forget — see [[catastrophic-forgetting]].

The two barriers are:

1. **Catastrophic forgetting** — fine-tuning a model for latent reasoning destroys its pre-existing instruction-tuned capabilities ([[softcot-efficient-reasoning|SoftCoT]] is the empirical centerpiece).
2. **The supervision–exploration trade-off** — training latent states *strongly* enough to prevent shortcut behavior simultaneously destroys the multi-candidate capacity that gives latent reasoning its theoretical advantage ([[latent-reasoning-supervision-analysis|Cui et al. 2026]] is the empirical centerpiece).

Together they explain why the field's most promising methods cluster at architectural extremes (frozen-backbone designs, training-free communication methods), and why no method has yet escaped both barriers simultaneously.

## Quantitative Evidence from SoftCoT

![[training-barriers-latent-reasoning/quantitative-evidence-from-softcot]]

## The Regime Boundary Problem

![[training-barriers-latent-reasoning/the-regime-boundary-problem]]

## Why It Happens: Detailed Mechanism Analysis

![[training-barriers-latent-reasoning/why-it-happens-detailed-mechanism-analysis]]

## Solutions in this Wiki

![[training-barriers-latent-reasoning/solutions-in-this-wiki]]

## The Second Barrier: The Supervision–Exploration Trade-Off

![[training-barriers-latent-reasoning/the-second-barrier-the-supervisionexploration-trade-off]]

## Inference-Time Methods: Avoiding the Problem Entirely

![[training-barriers-latent-reasoning/inference-time-methods-avoiding-the-problem-entirely]]

## Implications for the Field

![[training-barriers-latent-reasoning/implications-for-the-field]]

## Open Questions

![[training-barriers-latent-reasoning/open-questions]]
