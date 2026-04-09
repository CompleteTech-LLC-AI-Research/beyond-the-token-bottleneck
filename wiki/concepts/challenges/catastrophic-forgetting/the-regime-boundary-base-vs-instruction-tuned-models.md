The severity of catastrophic forgetting varies dramatically depending on how much post-training a model has undergone:

| Model Regime | Forgetting Risk | Evidence |
|-------------|----------------|----------|
| **Base model (pretrained only)** | Low — representations are general-purpose, no delicate alignment to disrupt | [[coconut-reasoning-latent-space\|Coconut]] works well on GPT-2; [[thinking-states-latent-reasoning\|Thinking States]] works on Qwen2.5-Base |
| **Instruction-tuned (SFT + RLHF/DPO)** | High — alignment is a thin veneer; small weight changes break it | [[softcot-efficient-reasoning\|SoftCoT]]'s LLaMA-3.1-8B-Instruct results show degradation |
| **Frontier models (proprietary)** | Likely very high — more training stages = more delicate balance | No published evidence |

The key insight is that alignment and instruction-following are **surface phenomena** — they occupy a relatively thin region of weight space compared to the model's core language modeling capabilities. Fine-tuning for latent reasoning pushes weights out of this region, destroying alignment while potentially preserving raw language modeling. This explains why Coconut works on GPT-2 (no alignment to disrupt) but damages instruction-tuned models.
