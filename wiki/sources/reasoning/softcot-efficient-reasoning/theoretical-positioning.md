SoftCoT introduces a new point on the [[latent-space-reasoning]] spectrum:

| Method | Who reasons in latent space? | Backbone modified? | Scale tested |
|--------|----------------------------|-------------------|-------------|
| [[coconut-reasoning-latent-space\|Coconut]] | The model itself (hidden-state feedback loop) | Yes (full training) | GPT-2 |
| Coconut on instruction-tuned | The model itself | Yes (LoRA) | 7-8B (**degrades**) |
| **SoftCoT** | **External assistant model** | **No (frozen)** | **7-8B (improves)** |
| Standard CoT | The model itself (in token space) | No | Any |

SoftCoT trades Coconut's elegant self-contained loop for a **two-model architecture** that preserves the backbone — a pragmatic solution to the [[catastrophic-forgetting|catastrophic forgetting]] problem that may be the only viable approach for frontier instruction-tuned models.

### Comparison of Training Approaches

The three latent reasoning training paradigms reveal a progression in how the field handles the tension between continuous reasoning power and model integrity:

| Property | [[icot-internalize-cot\|iCoT]] | [[coconut-reasoning-latent-space\|Coconut]] | **SoftCoT** |
|----------|------|---------|---------|
| Training target | Full model | Full model | Projection only |
| Curriculum | Progressive CoT token removal | Multi-stage CoT → latent replacement | Single-stage next-token prediction |
| Optimizer reset needed | Yes (critical) | Yes (adopted from iCoT) | No (single-phase training) |
| Backbone modification | Complete retraining | Complete retraining | **None** |
| Scale demonstrated | GPT-2 (117M) | GPT-2 (small) | 7-8B instruction-tuned |
| Continuous thought source | Internalized within model | Self-generated hidden states | External assistant model |

iCoT and Coconut both require the delicate multi-stage curriculum with optimizer resets — a training procedure that is fragile and empirically shown to fail on instruction-tuned models. SoftCoT sidesteps this entirely by externalizing the reasoning to a separate model, requiring only standard supervised training of a small projection layer.
