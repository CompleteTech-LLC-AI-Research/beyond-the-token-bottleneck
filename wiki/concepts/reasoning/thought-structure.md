---
type: concept
title: "Thought Structure"
created: "2026-04-06"
updated: "2026-04-06"
tags: [core-concept, latent-communication, multi-agent]
---

# Thought Structure

The organizational pattern of **which agents hold which latent thoughts** in a multi-agent system. Introduced by [[thought-communication-multiagent|ThoughtComm (Zheng et al., 2025)]], thought structure goes beyond the content of communication to capture the **topology of cognitive alignment** across agents.

## Why Structure Matters

Prior approaches to latent communication ([[cipher-multiagent-debate-embeddings|CIPHER]], [[activation-communication|activation sharing]]) treat communication as a uniform broadcast — every agent sends the same representation to every other agent. [[thought-communication-multiagent|ThoughtComm]] argues this is insufficient because:

1. **Not all thoughts are relevant to all agents**: In a multi-agent system, different agents may focus on different aspects of a problem. Sending irrelevant information wastes bandwidth and can confuse the receiver.
2. **Shared vs. private information serves different roles**: Common ground (shared thoughts) enables coordination; private thoughts enable novelty and complementary reasoning.
3. **Agreement level signals reliability**: A thought shared by 4 out of 5 agents is more likely to be correct than one held by a single agent — but the single agent's thought may also be the key insight everyone else missed.

## Formal Definition

Given $n_a$ agents and $n_z$ latent thoughts, the thought structure is a **binary incidence matrix** $B(J_f) \in \{0,1\}^{n_h \times n_z}$, where a non-zero entry indicates that latent thought $j$ influences agent dimension $i$. This is derived from the Jacobian of the generating function $f$ that maps thoughts to agent hidden states.

For each agent $A_k$, the relevant thoughts are:

> $$Z_{H_t^{(k)}} := \{Z_{t,j} \in Z_t \mid \exists\, i \in [k_l, k_h] \text{ such that } B(J_f)_{i,j} \neq 0\}$$

### The Three Types of Thoughts

For any pair of agents $A_i$ and $A_j$:

| Type | Definition | Role in communication |
|------|-----------|----------------------|
| **Shared thoughts** | $Z_{H_t^{(i)}} \cap Z_{H_t^{(j)}}$ | Common ground; basis for coordination |
| **Private to $A_i$** | $Z_{H_t^{(i)}} \setminus Z_{H_t^{(j)}}$ | Agent-specific reasoning; source of novelty |
| **Private to $A_j$** | $Z_{H_t^{(j)}} \setminus Z_{H_t^{(i)}}$ | Agent-specific reasoning; complementary perspective |
| **Irrelevant** | $Z_t \setminus (Z_{H_t^{(i)}} \cup Z_{H_t^{(j)}})$ | Latent dimensions that influence neither agent |

### Agreement Level

For multi-agent systems ($n_a > 2$), the **agreement level** $\sigma_j$ of a thought $Z_{t,j}$ measures how many agents' states depend on it:

> $$\sigma_j = \sum_{k=1}^{n_a} \mathbb{1}[Z_{t,j} \in Z_{H_t^{(k)}}]$$

This creates a spectrum from fully private ($\sigma = 1$) to fully shared ($\sigma = n_a$):

| Agreement level | Interpretation | Typical treatment |
|----------------|---------------|-------------------|
| $\sigma = 1$ | Unique to one agent | May be noise, or may be a critical unique insight |
| $\sigma = 2\text{-}3$ (small group) | Shared by a subgroup | Possible coalition or partial agreement |
| $\sigma \approx n_a/2$ | Divisive | Potential point of disagreement worth exploring |
| $\sigma = n_a$ | Universal consensus | Strong common ground; high confidence |

## Identifiability Guarantees

[[thought-communication-multiagent|ThoughtComm]] provides theoretical guarantees ([[raw/pdf/arxiv-2510.20733.pdf|ThoughtComm Theorems 1-3]]) that under minimal assumptions (invertible generating function, sparsity regularization):

1. Shared thoughts can be **disentangled** from private and irrelevant thoughts
2. Private thoughts can be **disentangled** from all other thoughts
3. The full incidence structure $B(J_f)$ can be **recovered** up to relabeling

These guarantees are **pairwise** — they hold for any pair of agents — and global structure is reconstructed by composing pairwise results. The key assumption is sparsity: each thought must have sparse influence on agent states (not every thought affects every dimension).

## Implementation: Agreement-Based Reweighting

