### Aggressive Schedules Fail
δ=16 (twice the standard δ=8) causes **complete training collapse** — the model never converges. The curriculum must be gradual enough for the model to adapt at each stage.

### Seed Sensitivity on 9×9
Two runs with identical hyperparameters but different random seeds: one succeeds (99% accuracy), the other fails completely. The training landscape for implicit reasoning is highly non-convex, and the curriculum only finds good solutions from certain initializations.

### Partial Internalization (Intermediate Checkpoints)
On 11×11 multiplication (too hard for full internalization), intermediate checkpoints achieve **>70% accuracy at 4× the speed of explicit CoT**. This demonstrates that even when full internalization fails, the method provides a practical accuracy-speed trade-off.
