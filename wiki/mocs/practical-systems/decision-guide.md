Use this table to narrow your method choice based on deployment constraints:

| Constraint | Recommended Methods | Avoid |
|---|---|---|
| **Zero training budget** | [[latentmas-collaboration\|LatentMAS]], [[agent-primitives-building-blocks\|Agent Primitives]], [[kvcomm-kth-selective\|KVComm]], [[state-delta-trajectory\|SDE]] | Coconut, Interlat, ThoughtComm |
| **Cross-architecture required** | [[activation-communication-harvard\|AC]], [[cache-to-cache-semantic-communication\|C2C]], [[vision-wormhole-heterogeneous\|Vision Wormhole]] | LatentMAS, KVComm, SDE |
| **Latency-critical (<2x single)** | Agent Primitives (1.3-1.6x latency), [[kvcomm-duke-online-reuse\|KVCOMM-online]] for prefill | Hybrid MAS (6.2x turns overhead), TextMAS (3.5-5.3x latency) |
| **LLaMA-family backbone** | Agent Primitives (with RoPE re-encoding) | LatentMAS (catastrophic on LLaMA) |
| **Maximum accuracy** | Agent Primitives composed (75.3% avg on Qwen3-8B) | Independent MAS (-70% on sequential tasks) |
| **Minimal bandwidth** | [[latentcompress-open-call\|LatentCompress]] slots (512B), [[cipher-multiagent-debate-embeddings\|CIPHER]] | Full KV-cache transfer (~MB) |
| **Safety/auditability required** | LatentCompress (slot-attention probing), [[thought-communication-multiagent\|ThoughtComm]] (identifiable factors) | Raw hidden-state transfer (opaque) |

### 8. Cross-Cutting Analyses

- **[[benchmark-overlap|Benchmark Overlap Analysis]]** — Maps which benchmarks appear across multiple papers, exposing where results are directly comparable and where claimed improvements may reflect benchmark selection rather than genuine gains. Essential context for interpreting the method comparison table above.
- **[[contradictions|Contradictions]]** — Documents deployment-relevant tensions across the literature, including conflicting claims about training-free viability, cross-architecture compatibility by depth, and when MAS helps vs. hurts. Read this to understand the caveats behind the Decision Guide.
- **[[paper-timeline|Paper Timeline]]** — Chronological view of all 27 papers showing the field's acceleration from theoretical foundations (2022-2023) through the 2025 Cambrian explosion to 2026 unification. Useful for understanding which results build on which, and for gauging the maturity of different approaches.
