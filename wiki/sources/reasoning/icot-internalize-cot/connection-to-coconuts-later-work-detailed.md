iCoT is the **direct ancestor** of [[coconut-reasoning-latent-space|Coconut]]. The progression represents a precise scientific advancement:

**The insight iCoT provides**: When CoT tokens are removed, the model must internalize reasoning into existing hidden states. iCoT proves this is possible (99% on 9x9 multiplication) but reveals a **capacity ceiling** — the model's fixed depth limits how much can be compressed. 11x11 multiplication exceeds this capacity.

**Coconut's innovation over iCoT**: Instead of deleting CoT tokens, Coconut **replaces** them with continuous latent thoughts — each a full forward pass that adds effective depth beyond the architectural limit. This directly addresses iCoT's capacity ceiling. The expressivity gap is measurable: on ProsQA (requiring search), Coconut achieves 97.0% where iCoT's approach (no recurrence, fixed depth) would be limited by the $\text{TC}^0$ barrier [[cot-expressivity-theory|Feng et al.]] identify.

**The Phi-3 anomaly**: iCoT's Phi-3 (3.8B) shows a **wider** gap vs. explicit CoT than GPT-2 Medium (355M), despite 10x more parameters. This suggests **architecture matters more than scale** for internalization. The finding has implications for Coconut: hidden-state quality varies across architectures, so continuous thoughts may benefit different architectures differently.
