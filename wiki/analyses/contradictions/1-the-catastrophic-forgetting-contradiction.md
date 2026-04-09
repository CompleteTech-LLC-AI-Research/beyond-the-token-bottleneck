**Claim A**: Coconut's multi-stage curriculum successfully trains [[latent-space-reasoning|latent reasoning]] on GPT-2, achieving 97% on ProsQA.
— [[coconut-reasoning-latent-space|Coconut (Hao et al., 2024)]]

**Claim B**: Coconut's curriculum approach **damages** instruction-tuned models. LLaMA-3.1-8B drops from 79.61% to 76.12% on GSM8K when trained with LoRA for latent reasoning.
— [[softcot-efficient-reasoning|SoftCoT (Xu et al., 2025)]]

**Status**: **Genuine tension, different regimes**. [[coconut-reasoning-latent-space|Coconut]] works on base models; it breaks instruction-tuned models. The gap is not a contradiction but a regime boundary — the instruction-tuning pipeline creates a delicate balance that curriculum training disrupts. However, Coconut's paper does not acknowledge this limitation, which [[softcot-efficient-reasoning|SoftCoT]] discovered.

**Resolution needed**: Can curriculum training be modified to work on instruction-tuned models, or is architectural innovation (frozen backbone, training-free) the only path? See [[catastrophic-forgetting]].

---
