---
type: entity
title: "CMU (Carnegie Mellon University)"
created: "2026-04-06"
updated: "2026-04-06"
aliases: [Carnegie Mellon University, Carnegie Mellon]
tags: [organization, university]
---

# CMU (Carnegie Mellon University)

A major research university contributing to multi-agent communication, causal representation learning, and cross-architecture latent communication.

## Contribution Timeline

| Date | Paper | Role | Key Result |
|------|-------|------|------------|
| Oct 2023 | [[pause-tokens\|Pause Tokens]] | Co-lead (with Google Research) | Existence proof: transformers use non-linguistic computation |
| Oct 2025 | [[thought-communication-multiagent\|ThoughtComm]] | Lead | Identifiable thought decomposition; MATH 93% |
| Feb 2026 | [[vision-wormhole-heterogeneous\|Vision Wormhole]] | Co-lead (with Purdue) | VLM visual pathway as universal heterogeneous channel |

## Research Themes

CMU's contributions span two distinct threads:
- **Identifiability and structure**: [[thought-communication-multiagent|ThoughtComm]] applies CMU's strength in causal representation learning to the multi-agent communication problem, providing the field's only formal guarantees that recovered latent factors correspond to true generative factors. This gives [[thought-structure|structured communication]] a theoretical foundation that pure engineering approaches lack.
- **Cross-architecture communication**: [[vision-wormhole-heterogeneous|Vision Wormhole]] (Matt Fredrikson's involvement) takes an architectural approach to the heterogeneity problem — repurposing VLM visual pathways as universal continuous channels.

## Collaboration Network

CMU bridges industry and academia more broadly than any other entity in this wiki:
- **ThoughtComm**: Joint with [[fair-meta|FAIR/Meta AI]] and [[mbzuai|MBZUAI]], combining CMU's identifiability theory with Meta's model ecosystem and MBZUAI's causal representation expertise
- **Vision Wormhole**: Joint with [[purdue|Purdue]], Contextual AI, and Georgia Tech, bringing security/robustness expertise (Fredrikson) to the communication design
- **Pause Tokens**: Sachin Goyal (CMU) is first author on the foundational pause tokens paper with [[google-research|Google Research]], establishing the existence proof for non-linguistic computation

### Cross-Entity Collaboration Summary

| Partner Entity | Paper(s) | Collaboration Nature |
|---|---|---|
| [[fair-meta\|FAIR/Meta AI]] | [[thought-communication-multiagent\|ThoughtComm]] | FAIR provides model ecosystem; CMU provides identifiability theory |
| [[mbzuai\|MBZUAI]] | [[thought-communication-multiagent\|ThoughtComm]] | Joint causal representation expertise |
| [[purdue\|Purdue]] | [[vision-wormhole-heterogeneous\|Vision Wormhole]] | Purdue leads architecture; CMU contributes security/robustness |
| [[google-research\|Google Research]] | [[pause-tokens\|Pause Tokens]] | Sachin Goyal bridges CMU and Google |

## Strategic Position

CMU is uniquely positioned to pursue **[[frontier-research-directions|frontier direction #2]]** — disentangling superposed reasoning paths. ThoughtComm already disentangles latent communication factors; applying the same identifiability framework to [[coconut-reasoning-latent-space|Coconut]]'s superposed continuous thoughts would connect the reasoning and communication threads. Kun Zhang's causal representation group has the theoretical depth to tackle this.

## Research Trajectory

CMU's contributions span three distinct phases and two research threads:

1. **Oct 2023 — Existence proof** (with [[google-research|Google Research]]): Sachin Goyal co-leads Pause Tokens, demonstrating that transformers benefit from non-linguistic computation. This is the minimal baseline for the entire [[latent-space-reasoning|latent reasoning]] field.
2. **Oct 2025 — Structured communication**: ThoughtComm applies CMU's causal representation expertise to multi-agent systems, producing the field's only identifiability guarantees.
3. **Feb 2026 — Cross-architecture communication**: Vision Wormhole pivots to the heterogeneity problem, repurposing VLM visual pathways as universal communication channels.

The trajectory shows CMU moving from foundational theory toward increasingly applied problems. The natural next step is combining ThoughtComm's identifiability framework with Vision Wormhole's cross-architecture capability — structured, disentangled communication across heterogeneous agents.

## Key Researchers

- **Kun Zhang**: Senior advisor on ThoughtComm; expert in causal discovery and identifiability. His theoretical framework (Theorems 1-3 in ThoughtComm) is the foundation for [[latent-variable-model|identifiability guarantees]] in this field. The central figure in CMU's structured communication program.
- **Yujia Zheng**: First author on ThoughtComm (joint CMU/Meta AI). Bridges the CMU–FAIR collaboration.
- **Matt Fredrikson**: Co-author on Vision Wormhole; security/robustness expertise. His involvement signals that adversarial robustness of latent communication channels is a growing concern.
- **Sachin Goyal**: First author on Pause Tokens (CMU affiliation, joint with [[google-research|Google Research]]). Established the existence proof for non-linguistic computation that underpins the entire latent reasoning field.
