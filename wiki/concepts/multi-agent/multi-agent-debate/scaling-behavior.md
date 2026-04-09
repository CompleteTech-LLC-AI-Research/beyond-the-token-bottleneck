The framing this section depends on — diversity as a precondition, and temperature as the standard knob for inducing it — lives in the shared fragment:

![[temperature-scaling-behavior]]

The rest of this section covers debate-protocol-specific scaling (rounds, debater count, and cross-method comparisons) that sits on top of that framing.

### Rounds
More rounds generally help, but with **rapidly diminishing returns**:
- Rounds 1→2: Large improvement (agents see each other's work for the first time)
- Rounds 2→3: Moderate improvement (refinement)
- Rounds 3→6: Marginal improvement (convergence has largely happened)

[[cipher-multiagent-debate-embeddings|CIPHER]] shows similar scaling to NLD — the communication medium doesn't change the diminishing-returns curve, it just shifts the whole curve up.

**Exception — ThoughtComm**: [[thought-communication-multiagent|ThoughtComm]] is the first approach to show **monotonically improving accuracy AND consensus** from 2→6 rounds, while natural language debate and multiagent finetuning both degrade. The structured routing of [[thought-structure|disentangled thoughts]] appears to filter noise and redundancy across rounds rather than accumulating it.

### Debaters
More debaters also help with diminishing returns. Going from 2→3→4 debaters on GSM8K:
- NLD: 60→64→67%
- [[cipher-multiagent-debate-embeddings|CIPHER]]: 63→68→70%

The cost scales roughly linearly with debaters (each must generate a full response per round), so **2-3 debaters for 2-3 rounds** is the practical sweet spot.
