---
type: entity
title: "Google Research"
created: "2026-04-06"
updated: "2026-04-06"
aliases: [Google Research]
tags: [organization, research-lab]
---

# Google Research

Google's research division (distinct from [[google-deepmind|Google DeepMind]]). Contributor of the most production-oriented approach to [[latent-space-reasoning|latent reasoning]] in this collection.

## Contribution Timeline

| Date | Paper | Role | Key Result |
|------|-------|------|------------|
| Oct 2023 | [[pause-tokens\|Pause Tokens]] | Co-lead (with CMU) | Existence proof: transformers use non-linguistic computation |
| Dec 2025 | [[scaling-agent-systems\|Scaling Agent Systems]] | Co-lead (with DeepMind, MIT) | Quantitative scaling framework; task-contingent coordination |
| Feb 2026 | [[thinking-states-latent-reasoning\|Thinking States]] | Lead | Supervised latent reasoning; 2.66× speedup; identifies state ambiguity |

## Research Themes

Google Research's work focuses on **making latent reasoning practical**:

- **Pause Tokens** (2023): An early exploration showing transformers benefit from extra compute steps even without meaningful content. Demonstrated +19.5 EM on SQuAD with learnable pause embeddings. This is the minimal "existence proof" that non-linguistic computation helps — but required training from scratch, limiting applicability.

- **[[thinking-states-latent-reasoning|Thinking States]]** (2026): The most production-oriented latent reasoning method. Key innovations:
  - **Supervised approach**: Uses teacher-generated NL thoughts compressed into continuous states, avoiding the unsupervised curriculum that causes [[catastrophic-forgetting]]
  - **Deep-to-shallow recurrence**: Processes through 26 layers per chunk with speculative prefill — a practical efficiency technique
  - **State ambiguity discovery**: Identified that causal (left-to-right) reasoning commits to quantities before seeing the question, losing 15% relative performance. This motivates [[frontier-research-directions|frontier direction #6]] (bidirectional latent reasoning)

## Collaboration Network

Google Research collaborates with both academic and corporate partners:
- **Pause Tokens**: Joint with [[cmu|CMU]] (Sachin Goyal as first author) — bridging Google's infrastructure with academic research
- **Thinking States**: Internal Google Research team (Tel Aviv office, primarily), with co-authors from Hebrew University of Jerusalem and Tel Aviv University
- **Scaling Agent Systems**: Joint with [[google-deepmind|Google DeepMind]] and [[mit|MIT]] — the [[scaling-agent-systems|scaling paper]] bridges both Google organizations and the academic multi-agent community

### Cross-Entity Collaboration Summary

| Partner Entity | Paper(s) | Collaboration Nature |
|---|---|---|
| [[cmu\|CMU]] | [[pause-tokens\|Pause Tokens]] | CMU provides Sachin Goyal as first author; Google provides infrastructure |
| [[google-deepmind\|Google DeepMind]] | [[scaling-agent-systems\|Scaling Agent Systems]] | Joint Google-internal scaling framework |
| [[mit\|MIT]] | [[scaling-agent-systems\|Scaling Agent Systems]] | MIT contributes multi-agent debate expertise |

## Strategic Position

Google Research occupies a unique niche: **production viability**. While other methods ([[coconut-reasoning-latent-space|Coconut]], [[latentmas-collaboration|LatentMAS]]) demonstrate dramatic results on benchmarks, Thinking States is designed for deployment — it preserves interpretability through NL teacher thoughts, avoids modifying the backbone, and offers concrete speedup with speculative prefill.

The state ambiguity finding (15% loss from causal reasoning order) is an underappreciated insight. It suggests that all causal latent reasoning methods may be fundamentally limited for tasks where goal-awareness matters. Google Research is positioned to develop bidirectional alternatives.

## Research Trajectory

Google Research's publication timeline traces the evolution from existence proof to production system:

1. **Oct 2023 — Existence proof**: Pause Tokens (with [[cmu|CMU]]) shows transformers exploit non-linguistic computation. Minimal approach, trains from scratch, limited applicability.
2. **Dec 2025 — Scaling framework**: The Scaling paper (with [[google-deepmind|DeepMind]] and [[mit|MIT]]) provides quantitative scaling laws for multi-agent systems, establishing when multi-agent helps and when it hurts.
3. **Feb 2026 — Production-ready latent reasoning**: Thinking States is designed for deployment — supervised training, speculative prefill for 2.66x speedup, frozen backbone. The state ambiguity finding (15% loss from causal ordering) opens a new research direction.

The trajectory shows Google Research moving from proof-of-concept to deployment optimization. The state ambiguity discovery suggests the next step is **bidirectional latent reasoning** — processing compressed states that can attend to the full input before committing to a reasoning direction.

## Key Researchers

- **Ido Amos**: First author on Thinking States. Leads the production-oriented latent reasoning effort.
- **Avi Caciularu**: Co-author on Thinking States; NLP expertise.
- **Mor Geva**: Co-author on Thinking States; interpretability and internal representations. Her expertise in understanding model internals informs the deep-to-shallow recurrence design.
- **Amir Globerson**: Senior researcher on Thinking States.
- **Jonathan Herzig**: Co-author on Thinking States.
- **Lior Shani**: Co-author on Thinking States.
- **Idan Szpektor**: Senior researcher on Thinking States.
- **Sachin Goyal**: First author on Pause Tokens ([[cmu|CMU]] affiliation). Bridges the CMU–Google Research collaboration.
- **Yubin Kim**: Lead author on Scaling Agent Systems (Google Research). Connects to [[google-deepmind|DeepMind]] and [[mit|MIT]] scaling work.
