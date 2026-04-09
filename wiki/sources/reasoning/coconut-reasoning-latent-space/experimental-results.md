All experiments use **GPT-2** as the base model — this is a small-scale proof of concept, not a demonstration at frontier scale.

### Main Results

| Dataset | CoT Acc. | Coconut Acc. | CoT Tokens | Coconut Tokens |
|---------|----------|--------------|------------|----------------|
| GSM8k (math) | 42.9% | 34.1% | 25.0 | 8.2 |
| ProntoQA (logic) | 98.8% | 99.8% | 92.5 | 9.0 |
| ProsQA (planning) | 77.5% | 97.0% | 49.4 | 14.2 |

Key observations:
- **ProsQA** (the paper's new DAG-based logical reasoning dataset, which demands planning and search): Coconut dramatically outperforms CoT (97.0% vs 77.5%). This is the task where BFS matters most.
- **ProntoQA** (simpler logical reasoning): Coconut matches CoT (~99.8%) with 10× fewer tokens.
- **GSM8k** (math): Coconut underperforms CoT (34.1% vs 42.9%) but with 3× fewer tokens. Math requires complex contextual understanding that benefits from the full expressiveness of language chains.

### Efficiency–Accuracy Trade-off

The critical comparison is not raw accuracy but the **Pareto frontier** of accuracy vs. tokens generated. When CoT models have their reasoning chains progressively shortened (via iCoT internalization), accuracy drops steeply. When Coconut replaces language steps with continuous thoughts, accuracy drops much more gradually. Coconut achieves better accuracy at every token budget below full CoT.

### Ablation Results

| Variant | GSM8k | ProntoQA | ProsQA |
|---------|-------|----------|--------|
| **Coconut (full)** | **34.1%** | **99.8%** | **97.0%** |
| w/o curriculum (direct training in final stage) | 14.4% | 52.4% | 76.1% |
| w/o thought (curriculum but no latent thoughts) | 21.6% | 99.9% | 95.5% |
| Pause as thought (learnable pause tokens) | 24.1% | 100.0% | 96.6% |
| Pause token baseline (Goyal et al.) | 16.4% | 77.7% | 75.9% |
| iCoT baseline (Deng et al.) | 30.0% | 99.8% | 98.2% |
| No-CoT baseline | 16.5% | 93.8% | 76.7% |

Critical findings:
- **Curriculum is essential**: Without it, Coconut collapses to near No-CoT performance. The model cannot learn latent reasoning from scratch with gradient descent alone.
- **Continuous thoughts > pause tokens**: On GSM8k, Coconut (34.1%) significantly outperforms pause-as-thought (24.1%), confirming that the hidden-state feedback carries real information beyond just providing extra compute.
- **The c hyperparameter matters**: Increasing c (latent thoughts per language step) from 0→1→2 steadily improves performance, validating that chaining more continuous thoughts scales reasoning ability.

### Decoding Continuous Thoughts

When a continuous thought is decoded to its nearest-neighbor tokens, the results are interpretable and often correspond to **intermediate variables** in the computation. For math problems, decoded thoughts reveal intermediate calculation results. This suggests the continuous thoughts are learning compressed but meaningful reasoning representations, not arbitrary vectors.
