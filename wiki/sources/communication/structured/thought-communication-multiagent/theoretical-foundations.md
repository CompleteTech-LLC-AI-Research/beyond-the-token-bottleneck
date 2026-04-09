### The Generative Model

ThoughtComm formalizes the data-generating process behind agent responses as a [[latent-variable-model]]:

> $$H_t = f(Z_t)$$

Where:
- $Z_t = (Z_{t,1}, \ldots, Z_{t,n_z}) \in \R^{n_z}$: the latent thoughts at communication round $t$. Each $Z_{t,i}$ is a scalar representing one thought dimension.
- $H_t = (H_t^{(1)}, \ldots, H_t^{(n_a)})$: the concatenated model states (hidden-layer representations) of all $n_a$ agents before communication round $t$.
- $f$: an unknown generating function, assumed to be **invertible** (information-preserving) and **twice differentiable**.

The structure of which thoughts influence which agents is encoded in the **Jacobian** $J_f(Z_t)$, specifically its binary non-zero pattern $B(J_f) \in \{0,1\}^{n_h \times n_z}$. A non-zero entry $B(J_f)_{i,j}$ means latent thought $j$ influences hidden-state dimension $i$.

### Three Identifiability Theorems

The paper's core theoretical contribution is proving that latent thoughts can be recovered from observed agent states under minimal assumptions — no auxiliary information, no parametric constraints, just invertibility and $\ell_0$ sparsity regularization on the Jacobian.

**Theorem 1 — Identifying shared thoughts**: For any pair of agents $A_i$ and $A_j$, the shared latent thoughts ($Z_{H_t^{(i)}} \cap Z_{H_t^{(j)}}$) can be recovered up to permutation, **disentangled** from all other thoughts in the system. This means recovered shared thoughts are not mixed with private or irrelevant thoughts.

**Theorem 2 — Identifying private thoughts**: For any pair of agents, the private thoughts of either agent ($Z_{H_t^{(i)}} \setminus Z_{H_t^{(j)}}$) can be recovered up to permutation, disentangled from all other latent variables. This ensures that agent-specific reasoning is preserved and not contaminated by others' private thoughts.

**Theorem 3 — Identifying the structure**: The full binary mapping $B(J_f)$ — which agents hold which thoughts — is identifiable up to relabeling. This means the system can recover not just *what* the thoughts are, but *who thinks what*, including clusters of agreement, regions of conflict, and sources of novel input.

### Why This Is Theoretically Novel

Prior identifiability work in latent variable models typically aims for **global recovery** of all latents, requiring strong assumptions (auxiliary variables, specific function classes, structural constraints on the dependency graph). ThoughtComm takes a different approach:

- **Goal**: Pairwise recovery of shared and private components (a weaker but practically sufficient target) 
- **Assumptions**: Only invertibility and sparsity (much weaker than prior work)
- **Trade-off**: Cannot recover *all* latent variables, but can recover the ones that matter for communication — shared and private thoughts for each agent pair

By composing pairwise results across all agent pairs, the full global structure can be reconstructed. This is a genuinely new contribution to identifiability theory, not just an application of existing results to LLMs.
