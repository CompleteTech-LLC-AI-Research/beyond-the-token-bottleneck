---
type: source-partial
parent: activation-communication-harvard
partial: one-liner
created: "2026-04-08"
updated: "2026-04-08"
---

**Activation Communication (AC)** replaces the receiver's last-token residual-stream activation at layer ~26 with the sender's, requiring only one partial + one full forward pass (<¼ the compute of NL debate). Works cross-family (LLaMA ↔ Qwen ↔ Gemma) without learned projections — the strongest empirical evidence for the Platonic Representation Hypothesis.
