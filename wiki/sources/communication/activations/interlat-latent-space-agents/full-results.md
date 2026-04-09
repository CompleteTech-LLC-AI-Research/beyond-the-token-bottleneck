### ALFWorld Results (All Models, All Methods)

**Qwen2.5-7B-Base:**

| Method | Seen | Unseen |
|---|---|---|
| **Interlat** | **70.48** | **65.42** |
| Text (CoT plan as input) | 64.29 | 62.44 |
| No-Comm | 62.14 | 62.19 |
| CoT (full, baseline) | 67.14 | 64.93 |
| No-CoT (baseline) | 65.71 | 62.69 |
| CrossTask | 61.43 | 61.94 |
| Noised (CovNoise-0.5x) | 64.29 | 60.95 |
| Noised (CovNoise-1.0x) | 63.81 | 63.68 |
| WhiteNoise | 61.90 | 61.19 |
| CovGauss-0 | 60.00 | 61.94 |
| CovGauss-mu | 65.71 | 64.93 |
| RandomRot | 57.86 | 63.68 |
| **Qwen2LLaMA (cross-family)** | **70.95** | **71.39** |

**Qwen2.5-0.5B-Base:**

| Method | Seen | Unseen |
|---|---|---|
| **Interlat** | **61.19** | **57.46** |
| Text | 54.52 | 47.26 |
| No-Comm | 50.48 | 44.03 |
| CoT (full) | 57.86 | 50.75 |
| No-CoT | 57.14 | 50.25 |
| CrossTask | 53.57 | 47.01 |
| WhiteNoise | 57.38 | 57.21 |
| CovGauss-0 | 13.81 | 13.18 |
| CovGauss-mu | 44.52 | 34.33 |
| RandomRot | 59.05 | 51.99 |

**LLaMA3.1-8B-Base:**

| Method | Seen | Unseen |
|---|---|---|
| **Interlat** | **70.71** | **70.90** |
| Text | 62.86 | 60.82 |
| No-Comm | 63.57 | 58.40 |
| CoT (full) | 69.35 | 70.82 |
| No-CoT | 67.18 | 70.34 |
| CrossTask | 65.00 | 63.43 |
| CovNoise-0.5x | 64.29 | 65.68 |
| CovNoise-1.0x | 58.57 | 64.93 |
| WhiteNoise | 61.43 | 64.93 |
| CovGauss-0 | 57.86 | 66.42 |
| CovGauss-mu | 60.71 | 64.93 |
| RandomRot | 57.86 | 63.44 |

### MATH Benchmark Results (Qwen2.5-7B)

| Method | Overall | Level-3 | Level-4 | Level-5 |
|---|---|---|---|---|
| **Interlat** | 36.88 | 40.08 | 27.45 | **15.80** |
| Text | 34.35 | 37.60 | 26.30 | 14.20 |
| No-Comm | 33.27 | 36.40 | 26.20 | 13.10 |
| CoT (full) | **38.35** | **45.65** | **31.19** | 15.05 |
| No-CoT | 36.25 | 40.10 | 26.80 | 14.80 |

CoT wins on easier problems (linguistic constraints act as beneficial regularizer, pruning search space). **Interlat surpasses CoT on Level-5** — the hardest problems — because forced text discretization causes "premature collapse" of the reasoning distribution, while Interlat maintains a superposition of parallel hypotheses in continuous space.

### Cross-Family Results

**Qwen2.5-7B-Instruct (sender) -> LLaMA3.1-8B-Base (actor)**: 70.95% seen / 71.39% unseen. This is the **best result in the entire paper**, beating even same-family Interlat. Since Qwen and LLaMA have distinct latent manifolds, the improvement cannot be attributed to superficial architectural compatibility — it suggests genuine latent-level inter-agent understanding that transfers across heterogeneous representations. Aligns with findings that heterogeneous LLM agents outperform homogeneous ensembles due to complementary inductive biases.

### Compression Table (Qwen2.5-7B-Base, Full Detail)

**Training-free (ratio R of full-length latents retained):**

| Ratio | Seen | Unseen | Latency |
|---|---|---|---|
| Full (100%) | 70.48 +/- 1.01 | 65.42 +/- 0.87 | 9.19s |
| 90% | 68.57 +/- 1.63 | 67.16 +/- 1.97 | - |
| 80% | 68.10 +/- 1.83 | 61.69 +/- 1.43 | - |
| 70% | 67.14 +/- 1.82 | 63.43 +/- 2.24 | - |
| 60% | 66.43 +/- 1.63 | 59.20 +/- 3.69 | - |
| 50% | 72.14 +/- 1.48 | 61.19 +/- 2.84 | - |
| 40% | 66.90 +/- 2.31 | 59.95 +/- 2.64 | - |
| 30% | 65.95 +/- 2.12 | 62.19 +/- 1.58 | - |
| 20% | 67.86 +/- 3.23 | 61.44 +/- 1.58 | - |
| 10% | 67.86 +/- 2.12 | 62.44 +/- 2.64 | - |
| 5% | 64.52 +/- 1.12 | 60.95 +/- 1.35 | - |
| 0% (no comm) | 62.14 +/- 2.01 | 62.19 +/- 2.32 | - |

**Untrained compression (direct truncation to fixed length):**

