Multiagent debate is one of several multi-agent LLM paradigms, now formalized by the Scaling paper into 5 canonical architectures:

| Architecture | Communication | Communication overhead | Error amplification |
|-------------|---------------|----------------------|-------------------|
| Single-Agent | None | 0% | 1.0× |
| Independent MAS | None (parallel, aggregated) | 58% | 17.2× |
| Centralized MAS | Hub-spoke | 285% | 4.4× |
| **Decentralized MAS (debate)** | **All-to-all** | **263%** | **7.8×** |
| Hybrid MAS | Orchestrator + limited P2P | 515% | 5.1× |

Key distinctions:
- **Debate** (Decentralized): Agents have the **same role**, interact symmetrically. Best for dynamic tasks requiring diverse perspectives.
- **Self-refinement** / **Review primitive**: A single agent or Solver-Critic pair iterates. Now implementable in latent space via [[agent-primitives-building-blocks|Agent Primitives]].
- **Critic-generator** (Centralized): Orchestrator coordinates. Lower error amplification but higher overhead.
- **Plan-Execute**: [[agent-primitives-building-blocks|Agent Primitives]]' Planning primitive. Decomposes tasks into latent subgoals.
