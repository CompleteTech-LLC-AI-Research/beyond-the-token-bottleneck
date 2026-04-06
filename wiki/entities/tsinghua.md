---
type: entity
title: "Tsinghua University"
created: "2026-04-06"
updated: "2026-04-06"
aliases: [Tsinghua University, Tsinghua, THU]
tags: [organization, university]
---

# Tsinghua University

A leading Chinese research university. Primary contributor to cross-architecture KV-cache communication and hidden-state delta methods.

## Contribution Timeline

| Date | Paper | Role | Key Result |
|------|-------|------|------------|
| Jun 2025 | [[state-delta-trajectory\|SDE]] | Lead | Deltas outperform raw states; +7.3pp over CIPHER |
| Oct 2025 | [[cache-to-cache-semantic-communication\|C2C]] | Lead | First cross-architecture KV-cache fusion; 2.5× speedup |

## Research Themes

Tsinghua's work focuses on **practical inter-model communication**:
- **[[cache-to-cache-semantic-communication|C2C]]**: Solved the cross-architecture KV-cache communication problem with learned pairwise fusers. Demonstrated cross-family (Qwen→LLaMA), cross-generation, and cross-size (0.6B→14B) communication. The effective rank analysis showing fused caches are richer than either input model's cache is a key theoretical contribution.
- **[[state-delta-trajectory|SDE]]**: Discovered that hidden-state *deltas* (inter-token differences) are more transferable than raw states. This insight — that reasoning dynamics carry more information than reasoning states — has implications beyond communication, suggesting [[frontier-research-directions|frontier direction #4]] (delta-based reasoning templates).

## Collaboration Network

Tsinghua's collaboration pattern is primarily industry-oriented, with no direct co-authorship with other academic entities in this wiki:
- **C2C**: Joint with Infinigence AI (Tianyu Fu dual affiliation), CUHK, SJTU, and Shanghai AI Lab (Wanli Ouyang). This reflects a Chinese AI ecosystem collaboration pattern.
- **SDE**: Internal work within Tsinghua's THUIR group (Information Retrieval), led by Qingyao Ai.

### Indirect Connections to Other Entities

While Tsinghua has no direct co-authorship with other wiki entities, strong methodological connections exist:
- **[[kth|KTH]]**: [[kvcomm-selective-kv-sharing|KVComm]] and C2C both address KV-cache communication but from opposite design points (training-free layer selection vs learned cross-architecture fusion). The papers cite each other and form the complementary "what to share" vs "how to fuse" axes of [[kv-cache-communication]].
- **[[google-deepmind|Google DeepMind]]**: KV Cache Alignment directly addresses C2C's $O(N^2)$ scaling limitation with an $O(N)$ interlingua approach. C2C's richer per-pair fusion vs DeepMind's scalable shared space represents a quality-scalability trade-off.
- **[[harvard|Harvard]]**: SDE refines Harvard's AC approach for same-model settings by using deltas instead of raw states.

## Strategic Position

Tsinghua's C2C approach scales $O(N^2)$ (pairwise fusers), which [[kv-cache-alignment-shared-space|KV Alignment]] improves to $O(N)$. However, C2C's learned fusers achieve richer cross-architecture integration. A combination of C2C's fusion quality with KV Alignment's scaling architecture is a natural next step.

Tsinghua is also well positioned to expand SDE into a general theory of reasoning dynamics — their empirical finding that deltas outperform raw states is replicated across 3 models and 10 benchmarks, providing a strong foundation for the transferable reasoning templates direction.

## Research Trajectory

Tsinghua's two papers appear within 4 months of each other (Jun-Oct 2025) and cover complementary dimensions:

1. **Jun 2025 — Reasoning dynamics**: SDE discovers that hidden-state deltas are more transferable than raw states, establishing the "reasoning dynamics > reasoning states" principle.
2. **Oct 2025 — Cross-architecture KV fusion**: C2C solves the cross-architecture KV-cache communication problem with learned fusers and effective rank analysis.

The trajectory suggests Tsinghua is building toward a **unified cross-architecture communication system** that uses delta-based representations (from SDE) with learned fusers (from C2C). Combining SDE's insight that deltas strip context-specific noise with C2C's cross-architecture projection would address both the quality and compatibility dimensions simultaneously — a direction no other group has pursued.

## Key Researchers

- **Yu Wang**: Corresponding author on C2C; systems and architecture focus. The senior figure driving Tsinghua's communication systems program.
- **Tianyu Fu**: Co-first author on C2C (joint Tsinghua/Infinigence AI). Dual affiliation reflects the industry collaboration pattern.
- **Yichen Tang**: First author on SDE. Bridges information retrieval and multi-agent communication.
- **Qingyao Ai**: Senior advisor on SDE; information retrieval background. His THUIR group provides the evaluation methodology expertise.
- **Wanli Ouyang**: Co-author on C2C (Shanghai AI Lab). Senior figure connecting Shanghai AI Lab to Tsinghua's vision.
