---
type: moc-partial
partial: compression-ratios
created: "2026-04-08"
updated: "2026-04-08"
---

| System | Compression ratio | What's compressed | Task-dependent? |
|--------|------------------|-------------------|-----------------|
| [[softcot-efficient-reasoning\|SoftCoT]] | ~4× (soft vs hard tokens) | Reasoning cues | Mild |
| [[interlat-latent-space-agents\|Interlat]] (trained) | ~46× (full to 8-step) | Full reasoning trajectory | Moderate (4–6% drop) |
| [[kvcomm-kth-selective\|KVComm]] | ~3× (30% of layers) | Attention context | Strong (selective > full on some tasks) |
| [[latentcompress-open-call\|LatentCompress]] | ~2000× (MB to 512B) | Inter-agent message | Very strong (GSM8K: lossless; GPQA: lossy) |

The pattern: **the minimum sufficient bandwidth is not a fixed quantity — it scales with the intrinsic information complexity of the task.** Simple tasks (GSM8K, easy MATH) tolerate extreme compression because the relevant information is low-dimensional. Complex tasks (GPQA, multi-hop QA, Level-5 MATH) resist compression because the reasoning depends on high-dimensional context that cannot be summarized without loss.
