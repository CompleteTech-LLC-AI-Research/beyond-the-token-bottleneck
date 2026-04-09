### Independent Component Analysis (ICA)

ThoughtComm is a descendant of the **ICA tradition** (Comon, 1994; Hyvärinen et al., 2001). Classical linear ICA recovers independent non-Gaussian sources from linear mixtures. The key insight that carries over: **structural constraints on the mixing function enable source separation**. In ICA, the constraint is linearity and source independence. In ThoughtComm, the constraint is Jacobian sparsity — a much weaker assumption that applies to nonlinear functions and does not require source independence.

The evolution from ICA to ThoughtComm follows a clear trajectory:
- **Linear ICA** (1990s): Linear $f$, independent sources → full recovery
- **Nonlinear ICA** (2016-2020): Nonlinear $f$, auxiliary variables → full recovery under auxiliary supervision
- **ThoughtComm** (2025): Nonlinear $f$, sparsity only → pairwise recovery without auxiliary supervision

### Variational Autoencoders (VAEs)

The **VAE literature** (Kingma & Welling, 2014) pursues a related goal — learning disentangled representations — but from a different angle. VAEs impose a factorial prior (typically independent Gaussians) on the latent space and train via variational inference. However, Locatello et al. (2019) proved that **unsupervised disentanglement is impossible** without inductive biases: infinitely many entangled solutions achieve the same marginal likelihood as the disentangled one.

ThoughtComm overcomes this impossibility result by introducing **sparsity as an inductive bias** — a constraint that the VAE framework lacks. The $\ell_1$ regularization on the Jacobian provides exactly the structural bias needed to break the symmetry between entangled and disentangled solutions. This is a theoretically significant contribution: it identifies a minimal inductive bias sufficient for disentanglement.

The practical difference is also notable. VAEs with $\beta$-regularization ($\beta$-VAE; Higgins et al., 2017) encourage disentanglement empirically but without formal guarantees. ThoughtComm provides **provable** disentanglement under stated assumptions — a stronger foundation for systems where communication correctness matters.

### Causal Representation Learning

The emerging field of **causal representation learning** (Scholkopf et al., 2021) seeks to recover causal factors from observations. ThoughtComm's latent thoughts can be interpreted as causal factors that **generate** agent states. The key difference: causal methods typically require interventional data (actively manipulating one factor to observe effects on others) or temporal structure (multiple time steps revealing causal dynamics). ThoughtComm requires neither — it works from a single snapshot of agent states, using sparsity alone.

However, ThoughtComm does not recover **causal direction** — it identifies which thoughts influence which agents but not whether thought A causes thought B. For multi-agent communication, this is acceptable (the routing decision depends on "who holds what," not "what caused what"), but for deeper interpretability goals, causal methods might be needed.
