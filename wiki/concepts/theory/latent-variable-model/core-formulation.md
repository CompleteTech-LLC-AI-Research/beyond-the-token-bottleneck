The generative model assumes:

> $$H = f(Z)$$

Where:
- $Z \in \R^{n_z}$: Latent variables (the "causes" or "thoughts") — each $Z_i$ is a scalar representing one latent dimension
- $H \in \R^{n_h}$: Observed variables (concatenated agent hidden states across all $n_a$ agents)
- $f$: Generating function, assumed **invertible** (bijective) and **twice differentiable**

The structure of how latent variables influence observations is encoded in the **Jacobian** $J_f(Z) \in \R^{n_h \times n_z}$, and specifically its binary non-zero pattern $B(J_f) \in \{0,1\}^{n_h \times n_z}$. A non-zero entry $B(J_f)_{i,j}$ means latent thought $j$ has a non-zero partial derivative with respect to hidden-state dimension $i$ — i.e., thought $j$ **influences** dimension $i$.

The invertibility assumption ensures that the mapping from thoughts to states is information-preserving: no two distinct thought configurations produce identical agent states. The twice-differentiability assumption is needed for the Jacobian analysis that underpins the identifiability proofs.
