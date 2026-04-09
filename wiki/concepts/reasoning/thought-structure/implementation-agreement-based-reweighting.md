In [[thought-communication-multiagent|ThoughtComm]]'s practical framework, the recovered structure is used for **selective routing**:

1. Extract latent thoughts via sparsity-regularized autoencoder
2. For each agent, identify relevant thoughts using the recovered Jacobian structure
3. Partition relevant thoughts by agreement level $\sigma$ ([[raw/pdf/arxiv-2510.20733.pdf|ThoughtComm §3.3]])
4. Assign weights $w_\sigma$ to each agreement level
5. Construct a weighted, structured latent representation per agent

This means each agent doesn't just receive "what others think" — it receives a structured representation that distinguishes "what everyone agrees on" from "what's unique to me" from "what's contested." This structured view enables more informed reasoning in subsequent debate rounds.
