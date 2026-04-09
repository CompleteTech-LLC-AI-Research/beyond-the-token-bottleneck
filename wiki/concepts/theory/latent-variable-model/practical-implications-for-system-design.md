### Choosing Latent Dimensionality

The number of latent dimensions $n_z$ must be specified in advance. ThoughtComm does not address automatic selection, but the theory suggests guidelines:

- $n_z$ should be at least as large as the true number of independent thought factors in the problem
- Too small $n_z$ forces multiple thoughts into single dimensions, violating sparsity and breaking identifiability
- Too large $n_z$ wastes capacity but is less harmful — extra dimensions can remain unused (zero Jacobian columns)

### Prefix Length Robustness

ThoughtComm demonstrates that performance is stable across prefix lengths $m \in \{1, 4, 8, 16\}$, with near-optimal performance at $m=1$ ([[raw/pdf/arxiv-2510.20733.pdf|ThoughtComm §4.2]]). This is a strong validation of the latent variable framework: a single prefix vector in $\R^d$, unconstrained by vocabulary membership, carries enough information to modulate agent behavior effectively. By contrast, a single discrete token (constrained to the vocabulary) carries at most $\log_2(V) \approx 15$ bits — the [[continuous-vs-discrete-representation|continuous advantage]] is dramatic.

### Task-Agnostic Components

Both the autoencoder and prefix adapter are task-agnostic — trained once and reused across tasks. Their computational cost depends only on the embedding dimension (e.g., 1024 or 4096), not the model parameter count. This means ThoughtComm's overhead is **identical for a 7B and a 405B model** sharing the same embedding dimension — a critical efficiency property for deployment at scale.
