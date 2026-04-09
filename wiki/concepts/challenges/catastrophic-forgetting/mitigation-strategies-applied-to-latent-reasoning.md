The critical question is how these classical strategies perform when adapted to the latent reasoning setting. The following table compares all approaches that have been empirically tested, with quantitative results:

| Approach | Representative Method | Backbone Modified? | Forgetting Guarantee | Best Quantitative Result | Scale Validated |
|----------|----------------------|-------------------|---------------------|-------------------------|----------------|
| **Frozen backbone + external reasoning** | [[softcot-efficient-reasoning\|SoftCoT]] | No | Complete (by construction) | +1.42 over zero-shot on GSM8K (LLaMA-3.1-8B-Instruct) | 7-8B instruction-tuned |
| **Multi-stage curriculum** | [[coconut-reasoning-latent-space\|Coconut]] | Yes (all parameters) | None | 97.0% on ProsQA (GPT-2), but -3.49 on instruction-tuned | GPT-2 base only |
| **Curriculum + replay mixing** | Improved Coconut (Cui et al.) | Yes (all parameters) | None | 41.06% GSM8K-Aug (+7.0 over original Coconut, GPT-2) | GPT-2 base only |
| **Frozen backbone + lightweight modules** | [[thinking-states-latent-reasoning\|Thinking States]] | No (frozen) | Complete (but untested on instruction-tuned) | Near-CoT accuracy on 2-hop QA with 2.66x speedup | 0.5-1.5B base |
| **LoRA fine-tuning** | Coconut + LoRA | Partially (low-rank) | Insufficient | 76.12% GSM8K (-3.49 vs. zero-shot, LLaMA-3.1-8B-Instruct) | 7-8B instruction-tuned |

*Sources: [[raw/pdf/arxiv-2502.12134.pdf|SoftCoT Tables 1, 4]], [[raw/pdf/arxiv-2412.06769.pdf|Coconut §4]], [[raw/pdf/arxiv-2602.22441.pdf|Cui et al. Table 3]]*

The pattern is clear: only methods that **completely freeze** the backbone avoid forgetting on instruction-tuned models. Even LoRA — which modifies only a small subspace of each weight matrix — causes enough representation drift to cascade through the network and degrade performance below the zero-shot baseline.
