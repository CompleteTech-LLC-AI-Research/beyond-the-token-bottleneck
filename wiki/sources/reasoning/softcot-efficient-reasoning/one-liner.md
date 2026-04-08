---
type: source-partial
parent: softcot-efficient-reasoning
partial: one-liner
created: "2026-04-08"
updated: "2026-04-08"
---

**SoftCoT** uses a small *frozen* assistant model to generate continuous soft-thought tokens, then projects them into the main model via a lightweight trained projection layer; only the projection trains, the backbone stays frozen. Six soft tokens match 24 hard tokens (~4× compression), assistant model size barely matters (0.5B ≈ 7B), and the frozen-backbone design avoids Coconut's catastrophic-forgetting damage to instruction-tuned models.
