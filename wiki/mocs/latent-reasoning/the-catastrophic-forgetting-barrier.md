Coconut's curriculum training damages instruction-tuned models (LLaMA-3.1-8B drops 79.61% → 76.12% on GSM8K). This is the central unsolved tension — see **[[catastrophic-forgetting]]**. Three solutions have been proposed:

| Solution | Paper | Approach | Trade-off |
|----------|-------|----------|-----------|
| Frozen backbone | [[softcot-efficient-reasoning\|SoftCoT]] | External assistant generates soft thoughts; only a projection layer is trained | Requires two models at inference |
| Teacher forcing | [[thinking-states-latent-reasoning\|Thinking States]] | NL thoughts → compressed states with deep-to-shallow recurrence | Needs teacher-generated thoughts for training |
| Training-free | [[latentmas-collaboration\|LatentMAS]] | Ridge regression alignment, no fine-tuning at all | Requires homogeneous architecture |
