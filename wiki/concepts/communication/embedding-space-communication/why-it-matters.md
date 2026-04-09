Natural language is optimized for human comprehension, not for inter-model information transfer. The fundamental tension is between **interpretability** and **information density**:

- A vocabulary of 32,000 tokens means each sampled token carries at most ~15 bits of information ($\log_2(32000)$).
- But the model's *belief* at that position is a full probability distribution over all 32,000 tokens — a much richer signal. When the model is uncertain between "6" and "9" in an arithmetic step, the sampled token discards that uncertainty entirely. The receiving model sees only the winner, not the margin.

Embedding-space communication preserves this distributional information by transmitting the full weighted mixture of token embeddings. The receiver gets a **soft token** — a point in continuous embedding space that encodes the sender's confidence landscape.
