The discrete bottleneck appears in multiple contexts within this wiki, and **the same principle applies in each**: bypassing the bottleneck by staying in continuous space preserves information and enables richer computation.

### Inter-Agent Communication
- **Discrete**: Agents exchange natural language messages. Each token collapses the sender's full belief distribution into one choice.
- **Continuous**: Agents exchange embedding vectors ([[embedding-space-communication|CIPHER]]), KV-cache entries ([[kv-cache-communication]]), or hidden-state activations ([[activation-communication]]).
- **Evidence**: [[cipher-multiagent-debate-embeddings|CIPHER]] shows 0.5-5.0% accuracy improvement from continuous communication in [[multi-agent-debate]].

### Intra-Agent Reasoning
- **Discrete**: The model reasons through chain-of-thought — discrete token sequences.
- **Continuous**: The model reasons through continuous thoughts ([[latent-space-reasoning|Coconut]]) — hidden-state feedback loops.
- **Evidence**: [[coconut-reasoning-latent-space|Coconut]] shows dramatic improvement on planning tasks (97.0% vs 77.5% on ProsQA) and emergent BFS from superposition.

### The Unifying Principle

Both cases are instances of the same information-theoretic phenomenon:

```mermaid
graph LR
    A["Rich continuous state"] --> B["discrete bottleneck"] --> C["impoverished discrete representation"] --> D["re-expansion"] --> E["degraded continuous state"]
```

Removing the bottleneck:

```mermaid
graph LR
    A["Rich continuous state"] --> B["direct transfer"] --> C["rich continuous state"]
```

The information lost at the discrete bottleneck includes:
- **Uncertainty**: The model's confidence distribution over alternatives (critical for [[temperature-diversity]] in debate)
- **Superposition**: Multiple simultaneous hypotheses (see [[#Superposition and Quantum Analogy|the superposition section below]]; critical for BFS in [[latent-space-reasoning]]; exploited by [[thought-structure|ThoughtComm's disentangled thoughts]])
- **Nuance**: Fine-grained distinctions between similar options (critical for reasoning at high-uncertainty positions)
