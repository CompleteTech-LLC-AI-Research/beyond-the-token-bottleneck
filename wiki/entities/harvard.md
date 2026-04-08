---
type: entity
title: "Harvard University"
created: "2026-04-06"
updated: "2026-04-06"
aliases: [Harvard University, Harvard]
tags: [organization, university]
---

# Harvard University

Contributor to both latent communication and [[latent-space-reasoning|latent reasoning]] research, with work spanning activation-level communication and implicit chain-of-thought.

## Contribution Timeline

![[harvard/timeline]]

## Research Themes

Harvard's contributions bridge the reasoning and communication threads:

- **[[icot-internalize-cot|iCoT]]**: Developed the progressive CoT token removal curriculum that became the foundation for [[coconut-reasoning-latent-space|Coconut]]. Key insight: models can internalize explicit reasoning steps into hidden-state computation if the transition is gradual (with optimizer resets between stages).

- **Activation Communication**: Demonstrated that a **single activation replacement** at one layer (~26/32) outperforms full natural language debate on 48/57 MMLU topics — at less than ¼ the compute. The breakthrough finding was **zero-shot cross-family compatibility** (LLaMA ↔ Qwen ↔ Gemma), validating the [[platonic-representation-hypothesis|Platonic Representation Hypothesis]] empirically.

## Collaboration Network

Harvard's collaborations span different research communities:
- **iCoT**: Joint with Ai2 (Allen Institute for AI), University of Waterloo, and University of Washington. Yuntian Deng is the connective figure. Yejin Choi (UW/Stanford, also in [[princeton-uiuc-stanford|Princeton/UIUC/Stanford]]'s [[latentmas-collaboration|LatentMAS]]) is a co-author.
- **AC**: Internal collaboration at the Kempner Institute for the Study of Natural and Artificial Intelligence at Harvard.
- **Yilun Du connection**: Yilun Du, first author of the foundational [[multiagent-debate-du-et-al|multiagent debate paper]] (originally [[mit|MIT]]/Google Brain), is now at Harvard, creating a direct institutional link to the origin of the debate paradigm.

### Cross-Entity Collaboration Summary

| Partner Entity | Paper(s) | Collaboration Nature |
|---|---|---|
| [[mit\|MIT]] | Intellectual lineage | Yilun Du (multiagent debate founder) moved from MIT to Harvard |
| [[princeton-uiuc-stanford\|Stanford/UW]] | [[icot-internalize-cot\|iCoT]] | Yejin Choi co-authors iCoT and LatentMAS, linking the reasoning→communication lineage |

### Indirect Connections

- **[[fair-meta|FAIR/Meta AI]]**: iCoT's progressive CoT removal directly inspired Coconut. Harvard's curriculum approach is the conceptual ancestor of FAIR's latent reasoning program.
- **[[tsinghua|Tsinghua]]**: [[state-delta-trajectory|SDE]] refines AC's approach for same-model settings by using deltas instead of raw states. The two methods represent complementary design points (cross-model raw states vs same-model deltas).
- **[[kth|KTH]]**: AC and [[kvcomm-kth-selective|KVComm]] independently find intermediate layers (~20-26) most informative, validating each other's layer selection findings from different angles.

## Strategic Position

Harvard's AC result is the strongest empirical evidence for cross-model representation convergence. The choice of layer ~26 as optimal aligns with [[linearity-relation-decoding|Hernandez et al.'s]] finding of "enriched entity representations" at mid-to-upper layers — a connection that strengthens both results.

## Research Trajectory

Harvard's two papers trace a progression from intra-model reasoning internalization to inter-model communication:

1. **May 2024 — Reasoning internalization**: iCoT demonstrates that explicit CoT can be progressively compressed into hidden-state computation, establishing the curriculum that Coconut builds upon.
2. **Jan 2025 — Cross-model communication**: AC shows that single-layer activation transfer outperforms full NL debate, with the remarkable zero-shot cross-family finding validating the Platonic Representation Hypothesis.

The trajectory points toward **combining internalized reasoning with [[activation-communication|activation communication]]** — agents that reason in latent space (iCoT/Coconut-style) and then communicate the results via activation transfer (AC-style). Harvard has the intellectual lineage in both threads.

## Key Researchers

![[harvard/researchers]]
