---
type: index
title: "Wiki Index"
created: "2026-04-06"
updated: "2026-04-08"
---


# Wiki Index

A catalog of all pages in the wiki, organized by research theme. Updated on every ingest.

```
wiki/
├── mocs/*.md                # Maps of Content — guided reading paths (9)
├── overview-*.md            # High-level narrative syntheses (1)
├── sources/
│   ├── reasoning/           # Intra-agent latent reasoning (7)
│   ├── communication/
│   │   ├── embeddings/      # Output-layer communication (2)
│   │   ├── activations/     # Hidden-state communication (2)
│   │   ├── kv-cache/        # KV-cache communication (4)
│   │   └── structured/      # Disentangled/structured (1)
│   ├── unified/             # Reasoning + communication combined (3)
│   └── meta/                # Frameworks, scaling, foundations (8)
├── concepts/                # 10 concept pages
├── entities/                # 13 entity pages + 26 partials (timeline.md, researchers.md per entity)
└── analyses/                # 7 analysis pages
```

---

## Start Here

- **[[overview-state-of-field]]** — Narrative synthesis of the entire research landscape. Read this first.

## Theme Maps

Navigate by research theme. Each MOC provides a guided reading path with narrative context.

- **[[latent-reasoning]]** — How individual models reason in continuous space. 6 source papers, the catastrophic forgetting barrier, and three proposed solutions.
- **[[latent-communication]]** — How agents exchange information through continuous representations. Organized by depth: embeddings → activations → KV-cache → structured thoughts. 9 source papers.
  - **[[communication-depth-spectrum]]** — The full 10-level depth spectrum walked through level by level.
- **[[unified-frameworks]]** — Systems combining latent reasoning + communication. LatentMAS, Vision Wormhole, Agent Primitives, plus scaling and applied work. 5 source papers.
- **[[theoretical-foundations]]** — Mathematical and theoretical underpinnings: complexity theory (depth bottleneck), representation geometry (linear structure, isometric maps), and convergence hypotheses (Platonic Representation). 6 foundational papers.
- **[[practical-systems]]** — The engineering lens: when to use which method, scaling considerations, deployment trade-offs, and a decision guide for method selection.
- **[[cross-architecture]]** — The cross-architecture compatibility problem: why deeper communication demands tighter coupling, and how the field is bending that curve from shared tokenizers to universal shared spaces.
- **[[compression-information-theory]]** — Compression and information-theoretic bounds on latent communication: bandwidth–accuracy trade-offs, rate–distortion limits, and learned compression.
- **[[safety-interpretability]]** — Safety, interpretability, and auditability of latent systems: monitoring opaque continuous channels, alignment guarantees, and trust frameworks.

---

## Concepts

- [[latent-space-reasoning]] — 8-method comparison spectrum, superposition, training challenges
- [[continuous-vs-discrete-representation]] — 4× to 2600× information density advantage
- [[catastrophic-forgetting]] — Why latent reasoning breaks instruction-tuned models
- [[embedding-space-communication]] — 10-level depth-compatibility spectrum
- [[activation-communication]] — 5-paper synthesis, cross-model compatibility
- [[kv-cache-communication]] — 4 design dimensions with 4 papers
- [[thought-structure]] — Shared/private decomposition, agreement routing
- [[latent-variable-model]] — Identifiability theory for ThoughtComm
- [[multiagent-debate]] — Debate paradigm, scaling principles, architecture comparison
- [[temperature-diversity]] — Anchor/explorer dynamics in embedding-space debate

---

## Entities

- [[fair-meta]] — FAIR at Meta: Coconut, ThoughtComm, LLaMA ecosystem enabler. Collaborates with CMU, MBZUAI, UC San Diego, UC Berkeley.
- [[cmu]] — CMU: Pause Tokens, ThoughtComm, Vision Wormhole. Bridges FAIR, MBZUAI, Purdue, Google Research.
- [[tsinghua]] — Tsinghua: C2C, SDE. Industry collaborations with Infinigence AI, Shanghai AI Lab.
- [[kth]] — KTH: KVComm. Internal systems/networking collaboration.
- [[google-deepmind]] — Google DeepMind: KV Cache Alignment, Scaling paper. Collaborates with Google Research, MIT.
- [[google-research]] — Google Research: Pause Tokens, Scaling paper, Thinking States. Collaborates with CMU, DeepMind, MIT.
- [[harvard]] — Harvard: AC, iCoT. Hosts Yilun Du (debate founder, ex-MIT). Intellectual lineage to FAIR (Coconut).
- [[princeton-uiuc-stanford]] — Princeton/UIUC/Stanford: LatentMAS, Agent Primitives. Yejin Choi bridges to Harvard/iCoT.
- [[purdue]] — Purdue: Vision Wormhole. Collaborates with CMU, Contextual AI, Georgia Tech.
- [[mit]] — MIT: Multiagent Debate, Platonic Rep Hypothesis, Scaling paper. Origin point for debate paradigm; collaborates with Google.
- [[mbzuai]] — MBZUAI: ThoughtComm (co-lead with CMU, FAIR). Gulf-Western research bridge.
- [[amazon]] — Amazon: Latent Reasoning Supervision Analysis. First systematic empirical critique of latent reasoning's BFS hypothesis; identifies the supervision–exploration trade-off.
- [[monash]] — Monash University: Inference-time Scaling for Continuous Reasoning. First implementation of PRM/ORM reranking for COCONUT; diagnoses geometric homogeneity as the root cause of the Pass@N / Maj@N gap.

---

## Analyses

- [[paper-timeline]] — Chronological publication order, citation chains, and field evolution
- [[method-comparison]] — Unified comparison table across all methods and key dimensions
- [[open-questions]] — All open questions across the wiki, grouped by theme
- [[frontier-research-directions]] — 8 paradigm-shift directions synthesized from all papers
- [[contradictions]] — 9 tensions and contradictions between papers, with resolution status
- [[latentcompress-collaboration-strategy]] — LatentCompress collaboration mapping and strategy
- [[benchmark-overlap]] — Benchmark overlap across papers: coverage matrix, focused comparisons, blind spots

---

## Meta

- [[log]] — Chronological record of all wiki activity
