### Filler Tokens vs. Learned Pause (Critical Distinction)

Using period characters (`.`) as filler tokens at inference gives **exactly zero gain** on all 9 tasks. This rules out the hypothesis that simply having more positions for attention is sufficient — the model must be **trained from scratch** to use the extra positions. The learned pause embedding (1024 parameters) encodes the model's "intention" to use these positions for computation, and this intention must be established during pretraining so that the entire model co-adapts.

### The $M_\text{inf} = 0$ Catastrophe

When a model pretrained and finetuned with pauses is run with zero pauses at inference, performance drops "spectacularly" — well below the baseline model that was never trained with pauses. This indicates that pause-pretraining fundamentally restructures the model's computation: the model **allocates** intermediate results to pause positions during its forward pass, and removing those positions eliminates the results those later computations depend on. The model cannot gracefully degrade because its computation graph is structurally dependent on the pause positions existing.

This fragility contrasts with Coconut, where reducing the number of latent thoughts produces graceful degradation (fewer thoughts = less reasoning depth, but the model can still function). The difference stems from the recurrence: each Coconut thought is an independent forward pass with its own complete computation, while pause tokens are woven into a single forward pass where removing them breaks internal dependencies.
