### Organizer Model Choice

| Model backbone | Organizer | AIME25 | HumanEval+ | MedQA |
|---------------|-----------|--------|------------|-------|
| Qwen3-8B | GPT-5.2 | 73.3% | 82.3% | 76.7% |
| Qwen3-8B | Claude-4 | 73.3% | 81.1% | 76.2% |
| Qwen3-8B | Random | 66.7% | 77.4% | 70.6% |
| DS-R1-Llama-70B | GPT-5.2 | 56.7% | 85.3% | 81.9% |
| DS-R1-Llama-70B | Claude-4 | 56.7% | 83.5% | 81.9% |
| DS-R1-Llama-70B | Random | 50.0% | 78.6% | 69.5% |

GPT-5.2 and Claude-4 yield very similar results (within 0-2 pp). Random selection drops 5-7% on Qwen3-8B and up to **12.4%** on Llama-70B (MedQA). The benefit comes from **problem-aware structure selection**, not a specific Organizer model.

### Knowledge Pool Removal

| Model backbone | Knowledge Pool | AIME25 | HumanEval+ | MedQA |
|---------------|---------------|--------|------------|-------|
| Qwen3-8B | with | 73.3% | 82.3% | 76.7% |
| Qwen3-8B | without | 63.3% (-10.0) | 77.4% (-4.9) | 71.6% (-5.1) |
| DS-R1-Llama-70B | with | 56.7% | 85.3% | 81.9% |
| DS-R1-Llama-70B | without | 50.0% (-6.7) | 73.4% (-11.9) | 75.9% (-6.0) |

Removing the Knowledge Pool causes **5-12% degradation** depending on task and model. Worst case: HumanEval+ on Llama-70B drops 11.9 pp.

### RoPE Removal Impact Per Model

**Qwen3-8B** (moderate degradation):

| Method | AIME25 w/ | w/o | HumanEval+ w/ | w/o | MedQA w/ | w/o |
|--------|-----------|-----|---------------|-----|----------|-----|
| Review | 60.0 | 56.7 (-3.3) | 78.6 | 73.8 (-4.8) | 64.2 | 61.5 (-2.7) |
| Voting | 66.7 | 60.0 (-6.7) | 81.0 | 79.9 (-1.1) | 70.3 | 66.8 (-3.5) |
| Planning | 66.7 | 56.7 (-10.0) | 78.6 | 78.0 (-0.6) | 67.0 | 65.2 (-1.8) |
| Primitives MAS | 73.3 | 60.0 (-13.3) | 82.3 | 81.1 (-1.2) | 76.7 | 74.0 (-2.7) |

**DeepSeek-R1-Distill-Llama-70B** (catastrophic degradation):

| Method | AIME25 w/ | w/o | HumanEval+ w/ | w/o | MedQA w/ | w/o |
|--------|-----------|-----|---------------|-----|----------|-----|
| Review | 50.0 | 16.7 (-33.3) | 82.3 | 22.6 (-59.7) | 72.9 | 31.4 (-41.5) |
| Voting | 56.7 | 26.7 (-30.0) | 82.9 | 29.9 (-53.0) | 77.8 | 34.7 (-43.1) |
| Planning | 50.0 | 23.3 (-26.7) | 82.3 | 24.4 (-57.9) | 74.0 | 30.5 (-43.5) |
| Primitives MAS | 56.7 | 26.7 (-30.0) | 85.3 | 31.1 (-54.2) | 81.9 | 36.6 (-45.3) |

Without RoPE, LLaMA-based models lose **30-60 pp** across all methods. Qwen loses only **1-13 pp**. This is the most dramatic finding in the paper.

### Single vs. Composed Primitives

No single primitive dominates across tasks. Composing multiple primitives into a unified MAS yields **3.5-7.0% additional improvement** over the strongest individual primitive. For example on Qwen3-8B: best single primitive averages 71.3% (Voting) while composed MAS achieves 75.3%.
