### Synthetic Validation

The identifiability theory is first validated on synthetic data:
- Random invertible transformations from multivariate Laplacian variables
- The sparsity-regularized autoencoder correctly identifies shared regions ($Z_A \cap Z_B$) and private regions ($Z_A \setminus Z_B$, $Z_B \setminus Z_A$), while a baseline without sparsity fails
- Mean Correlation Coefficient (MCC) exceeds the identifiability threshold across all settings (dimensionality 128-1024)

### Real-World Math Reasoning

Evaluated on MATH and GSM8K benchmarks, 3 agents, 2 debate rounds, across 5 models:

| Model | Method | MATH Acc. | GSM8K Acc. |
|-------|--------|-----------|------------|
| Qwen-3-0.6B | Single Answer | 45.8% | 58.2% |
| | Multiagent Finetuning | 71.2% | 70.8% |
| | **ThoughtComm** | **85.0%** | **75.8%** |
| Qwen-3-1.7B | Single Answer | 43.6% | 67.4% |
| | Multiagent Finetuning | 75.8% | 84.2% |
| | **ThoughtComm** | **93.0%** | **85.0%** |
| Phi-4-mini (3.84B) | Single Answer | 63.8% | 81.6% |
| | Multiagent Finetuning | 60.2% | 82.2% |
| | **ThoughtComm** | **74.6%** | **84.2%** |
| LLaMA-3-8B | Single Answer | 36.2% | 60.8% |
| | Multiagent Finetuning | 39.7% | 69.2% |
| | **ThoughtComm** | **45.6%** | **68.4%** |
| DeepSeek-R1-Distill-8B | Single Answer | 42.6% | 65.6% |
| | Multiagent Finetuning | 72.4% | 76.8% |
| | **ThoughtComm** | **82.8%** | **80.8%** |

Key observations:
- **Consistent improvement** across all 5 models and both benchmarks, from 0.6B to 8B parameters
- **Largest relative gains on smaller models**: Qwen-3-1.7B sees +17.2% absolute over multiagent finetuning on MATH — a 113.3% relative improvement over single answer
- **Consensus improves alongside accuracy**: ThoughtComm improves inter-agent agreement, meaning the gains come from genuine alignment, not just individual agent improvement

### Scaling with Debate Rounds

A critical differentiator: **ThoughtComm improves with more debate rounds** (accuracy and consensus both increase from 2→6 rounds), while multiagent finetuning **degrades** (accuracy drops, consensus plateaus). This suggests that language-based debate introduces redundant or confusing information over many rounds, while thought-based communication consistently surfaces true latent structure.

### Prefix Length Robustness

Performance is remarkably stable across prefix lengths $m \in \{1, 4, 8, 16\}$, with fluctuations under 5%. Near-optimal performance is achieved with **a single prefix vector** ($m=1$), demonstrating the information density of the latent representation. A single prefix embedding, unconstrained in $\R^d$, encodes far more than a single token embedding (which is tied to a discrete vocabulary item and typically occupies a lower-dimensional subspace).