In [[thought-communication-multiagent|ThoughtComm]]'s practical framework, the recovered structure is used for **selective routing**:

1. Extract latent thoughts via sparsity-regularized autoencoder
2. For each agent, identify relevant thoughts using the recovered Jacobian structure
3. Partition relevant thoughts by agreement level $\sigma$ ([[raw/pdf/arxiv-2510.20733.pdf|ThoughtComm §3.3]])
4. Assign weights $w_\sigma$ to each agreement level
5. Construct a weighted, structured latent representation per agent

This means each agent doesn't just receive "what others think" — it receives a structured representation that distinguishes "what everyone agrees on" from "what's unique to me" from "what's contested." This structured view enables more informed reasoning in subsequent debate rounds.

## Scaling Properties

[[thought-communication-multiagent|ThoughtComm]] demonstrates that thought structure enables **positive scaling with debate rounds** — more rounds improve both accuracy and consensus. This contrasts with natural language debate, which often degrades with more rounds due to redundant or confusing messages. The hypothesis: structured thought routing filters noise and redundancy at each round, while language-based communication accumulates it.

## Worked Examples

### Example 1: Three-Agent Math Debate

Consider three agents ($A_1, A_2, A_3$) reasoning about a multi-step algebra problem with $n_z = 5$ latent thought dimensions. After recovering the Jacobian structure, suppose the incidence matrix reveals:

| | $Z_1$ (problem decomposition) | $Z_2$ (algebraic manipulation) | $Z_3$ (numerical estimation) | $Z_4$ (sign tracking) | $Z_5$ (answer formatting) |
|---|---|---|---|---|---|
| $A_1$ | 1 | 1 | 0 | 1 | 1 |
| $A_2$ | 1 | 1 | 1 | 0 | 1 |
| $A_3$ | 0 | 1 | 1 | 1 | 0 |

From this structure: $Z_2$ (algebraic manipulation) has $\sigma = 3$ (universal consensus), $Z_1$ and $Z_5$ have $\sigma = 2$, and $Z_3, Z_4$ have $\sigma = 2$ but in different agent subsets. No thought is fully private ($\sigma = 1$) in this example, but $Z_4$ (sign tracking) is invisible to $A_2$ — if the correct answer is negative, $A_2$ might miss the sign. The routing system would ensure $A_2$ receives $Z_4$ with a weight reflecting its low agreement, flagging it as "a perspective you haven't considered."

### Example 2: Divergent Reasoning Paths

Suppose two agents tackle a combinatorics problem. $A_1$ attempts a constructive counting approach while $A_2$ uses inclusion-exclusion. With $n_z = 4$ latent thoughts:

- $Z_1$ (problem parsing): shared ($\sigma = 2$) — both agents understand the question
- $Z_2$ (constructive counting logic): private to $A_1$ ($\sigma = 1$)
- $Z_3$ (inclusion-exclusion framework): private to $A_2$ ($\sigma = 1$)
- $Z_4$ (final numerical answer): shared ($\sigma = 2$) — both converge on the same number

Here the agreement structure tells a clear story: the agents agree on the problem and the answer but used completely different methods. The shared thoughts ($Z_1, Z_4$) provide high-confidence signals (independent confirmation), while the private thoughts ($Z_2, Z_3$) represent genuinely complementary reasoning. In a subsequent round, routing $Z_3$ to $A_1$ (and vice versa) could enable both agents to verify their answer via an alternative method — a form of cross-validation that unstructured communication cannot achieve.

## Connections to Other Concepts

### vs. Unstructured Latent Communication

| Property | [[cipher-multiagent-debate-embeddings|CIPHER]] / Activation sharing | [[thought-communication-multiagent|ThoughtComm]] |
|----------|---------------------------|-------------|
| What's shared | Raw representations (embeddings, hidden states) | Disentangled latent factors |
| Routing | Broadcast (all-to-all) | Selective (structure-based) |
| Agreement information | None | Explicit ($\sigma$ scores) |
| Theoretical guarantees | None (empirical only) | Identifiability theorems |
| Interpretability | Via nearest-neighbor decoding | Via disentangled factors and structure |

### Connection to [[temperature-diversity]]

Temperature diversity in [[multi-agent-debate]] is a crude form of thought structure — different temperatures produce different "types" of information (confident vs. exploratory). [[thought-communication-multiagent|ThoughtComm]] makes this explicit and principled: rather than hoping that temperature differences produce complementary thoughts, ThoughtComm directly identifies and routes complementary information.

