### Aggressive Schedule Collapse ($\delta = 16$)

Doubling the removal rate causes **complete training collapse**: accuracy drops to near-zero early and stays there. The model needs a minimum number of training steps at each difficulty level to reorganize internal representations. Once the model falls behind the curriculum, it cannot catch up — the failure is catastrophic, not gradual.

### Seed Sensitivity on 9x9 Multiplication

Two identical runs with different random seeds produce 99% vs. complete failure. The optimization landscape for implicit reasoning is **highly non-convex** with many poor local minima. Reliable deployment requires multiple runs and best-checkpoint selection, significantly increasing effective training cost.

### 11x11 Multiplication: The Capacity Wall

Full internalization fails at 11x11 (~370-token CoT chains). However, intermediate checkpoints at partial internalization achieve **>70% accuracy at 4x the speed** of explicit CoT. The model handles early reasoning implicitly and hard late reasoning explicitly — a practical accuracy-speed trade-off that anticipates [[thinking-states-latent-reasoning|Thinking States]]'s chunk-level design where reasoning alternates between compressed states and explicit text.
