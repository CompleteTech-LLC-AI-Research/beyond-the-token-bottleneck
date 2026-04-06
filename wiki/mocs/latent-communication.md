---
type: overview
title: "Latent Communication"
created: "2026-04-06"
updated: "2026-04-06"
tags: [moc, latent-communication]
---

# Latent Communication

How multiple LLM agents exchange information through continuous representations rather than text. Natural language is optimized for human comprehension, not inter-model information transfer — every sampled token discards the model's full distributional belief. This research line explores progressively deeper channels that preserve more of that information.

## The Depth Spectrum

Communication methods form a spectrum from shallow (compatible, interpretable) to deep (information-dense, restrictive). For the full 10-level walkthrough with detailed analysis of each level, see **[[communication-depth-spectrum]]**. Navigate by depth below:

### Embedding Level — Output-layer representations
The shallowest continuous channel. Transmit weighted averages of token embeddings instead of sampled tokens.

- **[[cipher-multiagent-debate-embeddings]]** — CIPHER: the foundational paper. Weighted output embeddings in debate, 0.5–5% gains. Requires shared tokenizer.
- **[[state-delta-trajectory]]** — SDE: inter-token hidden-state *deltas* as steering vectors. Deltas outperform raw states. Same-model only.
- **[[embedding-space-communication]]** — Concept synthesis: information bottleneck theory, convex hull constraint, full 10-level depth spectrum.

### Activation Level — Hidden-state representations
Share intermediate transformer activations — richer than embeddings, but harder to align across architectures.

- **[[activation-communication-harvard]]** — AC: single-layer activation replacement at layer ~26, <¼ compute. Works cross-family (LLaMA/Qwen/Gemma).
- **[[interlat-latent-space-agents]]** — Interlat: full hidden-state sequences, $2600\times$ bandwidth vs text. Cross-family with learned adapters.
- **[[activation-communication]]** — Concept synthesis: 5-paper comparison, cross-model compatibility spectrum, information concentration problem.

### KV-Cache Level — Attention memory
Inject the sender's cached key-value pairs into the receiver's attention mechanism. The receiver attends to the sender's context as if it had processed it directly.

- **[[kvcomm-selective-kv-sharing]]** — KVComm: layer selection, 30% of layers $\approx$ full performance.
- **[[cache-to-cache-semantic-communication]]** — C2C: learned cross-architecture fusion with gating.
- **[[kv-cache-alignment-shared-space]]** — KV Alignment: global shared space, $O(N)$ scaling, self-improvement effect.
- **[[kvcomm-online-cross-context]]** — KVCOMM-online: anchor-based offset reuse, 7.8× speedup.
- **[[kv-cache-communication]]** — Concept synthesis: 4 design dimensions, combined stack vision.

### Structured Level — Disentangled thought representations
Impose structure on the communicated representations — decompose into shared/private components with identifiability guarantees.

- **[[thought-communication-multiagent]]** — ThoughtComm: disentangled thoughts, agreement routing, scales positively with debate rounds.
- **[[thought-structure]]** — Shared/private decomposition, agreement routing.
- **[[latent-variable-model]]** — Identifiability theory underpinning ThoughtComm.

## Cross-Cutting Concepts

- **[[continuous-vs-discrete-representation]]** — The theoretical foundation: why continuous > discrete for inter-model transfer.
- **[[multiagent-debate]]** — The debate paradigm these communication methods plug into.
- **[[temperature-diversity]]** — Anchor/explorer dynamics and diversity's role in embedding-space debate.

## Key Entities

- **[[tsinghua]]** — C2C, SDE
- **[[kth]]** — KVComm
- **[[google-deepmind]]** — KV Cache Alignment
- **[[cmu]]** — ThoughtComm
- **[[fair-meta]]** — CIPHER ecosystem (LLaMA family enables shared-tokenizer communication)

## Theoretical Foundations

- **[[platonic-representation-hypothesis]]** — Why cross-family activation communication works: models converge to shared statistical structure.
- **[[relative-representations-zero-shot]]** — Zero-shot model stitching via cosine-similarity anchors.
- **[[linearity-relation-decoding]]** — Linear relational embeddings; explains enriched entity representations at mid-layers.

## Connections

- Combines with latent reasoning in the [[unified-frameworks|unified frameworks]]
- [[frontier-research-directions]] identifies delta-based reasoning templates and learned compression as top open directions
- [[latentcompress-collaboration-strategy]] maps the practical collaboration landscape
