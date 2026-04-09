**The signal**: [[scaling-agent-systems|Scaling Agent Systems]] provides the first quantitative scaling framework for text-based MAS — 180 configurations, predictive model with $R^2 = 0.524$, identifies when MAS helps vs. hurts. But all communication is natural language.

**The gap**: Latent communication fundamentally changes the scaling parameters. Latent methods reduce **information loss** (addressing the "lossy communication" failure mode), reduce **token overhead** (4-7× fewer tokens), and change **error propagation** dynamics ([[latentmas-collaboration|LatentMAS]] shows latent transfer allows correction of upstream errors that text propagates). None of this is captured by the existing scaling framework.

**Why this could be paradigm-shifting**: If someone built a latent-MAS scaling framework, it could predict which tasks benefit from latent communication vs. text, what the optimal latent communication depth is (embeddings vs. KV-cache vs. activations), and where the crossover points are. This would transform latent MAS from ad-hoc experimentation into principled system design.

**Concrete next steps**:
- Replicate the Scaling paper's 180-configuration experiment with [[kvcomm-kth-selective|KVComm]]/[[latentmas-collaboration|LatentMAS]]/[[activation-communication-harvard|AC]] as communication channels instead of text
- Measure how the key scaling parameters (error amplification, coordination overhead, message density saturation) change under latent communication
- Build a predictive model that includes communication medium as a variable

---
