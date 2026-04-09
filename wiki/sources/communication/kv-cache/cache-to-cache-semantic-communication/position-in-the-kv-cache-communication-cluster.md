C2C addresses **how to fuse across architectures** — the cross-model projection problem. It pairs with:
- [[kvcomm-kth-selective|KVComm]]: which addresses **what to share** (layer selection for same-architecture models)
- [[kvcomm-duke-online-reuse|KVCOMM-online]]: which addresses **how to make sharing efficient** (cache reuse via offset estimation)

The three papers together cover complementary dimensions of [[kv-cache-communication]].
