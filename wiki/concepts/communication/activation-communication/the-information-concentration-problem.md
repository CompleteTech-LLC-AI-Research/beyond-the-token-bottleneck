[[kvcomm-kth-selective|KVComm]] showed that the **last token's hidden state** concentrates most output-relevant information in later layers. This creates a dilemma for hidden-state communication:
- **Replacing** the last token's state ([[activation-communication-harvard|AC]] approach): Works because B retains context at other positions
- **Averaging/summing** states: Dilutes or distorts both signals
- **Full sequence transfer** ([[interlat-latent-space-agents|Interlat]]): Avoids the dilemma entirely — transmits all positions
- **Delta transfer** ([[state-delta-trajectory|SDE]]): Also avoids it — deltas don't replace any state, they add to all relevant positions
- **KV-cache approach** ([[kvcomm-kth-selective|KVComm]], [[latentmas-collaboration|LatentMAS]]): KV pairs integrate through attention (non-destructive)

The field has converged on the understanding that **the last-token hidden state is problematic as a sole communication vector**, but multiple approaches exist to work around this.
