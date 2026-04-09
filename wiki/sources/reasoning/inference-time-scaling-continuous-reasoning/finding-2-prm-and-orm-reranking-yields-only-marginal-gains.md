### Best-of-N Across Reranking Methods (Table 1, GSM8K)

| N | Pass@N | Confidence | Self-Consistency | PRM-HE | PRM-SE | ORM |
|---|---|---|---|---|---|---|
| 1 | 31.08 | 31.08 | 31.08 | 31.08 | 31.08 | 31.08 |
| 2 | 35.10 | 31.08 | 31.01 | 31.69 | 30.86 | 31.61 |
| 4 | 38.67 | 30.48 | 31.61 | 32.45 | 32.37 | 32.15 |
| 8 | 41.02 | 29.87 | 31.24 | **33.06** | 32.52 | 31.46 |
| 16 | 42.61 | 31.39 | 32.15 | **33.36** | 32.37 | 32.37 |
| 32 | 44.43 | 30.71 | 32.15 | 32.83 | **33.28** | 31.39 |

**The gap is brutal**:
- Pass@N upper bound at N=16: **42.61%** (theoretical ceiling for this candidate pool)
- Best reranker (PRM-HE) at N=16: **33.36%** (+2.28pp over baseline)
- Realized fraction of the upper bound: **(33.36 − 31.08) / (42.61 − 31.08) = 19.8%**

PRM-HE is the best of the trained methods but recovers less than a quarter of the available headroom. **Confidence-based reranking is *worse* than the baseline at most $N$**, indicating that COCONUT's answer probabilities are completely uncalibrated. Self-consistency provides essentially zero gain — confirming directly that the majority answer is *systematically wrong*.

### Score Aggregation Strategies (Table 2)

To rule out the possibility that the issue is simple aggregation choice, Wang et al. compare last-step / min / max / mean aggregation following [Zhang et al., 2025]:

| N | Hard last | Hard min | Hard max | Hard mean | Soft last | Soft min | Soft max | Soft mean |
|---|---|---|---|---|---|---|---|---|
| 1 | 31.08 | 31.08 | 31.08 | 31.08 | 31.08 | 31.08 | 31.08 | 31.08 |
| 8 | 33.06 | 32.98 | 31.69 | 33.06 | 32.52 | 31.46 | 32.22 | 33.06 |
| 16 | 33.36 | 33.13 | 32.37 | 33.13 | 32.37 | 31.61 | 31.77 | 32.52 |
| 32 | 32.83 | 32.52 | 31.84 | 32.90 | 33.28 | 32.60 | 32.75 | 33.06 |

Aggregation choice changes results by less than 1pp. The bottleneck is *not* in how scores are combined — it is in the reward model's ability to assign meaningful scores in the first place.
