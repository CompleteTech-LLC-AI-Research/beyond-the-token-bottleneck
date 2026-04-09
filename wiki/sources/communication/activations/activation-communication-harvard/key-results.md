### Multi-Player Coordination Games (same model, A = B)

| Model | Game | Silent ($\emptyset$) | Skyline | NL | AC (replace) |
|-------|------|-----------|---------|-----|-------------|
| LLaMA-3.2-3B | Countries | 0.0% | 84.0% | 69.0% | **78.0%** |
| LLaMA-3.2-3B | Tip Sheets | 38.6% | 100.0% | 74.3% | **90.0%** |
| LLaMA-3.1-8B | Countries | 2.0% | 86.0% | 77.0% | **83.0%** |
| LLaMA-3.1-8B | Tip Sheets | 54.3% | 100.0% | 85.7% | **95.7%** |

AC nearly closes the gap between zero-communication and the single-agent skyline, substantially outperforming NL communication.

### Cross-Model Reasoning (LLaMA-3.2-3B → LLaMA-3.1-8B)

| Benchmark | 3B alone | 8B alone | NLD | AC | AC(W) |
|-----------|----------|----------|-----|-----|-------|
| Biographies | 79.4% | 83.9% | 80.2% | **84.6%** | **86.8%** |
| GSM8k | 58.0% | 60.0% | **75.0%** | 64.0% | 66.0% |
| HS Psychology | 30.0% | 65.0% | 83.0% | **85.0%** | 70.0% |
| Formal Logic | 16.0% | 42.0% | 37.0% | **47.0%** | 35.0% |
| College Biology | 11.0% | 50.0% | 71.0% | **78.0%** | **79.0%** |
| Professional Law | 0.0% | 20.0% | **30.0%** | **30.0%** | **45.0%** |
| Public Relations | 26.0% | 53.0% | 63.0% | **74.0%** | 63.0% |

AC outperforms NLD on **6 of 7 benchmarks**, with up to **27.0% improvement** (Public Relations: 63%→74%; College Biology: 71%→78%). The learned mapping $W$ provides further gains on 4/7 datasets.

**Exception: GSM8K** — NLD (75%) beats AC (64%). Multi-step mathematical reasoning benefits from **iterative refinement** across debate rounds; single-shot activation grafting communicates knowledge but doesn't enable the back-and-forth error correction that debate provides. This highlights that AC and debate serve complementary functions.

### Full MMLU
AC matches or outperforms NLD on **48 of 57 MMLU datasets**. Average: AC 62.7% vs NLD 60.7%.

### Cross-Family Communication (no learned mapping W)

| Model Pair (A → B) | NLD (Bio/GSM) | AC (Bio/GSM) |
|---------------------|---------------|--------------|
| LLaMA-3.2-3B → LLaMA-3.1-8B | 80.2/75.0 | **84.6/64.0** |
| Qwen-2.5-1.5B → Qwen-2.5-3B | 63.2/65.0 | **89.6/70.0** |
| Gemma-2-2B → Gemma-2-9B | 70.3/70.0 | **88.1/90.0** |
| Qwen-2.5-1.5B → LLaMA-3.2-3B | 75.4/75.0 | **79.5/75.0** |
| LLaMA-3.2-3B → Gemma-2-2B | 62.5/55.0 | **84.0/60.0** |

AC works across LLaMA, Qwen-2.5, and Gemma-2 families **without** learned projections.  This is remarkable — these models have different tokenizers, vocabularies, training data, and architectures. The authors cite this as possible evidence for the **[[platonic-representation-hypothesis|Platonic Representation Hypothesis]]** (Huh et al., 2024): independently trained models may converge to similar internal representations of the same concepts.

### Compute Efficiency

Formal analysis shows AC requires:
- **A**: 1 partial forward pass (k/L of a full pass)
- **B**: 1 full forward pass
- **Total**: < ¼ the compute of NLD (which requires M full forward passes of A for an M-token message, plus T forward passes of B on the extended prompt)

The **performance-per-FLOP ratio** (slope of accuracy vs. compute) is consistently steeper for AC than NLD across model scales — AC achieves greater improvement per additional unit of compute.

### Directionality

Swapping A and B (smaller model does full forward pass) yields lower accuracy but still beats both single-model baselines and sometimes NLD. This is more compute-efficient since the smaller model does the full pass.
