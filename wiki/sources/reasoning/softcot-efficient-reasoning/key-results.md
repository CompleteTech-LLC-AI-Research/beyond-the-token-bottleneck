### LLaMA-3.1-8B-Instruct (averages over 5 seeds)

| Benchmark | Zero-Shot CoT | SoftCoT | Δ |
|-----------|--------------|---------|---|
| GSM8K | 79.61% | 81.03% | +1.42 |
| ASDiv-Aug | 86.78% | 87.19% | +0.41 |
| AQuA | 54.65% | 56.30% | +1.65 |
| StrategyQA | 65.63% | 69.04% | +3.41 |
| Date Understanding | 54.40% | 59.04% | +4.64 |
| **Average** | **68.21%** | **70.52%** | **+2.31** |

### Qwen2.5-7B-Instruct

| Benchmark | Zero-Shot CoT | SoftCoT | Δ |
|-----------|--------------|---------|---|
| GSM8K | 83.70% | 85.81% | +2.11 |
| AQuA | 64.53% | 72.44% | +7.91 |
| StrategyQA | 49.65% | 60.61% | +10.96 |
| **Average** | **70.29%** | **75.06%** | **+4.77** |

Gains are especially large on tasks requiring commonsense reasoning (StrategyQA) and multiple-choice reasoning (AQuA). SoftCoT is orthogonal to self-consistency — combining them yields GSM8K 90.63%.