| Length | Seen | Unseen | Latency |
|---|---|---|---|
| 128L | 64.52 +/- 2.26 | 60.20 +/- 2.06 | 3.55s |
| 64L | 66.19 +/- 1.95 | 61.44 +/- 4.32 | 1.83s |
| 32L | 63.57 +/- 2.01 | 60.20 +/- 3.58 | 1.03s |
| 16L | 64.29 +/- 1.34 | 59.95 +/- 3.01 | 0.62s |
| 8L | 64.05 +/- 2.18 | 57.46 +/- 2.69 | 0.39s |

**Trained compression (reasoning model generates compressed latents):**

| Length | Seen | Unseen | Latency |
|---|---|---|---|
| 128L | 68.10 +/- 1.93 | 62.94 +/- 2.03 | 2.25s |
| 64L | 67.14 +/- 1.56 | 61.94 +/- 2.13 | 1.16s |
| 32L | 66.90 +/- 1.46 | 61.94 +/- 2.56 | 0.60s |
| 16L | 66.43 +/- 2.05 | 61.69 +/- 2.56 | 0.33s |
| **8L** | **66.43 +/- 1.22** | **60.45 +/- 2.23** | **0.20s** |

Trained 8-step compression: 66.43% seen (vs 70.48% full = ~4% drop), with **46x speedup** (9.19s to 0.20s). The bridge module eliminates decode-re-encode overhead.

**LLaMA3.1-8B-Base Trained Compression:**

| Length | Seen | Unseen | Latency |
|---|---|---|---|
| 128L | 66.46 +/- 1.98 | 66.35 +/- 1.86 | 2.80s |
| 64L | 66.21 +/- 1.72 | 65.42 +/- 1.94 | 1.40s |
| 32L | 65.45 +/- 1.63 | 65.01 +/- 1.88 | 0.72s |
| 16L | 64.41 +/- 1.95 | 65.20 +/- 1.76 | 0.39s |
| 8L | 64.32 +/- 1.84 | 64.89 +/- 1.69 | 0.24s |

LLaMA compression degrades even more gracefully — 8L unseen (64.89%) vs full (70.90%) is only ~6%.

### Full Ablation Table (with Steps)

**Actor Model Ablations (Qwen2.5-7B-Base):**

| Method | Seen | Steps (succ/all) | Unseen | Steps (succ/all) |
|---|---|---|---|---|
| Full | 70.48 +/- 1.01 | 9.41/12.54 | 65.42 +/- 0.87 | 9.86/13.37 |
| w/o curriculum | 33.10 +/- 2.97 | 9.07/16.38 | 20.65 +/- 2.15 | 10.47/18.03 |
| w/o $\Loss_{\text{sep}}$ | 58.81 +/- 1.41 | 8.07/12.98 | 60.70 +/- 5.50 | 9.64/13.71 |
| w/o $\Loss_{\text{align}}$ | 56.90 +/- 1.41 | 8.16/13.26 | 53.98 +/- 3.35 | 9.56/14.36 |
| w/o adapter | 4.05 +/- 1.70 | 9.32/19.57 | 4.48 +/- 1.31 | 10.53/19.58 |

Without adapter: model generates fluent, coherent responses but **cannot complete tasks** (4.05% seen) — the adapter bridges representation spaces. Without curriculum: 33.10%, with 16.38 avg steps (all) indicating unstructured wandering. Without $\Loss_{\text{sep}}$: model shortcuts to ignoring latent input. Without $\Loss_{\text{align}}$: model exploits separation objective with non-useful divergence.

**Reasoning Model Ablations (Compression, K=128):**

| Method | Seen | Steps (succ/all) | Unseen | Steps (succ/all) |
|---|---|---|---|---|
| Full | 68.10 +/- 1.93 | 9.21/12.65 | 62.94 +/- 2.03 | 9.88/13.63 |
| w/o $\Loss_{\text{task}}$ | 65.71 +/- 1.43 | 8.86/12.68 | 63.18 +/- 3.47 | 9.68/13.48 |
| w/o $\Loss_{\text{pref}}$ | 64.76 +/- 2.97 | 8.92/12.82 | 60.20 +/- 3.13 | 9.68/13.79 |
| w/o $\Loss_{\text{geom}}$ | 64.05 +/- 3.55 | 8.71/12.77 | 59.45 +/- 3.01 | 9.88/13.98 |

$\Loss_\text{geom}$ **is the most critical** compression loss — preserving geometric consistency between compressed and uncompressed latents matters most. Removing $\Loss_\text{task}$ slightly improves unseen (63.18 vs 62.94), suggesting a minor trade-off between in-distribution optimization and generalization.

### The "Aha Moment": Training Dynamics

The separation loss ($\Loss_\text{sep}$) reveals a distinctive learning curve:
- **Steps 0-2000**: $\Loss_\text{sep}$ plateaus near $\ln(2) = 0.69$, indicating zero effective distinction between matched and mismatched latent messages
- **~Step 2200**: Sharp drop in $\Loss_\text{sep}$ — the model suddenly begins distinguishing task-relevant from irrelevant latents
- This marks the moment the actor learns to exploit latent information rather than ignoring it

This pattern resembles phase transitions in learning and supports the interpretation that latent comprehension emerges abruptly rather than gradually.
