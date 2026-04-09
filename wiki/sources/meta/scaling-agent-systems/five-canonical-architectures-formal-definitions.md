The system S = (A, E, C, O) consists of agents A = {a_1, ..., a_n}, shared environment E, communication topology C, and orchestration policy O.

### Single-Agent System (SAS)
- |A| = 1, zero communication overhead
- Complexity: O(T) where T = max iterations
- Memory: O(T), sequential processing only

### Independent MAS
- C = {(a_i, agg) : all i} — agent-to-aggregator only, **no peer communication**
- Policy: synthesis_only (concatenates sub-agent outputs without cross-validation)
- LLM calls: O(nT) + O(1), sequential depth = 1, parallelization factor = n
- Memory: O(n * T), maximal parallelization but minimal coordination

### Centralized MAS
- C = {(orch, a_i) : all i} — orchestrator-to-agents only (hub-spoke)
- Policy: hierarchical — orchestrator decomposes tasks, coordinates R rounds across n sub-agents
- LLM calls: O(nT) + O(nR), sequential depth = R, parallelization factor = n
- Memory: O(n * T * R), creates validation bottleneck at orchestrator

### Decentralized MAS
- C = {(a_i, a_j) : all i,j where i != j} — all-to-all topology
- Policy: consensus — agents debate in D sequential rounds
- LLM calls: O(nT) + O(1), sequential depth = D
- Memory: O(n * T * D), each agent stores own debate history

### Hybrid MAS
- C = star_edges + peer_edges — orchestrator plus limited peer-to-peer
- Policy: hierarchical + lateral — combines orchestrator control with directed peer communication
- LLM calls: O(nT) + O(nR) + O(nP) where P = peer rounds
- Memory: O(n * T * R + n * P), inherits orchestrator control while enabling lateral exchange
