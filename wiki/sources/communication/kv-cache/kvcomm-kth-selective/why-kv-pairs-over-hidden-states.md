The paper begins with a systematic analysis of why hidden states are a poor communication medium, directly challenging the [[activation-communication]] approach:

### Information Concentration Bias

Experiments reveal that in decoder-only LLMs, the **last token's hidden state** becomes increasingly dominant in later layers — it concentrates most of the information needed for the model's output. This creates a dilemma for hidden-state communication:
- **Transmitting only the last token's hidden state** (as in AC/Ramesh & Li, 2025): Loses all other positional information. Replacing the receiver's last token state with the sender's corrupts the receiver's own context.
- **Transmitting all tokens' hidden states**: Only effective if taken from early layers and prepended to early layers of the receiver. If taken from late layers (where most computation savings would come), performance drops sharply. If taken from early layers, the computation savings are minimal.

### Why KV Pairs Avoid This

KV pairs are the **attention-native** representation — the receiver integrates them through its standard attention mechanism, attending to the sender's cached representations alongside its own. This is non-destructive: the receiver's own hidden states are never replaced or corrupted. The receiver decides via attention how much weight to place on the sender's information at each position.
