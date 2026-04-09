Most methods are tested in single-round or limited settings.

- How does KV-cache communication work in **iterative debate** settings? All papers evaluate single-round. — [[kv-cache-communication]]
- Could iterative activation grafting (multiple rounds) combine AC's information density with debate's iterative refinement? — [[activation-communication]]
- [[agent-primitives-building-blocks|Agent Primitives]]' Review primitive implements a 2-round latent feedback loop (Solver $\to$ Critic $\to$ Solver). How does performance scale with additional rounds, and is there a point of diminishing returns analogous to the message density saturation ($\mu \approx 0.39$) found by the scaling framework? — [[agent-primitives-building-blocks]], [[scaling-agent-systems]]
- KV Alignment's self-improvement effect (A $\to$ $\Omega$ $\to$ A improves model A) suggests that iterative cycling could be beneficial. Does this improvement saturate or continue monotonically? — [[kv-cache-alignment-shared-space]], [[frontier-research-directions]]
