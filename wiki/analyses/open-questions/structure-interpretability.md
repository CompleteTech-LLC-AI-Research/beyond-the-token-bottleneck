How to organize, audit, and debug latent communication. This cluster connects directly to safety (opaque communication cannot be audited) and to scaling (structured communication may scale better than unstructured). [[thought-communication-multiagent|ThoughtComm]]'s identifiability theorems provide the strongest formal foundation, but they assume a specific generative model that may not hold for all methods.

- How many latent thought dimensions are needed? Can this be determined **automatically** via variational or information-theoretic criteria? — [[thought-structure]]
- Does thought structure **evolve across debate rounds** as agents update reasoning? Can the framework adapt in real time? — [[thought-structure]]
- Can disentangled latent thoughts serve as an **interpretability tool** — revealing *why* agents disagree? — [[thought-structure]]
- Can the framework distinguish between **informative thoughts and noise**? — [[thought-structure]]
- Does pairwise identifiability composition remain robust with **dozens or hundreds of agents**? — [[thought-structure]]
- How do we **audit, debug, and verify** reasoning in opaque continuous space? — [[latent-space-reasoning]]
- [[agent-primitives-building-blocks|Agent Primitives]] introduce a meta-level structure (Review/Voting/Planning primitives) selected by an Organizer. Can this structural decomposition be learned end-to-end rather than pre-specified, and could the Organizer itself operate in latent space? — [[agent-primitives-building-blocks]]
- [[vision-wormhole-heterogeneous|Vision Wormhole]]'s style token encodes distributional statistics $[\text{mean}, \text{std}, \text{RMS}]$ of the latent rollout. Could richer structural metadata (e.g., attention entropy, layer-wise activation norms) improve cross-model alignment without additional training? — [[vision-wormhole-heterogeneous]]
