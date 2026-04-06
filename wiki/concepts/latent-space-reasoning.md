---
type: concept
title: "Latent-Space Reasoning"
created: "2026-04-06"
updated: "2026-04-06"
tags: [core-concept, latent-reasoning]
---

# Latent-Space Reasoning

The paradigm where LLMs perform reasoning steps in **continuous hidden-state space** rather than through discrete natural language tokens. Instead of generating a chain-of-thought as text, the model feeds its internal representations directly back as inputs, reasoning "silently" in vector space and only producing language when it needs to communicate a result.

## The Core Idea

Standard chain-of-thought (CoT) reasoning requires the model to "think out loud" — every intermediate reasoning step must be expressed as tokens. This imposes three constraints:

1. **The discretization bottleneck**: Each reasoning step must be compressed into a sequence of discrete tokens, losing the continuous richness of the model's internal representations. (The same bottleneck that [[embedding-space-communication]] addresses for inter-model communication.)

2. **The fluency tax**: Most generated tokens serve textual coherence ("Let's think step by step", "Therefore", "We can see that") rather than reasoning. Compute is wasted predicting these filler tokens.

3. **The commitment problem**: Once a token is generated, the model is committed to that path. Autoregressive generation cannot backtrack. A wrong turn at step 2 of a 10-step chain propagates irrecoverably.

Latent-space reasoning addresses all three by keeping reasoning in the model's internal vector space, where representations are continuous, there's no fluency overhead, and — critically — **multiple paths can be maintained simultaneously**.

## Mechanisms

### Hidden-State Feedback Loop ([[coconut-reasoning-latent-space|Coconut]])

The approach introduced by [[coconut-reasoning-latent-space|Coconut (Hao et al., 2024)]]:

> [!diagram|left]
> ```mermaid
> graph LR
>     A["Input"] --> B["Transformer"]
>     B --> C["Last hidden state"]
>     C -->|"fed back as<br>input embedding"| D["Transformer"]
>     D --> E["Next hidden state"]
>     E -->|"..."| F["..."]
> 
>     style A fill:#dae8fc,stroke:#6c8ebf
>     style B fill:#dae8fc,stroke:#6c8ebf
>     style C fill:#fff2cc,stroke:#d6b656
>     style D fill:#dae8fc,stroke:#6c8ebf
>     style E fill:#d5e8d4,stroke:#82b366
>     style F fill:#d5e8d4,stroke:#82b366
> ```

> [!notation|right]
> | Step | Notation |
> |---|---|
> | Last hidden state | $h(t)$ |
> | Next hidden state | $h(t+1)$ |
> | Feedback | $h(t)$ fed back as input embedding |

Each "continuous thought" is a $d$-dimensional vector (the last hidden state after layer norm) that is directly used as the next input embedding. Special tokens `<bot>` / `<eot>` bracket the latent mode. The model can switch between language and latent reasoning within a single inference pass.

**Key properties**:
- Each continuous thought requires a **full forward pass** through the transformer stack, so it adds effective depth (consistent with the theoretical analysis that CoT increases transformer expressivity by looping outputs back).
- The hidden state is processed by the **final layer norm** before feedback, keeping magnitudes in a reasonable range for the embedding layer to process.
- During training, the loss is computed only on language tokens — continuous thoughts are **unsupervised**. They are not trained to compress the language reasoning they replace, but to facilitate prediction of future tokens.

### Externalized Soft Thoughts ([[softcot-efficient-reasoning|SoftCoT]])

[[softcot-efficient-reasoning|SoftCoT (Xu et al., 2025)]] addresses a critical problem: Coconut's hidden-state feedback loop requires training the backbone LLM, which causes **[[catastrophic-forgetting]]** on instruction-tuned models (LLaMA-3.1-8B-Instruct drops from 79.61% to 76.12% on GSM8K when adapted with Coconut+LoRA). SoftCoT externalizes the continuous reasoning to a small frozen **assistant model** (e.g., 0.5B), whose hidden states are projected into the backbone's embedding space via a learned linear layer. The backbone remains completely frozen ([[raw/pdf/arxiv-2502.12134.pdf|SoftCoT Table 1]]).

