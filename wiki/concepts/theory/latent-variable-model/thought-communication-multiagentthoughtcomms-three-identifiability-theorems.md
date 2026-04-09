The theoretical core of [[thought-communication-multiagent|ThoughtComm]] consists of three theorems that establish identifiability of different aspects of the latent structure. All three require the same two assumptions: (1) $f$ is invertible and twice differentiable, and (2) the Jacobian $J_f$ satisfies an $\ell_0$ sparsity constraint — each latent thought influences only a bounded number of hidden-state dimensions.

### Theorem 1: Identifying Shared Thoughts

**Statement**: For any pair of agents $A_i$ and $A_j$, the shared latent thoughts $Z_{H^{(i)}} \cap Z_{H^{(j)}}$ can be recovered up to permutation, **disentangled** from all private and irrelevant thoughts.

**Proof intuition**: Consider the autoencoder's learned inverse $\hat{f}^{-1}$. With sparsity regularization on the Jacobian of the reconstruction $\hat{f}$, the solution is pushed toward one where each recovered latent dimension has sparse influence. The key insight is that shared thoughts, by definition, influence dimensions in **both** agents' portions of $H$. If the autoencoder tried to mix a shared thought with a private thought of $A_i$, the resulting recovered dimension would need to influence dimensions in $A_i$'s hidden state (from both the shared and private components) but only dimensions in $A_j$'s hidden state (from the shared component). The sparsity constraint penalizes this mixing — a disentangled solution where the shared thought maps to one recovered dimension and the private thought to another achieves lower sparsity cost. The invertibility of $f$ ensures that enough information exists in $H$ to perform this separation.

**Practical implication**: When the autoencoder extracts a latent dimension that loads on both agents' hidden states, it genuinely represents common ground — not an artifact of entangled representation.

### Theorem 2: Identifying Private Thoughts

**Statement**: For any pair of agents, the private thoughts of either agent ($Z_{H^{(i)}} \setminus Z_{H^{(j)}}$) can be recovered up to permutation, disentangled from all other latent variables.

**Proof intuition**: Private thoughts influence only one agent's portion of $H$. The sparsity constraint again prevents mixing: a recovered dimension that blends a private thought of $A_i$ with a shared thought would need to influence dimensions in both agents (from the shared component) plus additional dimensions in $A_i$ (from the private component). The sparser solution is to keep them separate. The key technical step is showing that the $\ell_0$ constraint makes the entangled solution **strictly suboptimal** compared to the disentangled one.

**Practical implication**: Agent-specific reasoning is preserved in its own latent dimensions, not contaminated by others' thoughts. When ThoughtComm routes private thoughts back to their originating agent with high weight, it reinforces genuinely unique reasoning rather than feeding back noise.

### Theorem 3: Identifying the Structure

**Statement**: The full binary incidence matrix $B(J_f)$ — which agents hold which thoughts — is identifiable up to relabeling.

**Proof intuition**: Given that Theorems 1 and 2 establish disentanglement of shared and private components for any pair, the full structure can be reconstructed by composing pairwise results. For each recovered latent dimension, its influence pattern across all agents' hidden states determines which agents "hold" that thought. The sparsity of the Jacobian ensures that this influence pattern is unambiguous — each thought's footprint in $H$ is sparse and distinctive enough to be attributed to the correct set of agents.

**Practical implication**: The system can construct a complete map of "who thinks what" — enabling the [[thought-structure|agreement-based routing]] that distinguishes common ground from private reasoning from contested claims.

### When Identifiability Fails

The theorems have clear failure modes:

1. **Dense Jacobian**: If the true generating function $f$ is dense (every thought influences every dimension of every agent's state), the sparsity assumption is violated. In practice, this would mean every agent's reasoning about one topic is entangled with every other topic — plausible for very simple problems but unlikely for complex multi-step reasoning where agents naturally focus on different aspects.

2. **Non-invertible $f$**: If multiple distinct thought configurations produce identical agent states (e.g., due to information compression in the model), the mapping cannot be uniquely inverted. This could occur when models are far too small for the complexity of the reasoning task.

3. **Insufficient data**: The theoretical results are asymptotic. With finite data, the autoencoder's Jacobian may not converge to the true sparsity pattern, especially in high-dimensional settings. ThoughtComm validates empirically that 500 training examples suffice for their benchmarks, but larger agent systems or more complex thought structures may require more.

4. **Accumulated composition errors**: Global structure recovery via pairwise composition may accumulate errors. If the pairwise recovery between agents $A_1$ and $A_2$ has small errors, and between $A_2$ and $A_3$ has small errors, the composed global structure inherits both. With dozens of agents, these errors could compound.
