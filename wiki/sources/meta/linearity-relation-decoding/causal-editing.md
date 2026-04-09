The LRE inverse enables **causal steering** of model outputs by editing internal representations:

> $$\delta_s = W_r^\dagger(o' - o), \quad \tilde{s} = s + \delta_s$$

To change prediction from object o to target o'. Uses low-rank pseudoinverse W_r^†. Closely matches oracle performance (direct subject-representation substitution) across layers.

**Faithfulness-causality correlation**: $R = 0.84$ (GPT-J), $R = 0.85$ (GPT2-XL), $R = 0.83$ (LLaMA-13B). The linear approximation is not just descriptive — it's **causally real**. Editing via LRE inverse changes model outputs as predicted.
