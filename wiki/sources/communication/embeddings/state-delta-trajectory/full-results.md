### Information Asymmetry (IA): 2 Agents, up to 5 Rounds

Agents hold disjoint private document corpora (3 passages each from BM25 top-6 retrieval) and must collaborate through Q&A to answer multi-hop questions. Greedy decoding throughout.

| Model | Method | Quasar-T EM | Quasar-T F1 | CWQ EM | CWQ F1 | StrategyQA Acc |
|-------|--------|------------|------------|--------|--------|---------------|
| **Qwen2.5-7B** | Single | 0.237 | 0.279 | 0.297 | 0.363 | 0.170 |
| | NL | 0.305 | 0.375 | 0.312 | 0.430 | 0.443 |
| | CIPHER | 0.282 | 0.357 | 0.297 | 0.404 | 0.373 |
| | **SDE** | **0.315** | **0.377** | **0.317** | **0.444** | **0.455** |
| **Llama3.1-8B** | Single | 0.233 | 0.281 | 0.247 | 0.324 | 0.150 |
| | NL | 0.285 | 0.350 | 0.325 | 0.429 | 0.497 |
| | CIPHER | 0.277 | 0.349 | 0.342 | 0.453 | 0.503 |
| | **SDE** | **0.305** | **0.367** | **0.352** | **0.464** | **0.548** |
| **Qwen2.5-14B** | Single | 0.327 | 0.385 | 0.347 | 0.426 | 0.453 |
| | NL | 0.372 | 0.445 | 0.375 | 0.497 | 0.673 |
| | CIPHER | 0.352 | 0.421 | 0.350 | 0.484 | 0.643 |
| | **SDE** | **0.372** | **0.444** | **0.382** | **0.498** | **0.682** |

Improvements are larger on multi-hop datasets (CWQ, StrategyQA) than simple factual QA (Quasar-T), confirming SDE is more effective for complex, multi-step reasoning. Llama-8B shows the largest gains, especially on StrategyQA (+4.5pp over CIPHER).

### Multi-Agent Debate (IS): 2 Agents, 3 Rounds

All agents share identical information. Default sampling with model-specific temperatures; results averaged over 3 independent runs.

| Model | Method | GSM8K | Abstract Algebra | College Math | Formal Logic |
|-------|--------|-------|-----------------|-------------|-------------|
| **Qwen2.5-7B** | Single | 0.879 | 0.477 | 0.390 | 0.450 |
| | NL | 0.906 | 0.458 | 0.362 | 0.476 |
| | CIPHER | 0.893 | 0.485 | 0.370 | 0.488 |
| | **SDE** | **0.918** | **0.517** | **0.443** | **0.520** |
| **Llama3.1-8B** | Single | 0.787 | 0.227 | 0.217 | 0.357 |
| | NL | 0.833 | 0.283 | 0.227 | 0.389 |
| | CIPHER | 0.817 | 0.215 | 0.195 | 0.353 |
| | **SDE** | **0.845** | **0.302** | **0.242** | **0.422** |
| **Qwen2.5-14B** | Single | 0.911 | 0.567 | 0.507 | 0.566 |
| | NL | 0.931 | 0.710 | 0.635 | 0.609 |
| | CIPHER | 0.930 | 0.650 | 0.635 | 0.568 |
| | **SDE** | **0.934** | **0.753** | **0.695** | **0.657** |

SDE enhances debate performance by **+0.3% to +13.7%** over best baseline. The largest gains appear on complex mathematical/logical reasoning (MMLU subsets), not arithmetic (GSM8K). CIPHER sometimes **underperforms NL** (e.g., Llama-8B Abstract Algebra: CIPHER 0.215 vs NL 0.283), while SDE consistently outperforms both.

### Agent Workflow (IS): Up to 7 Agents, Sequential (Qwen2.5-7B)

ReAct-style framework where agents collaborate sequentially: each agent generates a Thought + Action, receives an Observation from the environment (BM25-retrieved Wikipedia), then passes everything to the next agent. Up to 7 agents per question.

| Method | FEVER Acc | HotpotQA EM | HotpotQA F1 | StrategyQA Acc |
|--------|----------|------------|------------|---------------|
| Single | 0.007 | 0.157 | 0.219 | 0.157 |
| NL | 0.230 | 0.210 | 0.315 | 0.317 |
| CIPHER | 0.180 | 0.200 | 0.288 | 0.327 |
| **SDE** | **0.267** | **0.227** | **0.320** | **0.383** |

SDE achieves up to **+17.3%** over baselines (on StrategyQA: 0.383 vs NL 0.317). The workflow setting -- requiring more complex sequential reasoning -- benefits more from SDE than the IA setting with the same model on the same dataset (StrategyQA IA: +1.2pp; StrategyQA workflow: +5.6pp), confirming SDE is particularly effective for complex reasoning chains.
