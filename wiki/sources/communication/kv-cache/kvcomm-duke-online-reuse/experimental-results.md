### Efficiency Gains

| Setting | Prefill Speedup | Reuse Rate |
|---------|----------------|------------|
| 2 agents, GSM8K | 2.5× | 95% |
| 3 agents, GSM8K | 4.2× | 95% |
| 4 agents, GSM8K | 6.1× | 95% |
| 5 agents, GSM8K (512 prefix, 1K input) | **7.8×** | 95% |
| Average across workloads | **6.7×** | **70%+** |

TTFT (Time to First Token) drops from 430ms to 55ms in the 5-agent setting.

### Quality Preservation

| Dataset | Original Accuracy | KVCOMM Accuracy | Drop |
|---------|------------------|-----------------|------|
| MMLU (5 agents) | 69.9% | 69.9% | 0.0% |
| GSM8K (4 agents) | 68.0% | 66.6% | <2.5% |
| HumanEval (3 agents) | Pass@1 maintained | Comparable | Minimal |

KVCOMM achieves **>70% reuse rate** across diverse workloads (RAG, math reasoning, collaborative coding) with negligible quality degradation.

### Comparison to CacheBlend

CacheBlend (selective recomputation baseline) achieves similar reuse rates but uses a fixed acceleration policy that doesn't adapt to varying prefix contexts. KVCOMM's online anchor-based approach adapts dynamically, maintaining quality across diverse prefix variations.