**Key properties**:
- Only the projection layer is trained — the backbone never changes
- Soft thought tokens are ~**4× more information-dense** than discrete tokens (6 soft tokens $\approx$ 24 hard tokens)
- Assistant model size barely matters (0.5B nearly matches 7B)
- Soft thoughts **augment** standard CoT rather than replacing it — the LLM still generates a full discrete reasoning chain

### Supervised Compressed Thoughts ([[thinking-states-latent-reasoning|Thinking States]])

[[thinking-states-latent-reasoning|Thinking States (Amos et al., 2026)]] combines discrete and continuous reasoning: generate **natural-language thoughts** at chunk boundaries during input processing, then **compress** them into fixed-size continuous states injected at a shallow layer. This bridges the supervision problem (thoughts are supervisable because they're NL) with the compactness advantage (states are continuous).

**Key properties**:
- **Deep-to-shallow recurrence**: Thoughts extracted from layer 26 (of 28), injected at layer 1 — gives the compressed state maximum processing depth through the backbone ([[raw/pdf/arxiv-2602.08332.pdf|Thinking States §3]])
- **Teacher forcing**: Because ground-truth thoughts are available, all chunks process in a single parallel forward pass. No BPTT needed — training cost is **constant** regardless of recurrence depth (vs. Coconut's linear scaling)
- Matches CoT on 2-Hop QA (54.91% vs 54.79%) with 1.19× speedup; dramatically outperforms CoT on length generalization (Parity: 100% vs 64.38%)
- **State ambiguity**: When the question appears at the end of the input, the model may reason about the wrong intermediate quantity before seeing what's asked

### Multi-Agent Latent Reasoning ([[latentmas-collaboration|LatentMAS]])

[[latentmas-collaboration|LatentMAS (Zou et al., 2025)]] extends Coconut-style latent reasoning to multi-agent systems, creating the first framework that unifies **latent reasoning AND latent communication**: each agent generates latent thoughts via hidden-state feedback, then transfers its full KV caches (including the latent thoughts) to the next agent.

**Key properties**:
- **Training-free** — alignment via ridge regression on embedding matrices
- $471.4\times$ theoretical compression advantage over text ($d / \log|V|$ for Qwen3-14B)
- 4-4.3× faster end-to-end than TextMAS, 70.8-83.7% fewer tokens

### Precursors and Baselines (Now Ingested)

**[[icot-internalize-cot|iCoT (Deng et al., 2024)]]** — The direct precursor to Coconut. Progressive left-to-right removal of CoT tokens ([[raw/pdf/arxiv-2405.14838.pdf|iCoT §3]]), forcing the model to internalize reasoning into hidden states. Established two critical techniques Coconut adopted: **optimizer resets** between stages and **removal smoothing**. Limitation: no dedicated reasoning medium — internalization is limited to the model's fixed depth. Mistral 7B achieves 51% on GSM8K with zero visible reasoning (surpassing GPT-4's 44% no-CoT), but still 17 points below explicit CoT (68%).

**[[pause-tokens|Pause Tokens (Goyal et al., 2024)]]** — The **minimal baseline** for extra computation without language. A single learnable `<pause>` embedding appended to input gives the transformer more vectors per layer (width expansion). Wins on 8/9 tasks at 1B scale. But pause tokens add **width only**, not depth — they cannot encode information from the model's own reasoning. Coconut's continuous thoughts add both width AND depth AND carry rich continuous information. [[pause-tokens|Pause Tokens]] are the existence proof; [[coconut-reasoning-latent-space|Coconut]] is the mechanism.

**Filler tokens** (Pfau et al., 2024): Using "..." for extra computation. Works for parallelizable problems but doesn't extend expressivity like CoT.

### The Spectrum from Explicit to Implicit Reasoning

| Method | Reasoning medium | Supervision | Recurrence | Training cost | Backbone modified? | Interpretable? | Scale tested |
|--------|-----------------|-------------|------------|---------------|-------------------|---------------|-------------|
| Standard CoT | Discrete tokens | Direct | Sequential generation | Constant | No | Full | Any |
| **[[thinking-states-latent-reasoning\|Thinking States]]** | **NL → compressed states** | **Direct (teacher forcing)** | **Chunk-recurrent** | **Constant** | **Lightweight modules** | **Full (NL thoughts)** | **1.5B** |
| **[[softcot-efficient-reasoning\|SoftCoT]]** | **External soft tokens** | **Indirect (projection)** | **None (single pass)** | **Constant** | **No (frozen)** | **Via decoding** | **7-8B** |
| [[coconut-reasoning-latent-space\|Coconut]] | Continuous hidden states | Indirect (future token prediction) | Hidden-state feedback | Linear (BPTT) | Yes (full training) | Via probing | GPT-2 |
| **[[latentmas-collaboration\|LatentMAS]]** | **Hidden states + KV caches** | **None (training-free)** | **Hidden-state feedback** | **None** | **No** | **Via probing** | **4-14B** |
| [[icot-internalize-cot\|iCoT]] | Implicit (no output) | Curriculum | None | Curriculum overhead | Yes | None | 7B (51% GSM8K) |
| [[pause-tokens\|Pause tokens]] | Implicit (learnable embedding) | Indirect | None (width only) | Requires pretraining | Partial (new token) | None | 1B |
| No-CoT | Implicit (single pass) | Direct (answer only) | None | Constant | No | None | Any |

## Theoretical Foundations

Three foundational papers establish **why** latent reasoning works, forming a theoretical stack:

### 1. CoT Increases Effective Depth (Feng et al., NeurIPS 2023)

[[cot-expressivity-theory|Feng et al.]] prove via circuit complexity theory that bounded-depth transformers are limited to $\text{TC}^0$ — they **cannot** solve basic arithmetic or linear equations ($\text{NC}^1$ problems) without CoT. With CoT, constant-size transformers solve all these problems because autoregressive generation increases effective depth proportionally to generation length. This establishes the **depth bottleneck** as the core constraint that any latent reasoning method must address.

**Implication**: Any mechanism that adds effective depth — CoT tokens, pause tokens, continuous thoughts, chunk recurrence — should yield expressivity gains. The key question becomes: which mechanism adds depth most efficiently?

### 2. Continuous CoT Adds Superposition (Zhu et al., NeurIPS 2025)

[[superposition-coconut-theory|Zhu et al.]] extend Feng et al.'s framework to prove that continuous CoT is **provably more efficient** than discrete CoT. A 2-layer transformer with $D$ continuous thought steps solves directed graph reachability ($D$ = diameter), vs. $O(n^2)$ for the best known discrete CoT result ([[raw/pdf/arxiv-2505.12514.pdf|Zhu et al. Theorem 1]]). The mechanism: each continuous thought is a **superposition state** encoding the complete BFS frontier.

### 3. Enriched Entity Representations Peak at Mid-Layers (Hernandez et al., ICLR 2024)

[[linearity-relation-decoding|Hernandez et al.]] show that transformers encode relational knowledge as linear embeddings at intermediate layers (~layer 20-26 of 32), then **compress** this information for next-token prediction in later layers. This explains why Coconut's hidden-state feedback (which captures mid-computation representations) is richer than discrete tokens (which only capture the output-layer prediction).

### The Unified Picture

> [!diagram|left]
> ```mermaid
> graph TD
>     A["Feng et al.: CoT works because<br>it adds effective depth"] --> B["Zhu et al.: Continuous CoT is better<br>because it adds superposition"]
>     B --> C["Hernandez et al.: Mid-layer representations<br>are richer than output representations"]
>     C --> D["Combined: Latent reasoning = more depth<br>+ superposition + richer representations"]
> ```

> [!notation|right]
> | Claim | Notation |
> |---|---|
> | Depth gain | $\mathsf{TC}^0 \to \mathsf{NC}^1$ |
> | Superposition gain | $D$ steps vs $O(n^2)$ |

## The Superposition Property

The most profound discovery from [[coconut-reasoning-latent-space|Coconut]], now **rigorously formalized** by [[superposition-coconut-theory|Zhu et al. (2025)]]: continuous thoughts can encode **multiple alternative reasoning paths simultaneously** — a property called **superposition**.

### Why This Is Possible

A discrete token can represent exactly one choice. A continuous vector in $\R^d$ can represent a **weighted combination** of many choices simultaneously. Zhu et al. prove this precisely: the $c$-th continuous thought is the **normalized uniform mixture** of all vertex embeddings reachable within $c$ steps:

> $$[t_c] = \frac{1}{|V_c|} \sum_{v \in V_c} u_v$$

This is not a metaphor — it's a mathematical identity. The quantum mechanics analogy is exact: continuous thoughts are superposition states, token sampling is measurement/collapse, and the final answer token acts as a "measurement" projecting the superposition onto the correct candidate.

This is directly analogous to the advantage of [[embedding-space-communication]] over discrete tokens: the weighted average embedding in [[cipher-multiagent-debate-embeddings|CIPHER]] encodes uncertainty across multiple tokens. Coconut extends this principle from communication to reasoning.

### Emergent BFS

The superposition property gives rise to **emergent breadth-first search** (BFS):

1. **Step 1**: The continuous thought maintains probability mass on all immediate next steps (broad exploration).
2. **Step 2**: Paths are evaluated and weaker candidates are pruned (narrowing).
3. **Steps 3+**: Continued evaluation until a single path dominates (commitment).

This contrasts with CoT's inherent **depth-first / greedy** strategy — commit to one path immediately, follow it to the end, hope it's right.

The BFS behavior is **not explicitly trained** ([[raw/pdf/arxiv-2412.06769.pdf|Coconut §4.2, Figure 3]]). It emerges naturally from the interaction between:
- The continuous representation's ability to encode superpositions
- The training objective's pressure to predict the correct final answer
- The gradient-based optimization finding that maintaining multiple paths improves expected accuracy

### The Height–Confidence Principle

Coconut's analysis reveals a fundamental principle about reasoning under uncertainty: **nodes closer to the goal are easier to evaluate accurately**. The model's value estimates improve as paths approach terminal states. Therefore, the optimal strategy is:

- **Early in reasoning**: Maintain many candidate paths (high uncertainty, evaluation is unreliable).
- **Later in reasoning**: Narrow to the best path (low uncertainty, evaluation is reliable).

This is why BFS outperforms DFS/greedy for planning tasks — it delays commitment to when the model can make reliable decisions. CoT is forced to commit early, when evaluation is least reliable.

## The Training Challenge

A key finding from Coconut: **LLMs cannot learn latent reasoning from scratch**. Training directly on question-answer pairs with continuous thoughts (no curriculum) produces performance no better than the No-CoT baseline.

### Why Curriculum Is Necessary

The hypothesis: the latent reasoning space is too large and unstructured for gradient descent to find good solutions without guidance. Language CoT data provides a "scaffold" — it shows the model what reasoning looks like, then the curriculum progressively shifts that reasoning from language space to latent space.

The multi-stage curriculum ([[raw/pdf/arxiv-2412.06769.pdf|Coconut §3.1]]):
1. Start with full language CoT (the model knows how to reason in language).
2. Replace the first step with continuous thoughts (the model learns to initiate reasoning in latent space).
3. Replace the second step (the model learns to chain latent reasoning steps).
4. Continue until all steps are replaced (fully latent reasoning).

Optimizer state is reset between stages, suggesting that each stage requires fundamentally different optimization dynamics.

### The Catastrophic Forgetting Barrier

[[softcot-efficient-reasoning|SoftCoT]] reveals a critical barrier: Coconut's curriculum works on GPT-2 but **damages instruction-tuned models**. LoRA-adapted Coconut on LLaMA-3.1-8B-Instruct drops GSM8K from 79.61% to 76.12% — below zero-shot CoT. See [[catastrophic-forgetting]] for full details. This means **any approach that modifies the backbone** (Coconut, iCoT) may be fundamentally incompatible with frontier instruction-tuned models.

### Three Solutions to the Training Challenge

| Solution | Approach | Trade-off |
|----------|---------|-----------|
| **[[coconut-reasoning-latent-space|Coconut]] curriculum** | Multi-stage progressive replacement | Only works on base models (GPT-2); damages instruction-tuned |
| **[[softcot-efficient-reasoning|SoftCoT]] externalization** | Freeze backbone; external assistant generates soft thoughts | Requires two models; soft thoughts augment CoT, don't replace it |
| **[[thinking-states-latent-reasoning|Thinking States]] teacher forcing** | NL thoughts → compress → inject. Gold states enable parallel training | Requires chunk-level supervision annotations; uses base models |
| **[[latentmas-collaboration|LatentMAS]] alignment** | Ridge regression on embedding matrices; training-free | No optimization at all; limited to same-architecture agents |

### Implications

This training dependency is both a limitation and a research frontier:
- **Limitation**: You need high-quality language CoT data before you can train latent reasoning. Latent reasoning is currently bootstrapped from, not a replacement for, language reasoning.
- **Instruction-tuned models**: The [[catastrophic-forgetting|catastrophic forgetting]] barrier means frozen-backbone approaches ([[softcot-efficient-reasoning|SoftCoT]]) or training-free approaches ([[latentmas-collaboration|LatentMAS]]) may be the only viable paths for production models.
- **Open question**: Can alternative training approaches (RL, self-play, contrastive learning) enable latent reasoning without language CoT scaffolding and without damaging existing capabilities?

## Computational Properties

### Efficiency

Latent reasoning is **token-efficient** but not necessarily **compute-efficient**:
- **Token efficiency**: Coconut generates far fewer tokens than CoT (e.g., 14.2 vs 49.4 on ProsQA) because no fluency tokens are needed.
- **Compute per thought**: Each continuous thought requires a full forward pass through the transformer — the same compute as generating a token. But since there are fewer thoughts than tokens, total compute is often lower.
- **Parallelism limitation**: Continuous thoughts are inherently sequential (each depends on the previous). Unlike standard token generation (which can be parallelized across sequences in a batch), the sequential dependency limits training throughput.

### Scaling Properties

From Coconut's experiments:
- Increasing the hyperparameter $c$ (continuous thoughts per language step) from 0→1→2 steadily improves performance, suggesting that more latent computation scales reasoning ability.
- This parallels the finding that longer CoT chains improve accuracy — both are forms of **inference-time compute scaling**.
- Whether this scaling continues to frontier model sizes is an open question.

## Relationship to Other Concepts

### vs. Embedding-Space Communication

| Aspect | [[embedding-space-communication]] | Latent-space reasoning |
|--------|----------------------------------|----------------------|
| Context | Inter-agent (between models) | Intra-agent (within one model) |
| What's bypassed | Token sampling between sender and receiver | Token sampling within the reasoning loop |
| Information preserved | Output distribution over vocabulary | Full hidden state |
| Key insight | Soft tokens carry richer info than hard tokens | Continuous thoughts can encode path superpositions |

Both exploit the same fundamental principle: **the discrete token bottleneck discards valuable information**. They apply it in complementary contexts.

### vs. Chain-of-Thought

Latent-space reasoning is not anti-CoT — it's a **generalization** of CoT. CoT reasons through a sequence of discrete states (tokens). Latent reasoning reasons through a sequence of continuous states (hidden vectors). This is an instance of the [[continuous-vs-discrete-representation]] trade-off. The continuous version subsumes the discrete: any reasoning expressible as tokens is also expressible as vectors, but not vice versa (superpositions cannot be expressed as tokens).

### Connection to [[activation-communication]]

Coconut's continuous thoughts are exactly the kind of representation shared in activation communication. [[latentmas-collaboration|LatentMAS]] realizes this connection fully: agents generate latent thoughts via hidden-state feedback (Coconut-style), then transfer their complete KV caches (including the latent thoughts) to the next agent. This is the first framework that unifies latent reasoning and latent communication — agents that reason internally in latent space AND communicate in latent space. [[interlat-latent-space-agents|Interlat]] takes a similar approach with raw hidden-state sequences and learned compression.

## Open Questions

- **Scaling to frontier models**: Does BFS emergence persist with larger, more capable models? [[softcot-efficient-reasoning|SoftCoT]] and [[latentmas-collaboration|LatentMAS]] test at 7-14B; [[coconut-reasoning-latent-space|Coconut]] only at GPT-2 scale.
- **Catastrophic forgetting solutions**: Can latent reasoning be trained without damaging instruction-tuned models? SoftCoT's externalization and LatentMAS's training-free approach are workarounds; is there a fundamental fix?
- **Hybrid discrete-continuous reasoning**: [[thinking-states-latent-reasoning|Thinking States]] generates discrete NL thoughts then compresses them. Is this "best of both worlds" or an awkward compromise? What's the optimal discrete/continuous ratio?
- **Interpretability**: How do we audit, debug, and verify reasoning that happens in an opaque continuous space? Thinking States preserves interpretability via NL thoughts; Coconut and LatentMAS do not.
- **State ambiguity**: Thinking States identifies the problem of reasoning about the wrong quantity before seeing the question. Can bidirectional architectures or question-prepending solve this generally?
- **Beyond reasoning**: Can latent-space reasoning apply to creative generation, dialogue, or other tasks?
