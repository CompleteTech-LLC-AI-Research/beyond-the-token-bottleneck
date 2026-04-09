Pause tokens are the **existence proof** that transformers can learn to use extra compute that carries zero semantic content, provided they are trained to do so from the start. This establishes three baselines:

1. **Lower bound on gains**: Any richer latent reasoning approach (Coconut, SoftCoT, Thinking States) that doesn't exceed pause token performance on a given task is providing no value beyond extra compute.
2. **Width-only is not enough**: The modest gains (1-19 points) vs CoT's much larger gains show that depth, not just width, is the critical resource. This motivates Coconut's feedback loop (which adds depth).
3. **Training is required**: Filler tokens at inference give zero gains. The model must learn during pretraining how to use the extra computation — this is a structural requirement, not something that emerges from prompting.

Coconut and Thinking States both use pause tokens as an ablation baseline, confirming that their continuous thoughts carry real information beyond mere extra compute: Coconut 34.1% vs pause-as-thought 24.1% on GSM8K (GPT-2 scale).
