---
type: entity
title: "FAIR at Meta"
created: "2026-04-06"
updated: "2026-04-06"
aliases: [FAIR, Meta AI, Facebook AI Research]
tags: [organization, research-lab]
---

# FAIR at Meta

**Fundamental AI Research (FAIR)** is Meta's AI research lab. The most prolific contributor to the latent-space research tracked in this wiki, with foundational work in both [[latent-space-reasoning|latent reasoning]] and structured communication.

## Contribution Timeline

| Date | Paper | Role | Key Result |
|------|-------|------|------------|
| Dec 2024 | [[coconut-reasoning-latent-space\|Coconut]] | Lead | Emergent BFS via superposition; 97% ProsQA |
| May 2025 | [[superposition-coconut-theory\|Superposition Theory]] | Co-lead (with UC San Diego) | Rigorous proof: continuous CoT = parallel BFS in D steps |
| Oct 2025 | [[thought-communication-multiagent\|ThoughtComm]] | Co-lead (with CMU, MBZUAI) | Identifiable latent thought decomposition; MATH 93% |

## Research Themes

FAIR's contributions cluster around two themes:
- **Latent reasoning**: [[coconut-reasoning-latent-space|Coconut]] pioneered the hidden-state feedback loop; the Superposition Theory paper provided rigorous mathematical foundations. Together they establish that continuous reasoning enables qualitatively different computation (parallel BFS) impossible with discrete tokens.
- **Structured communication**: [[thought-communication-multiagent|ThoughtComm]] brings identifiability guarantees from causal representation learning to multi-agent latent communication, adding *structure* to what other approaches treat as opaque vector exchange.

## Collaboration Network

FAIR's most impactful work involves cross-institutional partnerships:
- **Coconut + Superposition Theory**: Joint with UC San Diego (Shibo Hao, Zhiting Hu) and UC Berkeley (Hanlin Zhu, Jiantao Jiao, Stuart Russell) — combining FAIR's scaling resources with West Coast theoretical depth
- **ThoughtComm**: Joint with [[cmu|CMU]] (Kun Zhang's causal representation group) and [[mbzuai|MBZUAI]] (Yaqi Xie, Mingze Gao) — bringing identifiability theory to multi-agent communication
- **Ecosystem enabler**: FAIR's open-weight LLaMA models are the test platform for [[harvard|Harvard]]'s AC, [[tsinghua|Tsinghua]]'s SDE, [[kth|KTH]]'s KVComm, and [[princeton-uiuc-stanford|Princeton/UIUC/Stanford]]'s LatentMAS. This makes FAIR an indirect collaborator with nearly every entity in the wiki.

### Cross-Entity Collaboration Summary

| Partner Entity | Paper(s) | Collaboration Nature |
|---|---|---|
| [[cmu\|CMU]] | [[thought-communication-multiagent\|ThoughtComm]] | CMU provides identifiability theory; FAIR provides model ecosystem |
| [[mbzuai\|MBZUAI]] | [[thought-communication-multiagent\|ThoughtComm]] | MBZUAI contributes causal representation expertise |
| UC San Diego | [[coconut-reasoning-latent-space\|Coconut]], [[superposition-coconut-theory\|Superposition Theory]] | Joint theoretical + empirical latent reasoning |
| UC Berkeley | [[superposition-coconut-theory\|Superposition Theory]] | Formal complexity theory contributions |

## Ecosystem Impact

FAIR's influence extends well beyond their direct papers. The **LLaMA model family** (open-weight) provides the shared-tokenizer ecosystem that makes [[embedding-space-communication]] practical. [[cipher-multiagent-debate-embeddings|CIPHER]], [[activation-communication-harvard|AC]], [[state-delta-trajectory|SDE]], [[kvcomm-selective-kv-sharing|KVComm]], and [[latentmas-collaboration|LatentMAS]] all use LLaMA variants as primary test models. Without open weights, activation and KV-cache sharing would be restricted to API providers.

## Strategic Position

FAIR is uniquely positioned to pursue [[frontier-research-directions|frontier direction #1]] (superposition reasoning at frontier scale) — they authored both Coconut and the theoretical proof, and control the LLaMA model family that would be the natural test platform. The key barrier — [[catastrophic-forgetting]] — directly affects their instruction-tuned LLaMA models.

FAIR could also connect Coconut's superposition with ThoughtComm's identifiability to pursue **frontier direction #2** (disentangling superposed reasoning paths), since both techniques originate from their lab and collaborators.

## Research Trajectory

FAIR's publication arc traces a clear progression from empirical discovery to theoretical foundations to structured application:

1. **Dec 2024 — Empirical discovery**: Coconut demonstrates that continuous reasoning produces emergent BFS via superposition, a qualitative surprise.
2. **May 2025 — Theoretical formalization**: The Superposition Theory paper (with UC Berkeley/UCSD) proves Coconut's BFS is not accidental but a provable consequence of continuous-space computation (D steps vs $O(n^2)$ for discrete CoT).
3. **Oct 2025 — Structured communication**: ThoughtComm (with CMU/MBZUAI) applies identifiability to multi-agent latent exchange, adding formal guarantees to what other approaches treat as opaque.

The trajectory points toward **controlled superposition** — combining Coconut's parallel reasoning with ThoughtComm's ability to disentangle latent factors. FAIR is the only entity with direct authorship on both the superposition mechanism and the identifiability framework needed to interpret it.

## Key Researchers

- **Yuandong Tian**: Senior researcher on Coconut and Superposition Theory; central figure linking empirical and theoretical latent reasoning. Appears in 2 of 3 FAIR papers — the connective hub for FAIR's latent reasoning program.
- **Shibo Hao**: First author on Coconut, co-author on Superposition Theory (joint UC San Diego). Bridges the empirical–theoretical gap across both papers.
- **Sainbayar Sukhbaatar**: Co-author on Coconut; deep experience with recurrent reasoning architectures.
- **Jason Weston**: Co-author on Coconut; long track record in open-domain dialogue and memory-augmented architectures.
- **Yujia Zheng**: First author on ThoughtComm (joint CMU/Meta AI affiliation). Leads the identifiability side.
- **Zhuokai Zhao**: Co-author on ThoughtComm (Meta AI affiliation)
- **Lizhu Zhang**: Co-author on ThoughtComm (Meta AI affiliation)
