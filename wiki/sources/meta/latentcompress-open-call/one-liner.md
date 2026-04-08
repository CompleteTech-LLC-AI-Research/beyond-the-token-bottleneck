---
type: source-partial
parent: latentcompress-open-call
partial: one-liner
created: "2026-04-08"
updated: "2026-04-08"
---

**LatentCompress** compresses inter-agent messages into 4 slots × 64 dimensions = **512 bytes** via slot attention, matching baseline accuracy on GSM8K while replacing MB-scale KV-cache transfers (~1/2000 ratio). Establishes that the minimum bandwidth is **task-dependent** — GSM8K is lossless at 512B, GPQA is not — and foregrounds safety-by-bandwidth-constraint as a first-class design goal.
