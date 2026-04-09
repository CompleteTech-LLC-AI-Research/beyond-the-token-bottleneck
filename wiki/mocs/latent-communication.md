---
type: moc
category: thread
title: "Latent Communication"
created: "2026-04-06"
updated: "2026-04-09"
tags: [moc, latent-communication]
---

# Latent Communication

How multiple LLM agents exchange information through continuous representations rather than text. Natural language is optimized for human comprehension, not inter-model information transfer — every sampled token discards the model's full distributional belief. This research line explores progressively deeper channels that preserve more of that information.

For the paper-by-paper walkthrough ordered by depth level (L0-L9), see **[[communication-depth-spectrum]]** — the detailed reference companion to this MOC.

## Reading Path

Start with the motivation, walk through the three main channel families, then see how structure and unification tie them together.

1. **[[continuous-vs-discrete-representation]]** — The theoretical foundation: why continuous vectors carry orders of magnitude more information than discrete tokens. Sampling a single token from a 32K vocabulary yields ~15 bits; the underlying distribution encodes far more. Every method below is an attempt to recover what sampling discards.
2. **[[embedding-space-communication]]** — The shallowest continuous channel. CIPHER replaces sampled tokens with expected embedding vectors — soft tokens that preserve the sender's confidence landscape. No architectural changes required, but information is limited to the output layer. Gains are strongest at positions of intermediate uncertainty where sampling would discard the most probability mass.
3. **[[activation-communication]]** — Going deeper: share hidden-state activations from the transformer's mid-to-late layers, where enriched entity representations live before the model compresses them for next-token prediction. AC's single-vector replacement at layer 26 outperforms NL debate on 48/57 MMLU datasets at less than one-quarter the compute. Remarkably works cross-family (LLaMA, Qwen, Gemma) without learned projections.
4. **[[kv-cache-communication]]** — Share key-value cache entries so the receiver attends to the sender's context through its own attention mechanism — non-destructive by design. KVComm shows 30% of layers suffices; C2C and KV Cache Alignment solve cross-architecture fusion via learned fusers and a global shared space, respectively.
5. **[[thought-structure]]** — Perpendicular to the depth axis: ThoughtComm adds structure by disentangling hidden states into shared (task-relevant) and private (agent-specific) factors, then selectively routes them via agreement scoring. Provides identifiability guarantees through [[latent-variable-model]] theory. Scales positively with debate rounds, unlike NL debate.
6. **[[unified-frameworks]]** — LatentMAS combines latent reasoning (Coconut-style hidden-state feedback) with latent communication (KV-cache transfer) in a single training-free framework. The deepest point on the spectrum: agents share complete working memory including internally generated thoughts, achieving 471x compression over text.
7. **[[multi-agent-debate]]** — The debate paradigm these communication methods plug into. Understanding the baseline protocol clarifies what each latent channel improves upon.

## Cross-Cutting Concerns

### Compatibility

The central tension in this space: deeper channels carry more information but demand tighter architectural alignment. Embeddings need only a shared tokenizer; activations work cross-family without projections; KV-cache methods require learned fusers or a global shared space for cross-architecture support.

![[compatibility-spectrum]]

### Compression and Efficiency

Bandwidth is not free. KVComm shows that selective layer sharing (30% of layers) matches full-cache transfer. Interlat compresses to 8 latent steps with only 4% accuracy loss and 46x speedup. KVCOMM-online achieves 7.8x prefill speedup through anchor-based offset estimation. The open question is whether learned compression can push deeper channels toward the bandwidth profile of shallower ones — bending the depth-compatibility curve.

### Diversity

- **[[temperature-diversity]]** — Anchor/explorer dynamics and diversity's role in embedding-space debate. The complementary information argument: latent communication is most valuable when agents encode genuinely different beliefs, which is why C2C finds limited overlap in correct-answer sets across model families.

## Key Entities

- **[[tsinghua]]** — C2C, SDE
- **[[kth]]** — KVComm
- **[[google-deepmind]]** — KV Cache Alignment
- **[[cmu]]** — ThoughtComm
- **[[fair-meta]]** — CIPHER ecosystem (LLaMA family enables shared-tokenizer communication)
- **[[harvard]]** — AC (activation communication)

## Theoretical Foundations

See **[[theoretical-foundations]]** for the full reading path through the representation-geometry and convergence results that ground this thread (Hernandez et al., Moschella et al., Huh et al.) plus the ThoughtComm identifiability theory in [[latent-variable-model]].

## Connections

- Combines with latent reasoning in the [[unified-frameworks|unified frameworks]]
- [[frontier-research-directions]] identifies delta-based reasoning templates and learned compression as top open directions
- [[latentcompress-collaboration-strategy]] maps the practical collaboration landscape
