This paper provides the first systematic evidence that latent reasoning techniques break when applied to capable instruction-tuned models:

| Method | GSM8K (LLaMA-3.1-8B-Instruct) |
|--------|-------------------------------|
| Zero-Shot CoT | 79.61% |
| LoRA Fine-Tuning | 75.66% (−3.95) |
| Coconut (adapted with LoRA) | 76.12% (−3.49) |
| **SoftCoT** | **81.03% (+1.42)** |

Both LoRA fine-tuning and Coconut **fall below** the zero-shot baseline — the instruction-tuned model's carefully calibrated capabilities are damaged by any parameter modification. SoftCoT is the only trained method that improves over zero-shot CoT, because it never modifies the backbone.

This finding has significant implications for [[latent-space-reasoning]]: Coconut's results on GPT-2 (a small, non-instruction-tuned model) may not transfer to frontier models. The training curriculum that works for GPT-2 actively harms instruction-tuned models.
