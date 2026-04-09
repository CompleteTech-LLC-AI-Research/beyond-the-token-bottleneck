Evaluated on 9 model pairs across 8 datasets (Countries, Tipsheets, HotpotQA, QASPER, MuSiQuest, MultiFieldQA-en, 2WikiMQA, TMATH).

### Key Comparisons

| Method | Complex task performance (HotpotQA F1) | Layers transmitted |
|--------|---------------------------------------|-------------------|
| Baseline (no communication) | 0.23 | 0 |
| NLD (natural language debate) | 0.43 | N/A (full decode) |
| CIPHER (embedding communication) | 0.50 | N/A (full decode) |
| AC — replace (hidden state replacement) | 0.05 | 1 layer |
| AC — mean (hidden state averaging) | 0.25 | 1 layer |
| **KVComm (30% layers)** | **0.46** | **~10 layers** |
| **KVComm (50% layers)** | **0.57** | **~16 layers** |
| **KVComm (70% layers)** | **0.65** | **~22 layers** |
| Skyline (full context concat) | 0.73 | All (upper bound) |

Critical observations:
- **KVComm at 70% matches or approaches Skyline** across most datasets — near-optimal communication with 30% less data transmitted
- **KVComm at 30% already outperforms NLD, CIPHER, and AC** — even minimal KV sharing beats full natural language or embedding communication
- NLD and CIPHER perform well on simple datasets (Countries, Tipsheets) where only small, salient information needs transfer, but **fail on complex long-context tasks** where the sender has context the receiver needs
- **KVComm sometimes exceeds Skyline** — selective KV sharing can act as regularization, filtering noise

### Efficiency

Compared to NLD, KVComm eliminates all decode steps for the sender — only a single prefill pass is needed. The computation margin is $O(L(T_s + T_r + |Q|)^2 d)$ where $T_s, T_r$ are debate token counts.
