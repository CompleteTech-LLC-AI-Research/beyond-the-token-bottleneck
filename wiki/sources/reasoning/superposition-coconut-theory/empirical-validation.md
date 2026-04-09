### Training Setup

- **Model**: GPT-2 style decoder, 2 layers, $d_{\text{model}} = 768$, $n_{\text{heads}} = 8$, trained from scratch
- **Dataset**: ProsQA (subset requiring 3-4 reasoning hops), from Hao et al. (2024)
  - Train: 14,785 problems, avg $|V| = 22.8$, avg $|E| = 36.5$, avg solution length 3.5
  - Val: 257 problems; Test: 419 problems
- **Training**: AdamW ($\beta_1 = 0.9$, $\beta_2 = 0.95$, weight decay $10^{-2}$), constant lr $= 10^{-4}$, multi-stage curriculum (stage $i$ trains with $i$ continuous thoughts), 25 epochs per stage, 300 epochs total
- **Compute**: ~24 hours on 2 NVIDIA A100 80GB GPUs

### Overall Accuracy

| Method | Accuracy |
|--------|----------|
| No CoT (2-layer) | ~75% |
| CoT (2-layer) | ~75% |
| CoT* (12-layer, 12 heads) | ~83% |
| **Coconut (2-layer)** | **~99%** |

A 2-layer Coconut model achieves near-perfect accuracy on ProsQA while both CoT baselines (including a much larger 12-layer model) fail to reliably solve the task. Random guessing baseline is 50%.

### Layer 1 Attention Patterns

Attention maps confirm the theoretical construction: edge tokens $\langle e \rangle$ attend almost exclusively to their source and target nodes, placing nearly all attention mass on exactly the predicted positions. This validates that the model has learned the information-gathering mechanism from the construction.

### Layer 2 Attention Scores by Edge Category

| Edge Category | Step 1 | Step 2 | Step 3 | Step 4 |
|---------------|--------|--------|--------|--------|
| **Not Reachable** | 0.04 $\pm$ 0.07 | 0.03 $\pm$ 0.09 | 0.08 $\pm$ 0.17 | 0.12 $\pm$ 0.20 |
| **Reachable** | 2.12 $\pm$ 1.07 | 0.71 $\pm$ 0.92 | 0.38 $\pm$ 0.72 | 0.29 $\pm$ 0.66 |
| **-- Frontier** | 2.12 $\pm$ 1.07 | 1.00 $\pm$ 0.96 | 0.67 $\pm$ 0.87 | 0.61 $\pm$ 0.95 |
| **-- Optimal** | 2.54 $\pm$ 1.03 | 1.72 $\pm$ 1.13 | 1.67 $\pm$ 1.20 | 2.23 $\pm$ 1.35 |

The model sharply concentrates attention on **Reachable** edges (mean score ~2.12 vs ~0.04 for Not Reachable at step 1), exactly as the theory predicts. Additional biases toward **Frontier** and **Optimal** edges emerge from training signals.

### Representation Analysis (Inner Products)

Inner products between continuous thought vectors $t_i$ and node embeddings $u_v$ show clear hierarchical separation across 3 random seeds:

| Node Category | Step 1 | Step 2 | Step 3 | Step 4 |
|---------------|--------|--------|--------|--------|
| **Not Reachable** | -0.37 to -0.25 | -0.26 to -0.04 | -0.09 to 0.02 | -0.27 to -0.23 |
| **Reachable** | 3.59 to 3.71 | 1.37 to 1.55 | 0.62 to 0.80 | 0.53 to 0.66 |
| **-- Frontier** | 5.09 to 5.38 | 2.45 to 2.69 | 1.95 to 2.11 | 2.12 to 2.29 |
| **-- Optimal** | 6.41 to 6.84 | 4.67 to 5.11 | 5.44 to 6.43 | 8.98 to 9.58 |

The separation pattern (Not Reachable $\ll$ Reachable $<$ Frontier $<$ Optimal) is consistent across all 3 runs, confirming the superposition representation is a stable, reproducible phenomenon.

### BFS Emerges Without Multi-Path Supervision

**COCONUT-BFS experiment.** When training supervision is drawn uniformly from frontier nodes (not just the optimal path), the model achieves the same near-perfect accuracy. Crucially, comparing inner product distributions between standard Coconut and Coconut-BFS reveals:

- **Coconut-BFS** learns expected BFS behavior (uniform attention to frontier nodes)
- **Standard Coconut** (trained only on optimal paths) **still** assigns elevated weight to non-optimal frontier nodes compared to non-frontier reachable nodes

This means **BFS emerges from training dynamics, not from explicit supervision**. The model discovers that parallel frontier exploration is the efficient algorithm for reachability, even when training data only shows single optimal paths.
