A fundamentally different approach is to avoid fine-tuning altogether. **Inter-agent communication methods** operate at inference time without modifying model parameters, making both training barriers irrelevant:

| Method | Communication mechanism | Parameter modification | Forgetting risk |
|--------|------------------------|----------------------|-----------------|
| [[cipher-multiagent-debate-embeddings|CIPHER]] | Weighted-average output embeddings | None | Zero |
| [[kvcomm-kth-selective|KVComm]] | KV-cache injection | None | Zero |
| [[activation-communication-harvard|AC]] | Hidden-state sharing | None | Zero |
| [[thought-communication-multiagent|ThoughtComm]] | Disentangled latent thoughts via prefix adaptation | Autoencoder + adapter trained, but LLM frozen | Zero for LLM |

These methods achieve latent communication benefits without any training, bypassing both barriers entirely. The trade-off is that they do not improve single-model reasoning — they only improve multi-agent collaboration. Both training barriers are specific to methods that require fine-tuning for latent **reasoning**, not latent **communication**.
