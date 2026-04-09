---
type: concept
title: "Activation Communication"
created: "2026-04-06"
updated: "2026-04-08"
tags: [core-concept, latent-communication]
---

# Activation Communication

Approaches where LLM agents share **hidden-state activations** or intermediate representations directly, rather than text or output embeddings. Five papers in this collection address activation-level communication, each with a distinct approach:

| Paper | What's shared | How | Cross-model? |
|-------|--------------|-----|-------------|
| [[activation-communication-harvard\|AC]] | Single last-token activation at one layer | Replace/sum/mean | Yes (cross-family) |
| [[interlat-latent-space-agents\|Interlat]] | Full sequence of last-layer hidden states | Learned communication adapter | Yes (Qwen→LLaMA) |
| [[latentmas-collaboration\|LatentMAS]] | Full layer-wise KV caches (including latent thoughts) | Direct concatenation with alignment matrix | Same model only |
| [[state-delta-trajectory\|SDE]] | Inter-token hidden state **deltas** | Additive injection at selected layers | Same model only |
| [[agent-primitives-building-blocks\|Agent Primitives]] | KV caches structured via Review/Voting/Planning primitives | Concatenation with RoPE re-encoding | Same model only |

## What Are Activations?

![[activation-communication/what-are-activations]]

## Why Share Activations?

![[activation-communication/why-share-activations]]

## Five Approaches to Activation Communication

![[activation-communication/five-approaches-to-activation-communication]]

## The Information Concentration Problem

![[activation-communication/the-information-concentration-problem]]

## Cross-Model Compatibility

![[activation-communication/cross-model-compatibility]]

## Structured vs. Unstructured Activation Sharing

![[activation-communication/structured-vs-unstructured-activation-sharing]]

## Connection to Latent-Space Reasoning

![[activation-communication/connection-to-latent-space-reasoning]]

## Maps of Content

![[activation-communication/maps-of-content]]

## Open Questions

![[activation-communication/open-questions]]
