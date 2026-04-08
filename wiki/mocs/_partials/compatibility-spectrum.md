---
type: moc-partial
partial: compatibility-spectrum
created: "2026-04-08"
updated: "2026-04-08"
---

Methods ranked by cross-architecture support, from most restrictive to most general.

| Method | Cross-Arch Support | Alignment Cost | Scaling | Key Limitation |
|--------|-------------------|----------------|---------|----------------|
| [[state-delta-trajectory\|SDE]] | Same weights only | None | N/A | Deltas only meaningful in shared weight space |
| [[kvcomm-kth-selective\|KVComm]] | Same architecture | None (training-free) | N/A | Requires identical layer structure |
| [[cipher-multiagent-debate-embeddings\|CIPHER]] | Shared tokenizer | None | N/A | Different tokenizers produce incompatible embeddings |
| [[activation-communication-harvard\|AC (no W)]] | Cross-family | None | N/A | Assumes roughly aligned activation spaces |
| [[activation-communication-harvard\|AC (with W)]] | Cross-family | 1 linear map per pair | $O(N^2)$ | 3,072 calibration sentences per pair |
| [[interlat-latent-space-agents\|Interlat]] | Cross-family | 1 adapter per model | O(N) | Requires adapter training (curriculum learning) |
| [[cache-to-cache-semantic-communication\|C2C]] | Cross-family + cross-size | 1 neural fuser per pair | $O(N^2)$ | Fuser training overhead |
| [[kv-cache-alignment-shared-space\|KV Cache Alignment]] | Cross-family + cross-size | 2 adapters per model | **O(N)** | Validated at small scale only |
| [[vision-wormhole-heterogeneous\|Vision Wormhole]] | Fully heterogeneous VLMs | 1 codec per model + ridge regression | **O(N)** | Requires VLM receivers |
