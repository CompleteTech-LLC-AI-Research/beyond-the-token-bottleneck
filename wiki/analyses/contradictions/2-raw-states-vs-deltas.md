**Claim A**: Sharing raw hidden states outperforms text communication. AC shows activation replacement outperforms NLD on 48/57 MMLU topics.
— [[activation-communication-harvard|AC (Ramesh & Li, 2025)]]

**Claim B**: Raw hidden states sometimes **degrade below the natural language baseline**. Deltas (inter-token differences) consistently outperform raw states.
— [[state-delta-trajectory|SDE (Tang et al., 2025)]]

**Status**: **Genuine tension, same regime**. Both test on similar model sizes and benchmarks. The discrepancy may be due to:
- [[activation-communication-harvard|AC]] shares a single layer's activation; [[state-delta-trajectory|SDE]] shares multi-layer deltas — different information content
- AC uses replacement/sum/mean aggregation; SDE uses additive injection — different integration methods
- The tasks where raw states degrade in SDE may be tasks where AC would also struggle

**Resolution needed**: A controlled comparison using the same models, benchmarks, and injection method, varying only whether raw states or deltas are transmitted.

---
