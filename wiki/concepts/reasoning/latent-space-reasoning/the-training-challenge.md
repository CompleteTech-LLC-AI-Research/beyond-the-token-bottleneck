A key finding from Coconut: **LLMs cannot learn latent reasoning from scratch**. Training directly on question-answer pairs with continuous thoughts (no curriculum) produces performance no better than the No-CoT baseline.

### Why Curriculum Is Necessary

The hypothesis: the latent reasoning space is too large and unstructured for gradient descent to find good solutions without guidance. Language CoT data provides a "scaffold" — it shows the model what reasoning looks like, then the curriculum progressively shifts that reasoning from language space to latent space.

The multi-stage curriculum ([[raw/pdf/arxiv-2412.06769.pdf|Coconut §3.1]]):
1. Start with full language CoT (the model knows how to reason in language).
2. Replace the first step with continuous thoughts (the model learns to initiate reasoning in latent space).
3. Replace the second step (the model learns to chain latent reasoning steps).
4. Continue until all steps are replaced (fully latent reasoning).

Optimizer state is reset between stages, suggesting that each stage requires fundamentally different optimization dynamics.

### The Catastrophic Forgetting Barrier

[[softcot-efficient-reasoning|SoftCoT]] reveals a critical barrier: Coconut's curriculum works on GPT-2 but **damages instruction-tuned models**. LoRA-adapted Coconut on LLaMA-3.1-8B-Instruct drops GSM8K from 79.61% to 76.12% — below zero-shot CoT. See [[catastrophic-forgetting]] for full details. This means **any approach that modifies the backbone** (Coconut, iCoT) may be fundamentally incompatible with frontier instruction-tuned models.

### The Supervision–Exploration Trade-Off

[[latent-reasoning-supervision-analysis|Cui et al. (2026)]] identifies a **second** training-time barrier orthogonal to catastrophic forgetting. Sweeping four representative methods (Coconut, CODI, SIM-CoT, CoLaR) across the supervision spectrum, they find a fundamental tension:

| Supervision strength | Shortcut behavior | Latent diversity (distinct outcomes/100 samples) | Pass@100 |
|---|---|---|---|
| Weak ([[coconut-reasoning-latent-space\|Coconut]], CODI) | Severe — most methods retain accuracy at depth=0 and under noise injection | High (15.84 for Improved Coconut on GPT-2) | High (~70%) |
| Strong (SIM-CoT, **CoLaR**) | Eliminated — CoLaR collapses to ~0% at depth=0 | Low (3.21 for CoLaR on GPT-2) | Low (~23%) |

**The trade-off**: stronger supervision constrains latent representations enough to prevent shortcut behavior but **simultaneously destroys the multi-candidate capacity** that makes latent reasoning theoretically interesting. Weaker supervision preserves capacity but allows the model to bypass its own latent steps.

This is **distinct from** the alignment trade-off:
- **Alignment trade-off** (SoftCoT): Backbone modification damages instruction-tuning. *Mitigation*: frozen-backbone designs.
- **Supervision–exploration trade-off** (Cui et al.): The supervision signal that fixes shortcut behavior also destroys latent capacity. *Mitigation*: **none yet**.

Together, the two trade-offs **bound the latent reasoning design space from both sides** — and they explain why no method in this collection has successfully matched both strong CoT performance AND demonstrably-used latent reasoning at the same time.

### Three Solutions to the Training Challenge

| Solution | Approach | Trade-off |
|----------|---------|-----------|
| **[[coconut-reasoning-latent-space|Coconut]] curriculum** | Multi-stage progressive replacement | Only works on base models (GPT-2); damages instruction-tuned |
| **[[softcot-efficient-reasoning|SoftCoT]] externalization** | Freeze backbone; external assistant generates soft thoughts | Requires two models; soft thoughts augment CoT, don't replace it |
| **[[thinking-states-latent-reasoning|Thinking States]] teacher forcing** | NL thoughts → compress → inject. Gold states enable parallel training | Requires chunk-level supervision annotations; uses base models |
| **[[latentmas-collaboration|LatentMAS]] alignment** | Ridge regression on embedding matrices; training-free | No optimization at all; limited to same-architecture agents |

### Implications

This training dependency is both a limitation and a research frontier:
- **Limitation**: You need high-quality language CoT data before you can train latent reasoning. Latent reasoning is currently bootstrapped from, not a replacement for, language reasoning.
- **Instruction-tuned models**: The [[catastrophic-forgetting|catastrophic forgetting]] barrier means frozen-backbone approaches ([[softcot-efficient-reasoning|SoftCoT]]) or training-free approaches ([[latentmas-collaboration|LatentMAS]]) may be the only viable paths for production models.
- **Open question**: Can alternative training approaches (RL, self-play, contrastive learning) enable latent reasoning without language CoT scaffolding and without damaging existing capabilities?
