### Benchmarks and Models

**8 benchmarks** across 3 categories:
- Math: AIME24, AIME25, MATH, GSM8K
- Code: HumanEval+, MBPP+
- Q&A: MedQA, GPQA-Diamond

**5 models**: Qwen3-4B, Qwen3-8B, Qwen3-14B, DeepSeek-R1-Distill-Qwen-32B, DeepSeek-R1-Distill-Llama-70B

### Primitives-based MAS vs. Single Agent (all 5 models, averages)

| Model | Single Avg | Primitives Avg | Gain |
|-------|-----------|---------------|------|
| Qwen3-4B | 55.7% | 69.6% | **+13.9%** |
| Qwen3-8B | 58.8% | 75.3% | **+16.5%** |
| Qwen3-14B | 65.5% | 77.6% | **+12.0%** |
| DeepSeek-R1-Distill-Qwen-32B | 71.0% | 77.6% | **+6.6%** |
| DeepSeek-R1-Distill-Llama-70B | 70.1% | 76.4% | **+6.3%** |

### Qwen3-8B Full Benchmark Breakdown

| Method | AIME25 | AIME24 | MATH | GSM8K | HumanEval+ | MBPP+ | MedQA | GPQA | Avg |
|--------|--------|--------|------|-------|-------------|-------|-------|------|-----|
| Single | 46.7 | 50.0 | 60.8 | 81.1 | 74.4 | 64.8 | 53.0 | 39.9 | 58.8 |
| TextMAS | 53.3 | 53.3 | 61.4 | 92.3 | 80.5 | 69.5 | 75.0 | 43.4 | 66.1 |
| LatentMAS | 53.3 | 56.7 | 62.6 | 93.8 | 80.5 | 74.6 | 75.3 | 45.5 | 67.8 |
| Review | 60.0 | 63.3 | 61.0 | 93.2 | 78.6 | 70.6 | 64.2 | 48.9 | 67.5 |
| Voting | 66.7 | 70.0 | 61.4 | 91.8 | 81.0 | 74.3 | 70.3 | 55.0 | 71.3 |
| Planning | 66.7 | 63.3 | 60.8 | 93.2 | 78.6 | 75.9 | 67.0 | 51.0 | 69.6 |
| **Primitives MAS** | **73.3** | **76.7** | **63.7** | **94.2** | **82.3** | **75.9** | **76.7** | **59.6** | **75.3** |

### DeepSeek-R1-Distill-Llama-70B Full Breakdown

| Method | AIME25 | AIME24 | MATH | GSM8K | HumanEval+ | MBPP+ | MedQA | GPQA | Avg |
|--------|--------|--------|------|-------|-------------|-------|-------|------|-----|
| Single | 50.0 | 70.0 | 69.6 | 92.4 | 82.3 | 66.4 | 64.5 | 65.2 | 70.1 |
| TextMAS | 53.3 | 70.0 | 72.8 | 93.2 | 82.3 | 68.8 | 77.8 | 65.7 | 73.0 |
| LatentMAS | 40.0 | 43.3 | 78.6 | 78.6 | 73.2 | 55.6 | 68.6 | 41.9 | 60.0 |
| **Primitives MAS** | **56.7** | **76.7** | **79.3** | **93.8** | **85.3** | **70.6** | **81.9** | **66.7** | **76.4** |

**LatentMAS catastrophically fails on LLaMA**: average drops from 70.1% to 60.0% (-10.1 pp). AIME24 drops from 70.0% to 43.3% (-26.7 pp), GSM8K from 92.4% to 78.6% (-13.8 pp), GPQA from 65.2% to 41.9% (-23.3 pp).

### vs. TextMAS and LatentMAS (Summary)

- **TextMAS**: only +2.4% to +7.3% average gain with high variance across tasks and models due to NL communication reliance
- **LatentMAS**: competitive on Qwen-based models (especially math) but catastrophically fails on LLaMA-based backbones (-10.1% on DeepSeek-R1-Distill-Llama-70B). Uses aggressive chunking ($m=40$) causing instability.
- **Primitives-based MAS**: stable across all model families, +6.3% to +16.5% average gain

### vs. 10 Existing MAS Methods (Llama-3-70B-Instruct)

| Method | MATH | GSM8K | HumanEval+ | GPQA |
|--------|------|-------|-------------|------|
| Single | 50.6 | 92.4 | 75.8 | 36.7 |
| Chain-of-Thought | 53.2 | 92.8 | 77.0 | 35.3 |
| Self-Consistency | 61.6 | 95.0 | 75.8 | 37.2 |
| LLM-Debate | 61.4 | 91.6 | 74.5 | 34.4 |
| Self-Refine | 58.5 | 90.8 | 62.7 | 38.3 |
| Quality-Diversity | 60.5 | 93.0 | 70.2 | 33.6 |
| SPP | 51.7 | 92.8 | 73.3 | 35.1 |
| AgentVerse | 55.6 | 93.4 | 73.9 | 40.2 |
| GPTSwarm | 55.4 | 93.2 | 73.9 | 36.5 |
| DyLAN | 59.6 | 91.2 | 75.8 | 36.0 |
| MAS-GPT | 68.7 | 93.4 | 78.9 | 37.6 |
| **Primitives MAS** | **72.4** | **93.8** | **82.3** | **53.2** |

Primitives-based MAS is best on **all 4 benchmarks**. The GPQA advantage is particularly striking: 53.2% vs. next-best 40.2% (AgentVerse), a +13.0 pp margin.