The correspondence can be made precise. A low-temperature agent's peaked softmax distribution produces embeddings dominated by the top token — analogous to a high-agreement thought ($\sigma \approx n_a$) that reflects consensus. A high-temperature agent's flat distribution produces embeddings blending many alternatives — analogous to low-agreement thoughts ($\sigma \approx 1$) that surface rare possibilities. Temperature diversity creates these complementary profiles *implicitly* through the sampling distribution; thought structure identifies them *explicitly* through the Jacobian. The practical consequence: [[temperature-diversity]] requires Bayesian optimization over temperature pairs to find the right balance (e.g., the optimal $(0.15, 1.75)$ pair for Arithmetic in [[cipher-multiagent-debate-embeddings|CIPHER]]), while thought structure discovers the balance automatically from the data.

### Connection to [[latent-variable-model]]

Thought structure is the **practical instantiation** of the [[latent-variable-model]]'s structural identification. The incidence matrix $B(J_f)$ is the core object that the three identifiability theorems recover: Theorem 1 identifies which entries correspond to shared thoughts, Theorem 2 identifies private entries, and Theorem 3 recovers the full matrix. Without the [[latent-variable-model]] framework and its sparsity-based identifiability guarantees, the recovered structure would be an arbitrary factorization with no guarantee of semantic meaning. The theoretical grounding ensures that when the structure says "thought $Z_3$ is private to $A_2$," this reflects a genuine cognitive separation — not an artifact of the autoencoder's arbitrary basis choice.

### Connection to [[latent-space-reasoning]]

[[coconut-reasoning-latent-space|Coconut]] shows that hidden states can encode **superpositions** of reasoning paths. [[superposition-coconut-theory|Zhu et al.]] formalize this: each continuous thought is the normalized uniform mixture $\frac{1}{\sqrt{|V_c|}} \sum_{v \in V_c} u_v$ of all reachable vertices at BFS step $c$. Thought structure could be a way to **disentangle** these superpositions — each latent thought dimension might correspond to a distinct reasoning path, and the structure would reveal which paths each agent is considering. In the graph reachability setting, a thought with $\sigma = n_a$ would indicate a vertex that all agents agree is reachable, while a thought with $\sigma = 1$ would flag a path only one agent has found. This connection is speculative but compelling — it would unify intra-agent superposition (Coconut) with inter-agent structure (ThoughtComm).

### The Long-Tail Phenomenon

The paper makes an important observation: some thoughts are rare (low agreement, held by only one agent) but carry critical value. This connects to the **long-tail phenomenon** — infrequent but important signals. Without structured recovery, these rare thoughts would be drowned out by common-ground thoughts. ThoughtComm's disentanglement and explicit agreement scoring ensure that rare, high-value thoughts are preserved and surfaced.

### Connection to [[continuous-vs-discrete-representation]]

Thought structure operates entirely in [[continuous-vs-discrete-representation|continuous space]], but it adds a layer of **discrete annotation** (the binary incidence matrix $B(J_f)$ and integer agreement scores $\sigma_j$) on top of continuous representations. This is a hybrid approach: the thoughts themselves are continuous vectors preserving the full information density of the latent space, while the routing decisions are discrete (share/don't share, weight by integer agreement level). This hybrid design avoids the [[continuous-vs-discrete-representation|discrete bottleneck]] for content while using discreteness for structure — arguably the best of both worlds.

## Maps of Content

This concept appears in the following guided reading paths:
- [[latent-communication|Latent Communication]] — how multiple LLM agents exchange information through continuous representations rather than text
- [[theoretical-foundations|Theoretical Foundations]] — the theoretical pillars explaining why continuous representations outperform discrete tokens

## Open Questions

- **Automatic dimensionality**: How many latent thought dimensions ($n_z$) are needed? Can this be determined automatically, perhaps through a variational approach or information-theoretic criterion?
- **Dynamic structure**: Thought structure likely evolves across debate rounds as agents update their reasoning. Can the framework track and adapt to this evolution in real time?
- **Cross-architecture application**: The theory requires access to hidden states. Can thought structure be inferred from observable outputs (generated text, logits) for closed-source models?
- **Thought quality**: Not all identified thoughts are equally useful. Can the framework distinguish between informative thoughts and noise in the latent space?
- **Scaling to many agents**: Pairwise identifiability composes to global structure, but does this composition remain robust with dozens or hundreds of agents?
- **Connection to interpretability**: Disentangled latent thoughts could serve as an interpretability tool — revealing *why* agents disagree by identifying which private thoughts drive divergent answers.
