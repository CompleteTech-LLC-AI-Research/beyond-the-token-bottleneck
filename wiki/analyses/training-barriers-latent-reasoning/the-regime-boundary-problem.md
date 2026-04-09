The severity of catastrophic forgetting varies dramatically across model regimes:

| Model Regime | Training Pipeline | Forgetting Risk | Evidence |
|-------------|-------------------|----------------|----------|
| **Base model (pretrained only)** | Pretraining on web text | Low — representations are general-purpose, no delicate alignment to disrupt | [[coconut-reasoning-latent-space|Coconut]] works well on GPT-2 ([[raw/pdf/arxiv-2412.06769.pdf|Coconut §4]]); [[thinking-states-latent-reasoning|Thinking States]] works on Qwen2.5-Base |
| **Instruction-tuned (SFT)** | Pretraining + supervised fine-tuning | Medium — instruction-following behavior is more fragile than raw language modeling | Not directly tested in isolation |
| **RLHF/DPO-aligned** | Pretraining + SFT + RLHF/DPO | High — alignment is a thin veneer on top of base capabilities; small weight changes can break it | [[softcot-efficient-reasoning|SoftCoT]]'s LLaMA-3.1-8B-Instruct results show degradation |
| **Frontier models (proprietary)** | Complex multi-stage pipeline | Unknown but likely very high — more stages = more delicate balance | No published evidence |

The key insight is that alignment and instruction-following are **surface phenomena** — they occupy a relatively thin region of weight space compared to the model's core language modeling capabilities. Fine-tuning for latent reasoning pushes weights out of this region, destroying alignment while potentially preserving (or even improving) raw language modeling. This explains why [[coconut-reasoning-latent-space|Coconut]] works on GPT-2 (a base model with no alignment to disrupt) but damages instruction-tuned models.
