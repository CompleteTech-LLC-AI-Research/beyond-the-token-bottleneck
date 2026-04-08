---
type: source-partial
parent: kvcomm-kth-selective
partial: one-liner
created: "2026-04-08"
updated: "2026-04-08"
---

**KVComm** shares the sender's KV-cache from only the most informative ~30% of layers (chosen via attention importance with a Gaussian prior favoring upper layers), matching or sometimes *exceeding* full-cache transfer. Training-free, but requires identical architecture. The "selective beats full" finding reframes the compression question: noisy layers can be actively harmful.
