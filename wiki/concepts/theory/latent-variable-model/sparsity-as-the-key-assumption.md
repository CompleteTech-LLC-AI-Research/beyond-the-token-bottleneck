The $\ell_0$ sparsity constraint on $J_f$ is the linchpin of all three theorems. It means: each latent thought influences only a **sparse subset** of the observed dimensions. In the multi-agent context, this means each thought influences only some agents' states — not every thought drives every agent.

### Why Sparsity Is Naturally Satisfied

In multi-agent reasoning systems, sparsity is a reasonable assumption because:

- **Agents specialize**: In a debate about a math problem, one agent might focus on algebraic manipulation while another focuses on problem decomposition. Each reasoning thread (thought) primarily influences the agent pursuing it.
- **Attention is selective**: LLM hidden states are shaped by attention, which is inherently sparse — each token attends to a subset of the context. This induces sparsity in how underlying thoughts manifest in hidden states.
- **Dimensionality**: Hidden states are high-dimensional ($d = 1024$ to $8192$). A thought that influences all $n_a \times d$ dimensions would need to be incredibly fundamental — most thoughts are more specific.

### Practical Relaxation: $\ell_1$ Regularization

In practice, $\ell_0$ sparsity (counting non-zero entries) is computationally intractable (NP-hard to optimize). ThoughtComm relaxes this to $\ell_1$ regularization on the Jacobian:

> $$\Loss_\text{rec} = \|H - \hat{f}(\hat{Z})\|^2 + \lambda\|J_{\hat{f}}\|_1$$

The $\ell_1$ penalty is the tightest convex relaxation of $\ell_0$ and is well-known to promote sparsity (the basis of LASSO regression and compressed sensing). The regularization strength $\lambda$ controls the sparsity-fidelity trade-off: too low and the Jacobian remains dense (no disentanglement); too high and the autoencoder sacrifices reconstruction quality to achieve artificial sparsity.

ThoughtComm validates this relaxation empirically: the sparsity-regularized autoencoder correctly identifies shared and private thought regions on synthetic data, with Mean Correlation Coefficient (MCC) exceeding the identifiability threshold across dimensionalities from 128 to 1024 ([[raw/pdf/arxiv-2510.20733.pdf|ThoughtComm §4.1]]).
