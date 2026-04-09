Catastrophic forgetting is not the only training-time barrier. [[latent-reasoning-supervision-analysis|Cui et al. (2026)]] identifies a second, orthogonal barrier: the **supervision-exploration trade-off**. While catastrophic forgetting concerns what happens to *existing* model capabilities under new training, the supervision-exploration trade-off concerns what happens to the *new* latent reasoning capability itself.

Sweeping four representative latent reasoning methods across the supervision spectrum, Cui et al. find that the strength of supervision on latent states creates a dilemma ([[raw/pdf/arxiv-2602.22441.pdf|Cui et al. §5]]):

| Supervision Strength | Representative Methods | Shortcut Behavior | Latent Diversity (distinct outcomes, GPT-2) | Pass@100 |
|---------------------|----------------------|-------------------|---------------------------------------------|----------|
| **Weak** | [[coconut-reasoning-latent-space\|Coconut]], CODI | Severe — accuracy retained at depth=0 | High (15.84 for Improved Coconut) | High (~70%) |
| **Strong** | SIM-CoT, CoLaR | Eliminated — CoLaR collapses to ~0% at depth=0 | Low (3.21 for CoLaR) | Low (~23%) |

Stronger supervision constrains latent representations enough to prevent shortcut behavior (where the model bypasses its own latent steps entirely), but **simultaneously destroys the multi-candidate capacity** that gives latent reasoning its theoretical advantage. Weaker supervision preserves capacity but lets the model game its own representations. No published method achieves both.

### How the Two Barriers Interact

The two trade-offs **bound the latent reasoning design space from both sides**:

| Trade-off | What Gets Damaged | When It Triggers | Known Mitigations |
|-----------|-------------------|-----------------|-------------------|
| **Catastrophic forgetting** | Pre-existing instruction-tuned capabilities | When the backbone is fine-tuned | Frozen-backbone designs ([[softcot-efficient-reasoning\|SoftCoT]], [[thinking-states-latent-reasoning\|Thinking States]]) |
| **Supervision-exploration** | The new latent reasoning capability itself | Whenever latent states are trained, regardless of backbone freezing | **None yet** — open problem |

This creates a four-way bind:

- Modify the backbone heavily --> destroy instruction-tuning (catastrophic forgetting)
- Don't modify the backbone, supervise latents weakly --> shortcut behavior (Cui et al.)
- Don't modify the backbone, supervise latents strongly --> destroy latent capacity (Cui et al.)
- Don't supervise latents at all --> no learning signal

This explains why the field's most promising methods cluster at architectural extremes: [[softcot-efficient-reasoning|SoftCoT]] freezes the backbone and uses moderate supervision through projection alignment; [[thinking-states-latent-reasoning|Thinking States]] freezes the backbone and uses strong teacher-forced NL supervision; [[latentmas-collaboration|LatentMAS]] avoids training entirely. Whether any of these escape the supervision-exploration trade-off at scale remains an **untested empirical question**.
