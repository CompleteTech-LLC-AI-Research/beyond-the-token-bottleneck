Standard chain-of-thought (CoT) reasoning requires the model to "think out loud" — every intermediate reasoning step must be expressed as tokens. This imposes three constraints:

1. **The discretization bottleneck**: Each reasoning step must be compressed into a sequence of discrete tokens, losing the continuous richness of the model's internal representations. (The same bottleneck that [[embedding-space-communication]] addresses for inter-model communication.)

2. **The fluency tax**: Most generated tokens serve textual coherence ("Let's think step by step", "Therefore", "We can see that") rather than reasoning. Compute is wasted predicting these filler tokens.

3. **The commitment problem**: Once a token is generated, the model is committed to that path. Autoregressive generation cannot backtrack. A wrong turn at step 2 of a 10-step chain propagates irrecoverably.

Latent-space reasoning addresses all three by keeping reasoning in the model's internal vector space, where representations are continuous, there's no fluency overhead, and — critically — **multiple paths can be maintained simultaneously**.
