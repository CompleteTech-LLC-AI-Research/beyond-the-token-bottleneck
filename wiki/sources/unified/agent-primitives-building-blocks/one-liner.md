---
type: source-partial
parent: agent-primitives-building-blocks
partial: one-liner
created: "2026-04-08"
updated: "2026-04-08"
---

**Agent Primitives** decomposes MAS into three reusable computation patterns — **Review** (iterative critique), **Voting and Selection** (consensus), **Planning and Execution** (decomposition) — all operating in latent space via KV-cache concatenation, with an Organizer agent composing them per-query. +6.3% to +16.5% over single agents across 5 model families with only 1.3–1.6× latency overhead; **RoPE positional re-encoding is mandatory** for LLaMA-based models (without it, ~27–60pp accuracy drops).
