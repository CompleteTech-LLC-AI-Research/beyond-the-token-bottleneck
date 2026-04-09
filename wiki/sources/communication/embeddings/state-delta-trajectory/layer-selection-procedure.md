SDE is applied to only **1-3 carefully selected layers** per model. Layers are chosen via a single preliminary experiment on the **2WikiMultihopQA** dataset (300 questions, information asymmetry setting). Each layer is evaluated individually; the top-k layers (by combined EM + F1) are selected and **fixed for all subsequent experiments**. 2WikiMultihopQA is excluded from all main evaluations.

**Selected layers per model** (from Appendix A, Table 6):

| Model | Total Layers | Layers Selected | Top-5 Layers (by EM+F1) |
|-------|-------------|-----------------|------------------------|
| Qwen2.5-7B | 28 | **Layer 22** (1 layer) | 22, 24, 9, 20, 12 |
| Llama3.1-8B | 32 | **Layers 17, 20** (2 layers) | 17, 20, 5, 8, 30 |
| Qwen2.5-14B | 48 | **Layers 21, 23, 33** (3 layers) | 33, 21, 23, 19, 36 |

The most effective layers tend to fall in **middle-to-late** positions (e.g., Layer 22 of 28 for Qwen-7B, Layer 17 of 32 for Llama-8B). However, some early layers also perform well (Layers 5 and 8 in Llama-8B), indicating flexibility. The number of selected layers scales with model size: 1 for 7B, 2 for 8B, 3 for 14B.
