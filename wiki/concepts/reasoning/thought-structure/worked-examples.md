### Example 1: Three-Agent Math Debate

Consider three agents ($A_1, A_2, A_3$) reasoning about a multi-step algebra problem with $n_z = 5$ latent thought dimensions. After recovering the Jacobian structure, suppose the incidence matrix reveals:

| | $Z_1$ (problem decomposition) | $Z_2$ (algebraic manipulation) | $Z_3$ (numerical estimation) | $Z_4$ (sign tracking) | $Z_5$ (answer formatting) |
|---|---|---|---|---|---|
| $A_1$ | 1 | 1 | 0 | 1 | 1 |
| $A_2$ | 1 | 1 | 1 | 0 | 1 |
| $A_3$ | 0 | 1 | 1 | 1 | 0 |

From this structure: $Z_2$ (algebraic manipulation) has $\sigma = 3$ (universal consensus), $Z_1$ and $Z_5$ have $\sigma = 2$, and $Z_3, Z_4$ have $\sigma = 2$ but in different agent subsets. No thought is fully private ($\sigma = 1$) in this example, but $Z_4$ (sign tracking) is invisible to $A_2$ — if the correct answer is negative, $A_2$ might miss the sign. The routing system would ensure $A_2$ receives $Z_4$ with a weight reflecting its low agreement, flagging it as "a perspective you haven't considered."

### Example 2: Divergent Reasoning Paths

Suppose two agents tackle a combinatorics problem. $A_1$ attempts a constructive counting approach while $A_2$ uses inclusion-exclusion. With $n_z = 4$ latent thoughts:

- $Z_1$ (problem parsing): shared ($\sigma = 2$) — both agents understand the question
- $Z_2$ (constructive counting logic): private to $A_1$ ($\sigma = 1$)
- $Z_3$ (inclusion-exclusion framework): private to $A_2$ ($\sigma = 1$)
- $Z_4$ (final numerical answer): shared ($\sigma = 2$) — both converge on the same number

Here the agreement structure tells a clear story: the agents agree on the problem and the answer but used completely different methods. The shared thoughts ($Z_1, Z_4$) provide high-confidence signals (independent confirmation), while the private thoughts ($Z_2, Z_3$) represent genuinely complementary reasoning. In a subsequent round, routing $Z_3$ to $A_1$ (and vice versa) could enable both agents to verify their answer via an alternative method — a form of cross-validation that unstructured communication cannot achieve.
