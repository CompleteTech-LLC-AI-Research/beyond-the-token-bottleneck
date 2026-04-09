Given $n_a$ agents and $n_z$ latent thoughts, the thought structure is a **binary incidence matrix** $B(J_f) \in \{0,1\}^{n_h \times n_z}$, where a non-zero entry indicates that latent thought $j$ influences agent dimension $i$. This is derived from the Jacobian of the generating function $f$ that maps thoughts to agent hidden states.

For each agent $A_k$, the relevant thoughts are:

> $$Z_{H_t^{(k)}} := \{Z_{t,j} \in Z_t \mid \exists\, i \in [k_l, k_h] \text{ such that } B(J_f)_{i,j} \neq 0\}$$

### The Three Types of Thoughts

For any pair of agents $A_i$ and $A_j$:

| Type | Definition | Role in communication |
|------|-----------|----------------------|
| **Shared thoughts** | $Z_{H_t^{(i)}} \cap Z_{H_t^{(j)}}$ | Common ground; basis for coordination |
| **Private to $A_i$** | $Z_{H_t^{(i)}} \setminus Z_{H_t^{(j)}}$ | Agent-specific reasoning; source of novelty |
| **Private to $A_j$** | $Z_{H_t^{(j)}} \setminus Z_{H_t^{(i)}}$ | Agent-specific reasoning; complementary perspective |
| **Irrelevant** | $Z_t \setminus (Z_{H_t^{(i)}} \cup Z_{H_t^{(j)}})$ | Latent dimensions that influence neither agent |

### Agreement Level

For multi-agent systems ($n_a > 2$), the **agreement level** $\sigma_j$ of a thought $Z_{t,j}$ measures how many agents' states depend on it:

> $$\sigma_j = \sum_{k=1}^{n_a} \mathbb{1}[Z_{t,j} \in Z_{H_t^{(k)}}]$$

This creates a spectrum from fully private ($\sigma = 1$) to fully shared ($\sigma = n_a$):

| Agreement level | Interpretation | Typical treatment |
|----------------|---------------|-------------------|
| $\sigma = 1$ | Unique to one agent | May be noise, or may be a critical unique insight |
| $\sigma = 2\text{-}3$ (small group) | Shared by a subgroup | Possible coalition or partial agreement |
| $\sigma \approx n_a/2$ | Divisive | Potential point of disagreement worth exploring |
| $\sigma = n_a$ | Universal consensus | Strong common ground; high confidence |
