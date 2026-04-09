Embedding-space communication sits at one stage of a broader continuum. The canonical framing:

![[depth-spectrum]]

Within that spine, this concept focuses on stage 2 — **output embeddings** — and its relationship to the stages immediately above (tokens) and below (KV-cache, activations).

### Output Embedding Averages (the embedding-space stage)

- Introduced by [[cipher-multiagent-debate-embeddings|CIPHER (Pham et al., 2023)]].
- Each "token" transmitted is the expected embedding under the model's output distribution: emb(t) = Σ p(vocabᵢ) · emb(vocabᵢ) ([[raw/pdf/arxiv-2310.06272.pdf|CIPHER §3.1]]).
- Stays within the **convex hull** of the vocabulary's embedding space (see [The Convex Hull Constraint](#the-convex-hull-constraint) below), so the receiver can process it through its normal embedding layer.
- **Pros**: No architectural changes, works with any model sharing the same tokenizer, human-interpretable via nearest-neighbor decoding.
- **Cons**: Only captures output-layer information; deeper internal representations (see [[kv-cache-communication]], [[activation-communication]]) are still lost.

### Structure as an Orthogonal Axis

Depth is not the only dimension. [[thought-communication-multiagent|ThoughtComm (Zheng et al., 2025)]] adds **structure** on top of the depth spine: a sparsity-regularized autoencoder extracts **disentangled latent factors** from agent hidden states, then selectively routes them based on recovered [[thought-structure|shared/private structure]]. This is orthogonal to where on the depth axis the communication is tapped — it's about *how* the latent signal is organized before transmission, with identifiability guarantees via [[latent-variable-model]] theory. The cost is a learned autoencoder between sender and receiver.

### Embedding-Specific Methods at a Glance

The table below lists methods that either live at the output-embedding stage or add structure on top of the latent communication axis. For KV-cache and activation methods, see [[kv-cache-communication]] and [[activation-communication]] respectively.

| Method | What's shared | Compatibility requirement | Key paper |
| ------ | ------------- | ------------------------- | --------- |
| CIPHER | Soft token vectors (convex hull) | Shared tokenizer | [[cipher-multiagent-debate-embeddings\|CIPHER]] |
| Disentangled thoughts | Structured latent factors | Trained autoencoder | [[thought-communication-multiagent\|ThoughtComm]] |
| Vision-pathway injection | Encoded latent rollouts | VLMs + trained codec | [[vision-wormhole-heterogeneous\|Vision Wormhole]] |
