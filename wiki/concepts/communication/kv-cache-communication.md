---
type: concept
title: "KV-Cache Communication"
created: "2026-04-06"
updated: "2026-04-08"
tags: [core-concept, latent-communication]
---

# KV-Cache Communication

A family of approaches to inter-agent communication where models share **key-value cache entries** from their transformer layers rather than generated text or embeddings. This allows agents to directly inject internal representations into each other's attention mechanism — the receiver attends to the sender's cached context as if it had processed that context itself.

Four papers in this collection address complementary dimensions of KV-cache communication:

| Paper | Dimension | Approach |
|-------|-----------|----------|
| [[kvcomm-kth-selective\|KVComm]] | **What to share** | Layer selection via attention importance + Gaussian prior |
| [[cache-to-cache-semantic-communication\|C2C]] | **How to fuse across architectures** | Learned pairwise neural fuser with gating |
| [[kv-cache-alignment-shared-space\|KV Cache Alignment]] | **How to scale to many models** | Global shared KV-cache space with per-model adapters |
| [[kvcomm-duke-online-reuse\|KVCOMM-online]] | **How to make it efficient** | Anchor-based offset estimation for cache reuse |

## Background: What the KV-Cache Is

![[kv-cache-communication/background-what-the-kv-cache-is]]

## Why KV Pairs Over Other Representations

![[kv-cache-communication/why-kv-pairs-over-other-representations]]

## The Three Design Dimensions

![[kv-cache-communication/the-three-design-dimensions]]

## Combined Picture: The KV-Cache Communication Stack

![[kv-cache-communication/combined-picture-the-kv-cache-communication-stack]]

## Relation to the Communication Spectrum

![[kv-cache-communication/relation-to-the-communication-spectrum]]

## Maps of Content

![[kv-cache-communication/maps-of-content]]

## Open Questions

![[kv-cache-communication/open-questions]]

## Emergent Theme: Latent Space Mediation as Regularization

![[kv-cache-communication/emergent-theme-latent-space-mediation-as-regularization]]
