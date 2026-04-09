Synthesizing across these readings, three distinct approaches to auditability emerge, each with different guarantees and costs:

| Layer | Approach | Guarantee | Cost | Example |
|-------|----------|-----------|------|---------|
| **By construction** | Generate interpretable intermediates, then compress | Full visibility of reasoning before compression | Power ceiling --- cannot exploit superposition | [[thinking-states-latent-reasoning\|Thinking States]] |
| **By recovery** | Provably disentangle latent factors after computation | Structural map of who-thinks-what, up to permutation | Requires sparsity assumption; pairwise only | [[thought-communication-multiagent\|ThoughtComm]] |
| **By constraint** | Limit bandwidth, require decodable audit shadows | Forced structuring; anomaly-detectable | Caps performance; audit shadow may not capture full content | [[latentcompress-open-call\|LatentCompress]] |

No single layer is sufficient. A production-grade auditable latent system would likely combine all three: interpretable reasoning where possible (Thinking States), provable disentanglement where opacity is necessary (ThoughtComm), and architectural bandwidth constraints as a backstop (LatentCompress).
