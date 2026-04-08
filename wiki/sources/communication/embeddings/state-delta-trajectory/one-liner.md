---
type: source-partial
parent: state-delta-trajectory
partial: one-liner
created: "2026-04-08"
updated: "2026-04-08"
---

**State Delta Encoding (SDE)** communicates inter-token hidden-state *differences* ($h_{t+1} - h_t$) rather than raw states, on the finding that the derivative of the hidden state carries more transferable information than the state itself. Deltas are context-agnostic — they capture only the reasoning dynamics — and are applied as additive steering vectors at selected receiver layers; requires identical model weights.
