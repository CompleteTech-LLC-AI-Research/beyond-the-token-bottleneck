**Claim A**: Training-free methods ([[latentmas-collaboration|LatentMAS]], [[kvcomm-kth-selective|KVComm]], [[agent-primitives-building-blocks|Agent Primitives]], [[state-delta-trajectory|SDE]]) achieve competitive or superior results without model modification.
— Multiple papers

**Claim B**: Trained methods (C2C, Interlat, ThoughtComm) achieve richer cross-architecture communication and structured representations that training-free methods cannot.
— [[cache-to-cache-semantic-communication|C2C]], [[interlat-latent-space-agents|Interlat]], [[thought-communication-multiagent|ThoughtComm]]

**Status**: **Genuine trade-off, not contradiction**. Training-free methods are faster to deploy and don't risk [[catastrophic-forgetting|catastrophic forgetting]], but they're limited to homogeneous architectures or shallow communication. Trained methods enable cross-architecture and structured communication at the cost of training overhead. The tension is real but represents a design choice, not conflicting findings.

**Resolution needed**: Quantify the exact performance gap between training-free and trained approaches in controlled settings to determine when the training overhead is justified.

---
