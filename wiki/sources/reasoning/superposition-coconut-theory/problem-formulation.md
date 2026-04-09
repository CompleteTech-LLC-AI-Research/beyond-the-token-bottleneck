### Graph Reachability Task

Given a directed graph $\mathcal{G} = (V, E)$ with vertices $V = \{v_1, \ldots, v_n\}$ and edges $E = \{e_1, \ldots, e_m\}$, a root node $s$, and two candidate destinations $t_1, t_2$ (exactly one reachable from $s$), determine which candidate is reachable.

### Input Format

The prompt follows a structured sequence: BOS token, followed by $3m$ tokens representing $m$ edges (each edge as source-target-edge_marker triplet), a query token with two candidates $t_1, t_2$, a reasoning token with root $s$, then $C$ continuous thought steps, and finally an answer token. Total prompt length: $t_0 = 3m + 6$ tokens before thoughts begin.

### Embedding Structure

Token embeddings $u_v \in \R^d$ with $d = O(|V|)$ are partitioned into four subspaces:
- **Content space** ($d_{te}$ dimensions): Stores the token identity via orthonormal embeddings ($U^T U = I_V$)
- **Buffer 1** ($d_{te}$ dimensions): Scratch space for intermediate computations (source nodes)
- **Buffer 2** ($d_{te}$ dimensions): Scratch space for intermediate computations (target nodes)
- **Positional encoding space** ($d_{pe}$ dimensions): Sinusoidal positional encodings

The orthonormality assumption ($\langle u_a, u_b \rangle = \delta_{ab}$) is critical -- it ensures that superpositions of different vertex embeddings are distinguishable and that inner products between a continuous thought and vertex embeddings cleanly measure membership in the reachable set.

### Chain of Continuous Thought

Unlike discrete CoT (which samples a token and feeds back its embedding), continuous CoT skips the sampling step: $h_{t_0+c} = \text{Transformer}_\theta(h_1, \ldots, h_{t_0+c-1})$. The raw output embedding becomes the next input. This preserves the continuous superposition state that would be destroyed by sampling.
