| Primitive | Pattern | Latent implementation |
|-----------|---------|----------------------|
| **Review** | Solver -> Critic -> Solver (iterative) | Solver produces KV cache -> Critic consumes and produces feedback KV -> loops back |
| **Voting** | N parallel Solvers -> Selector | N independent KV caches -> latent-space aggregation/selection |
| **Planning** | Planner -> Executor(s) | Planner KV cache -> Executor(s) condition on latent plan |

All inter-agent communication via **KV cache concatenation** with **RoPE positional re-encoding** (critical — without it, LLaMA-based models collapse: AIME25 56.7% -> 26.7%, HumanEval+ 85.3% -> 31.1%).

### Review Primitive (Step by Step)

The Review primitive instantiates two agents: a **Solver A** and a **Critic B**, connected through a latent feedback channel.

1. Given an input prompt, **Solver A** produces an initial latent representation as a KV cache, exposing its intermediate reasoning state.
2. This KV cache is directly consumed by **Critic B**, which generates corrective feedback — identifying errors, inconsistencies, or missing reasoning steps. The Critic does not revise or complete the solution; it only provides evaluative signals.
3. The Critic's modified latent representation (feedback KV cache) is fed back to Solver A.
4. Solver A performs a subsequent refinement of its internal computation, conditioned on the feedback.
5. This defines a **latent feedback loop** that can execute for multiple iterations. In practice, **two rounds** are used.
6. A **stopping condition** derived from intermediate latent states governs adaptive depth of refinement.

The Solver prompt instructs it to "identify errors, inconsistencies, or missing reasoning, and incorporate feedback from other internal agents." The Critic prompt constrains it to "provide targeted feedback that helps guide further improvement, but you must not revise, rewrite, or complete the solution yourself."

### Voting and Selection Primitive (Step by Step)

Instantiated with a set of **parallel Solver agents** and a **Selector** module.

1. Given an input prompt, each Solver agent A_i **independently** produces a KV cache — each exposes a diverse intermediate reasoning state for the same task.
2. Solvers rely only on the input query and their own reasoning; they do not coordinate or see each other's outputs.
3. Rather than text-level majority voting, the **Selector operates directly in latent space**, performing voting and selection over the set of KV-cache representations.
4. The aggregated latent representation produces the final output.
5. In practice: **3 Solvers + 1 Selector** (4 agents total).

### Planning and Execution Primitive (Step by Step)

Instantiated with a **Planner agent P** and **Executor agents E**.

1. Given an input prompt, the **Planner** produces a latent plan — a KV cache encoding a structured decomposition of the task into intermediate steps or subgoals.
2. The latent plan serves as an explicit internal representation that conditions subsequent computation.
3. **Executor agents** consume the latent plan and perform task-specific reasoning conditioned on this representation, generating the final output.
4. In practice: **1 Planner + 3 Executors** (4 agents total).

The Planner prompt: "analyze the input task and construct a structured plan that decomposes the task into intermediate steps or subgoals. Focus on outlining what needs to be done rather than performing the task itself. Do not produce the final solution."
