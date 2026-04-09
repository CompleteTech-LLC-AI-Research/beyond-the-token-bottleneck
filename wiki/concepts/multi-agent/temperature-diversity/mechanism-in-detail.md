### The Low-Temperature Agent (Anchor)

- Produces sharp, confident outputs — essentially greedy generation
- Serves as the **final answer selector** because its outputs are closest to natural language and most interpretable (CIPHER selects the lowest-temperature debater's response as the final answer)
- Provides a strong "hypothesis" for the other agent to react to
- In CIPHER, its embeddings are close to actual token embeddings (since the distribution is peaked)
- Error profile: high accuracy on easy positions, systematic failures on hard positions

### The High-Temperature Agent (Explorer)

- In natural language debate: produces garbled text at high temperatures ($T > 1.5$), which **actively harms** the other agent. This is why NLD wants all temperatures below 1.0
- In CIPHER: produces embedding vectors that are **rich weighted averages** over many tokens. These vectors encode the model's nuanced beliefs, including uncertainty and alternative possibilities. The receiving model processes these as soft inputs that carry richer information than any single token could
- Error profile: noisy on easy positions, but preserves critical information on hard positions

### Why They Complement Each Other

The pair works because they contribute **different types of information**:
- The anchor contributes **decisive, focused reasoning** — strong on the tokens where the model is confident
- The explorer contributes **distributional information** — valuable precisely at positions where the model is uncertain and a single token would be misleading

This is analogous to **exploration vs. exploitation** in reinforcement learning. The low-temperature agent exploits known-good reasoning; the high-temperature agent explores the space of possibilities. Together they cover more of the information landscape.
