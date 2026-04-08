---
type: concept-partial
partial: temperature-scaling-behavior
created: "2026-04-08"
updated: "2026-04-08"
---

Multi-agent debate and related ensemble methods only outperform a single well-tuned agent when the agents actually disagree in informative ways. **Response diversity is a precondition, not a bonus**: if every debater produces the same answer, additional rounds and additional agents add cost without adding signal.

The simplest knob for inducing this diversity is **sampling temperature**. Greedy decoding ($T \to 0$) collapses every agent onto the same mode, so debate degenerates into self-agreement; very high temperatures ($T \gg 1$) flatten the output distribution until agents become incoherent and debate cannot extract a usable signal from the noise. Between these extremes sits a productive middle range where agents disagree on hard positions while staying coherent on easy ones — and empirically this is where ensemble gains materialise. The exact boundaries of that middle range depend on both the task (how much genuine uncertainty it contains) and the model (how well-calibrated its softmax is), which is why published optimal-temperature settings vary across benchmarks and model families rather than converging on a single number.

Temperature is best understood as a **proxy for the deeper quantity**: coverage of the answer distribution. Other diversity techniques — varying prompts, swapping model checkpoints, running agents at different temperatures simultaneously — interact with the same underlying phenomenon and obey the same too-low / too-high / productive-middle pattern. Any method that claims to exploit multi-agent coordination is implicitly making a bet about where the task sits on this diversity-scaling curve.

## Used by

- [[multiagent-debate]]
- [[temperature-diversity]]
