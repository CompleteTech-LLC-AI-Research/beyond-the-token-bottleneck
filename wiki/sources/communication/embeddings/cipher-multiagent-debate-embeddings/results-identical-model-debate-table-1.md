Debate accuracies (%) between two identical LLaMA family models at different temperatures, 3 rounds:

### LLaMA2-70B

| Method | GSM8K | H.S. Math | Psychology | Formal Logic | Arithmetic |
|---|---|---|---|---|---|
| Single Answer | 60.0±2.3 | 38.3±2.6 | 73.6±1.2 | 46.0±2.9 | 79.5±0.3 |
| Major@5 | 64.3±1.4 | 41.3±1.5 | 74.0±0.7 | 44.4±2.3 | 79.7±0.3 |
| NLD | 64.8±2.4 | 39.4±0.9 | 74.2±0.7 | 49.2±0.9 | 81.1±0.8 |
| **CIPHER** | **66.0±0.0** | **41.5±0.0** | **75.0±0.0** | **52.4±0.0** | **85.0±0.0** |

### LLaMA-65B

| Method | GSM8K | H.S. Math | Psychology | Formal Logic | Arithmetic |
|---|---|---|---|---|---|
| Single Answer | 50.8±1.6 | 33.8±1.8 | 68.8±1.5 | 43.5±2.7 | 27.6±1.1 |
| Major@5 | 52.7±3.3 | 36.7±0.7 | 70.5±0.4 | 46.8±2.1 | 29.8±0.9 |
| NLD | 51.7±1.4 | 36.7±0.9 | 70.0±2.0 | 46.0±1.7 | 30.4±0.4 |
| **CIPHER** | **52.9±0.0** | **38.5±0.0** | **70.9±0.0** | **50.8±0.0** | **33.0±0.0** |

Key observations: CIPHER achieves **zero variance** (deterministic embedding generation) while all baselines show 0.3–3.3% standard deviation from token sampling randomness. The largest gains are on Formal Logic (+3.2% over NLD for LLaMA2-70B) and Arithmetic (+3.9% over NLD for LLaMA2-70B).
