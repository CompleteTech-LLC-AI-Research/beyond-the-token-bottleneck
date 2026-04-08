---
type: entity
title: "KTH Royal Institute of Technology"
created: "2026-04-06"
updated: "2026-04-06"
aliases: [KTH Royal Institute of Technology, KTH]
tags: [organization, university]
---

# KTH Royal Institute of Technology

Swedish research university contributing foundational work on efficient multi-agent communication via selective KV-cache sharing.

## Contribution Timeline

![[kth/timeline]]

## Research Themes

KTH's contribution focuses on **efficiency in latent communication**:
- **[[kvcomm-kth-selective|KVComm]]** established two key findings: (1) KV-cache sharing outperforms both NL debate and embedding communication ([[cipher-multiagent-debate-embeddings|CIPHER]]) on multi-hop reasoning tasks, and (2) only ~30% of layers need to be shared, with attention importance-based selection identifying the most informative layers. This was the first systematic comparison showing KV > embeddings > text for inter-LLM communication.
- The **Gaussian prior** favoring upper layers in KVComm's selection mechanism aligns with [[linearity-relation-decoding|Hernandez et al.'s]] finding of enriched entity representations at mid-to-upper layers.

## Collaboration Network

KVComm is a KTH-internal collaboration between the networking/systems group (Chiesa, Kostić) and ML researchers (Shi), bringing a **systems perspective** to latent communication — framing it as a bandwidth optimization problem with attention-based "importance sampling" of which layers to transmit.

### Indirect Connections to Other Entities

KTH has no direct co-authorship with other wiki entities, but KVComm is deeply methodologically connected:
- **[[tsinghua|Tsinghua]]**: KVComm and C2C form a complementary pair — KVComm answers "what to share" (layer selection), C2C answers "how to fuse" (cross-architecture projection). They address the same [[kv-cache-communication]] problem from opposite design dimensions and cite each other.
- **[[google-deepmind|Google DeepMind]]**: KVComm's finding that selective sharing sometimes exceeds full-context performance (the "Skyline paradox") is independently replicated by KV Cache Alignment's self-improvement effect, suggesting latent-space mediation acts as beneficial regularization.
- **[[harvard|Harvard]]**: Both AC and KVComm find intermediate layers (~20-26) most informative for communication. KVComm's Gaussian prior favoring upper layers aligns with AC's layer-26 optimum and [[linearity-relation-decoding|Hernandez et al.'s]] enriched entity representation theory.

## Strategic Position

KVComm's training-free approach makes it immediately deployable. The natural extension is combining KVComm's layer selection with [[cache-to-cache-semantic-communication|C2C]]'s cross-architecture fusion — using importance scores to select layers, then applying learned fusers only to the selected subset. This would reduce C2C's computational overhead proportionally.

KVComm's finding that sometimes selective sharing exceeds full-context performance (the Skyline) connects to [[kv-cache-alignment-shared-space|KV Alignment]]'s self-improvement effect, suggesting that selective filtering acts as a beneficial regularizer.

## Research Trajectory

KTH has a single paper in this collection (Oct 2025), but its findings are foundational for the KV-cache communication subfield. The natural next steps for KTH would be:

1. **Combining layer selection with cross-architecture fusion**: Apply KVComm's importance scores to select layers, then use [[tsinghua|Tsinghua]]'s C2C fusers only on the selected subset — reducing C2C's computational overhead proportionally.
2. **Investigating the Skyline paradox**: KVComm's finding that selective sharing can exceed full-context performance deserves a dedicated theoretical analysis. The regularization explanation connects to [[google-deepmind|Google DeepMind]]'s self-improvement effect.
3. **Dynamic layer selection**: Current calibration uses a single sample; extending to input-dependent layer selection could further improve efficiency.

## Key Researchers

![[kth/researchers]]
