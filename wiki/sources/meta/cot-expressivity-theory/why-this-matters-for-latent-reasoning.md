1. **The depth bottleneck is the core insight**: Transformers are limited by parallel depth ($\text{TC}^0$). Any mechanism that increases effective depth -- CoT tokens, [[pause-tokens|pause tokens]], [[coconut-reasoning-latent-space|Coconut]]'s continuous thoughts, [[thinking-states-latent-reasoning|Thinking States]]' chunk recurrence -- should yield similar expressivity gains.

2. **Constant-size sufficiency**: A fixed-size model can solve arbitrarily large problems via CoT. The reasoning capacity is in the *process* (generation steps), not the *model* (parameters). This motivates latent approaches that provide more "thinking steps" rather than more parameters.

3. **RNNs cannot substitute**: Constant-size RNNs fail where transformers with CoT succeed -- attention's selective retrieval of previous intermediate results is essential. Latent reasoning architectures need analogous retrieval mechanisms.

4. **The construction reveals essential components**: The proof identifies specific roles for softmax attention (conditional copy/mean), multi-head parallelism (extracting multiple context tokens simultaneously), FFNs (arithmetic lookup tables), and residual connections (maintaining information across layers). These are not interchangeable with simpler alternatives.

5. **[[superposition-coconut-theory|Superposition theory]]** extends this: Feng et al. prove CoT adds depth; Zhu et al. prove continuous CoT additionally exploits **width** (superposition). Together they explain why continuous thoughts outperform discrete CoT on planning tasks.

6. **DP generalization bridges to real tasks**: Many practical reasoning problems (planning, multi-hop QA, code execution) can be cast as DP, meaning the theoretical sufficiency result applies broadly. The $\text{P}$-completeness of CFG membership testing shows CoT-equipped transformers can, in principle, solve anything in polynomial time.
