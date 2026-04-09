The theoretical concern about catastrophic forgetting in latent reasoning became empirically concrete with [[softcot-efficient-reasoning|SoftCoT]] (Xu et al., 2025), which provides the first systematic evidence that latent reasoning methods **degrade** instruction-tuned models below their zero-shot baselines.

### SoftCoT's GSM8K Results on LLaMA-3.1-8B-Instruct

| Method | GSM8K Accuracy | Change from Zero-Shot |
|--------|---------------|----------------------|
| Zero-Shot CoT (no training) | 79.61% | baseline |
| LoRA Fine-Tuning | 75.66% | **-3.95** |
| [[coconut-reasoning-latent-space\|Coconut]] (adapted with LoRA) | 76.12% | **-3.49** |
| [[softcot-efficient-reasoning\|SoftCoT]] (backbone frozen) | 81.03% | **+1.42** |

*Source: [[raw/pdf/arxiv-2502.12134.pdf|SoftCoT Table 1]]*

The 79.61% to 76.12% drop when applying Coconut via LoRA to an instruction-tuned model is decisive: even parameter-efficient fine-tuning destroys enough of the alignment surface to produce a net-negative result. The model loses more instruction-following capability than it gains in latent reasoning. Only [[softcot-efficient-reasoning|SoftCoT]], which **never modifies the backbone**, manages to improve over the zero-shot baseline.

### Coconut's Curriculum Sensitivity

[[coconut-reasoning-latent-space|Coconut]]'s multi-stage curriculum — which progressively replaces language CoT steps with continuous thoughts — illustrates how fragile latent reasoning training is even on base models. Without the curriculum, performance collapses dramatically ([[raw/pdf/arxiv-2412.06769.pdf|Coconut §4.1]]):

| Variant | GSM8K | ProntoQA | ProsQA |
|---------|-------|----------|--------|
| Coconut (full curriculum) | 34.1% | 99.8% | 97.0% |
| Without curriculum (direct final-stage training) | 14.4% | 52.4% | 76.1% |
| No-CoT baseline | 16.5% | 93.8% | 76.7% |

Skipping the curriculum produces results barely above the no-CoT baseline, confirming that the model **cannot learn latent reasoning from scratch** — it must be guided through a gradual transition. Each stage must be close enough to the previous one that the optimizer can follow without destroying what was learned. This is a continual-learning problem in miniature: each curriculum stage is a new "task" that risks overwriting the previous stage's knowledge.

Furthermore, [[latent-reasoning-supervision-analysis|Cui et al. (2026)]] discovered that Coconut's stage-wise curriculum produces a **degenerate inference mode**: later training stages override earlier ones so completely that reducing latent steps below the final-stage maximum causes the model to skip remaining textual reasoning entirely. Their Improved Coconut fix — mixing earlier-stage data into later stages with proportion $(i+1)$ for stage $i$ — raised GPT-2 GSM8K-Aug accuracy from 34.09% to 41.06% ([[raw/pdf/arxiv-2602.22441.pdf|Cui et al. §4.2]]). This is essentially **replay-based continual learning** applied within the curriculum — the same class of solution that the broader forgetting literature prescribes.
