---
type: source-partial
parent: thinking-states-latent-reasoning
partial: one-liner
created: "2026-04-08"
updated: "2026-04-08"
---

**Thinking States** generates natural-language thoughts at chunk boundaries during input processing, then compresses them into fixed-size continuous states injected back at shallow layers. Preserves auditability by construction — the intermediate reasoning is briefly visible before compression — while matching CoT on 2-hop QA at 1.19–2.66× speedup. Uses teacher forcing rather than BPTT, enabling parallel training.
