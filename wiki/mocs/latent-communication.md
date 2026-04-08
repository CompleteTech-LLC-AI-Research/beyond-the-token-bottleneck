---
type: overview
title: "Latent Communication"
created: "2026-04-06"
updated: "2026-04-08"
tags: [moc, latent-communication]
---

# Latent Communication

How multiple LLM agents exchange information through continuous representations rather than text. Natural language is optimized for human comprehension, not inter-model information transfer — every sampled token discards the model's full distributional belief. This research line explores progressively deeper channels that preserve more of that information.

This MOC is the **thematic hub** for latent communication: concepts, entities, and theoretical foundations. For the paper-by-paper walkthrough by depth, see **[[communication-depth-spectrum]]**.

## Cross-Cutting Concepts

- **[[continuous-vs-discrete-representation]]** — The theoretical foundation: why continuous > discrete for inter-model transfer.
- **[[embedding-space-communication]]** — Output-layer synthesis: information bottleneck theory, convex hull constraint.
- **[[activation-communication]]** — Hidden-state synthesis: 5-paper comparison, cross-model compatibility spectrum, information concentration problem.
- **[[kv-cache-communication]]** — KV-cache synthesis: 4 design dimensions, combined stack vision.
- **[[thought-structure]]** — Shared/private decomposition, agreement routing.
- **[[multiagent-debate]]** — The debate paradigm these communication methods plug into.
- **[[temperature-diversity]]** — Anchor/explorer dynamics and diversity's role in embedding-space debate.

## Key Entities

- **[[tsinghua]]** — C2C, SDE
- **[[kth]]** — KVComm
- **[[google-deepmind]]** — KV Cache Alignment
- **[[cmu]]** — ThoughtComm
- **[[fair-meta]]** — CIPHER ecosystem (LLaMA family enables shared-tokenizer communication)
- **[[harvard]]** — AC (activation communication)

## Theoretical Foundations

- **[[platonic-representation-hypothesis]]** — Why cross-family activation communication works: models converge to shared statistical structure.
- **[[relative-representations-zero-shot]]** — Zero-shot model stitching via cosine-similarity anchors.
- **[[linearity-relation-decoding]]** — Linear relational embeddings; explains enriched entity representations at mid-layers.
- **[[latent-variable-model]]** — Identifiability theory underpinning ThoughtComm.

## Connections

- Combines with latent reasoning in the [[unified-frameworks|unified frameworks]]
- [[frontier-research-directions]] identifies delta-based reasoning templates and learned compression as top open directions
- [[latentcompress-collaboration-strategy]] maps the practical collaboration landscape
