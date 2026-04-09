### Why Left-Side Removal Works: The Compression Hierarchy

The paper's most important design choice is removing tokens from the **left** (beginning) of the CoT rather than the right. The underlying reasoning connects to how information flows through chains:

**Early CoT tokens** (problem setup, initial reasoning) encode context-setting information that the model can plausibly reconstruct from the input question alone. Removing these asks the model to internalize information it already has access to via its encoding of the question.

**Late CoT tokens** (near the answer) encode specific conclusions that depend on earlier steps. Right-side removal creates **orphaned context** — intermediate results pointing to a conclusion the model must produce from nothing. Right-side removal fails at ~100 tokens because this orphaned-context problem becomes intractable.

### The Optimizer Reset Mechanism

When CoT tokens are removed at stage transitions, AdamW's second-order gradient estimates ($v_t$ and $m_t$) become **stale**: they reflect the previous stage's optimization landscape. Without resetting, training **collapses permanently** around step 100 — the model enters a local minimum the stale momentum cannot escape. This finding was **directly adopted by** [[coconut-reasoning-latent-space|Coconut]], revealing that each stage of internalization is a qualitatively different optimization problem.

### The Removal Smoothing Distribution

The stochastic offset $o \sim P(o) \propto \exp(-\lambda o)$ with $\lambda = 4$ gives $P(o=0) \approx 0.982$, $P(o=1) \approx 0.018$. So ~2% of training examples briefly expose the model to the next stage's difficulty. Without this lookahead, accuracy drops to **zero** at ~50 tokens removed and never recovers — the transition is too abrupt.
