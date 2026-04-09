| Design choice | iCoT | Coconut |
|--------------|------|---------|
| What happens to removed tokens | Deleted (model must internalize into existing hidden states) | **Replaced with continuous latent thoughts** (model gets dedicated reasoning medium) |
| Reasoning medium after removal | Implicit (hidden states only, fixed depth) | Explicit continuous vectors (each adds effective depth via [[cot-expressivity-theory|depth extension]]) |
| Recurrence | None — limited to model's fixed depth | Yes — each latent thought is a full forward pass |
| Superposition | Cannot encode (implicit, fixed architecture) | **Enabled** — continuous vectors support [[superposition-coconut-theory|proven BFS via superposition]] |
| Curriculum | Progressive left-side token removal | Progressive token-to-latent replacement |
| Optimizer reset | Yes (critical) | Yes (adopted from iCoT) |
| Removal smoothing | Yes (λ=4) | Not explicitly reported |
| Capacity ceiling | Fails on 11×11+ multiplication | Handles ProsQA (97.0%) requiring search |

iCoT's capacity ceiling — inability to fully internalize long reasoning chains because hidden-state compression is bounded by fixed model depth — is exactly what motivated Coconut to provide an explicit continuous thought space. [[cot-expressivity-theory|Feng et al.]] prove that effective depth is the key bottleneck; iCoT cannot add depth (it only uses existing hidden states), while Coconut adds depth via the latent feedback loop.
