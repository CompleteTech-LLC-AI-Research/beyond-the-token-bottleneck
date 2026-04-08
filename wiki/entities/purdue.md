---
type: entity
title: "Purdue University"
created: "2026-04-06"
updated: "2026-04-06"
aliases: [Purdue University, Purdue]
tags: [organization, university]
---

# Purdue University

Lead institution on the [[vision-wormhole-heterogeneous|Vision Wormhole]] — the most creative architectural solution to cross-architecture latent communication in this collection.

## Contribution Timeline

| Date | Paper | Role | Key Result |
|------|-------|------|------------|
| Feb 2026 | [[vision-wormhole-heterogeneous\|Vision Wormhole]] | Lead (multi-institution) (with CMU, Contextual AI, Georgia Tech) | VLM visual pathway as universal heterogeneous channel; +6.3pp vs TextMAS |

## Research Themes

Purdue's contribution is a conceptual breakthrough: rather than trying to align different models' internal representations (the approach taken by [[cache-to-cache-semantic-communication|C2C]], [[kv-cache-alignment-shared-space|KV Alignment]]), **repurpose an existing cross-architecture interface** — the visual input pathway that all VLMs share.

- **Repurposing the cross-architecture interface**: Rather than aligning different models' internal representations, Vision Wormhole uses the visual input pathway that all VLMs share as a universal communication channel. The insight is architectural rather than algorithmic — as VLMs become the default frontier architecture, every model already has the "communication port" built in.

- **Key technical innovations**:
  - **NormMatch operator**: Aligns heterogeneous activation distributions using mean/std/RMS normalization
  - **Perceiver-style resampler**: Compresses latent rollouts to fixed-size representations
  - **Affine alignment**: Requires only ~90 anchor texts for weakly supervised cross-model alignment
  - **Self-distillation training**: MSE + KL + RMS loss combination

## Collaboration Network

Vision Wormhole is a multi-institution effort with strong connections to other wiki entities:

| Partner Entity | Paper | Collaboration Nature |
|---|---|---|
| [[cmu\|CMU]] | [[vision-wormhole-heterogeneous\|Vision Wormhole]] | Matt Fredrikson contributes security/robustness expertise |
| Contextual AI | [[vision-wormhole-heterogeneous\|Vision Wormhole]] | Industry partner; contextual AI systems |
| Georgia Tech | [[vision-wormhole-heterogeneous\|Vision Wormhole]] | Additional academic collaborator |

### Indirect Connections

- **[[tsinghua|Tsinghua]]** and **[[google-deepmind|Google DeepMind]]**: All three tackle cross-architecture communication but via fundamentally different mechanisms. C2C uses learned fusers, KV Alignment uses a shared interlingua, Vision Wormhole repurposes the visual pathway. These represent three competing solutions to the same problem.
- **[[fair-meta|FAIR/Meta AI]]**: Vision Wormhole tests on LLaMA-based VLMs, making FAIR an indirect contributor through its open-weight model ecosystem.

## Strategic Position

Purdue is positioned to pursue [[frontier-research-directions|frontier direction #5]] (vision pathway as universal continuous interface). The natural extensions: using the visual pathway for intra-model [[latent-space-reasoning|latent reasoning]] (avoiding the off-manifold problem), multi-modal latent reasoning, and expanding the 256 visual token bandwidth budget.

## Research Trajectory

Purdue has a single paper in this collection (Feb 2026), but its architectural insight — repurposing existing cross-modal interfaces for model-to-model communication — opens several natural extensions:

1. **Intra-model latent reasoning via visual pathway**: Using the visual pathway for [[coconut-reasoning-latent-space|Coconut]]-style hidden-state feedback, avoiding the off-manifold problem that plagues direct hidden-state injection into text-only models.
2. **Multi-modal latent reasoning**: Combining visual reasoning traces with textual latent thoughts through the same communication port.
3. **Bandwidth scaling**: Expanding beyond the current 256 visual token budget to increase communication capacity.
4. **Security analysis**: With [[cmu|CMU]]'s Matt Fredrikson involved, adversarial robustness of the visual communication channel is a likely next direction.

## Key Researchers

- **Xiaoze Liu**: First author; designed the wormhole architecture. The core architect of the visual pathway communication concept.
- **Ruowang Zhang**: Co-author (Contextual AI affiliation).
- **Matt Fredrikson**: Co-author ([[cmu|CMU]] affiliation); his security/robustness expertise suggests adversarial analysis of the communication channel may follow.
- **Jing Gao**: Senior advisor; data mining and ML.
- **Xiaoqian Wang**: Co-advisor.
