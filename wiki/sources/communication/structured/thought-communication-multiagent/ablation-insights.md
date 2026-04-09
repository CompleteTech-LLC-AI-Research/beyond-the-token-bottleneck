### Sparsity Regularization Effects

The $\ell_1$ regularization on the Jacobian $J_{\hat{f}}$ is the critical ingredient enabling disentanglement. Without sparsity ($\lambda = 0$), the autoencoder learns entangled representations where recovered "thoughts" are arbitrary mixtures of true latent factors — the synthetic validation confirms this with MCC scores falling below the identifiability threshold. As $\lambda$ increases, the Jacobian becomes sparser and disentanglement improves, up to a point: excessive regularization ($\lambda$ too large) collapses the latent space, discarding informative dimensions. The practical $\ell_1$ relaxation of the theoretical $\ell_0$ requirement introduces a soft trade-off — some residual entanglement persists, but the pairwise recovery of shared/private thoughts remains robust across dimensionalities 128-1024 in synthetic experiments.

### Number of Latent Factors

The latent dimensionality $n_z$ must be chosen in advance and represents a fundamental design parameter. Too few latent factors ($n_z$ much smaller than the true number of underlying thoughts) forces the autoencoder to merge distinct thoughts into shared dimensions, breaking the disentanglement guarantee. Too many factors ($n_z$ much larger than needed) introduces spurious dimensions that are either constant (carrying no information) or redundant copies of real thoughts, complicating the structural routing in Stage 2. The paper does not address automatic determination of appropriate $n_z$ — this remains an open limitation. In practice, the choice is informed by the embedding dimension $d$ of the base model and the expected complexity of the task.

### Agreement Threshold Sensitivity

The agreement-based reweighting (Stage 2) assigns weights $w_\sigma$ based on how many agents share each thought. The threshold separating "common ground" from "novel perspective" affects the routing behavior:

- **Low thresholds** (treating a thought as shared if held by $\geq 2$ of $n_a$ agents) emphasize consensus, potentially drowning out valuable minority perspectives. This configuration works well when agents have high baseline accuracy and disagreement signals noise rather than genuine alternative reasoning.
- **High thresholds** (requiring near-unanimity for "shared" status) preserve more diverse perspectives but risk amplifying noise from individual agent errors. This is better for tasks where agents have complementary knowledge and minority views are informative.

The prefix length robustness finding ($m \in \{1, 4, 8, 16\}$ with <5% fluctuation) suggests that the system is more sensitive to the agreement weighting than to the injection capacity — the bottleneck is in thought selection and routing, not in the adapter's ability to encode the selected thoughts.
