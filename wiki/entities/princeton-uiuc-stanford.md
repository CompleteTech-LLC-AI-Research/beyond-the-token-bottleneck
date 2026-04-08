---
type: entity
title: "Princeton / UIUC / Stanford"
created: "2026-04-06"
updated: "2026-04-06"
aliases: [Princeton, UIUC, Stanford, Princeton University, University of Illinois, Stanford University]
tags: [organization, university, multi-institution]
---

# Princeton / UIUC / Stanford

A multi-institutional collaboration behind two of the most significant unified frameworks in this collection.

## Contribution Timeline

| Date | Paper | Role | Key Result |
|------|-------|------|------------|
| Nov 2025 | [[latentmas-collaboration\|LatentMAS]] | Lead (multi-institution) | First unified latent reasoning + communication; training-free; GSM8K 95.2% |
| Feb 2026 | [[agent-primitives-building-blocks\|Agent Primitives]] | Lead (multi-institution) | Composable latent operators; beats 10 MAS baselines |

## Research Themes

This collaboration produces the field's most ambitious **unified frameworks**:

- **[[latentmas-collaboration|LatentMAS]]**: The first system combining [[latent-space-reasoning|latent reasoning]] (hidden-state feedback, [[coconut-reasoning-latent-space|Coconut]]-style) with latent communication (KV-cache transfer between agents). Training-free via ridge regression alignment. Achieved 95.2% on GSM8K (+11.5pp vs single agent) and 4–4.3× speedup over text-based MAS. Demonstrated 471.4× theoretical compression advantage. **Limitation**: requires homogeneous architecture.

- **[[agent-primitives-building-blocks|Agent Primitives]]**: Introduced composable operators (Review, Voting, Planning) that structure how agents share KV-cache representations. Key contribution: the **Organizer** system that uses in-context learning to select and compose primitives from a knowledge pool of 45 entries across 5 frameworks. RoPE re-encoding critical for stability. Outperforms 10 existing MAS methods across all benchmarks including at 70B scale.

## Collaboration Network

The author teams overlap significantly within the consortium and connect outward to other wiki entities:
- **LatentMAS**: Princeton (Mengdi Wang, James Zou), UIUC (Hanghang Tong, Jingrui He), Stanford (Yejin Choi), with additional contributors from Peking University (Ling Yang)
- **Agent Primitives**: UIUC (Haohan Wang), with contributions from other institutions

This represents a concentration of multi-agent systems expertise across three top CS departments, with complementary strengths: Princeton's optimization/RL, UIUC's graph/network theory, Stanford's NLP.

### Cross-Entity Collaboration Summary

| Partner Entity | Connection | Nature |
|---|---|---|
| [[harvard\|Harvard]] | Yejin Choi co-authors both LatentMAS and [[icot-internalize-cot\|iCoT]] | Bridges reasoning internalization and unified frameworks |
| [[fair-meta\|FAIR/Meta AI]] | LatentMAS builds on Coconut's hidden-state feedback | Methodological dependency; LatentMAS uses Coconut-style latent thoughts |
| [[kth\|KTH]] / [[tsinghua\|Tsinghua]] | LatentMAS uses KV-cache transfer between agents | Methodological alignment with KVComm/C2C's KV communication approach |

**Yejin Choi** is the most notable cross-entity figure: she co-advises LatentMAS (Stanford) and co-authors iCoT (Harvard/UW), directly linking the reasoning internalization lineage (iCoT → Coconut) to the unified framework lineage (LatentMAS). This makes her the intellectual bridge between the reasoning and communication threads.

## Strategic Position

This collaboration is positioned to pursue [[frontier-research-directions|frontier direction #7]] (scaling laws for latent MAS) — LatentMAS and Agent Primitives together provide the broadest empirical foundation for understanding when and how latent multi-agent systems outperform text-based alternatives. The [[scaling-agent-systems|Scaling paper]]'s framework could be directly extended with their methods as communication channels.

## Research Trajectory

This collaboration produces increasingly sophisticated unified frameworks:

1. **Nov 2025 — First unified system**: LatentMAS combines Coconut-style latent reasoning with [[kv-cache-communication|KV-cache communication]] in a training-free framework. Achieves dramatic results (GSM8K 95.2%) but requires homogeneous architecture.
2. **Feb 2026 — Composable primitives**: Agent Primitives introduces modular, reusable operators that scale to 70B and beat 10 existing MAS baselines. The Organizer system adds automatic primitive composition.

The trajectory moves from monolithic system to composable architecture. The next step is likely **heterogeneous Agent Primitives** — combining [[vision-wormhole-heterogeneous|Vision Wormhole]]-style cross-architecture channels with composable Review/Voting/Planning primitives, enabling primitives to work across different model families.

## Key Researchers

- **Jiaru Zou**: First author on LatentMAS. Designed the training-free unified pipeline.
- **Mengdi Wang**: Senior advisor (Princeton); optimization and RL. Her optimization expertise drives the ridge regression alignment approach in LatentMAS.
- **James Zou**: Senior advisor (Stanford); statistical ML. Appears in both the multi-agent and medical AI literature.
- **Hanghang Tong, Jingrui He**: Senior advisors (UIUC); graph learning. Their graph-theoretic perspective explains LatentMAS's topology-aware design (sequential, hierarchical).
- **Yejin Choi**: Co-advisor (Stanford/UW); NLP. The key cross-entity figure — co-authors LatentMAS and [[icot-internalize-cot|iCoT]] ([[harvard|Harvard]]), bridging reasoning internalization and unified frameworks.
- **Haibo Jin**: First author on Agent Primitives. Designed the composable primitive abstraction.
- **Haohan Wang**: Senior advisor on Agent Primitives (UIUC). Leads the UIUC contribution to the primitives framework.
