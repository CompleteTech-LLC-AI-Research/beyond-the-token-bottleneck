For a relation r (e.g., "plays the sport of"), the mapping from subject representation s at an intermediate layer to the object representation o:

> $$\text{LRE}(s) = \beta \cdot W_r \cdot s + b_r$$

Where $W_r$ is estimated as the mean Jacobian over $n=8$ examples within the same relation:

> $$W = \E_{s_i, c_i}\left[\frac{\partial F}{\partial s} \;\middle|\; (s_i, c_i)\right]$$

And $b_r = \E[F(s,c) - (\partial F / \partial s) \cdot s]$. This is a first-order Taylor approximation of the model's internal computation $F$.

**$\beta$ correction**: Layer normalization causes the Jacobian to underestimate magnitude by 2.5-4.3x. $\beta$ compensates: GPT-J $\beta=2.25$, LLaMA-13B $\beta=8.0$, GPT2-XL $\beta=2.25$. Selected to maximize faithfulness-causality correlation.

**Low-rank pseudoinverse**: For causal editing, uses $W_r^\dagger$ (low-rank pseudoinverse, rank $\rho_r$ per relation) instead of full inverse, preventing noisy small singular values from washing out meaningful ones.
