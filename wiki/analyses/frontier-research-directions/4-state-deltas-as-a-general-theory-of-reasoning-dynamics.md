**The signal**: [[state-delta-trajectory|SDE]] shows that **inter-token hidden-state differences** (deltas) outperform raw hidden states for communication — sometimes raw states actually *degrade below the natural language baseline*, while deltas consistently improve. Deltas are context-agnostic: they capture reasoning dynamics stripped of the sender's specific context.

**The gap**: SDE applies deltas only as inter-agent steering vectors. But deltas could be a **general-purpose representation of reasoning processes** — independent of the specific input, transferable across contexts, and composable. Nobody has explored:
- Building a **library of reasoning deltas** from diverse problems, then applying them as few-shot "reasoning templates" in latent space
- Using deltas as the **communication medium for latent debate** (agents exchange delta trajectories rather than text or raw activations)
- Training models to generate deltas directly (rather than extracting them from token-by-token generation)

**Why this could be paradigm-shifting**: If reasoning dynamics are transferable across contexts (which SDE's results suggest), then a pre-computed library of "latent reasoning strategies" could provide instant reasoning abilities without chain-of-thought generation at all. Think of it as "reasoning retrieval" in latent space — find the most similar delta trajectory from your library and apply it as a steering vector.

**Concrete next steps**:
- Cluster delta trajectories from diverse reasoning tasks — do common patterns emerge?
- Test cross-task transfer: extract deltas from math reasoning, apply to logic reasoning
- Build a delta library and test retrieval-augmented reasoning (find nearest delta, inject, measure accuracy vs. CoT)
- Compare delta-based communication to all existing approaches in a controlled [[multi-agent-debate|multi-agent debate]] setting

---
