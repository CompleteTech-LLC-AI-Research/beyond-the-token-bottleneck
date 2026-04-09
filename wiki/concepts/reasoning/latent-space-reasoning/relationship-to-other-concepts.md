### vs. Embedding-Space Communication

| Aspect | [[embedding-space-communication]] | Latent-space reasoning |
|--------|----------------------------------|----------------------|
| Context | Inter-agent (between models) | Intra-agent (within one model) |
| What's bypassed | Token sampling between sender and receiver | Token sampling within the reasoning loop |
| Information preserved | Output distribution over vocabulary | Full hidden state |
| Key insight | Soft tokens carry richer info than hard tokens | Continuous thoughts can encode path superpositions |

Both exploit the same fundamental principle: **the discrete token bottleneck discards valuable information**. They apply it in complementary contexts.

### vs. Chain-of-Thought

Latent-space reasoning is not anti-CoT — it's a **generalization** of CoT. CoT reasons through a sequence of discrete states (tokens). Latent reasoning reasons through a sequence of continuous states (hidden vectors). This is an instance of the [[continuous-vs-discrete-representation]] trade-off. The continuous version subsumes the discrete: any reasoning expressible as tokens is also expressible as vectors, but not vice versa (superpositions cannot be expressed as tokens).

### Connection to [[activation-communication]]

Coconut's continuous thoughts are exactly the kind of representation shared in activation communication. [[latentmas-collaboration|LatentMAS]] realizes this connection fully: agents generate latent thoughts via hidden-state feedback (Coconut-style), then transfer their complete KV caches (including the latent thoughts) to the next agent. This is the first framework that unifies latent reasoning and latent communication — agents that reason internally in latent space AND communicate in latent space. [[interlat-latent-space-agents|Interlat]] takes a similar approach with raw hidden-state sequences and learned compression.
