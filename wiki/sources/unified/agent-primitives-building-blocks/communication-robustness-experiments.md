### Noise Injection (GSM8K, Qwen3-8B)

100 correctly-solved GSM8K instances, reasoning traces truncated to 6,000 tokens, passed to a second Qwen3-8B. Unrelated GSM8K reasoning sentences injected as noise.

| Noise sentences | 0 | 1 | 3 | 10 | 25 |
|----------------|---|---|---|----|----|
| Natural Language | 100% | 91% | 73% | 47% | 40% |
| KV Cache | 100% | 100% | 100% | **93%** | **77%** |

At 10 injected noise sentences, **KV-cache retains 93% accuracy vs. 47% for natural language** (a 46 pp gap). Even at extreme noise (25 sentences), KV-cache still achieves 77% vs. 40%.

### Long-Context Task Injection (InfiniteBench En.QA, 351 examples, Qwen3-8B)

Auxiliary instruction injected at beginning/mid/end of long context. Two metrics: accuracy on the original QA task, and compliance with the injected instruction.

| Method | Acc (no inj.) | Acc (begin) | Acc (mid) | Acc (end) | Compliance (begin) | Compliance (mid) | Compliance (end) |
|--------|--------------|-------------|-----------|-----------|-------------------|------------------|-------------------|
| Natural Language | 51.6% | 51.3% | 51.0% | 50.4% | 82.9% | **15.6%** | 100.0% |
| KV Cache | **61.3%** | **61.0%** | **60.4%** | **61.3%** | **88.9%** | **73.3%** | 100.0% |

KV-cache achieves **73.3% mid-context compliance vs. 15.6% for NL** — a 57.7 pp gap. Both methods achieve 100% compliance at end position. KV-cache also has ~10 pp higher baseline accuracy (61.3% vs. 51.6%).
