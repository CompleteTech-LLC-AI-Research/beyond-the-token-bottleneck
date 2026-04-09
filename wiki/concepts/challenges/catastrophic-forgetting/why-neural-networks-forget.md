The fundamental cause is **shared representation**: neural networks distribute knowledge across overlapping sets of parameters. When gradients from new data update weights that encode existing knowledge, the old knowledge is overwritten. Three distinct mechanisms drive this:

1. **Weight drift**: Gradient updates for the new task move parameters away from the region of weight space that encodes old-task performance. Even small per-parameter changes can compound across layers, producing large shifts in network behavior.

2. **Representation shift**: Internal representations (hidden-state geometry, attention patterns, activation distributions) realign to the new data distribution. Features that were diagnostic for old tasks may become entangled with new-task features or suppressed entirely.

3. **Objective conflict**: When the new training objective differs from the original one — as it does when adding latent reasoning to an instruction-following model — the loss landscape itself changes. The optimal parameter region for the new objective may be far from the optimum for the old one, with no good compromise point.
