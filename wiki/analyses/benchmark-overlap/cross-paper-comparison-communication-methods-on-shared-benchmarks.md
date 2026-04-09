Where multiple communication papers test on the same benchmark and model family, we can attempt normalized comparisons.

### GSM8K on Qwen 7B-Class Models (Debate Setting)

| Method | Model | GSM8K | Communication Type |
|---|---|---|---|
| Single agent | Qwen2.5-7B | 87.9% | None |
| NL debate | Qwen2.5-7B | 90.6% | Natural language |
| CIPHER | Qwen2.5-7B | 89.3% | Output embeddings |
| **SDE** | **Qwen2.5-7B** | **91.8%** | **State deltas** |

### GSM8K on Multi-Agent Systems (Qwen3 8B-Class)

| Method | Model | GSM8K | Agents |
|---|---|---|---|
| Single agent | Qwen3-8B | 81.1% | 1 |
| TextMAS | Qwen3-8B | 92.3% | 4 (sequential) |
| LatentMAS | Qwen3-8B | 93.8% | 4 (sequential) |
| **Agent Primitives** | **Qwen3-8B** | **94.2%** | **Variable (composed)** |

### Formal Logic (MMLU) on Qwen 7B-Class (Debate Setting)

| Method | Model | Formal Logic | Communication Type |
|---|---|---|---|
| Single agent | Qwen2.5-7B | 45.0% | None |
| NL debate | Qwen2.5-7B | 47.6% | Natural language |
| CIPHER | Qwen2.5-7B | 48.8% | Output embeddings |
| **SDE** | **Qwen2.5-7B** | **52.0%** | **State deltas** |

---
