[[softcot-efficient-reasoning|SoftCoT]] provides the first systematic evidence that latent reasoning approaches **break** on instruction-tuned models. The results are stark:

| Method | GSM8K (LLaMA-3.1-8B-Instruct) | Change from zero-shot |
|--------|-------------------------------|----------------------|
| Zero-Shot CoT (no training) | 79.61% | baseline |
| LoRA fine-tuning | 75.66% | **-3.95** |
| [[coconut-reasoning-latent-space|Coconut]] (adapted with LoRA) | 76.12% | **-3.49** |
| [[softcot-efficient-reasoning|SoftCoT]] (backbone frozen) | 81.03% | **+1.42** |

*Source: ([[raw/pdf/arxiv-2502.12134.pdf|SoftCoT Table 1]])*

The instruction-tuned model's carefully calibrated capabilities — instruction following, format compliance, reasoning patterns — are **damaged** by any parameter modification, even efficient methods like LoRA. Both LoRA fine-tuning and Coconut fall below the zero-shot baseline, while [[softcot-efficient-reasoning|SoftCoT]], which never modifies the backbone, is the only trained method that improves over zero-shot CoT.
