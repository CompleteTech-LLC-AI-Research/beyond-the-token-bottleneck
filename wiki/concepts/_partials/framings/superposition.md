---
type: concept-partial
partial: superposition
created: "2026-04-08"
updated: "2026-04-08"
---

**Superposition** is the property that a single continuous vector in $\R^d$ can simultaneously encode a weighted combination of many distinct features, hypotheses, or candidates, rather than collapsing to exactly one. A discrete token from a vocabulary of size $V$ is a single symbol: it is one choice among $V$, carrying at most $\log_2 V \approx 15$ bits and committing the model to that choice. A $d$-dimensional continuous vector can instead hold, at the same position, a mixture like "0.45 candidate A + 0.35 candidate B + 0.20 candidate C" — arbitrarily many alternatives, weighted by their probability mass, with no commitment.

This asymmetry is not a matter of degree. It is structural: the discrete token interface is a projection onto basis vectors (a one-hot vocabulary), while the continuous residual stream is the full vector space those basis vectors live in. Any weighted sum of candidates is a legal point in that space; no such sum is a legal token. Sampling from a softmax is the operation that destroys the superposition — it forces the mixture to collapse to one vertex, discarding the relative weights on everything that wasn't sampled. This is the precise information-theoretic cost of the token bottleneck: the KL divergence between the model's full distribution and the degenerate post-sample distribution, largest exactly when the model is most uncertain.

Superposition matters in two directions. For **latent reasoning**, a single hidden state can carry multiple partial reasoning candidates in parallel, so the model does not have to commit to one path before it has enough evidence to evaluate them — the representational capacity for breadth-first exploration is present by construction, even if whether a given training recipe actually exploits that capacity is a separate empirical question. For **latent communication**, a single transmitted vector carries the sender's full belief distribution rather than one sampled token, so each communication step conveys strictly more information than any token-level channel could. Both are instances of the same underlying fact: continuous space admits mixtures; discrete space does not.

Superposition is one of the core reasons deeper taps on the [[depth-spectrum]] carry more information than tokens — every level below the token interface is a level at which mixtures survive instead of being collapsed.

## Used by

- [[continuous-vs-discrete-representation]]
- [[latent-space-reasoning]]
