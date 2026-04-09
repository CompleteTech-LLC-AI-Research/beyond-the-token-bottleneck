ThoughtComm introduces a new level in the [[embedding-space-communication]] spectrum — between raw activation sharing and natural language:

| Level | What's communicated | Key property |
|-------|-------------------|-------------|
| Natural language | Discrete tokens | Universal, lossy |
| Output embeddings ([[cipher-multiagent-debate-embeddings|CIPHER]]) | Soft token vectors | Preserves output distribution |
| **Disentangled thoughts (ThoughtComm)** | **Structured latent factors** | **Identified, routed, agreement-annotated** |
| KV-cache ([[kv-cache-communication]]) | Attention key-value pairs | Layer-specific representations |
| Raw activations ([[activation-communication]]) | Hidden states | Maximum information, minimum structure |

ThoughtComm's unique contribution is not just going deeper in the representation stack, but adding **structure** — disentangling what is shared vs. private, routing thoughts selectively, and annotating agreement levels. Raw activation sharing gives you everything but with no organization; ThoughtComm gives you less but **organized**.
