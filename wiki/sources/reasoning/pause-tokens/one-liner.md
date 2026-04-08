---
type: source-partial
parent: pause-tokens
partial: one-liner
created: "2026-04-08"
updated: "2026-04-08"
---

**Pause Tokens** appends $M$ copies of a learnable `<pause>` token to the input, widening the computational pathway with ~1024 extra params. Wins on 8/9 tasks at 1B scale (+19.5 EM on SQuAD) — the minimal existence proof that transformers exploit non-linguistic computation when given the room. The lower bound that all richer latent reasoning approaches must exceed.
