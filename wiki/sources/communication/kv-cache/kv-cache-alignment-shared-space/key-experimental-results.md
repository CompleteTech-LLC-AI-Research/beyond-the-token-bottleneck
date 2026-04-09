### Experiments with Gemma-2 models (100M-400M parameters)

**Setting 1 — Same trajectory, different checkpoints**: Two checkpoints from the same training run (early and late). Translating prefixes through the shared space improves **both** models' performance beyond their baselines. The shared space **sharpens** KV-cache features.

**Setting 2 — Same origin, different fine-tuning**: Russian expert and Spanish expert branched from the same parent. The shared space successfully mediates between their divergent latent spaces. Cross-lingual prefix translation works — Spanish prefix KV → shared space → Russian model generates Russian suffix.

**Setting 3 — Different random initialization**: Three models trained on identical data but with different seeds. Despite zero trajectory overlap, the shared space enables effective translation. This demonstrates that the shared space captures **task-relevant structure** that transcends model-specific parameterizations.

**Setting 4 — Different model sizes**: A 400M model (16 layers) and a 100M model (4 layers). Despite the 4× layer difference, the adapters successfully learn the mapping. The weaker 100M model benefits from 400M model's translated prefix KV-cache.

### The Self-Improvement Effect

A remarkable finding: passing a model's own KV-cache through the shared space and back (cyclic: A → Ω → A) **improves** that model's language modeling performance. The shared space acts as a **regularizer or feature sharpener** — it distills the most transferable features of the KV-cache, filtering noise.

This parallels [[kvcomm-kth-selective|KVComm]]'s finding that selective KV sharing sometimes exceeds the Skyline (full context) — less can be more when the selection/transformation acts as beneficial regularization.

### Zero-Shot Extensibility

When a 4th model is added to a pool of 3:
- Only adapters for the new model are trained (using paths to/from 2 of the 3 existing models)
- The **untrained** paths (new model ↔ 3rd existing model) work zero-shot with only mild performance degradation
- This proves the shared space is genuinely **global** — not segmented by model pair. Cache blocks from different models become interchangeable once translated into the shared space.

### Module Portability

The shared space enables **zero-shot transfer of learned skills** between models:
- Soft prompts (prefix-tuning) learned on Model A for a specific task
- Translated through shared space to Model B's KV-cache space
- Model B can perform the task **without any task-specific training**

Evaluated on a prompt recovery meta-learning task with ~6K training tasks and 200 eval tasks. Performance approaches the upper bound of learning soft prompts directly on the target model. This has implications for:
- **Compute amortization**: Learn a skill once, deploy across all models in the pool
- **Data privacy**: Only one model needs exposure to task data; the skill transfers via the shared space
