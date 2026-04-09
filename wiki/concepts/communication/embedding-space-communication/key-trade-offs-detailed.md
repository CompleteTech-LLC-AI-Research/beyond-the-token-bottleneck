| Dimension | Natural Language | Embedding Communication |
|-----------|-----------------|------------------------|
| Information per position | ~15 bits (1 of ~32K tokens) | Continuous (full distribution) |
| Interpretability | Human-readable | Requires nearest-neighbor decoding |
| Cross-model compatibility | Universal | Requires shared tokenizer or alignment |
| Determinism | Stochastic (sampling) | Deterministic (expectation) |
| Computational cost | Standard generation | Similar (no extra forward passes) |
| Bandwidth | Token IDs (compact) | Dense vectors (d-dimensional per position) |
| Error propagation | Errors are discrete and local | Errors are continuous and can compound |
