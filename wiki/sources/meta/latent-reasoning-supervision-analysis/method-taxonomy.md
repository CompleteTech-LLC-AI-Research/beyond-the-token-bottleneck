> [!diagram|left]
> ```mermaid
> graph TD
>     A["Latent Reasoning Methods"]
>     A --> WS["Weak Supervision<br>(outcome-level only)"]
>     A --> SS["Strong Supervision<br>(intermediate alignment)"]
>     WS --> CN["Coconut<br>(stage-wise CoT loss)"]
>     WS --> CD["CODI<br>(outcome + final-state distillation)"]
>     SS --> SC["SIM-CoT<br>(decoder reconstruction loss)"]
>     SS --> CL["CoLaR<br>(token-level compression alignment)"]
>     style A fill:#dae8fc,stroke:#6c8ebf
>     style WS fill:#fff2cc,stroke:#d6b656
>     style SS fill:#ffe6cc,stroke:#d79b00
>     style CN fill:#d5e8d4,stroke:#82b366
>     style CD fill:#d5e8d4,stroke:#82b366
>     style SC fill:#f8cecc,stroke:#b85450
>     style CL fill:#f8cecc,stroke:#b85450
> ```

> [!notation|right]
> | Class | Definition |
> |---|---|
> | Weak supervision | Latent state $c_t$ trained only via final answer loss or final latent alignment |
> | Strong supervision | Latent state $c_t$ trained against per-step textual or compressed targets |

The paper evaluates **four representative methods** spanning the supervision spectrum:

| Method | Supervision | Mechanism | Reference |
|---|---|---|---|
| **[[coconut-reasoning-latent-space\|Coconut]]** (Hao et al., 2024) | Weak | Stage-wise progressive replacement of CoT tokens with continuous thoughts; cross-entropy loss only on remaining textual predictions | arXiv 2412.06769 |
| **CODI** (Shen et al., 2025) | Weak | Unified training with outcome-level loss + teacher–student distillation aligning final latent states from a CoT teacher | arXiv 2502.21074 |
| **SIM-CoT** (Wei et al., 2025) | Strong | Decoder-based explanation loss: reconstructs the corresponding textual reasoning step from each intermediate latent state | arXiv 2509.20317 |
| **CoLaR** (Tan et al., 2025) | Strong | Token-level compression: averages every $c$ consecutive token representations, uses the average as the supervision target | arXiv 2505.16552 |

For all experiments, SIM-CoT is implemented on top of CODI (the better-performing variant) and CoLaR uses compression factor $c = 5$ to match the latent step count of other methods.
