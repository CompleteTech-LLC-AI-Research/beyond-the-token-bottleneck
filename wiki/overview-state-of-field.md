---
type: overview
title: "State of the Field: Latent Reasoning & Communication (April 2026)"
created: "2026-04-06"
updated: "2026-04-08"
tags: [overview, state-of-field]
---

# State of the Field: Latent Reasoning & Communication (April 2026)

This page provides a single narrative synthesis of the research landscape tracked in this wiki — 26 papers spanning December 2022 to April 2026, covering how LLMs can reason and communicate in continuous representation space rather than through discrete tokens. For the full page inventory and guided reading paths, see [[index]].

## The Central Insight

Large language models are internally continuous systems — dense vectors in $\R^d$ at every layer — forced to interface with the world through a **discrete bottleneck**: token sampling. This bottleneck discards distributional uncertainty, prevents superposition of hypotheses, and wastes compute on fluency tokens. The research tracked here explores what happens when you remove that bottleneck, both within individual models ([[latent-space-reasoning|latent reasoning]]) and between models (latent communication).

The unifying principle, detailed in [[continuous-vs-discrete-representation]], is that continuous representations carry 4x to 2600x more information per position than discrete tokens. This is not merely an engineering optimization — it enables qualitatively different computation, most notably **superposition**: the ability to maintain multiple hypotheses simultaneously in a single vector. The information-theoretic argument and compression bounds are further explored in [[compression-information-theory]].

## Theoretical Foundations

Before diving into systems, the theoretical results that explain *why* any of this works deserve attention. The [[theoretical-foundations]] traces a path from complexity theory to representation geometry to convergence hypotheses.

The starting point is the **depth bottleneck**: [[cot-expressivity-theory|Feng et al. (NeurIPS 2023)]] proved that bounded-depth transformers are limited to $\text{TC}^0$ circuits and cannot solve basic arithmetic without additional reasoning steps. Chain-of-thought breaks this barrier by adding effective circuit depth. Any mechanism that adds reasoning steps — discrete tokens, pause tokens, continuous thoughts, recurrence — yields expressivity gains. But the *form* of those steps matters enormously.

[[superposition-coconut-theory|Zhu et al. (NeurIPS 2025)]] formalized exactly how continuous reasoning exploits its advantage over discrete tokens. They proved that continuous CoT implements **parallel BFS via superposition**: each latent vector encodes the complete frontier of reachable vertices. A 2-layer transformer solves graph reachability in $D$ steps (graph diameter) vs. $O(n^2)$ for discrete CoT. This is not a constant-factor speedup — it is a complexity-class transition.

**The empirical bracket on this theory** comes from [[latent-reasoning-supervision-analysis|Cui et al. (Amazon, Feb 2026)]], which conducted the first systematic test of whether the iterative latent process actually performs BFS in practice. Their findings split the literature's central narrative cleanly: the **capacity** to encode multiple candidates is real (latent reasoning's Pass@100 exceeds explicit reasoning's by 20+ points), but the **iterative dynamics** are pruning, not expansion (distinct outcomes *decrease* monotonically with latent depth, and majority-vote accuracy is 3-4 points *below* explicit reasoning). Zhu et al.'s theoretical bound is achievable in capacity but not in dynamics — the gradient-based optimization process actively destroys the very property the theory permits. This is the strongest empirical evidence to date that scaling Coconut alone will not produce frontier-scale BFS; the optimization process must also be redesigned. See [[contradictions|tension #9]] for the full discussion.

On the representation side, three results converge to explain why cross-model transfer works at all. [[linearity-relation-decoding|Hernandez et al. (ICLR 2024)]] showed that ~48% of tested relation types in transformers are well-approximated by affine transforms, with mid-layer representations richer than final-layer ones. [[relative-representations-zero-shot|Moschella et al. (ICLR 2023)]] proved that well-trained networks produce latent spaces related by approximately angle-preserving transformations, enabling zero-shot model stitching that jumps from 6% to 80%+ accuracy. And the [[platonic-representation-hypothesis|Platonic Representation Hypothesis (Huh et al., ICML 2024)]] makes the strongest claim: all sufficiently capable models converge toward a shared pointwise mutual information kernel reflecting the statistical structure of reality. Together, these results predict that simple linear projections should suffice for cross-model alignment — and the empirical results confirm it.

## Thread 1: Latent Reasoning (Intra-Agent)

The quest to make models reason without producing tokens has a clear lineage, traced in [[latent-reasoning]].

**The existence proof**: [[pause-tokens|Goyal et al. (ICLR 2024)]] showed that inserting learnable dummy tokens — "pause tokens" — at inference time gives the model extra computation steps and improves accuracy. The tokens carry no linguistic meaning; they simply add depth. This is the minimal confirmation that non-verbal computation helps.

**The progressive approach**: [[icot-internalize-cot|iCoT (Deng et al., 2024)]] took existing chain-of-thought traces and progressively removed tokens during training, teaching models to internalize reasoning. The result: GPT-2 and Mistral-7B achieve 51% on GSM8K with no visible reasoning steps and an 11x inference speedup. The model learned to compress explicit reasoning into implicit computation.

**The breakthrough**: [[coconut-reasoning-latent-space|Coconut (Hao et al., 2024)]] demonstrated that feeding a model's last hidden state back as its next input embedding creates a "continuous thought" loop. The model reasons silently in vector space, producing language only when communicating results. The stunning finding: continuous thoughts spontaneously encode **multiple reasoning paths simultaneously** (emergent BFS), achieving 97.0% on planning tasks vs. 77.5% for chain-of-thought.

**The barrier**: Coconut only works on base models. [[softcot-efficient-reasoning|SoftCoT (ACL 2025)]] showed that Coconut's curriculum training **damages instruction-tuned models** — LLaMA-3.1-8B drops from 79.61% to 76.12% on GSM8K. This [[catastrophic-forgetting]] barrier is the central unsolved problem for deploying latent reasoning in production. The instruction-tuning pipeline creates a delicate balance that curriculum training disrupts, as documented in [[contradictions]].

**A second, orthogonal barrier**: [[latent-reasoning-supervision-analysis|Cui et al. (2026)]] documents a **supervision–exploration trade-off** that bounds the design space from a different angle. Strong supervision (CoLaR-style token-level alignment) eliminates shortcut behavior but **destroys latent diversity** (collapsing to ~3 distinct outcomes vs. ~16 for weakly-supervised methods); weak supervision preserves capacity but lets the model bypass its own latent steps entirely (most methods retain accuracy at depth=0 and under noise injection). Together, the catastrophic forgetting barrier and the supervision–exploration trade-off **bound the latent reasoning design space from both sides**, explaining why no method has yet matched both strong CoT performance AND demonstrably-used latent reasoning at the same time.

**Three workarounds** exist, each with trade-offs:

- **[[softcot-efficient-reasoning|SoftCoT]]** freezes the backbone and trains only a small projection layer, producing 6 soft tokens that approximate 24 hard tokens (4x compression). It preserves instruction-tuning (+2.31pp average on benchmarks) but the latent thoughts are external to the model.
- [[thinking-states-latent-reasoning|**Thinking States**]] uses teacher forcing and compressed natural-language states, achieving 2.66x speedup and 97.71% out-of-distribution generalization. It also identified a fundamental limitation of causal latent reasoning: **state ambiguity** — when the question appears at the end of the input, the model may commit to reasoning about the wrong quantity before seeing what is being asked. Prepending the question yields a 15% relative gain (42.22% to 48.65%).
- [[latentmas-collaboration|**LatentMAS**]] sidesteps training entirely with ridge regression alignment, but is limited to homogeneous architectures.

None fully solve [[catastrophic-forgetting|catastrophic forgetting]]. The field needs either a training approach that preserves instruction-tuning or an architectural innovation that bypasses the problem entirely. [[vision-wormhole-heterogeneous|Vision Wormhole]]'s use of the visual pathway is the most promising architectural bypass currently proposed — since the text pathway remains untouched, it may avoid the forgetting problem entirely.

## Thread 2: Latent Communication (Inter-Agent)

When multiple models collaborate, the discrete bottleneck doubles: the sender must compress its knowledge into tokens, and the receiver must reconstruct the intent from them. The [[latent-communication]] and [[communication-depth-spectrum]] trace a 10-level depth spectrum from natural language (~15 bits/position) to full KV-cache + latent thought sharing ($471\times$ compression). Each level trades compatibility for information density.

**Embeddings**: [[cipher-multiagent-debate-embeddings|CIPHER]] transmits weighted token embedding averages. It requires only a shared tokenizer and achieves +0.5-5% over text debate. The approach stays within the vocabulary's convex hull, making it the safest entry point for latent communication.

**State deltas**: [[state-delta-trajectory|SDE]] shares inter-token hidden-state differences rather than raw states. A key finding: deltas outperform raw states, and raw states sometimes **degrade below the natural language baseline**. This suggests reasoning *dynamics* are more transferable than reasoning *states* — a distinction with deep implications for how we think about knowledge transfer. However, deltas require identical model weights, the most restrictive compatibility requirement in the spectrum.

**Activations**: [[activation-communication-harvard|AC]] replaces a single activation at approximately layer 26 for less than one-quarter compute. The most striking result: cross-family transfer (LLaMA/Qwen/Gemma) works even **without a learned mapping** — raw activation replacement transfers knowledge with zero learned parameters on 48 of 57 MMLU topics. This is the strongest empirical evidence for the [[platonic-representation-hypothesis|Platonic Representation Hypothesis]].

**KV-cache**: Four papers explore complementary dimensions. [[kvcomm-selective-kv-sharing|KVComm]] discovered that 30% of KV layers approximately equals full performance — massive redundancy in what is shared. [[cache-to-cache-semantic-communication|C2C]] builds per-pair neural fusers enabling cross-family transfer (+6.4-14.2% vs. receiver alone, 2.5x speedup). [[kv-cache-alignment-shared-space|KV Cache Alignment]] solves C2C's $O(N^2)$ scaling with a shared interlingua space requiring only $O(N)$ adapters, and discovered a surprising **self-improvement effect**: cyclic translation through the shared space actually improves the original model's language modeling. [[kvcomm-online-cross-context|KVCOMM-online]] tackles the systems-level problem of overlapping context with anchor-based reuse, achieving 6.7x average prefill speedup with less than 2.5% quality drop.

**Structured thoughts**: [[thought-communication-multiagent|ThoughtComm]] adds identifiability guarantees, decomposing latent states into shared/private factors with agreement-based routing and proving (Theorems 1-3) that the factors can be recovered. This is the most theoretically principled approach, connecting to [[latent-variable-model]] and laying groundwork for the safety and auditability concerns explored in [[safety-interpretability]].

## The Cross-Architecture Challenge

The central tension, mapped in detail by [[cross-architecture]], is that **deeper communication channels carry more information but demand tighter architectural coupling**. Natural language works between any two models; KV-cache sharing requires identical architectures; state deltas require identical weights.

The field is bending this curve through three strategies:

1. **Learned linear maps** — AC shows that a single task-agnostic projection trained on 3,072 C4 sentences bridges model families. The cost scales $O(N^2)$ with pool size, but the maps are cheap to compute.
2. **Shared interlingua spaces** — KV Cache Alignment trains two adapters per model (into and out of a global shared space), scaling $O(N)$. New models join by training two adapters; untrained paths work zero-shot. Currently validated only at 100M-400M scale.
3. **Architectural bypass** — [[vision-wormhole-heterogeneous|Vision Wormhole]] routes communication through VLM visual input pathways, which are explicitly designed to accept dense continuous vectors. Hub-and-spoke alignment via ridge regression on anchor texts scales $O(N)$ and achieves +6.3pp accuracy and 1.87x speedup over text MAS across fully heterogeneous pools (Gemma, Qwen, SmolVLM, LFM at 1.6B-4B scale). At mid-scale (4B-12B), speedups reach 5.92x but accuracy degrades, suggesting a fixed bandwidth bottleneck.

The counter-example matters: [[latentmas-collaboration|LatentMAS]] demonstrates what happens when cross-architecture compatibility is ignored. Its training-free KV-cache transfer works well within Qwen-family models but catastrophically fails on LLaMA (-10.1% average), illustrating how same-architecture assumptions break down across families.

## The Convergence: Unified Frameworks

Three systems combine both threads — latent reasoning within agents AND latent communication between agents — as detailed in [[unified-frameworks]]:

- **[[latentmas-collaboration|LatentMAS]]**: Training-free, 4x faster than text MAS, GSM8K 95.2%, 70-84% token reduction. Homogeneous architecture only.
- **[[vision-wormhole-heterogeneous|Vision Wormhole]]**: Repurposes VLM visual pathways as universal continuous channels, solving the heterogeneous architecture problem. The only system that works across fully different model families without per-pair training.
- **[[agent-primitives-building-blocks|Agent Primitives]]**: Composable operators (Review/Voting/Planning) structured by an Organizer agent. Outperforms 10 existing MAS methods, achieving 75.3% average vs. 58.8% single-agent (+16.5pp) on Qwen3-8B. Uses **fewer tokens than single agents** on smaller models, with only 1.3-1.6x latency overhead. Critical detail: RoPE positional re-encoding is mandatory for LLaMA models (without it, 27-60pp accuracy drops).

## The Safety and Interpretability Tension

As latent communication grows more capable, it also grows more opaque. When agents exchange raw hidden states or KV-cache entries, no human can inspect what was communicated. This creates a fundamental tension explored in [[safety-interpretability]]: the methods that carry the most information are the hardest to audit.

Two approaches offer partial solutions. [[thought-communication-multiagent|ThoughtComm]]'s identifiable latent factors provide mathematical guarantees that communicated content can be decomposed and inspected. [[latentcompress-open-call|LatentCompress]]'s slot-attention probing mechanism enables interpretable compression where the bottleneck itself becomes a point of inspection. But neither has been tested at the scale or adversarial rigor required for deployment in safety-critical systems.

The practical implication: any production deployment of latent multi-agent systems must choose a position on the information-density vs. auditability frontier. [[practical-systems]] provides a decision guide that includes safety and auditability as explicit constraint dimensions.

## Compression and Information-Theoretic Bounds

A recurring theme across the literature is that latent representations contain massive redundancy. [[kvcomm-selective-kv-sharing|KVComm]] shows 30% of layers suffice. [[interlat-latent-space-agents|Interlat]] compresses 500+ latent steps to 8 with only 4% accuracy drop and 46x speedup. [[softcot-efficient-reasoning|SoftCoT]] achieves 4x token compression. [[latentcompress-open-call|LatentCompress]] establishes concrete bandwidth targets: 512 bytes suffices for simple tasks (GSM8K matches 91% baseline), but hard reasoning tasks (GPQA) need MB-scale bandwidth.

These results hint at a deeper question explored in [[compression-information-theory]]: what is the **minimum sufficient representation** for inter-agent communication? The bandwidth-accuracy relationship follows an S-curve with cumulative degradation modeled as $Q \propto e^{-T\varepsilon/C}$. But no paper has established theoretical lower bounds on the bandwidth needed to transmit a reasoning trajectory losslessly. If the true minimum is far below current transmission sizes — which the 46x compression result suggests — latent communication could become essentially free for real-time applications.

## What We Know (Established Results)

- **Continuous > discrete for inter-model transfer**: Every paper in the communication thread confirms this, across diverse architectures and tasks.
- **Superposition is real and provable**: Not a metaphor — continuous thoughts mathematically encode parallel BFS paths, reducing complexity from $O(n^2)$ to $D$ steps.
- **Cross-family communication works**: AC demonstrates zero-shot activation transfer across LLaMA/Qwen/Gemma. The Platonic Representation Hypothesis provides theoretical grounding.
- **30% of KV layers $\approx$ full performance**: [[kvcomm-selective-kv-sharing|KVComm]]'s finding suggests massive redundancy in what is transmitted between agents.
- **Training-free methods are competitive**: [[latentmas-collaboration|LatentMAS]], [[agent-primitives-building-blocks|Agent Primitives]], [[kvcomm-selective-kv-sharing|KVComm]], and [[state-delta-trajectory|SDE]] achieve strong results without model modification.
- **Scaling is task-contingent**: The [[scaling-agent-systems|Scaling paper]] shows multi-agent benefits range from +80.9% (finance) to -70% (sequential planning). The baseline paradox (beta = -0.404) means single-agent accuracy above ~45% often makes MAS counterproductive.
- **Composable primitives > ad-hoc designs**: Agent Primitives' structured operators outperform monolithic MAS architectures across 5 model families.
- **Self-improvement through shared spaces**: Cyclic translation through a shared latent space improves the original model — an unexplained but reproducible phenomenon observed in [[kv-cache-alignment-shared-space|KV Alignment]], [[cache-to-cache-semantic-communication|C2C]], and KVComm.

## What We Don't Know (Open Frontier)

The [[open-questions|open questions]] cluster around several themes, and the [[frontier-research-directions|frontier research directions]] synthesize 8 paradigm-shift opportunities:

1. **Scale**: Almost everything is tested at 1-14B parameters. Does superposition persist at 70B+? Do layer selection patterns hold? [[kv-cache-alignment-shared-space|KV Cache Alignment]] is validated only at 100M-400M.
2. **Catastrophic forgetting**: No fundamental fix exists for enabling latent reasoning on instruction-tuned models. [[softcot-efficient-reasoning|SoftCoT]]'s frozen backbone, [[thinking-states-latent-reasoning|Thinking States]]' teacher forcing, and [[latentmas-collaboration|LatentMAS]]'s training-free approach are workarounds, not solutions.
3. **Cross-architecture universality**: The Platonic Representation Hypothesis is promising but not proven at scale. Cross-tokenizer communication remains unsolved. [[vision-wormhole-heterogeneous|Vision Wormhole]]'s bandwidth bottleneck at mid-scale suggests architectural bypasses have their own limits.
4. **Information-theoretic bounds**: We lack the minimum bandwidth for lossless latent communication, or principled understanding of where discrete representations actually win.
5. **Beyond reasoning benchmarks**: All results are on math/logic/QA. Creative generation, dialogue, and open-ended tasks are unexplored.
6. **Safety at scale**: No adversarial evaluation of latent communication channels exists. The interpretability tools ([[thought-communication-multiagent|ThoughtComm]], [[latentcompress-open-call|LatentCompress]] probing) are untested against intentional misuse.

The two biggest bets from the [[frontier-research-directions|frontier analysis]]: **(1)** superposition reasoning at frontier scale with disentanglement control — connecting [[coconut-reasoning-latent-space|Coconut]]'s emergent BFS with [[thought-communication-multiagent|ThoughtComm]]'s identifiability framework to create controllable tree search in latent space, and **(2)** state deltas as transferable reasoning templates — building libraries of context-agnostic reasoning dynamics that provide instant problem-solving without chain-of-thought generation.

## The Research Ecosystem

Six institutions drive most of the work tracked here:

| Institution | Key Contributions | Focus Area |
|------------|-------------------|------------|
| [[fair-meta\|FAIR/Meta]] | [[coconut-reasoning-latent-space\|Coconut]], [[thought-communication-multiagent\|ThoughtComm]], LLaMA ecosystem | Latent reasoning, structured communication |
| [[cmu\|CMU]] | [[thought-communication-multiagent\|ThoughtComm]], [[vision-wormhole-heterogeneous\|Vision Wormhole]] | Cross-architecture, identifiability |
| [[tsinghua\|Tsinghua]] | [[cache-to-cache-semantic-communication\|C2C]], [[state-delta-trajectory\|SDE]] | KV-cache fusion, state deltas |
| [[kth\|KTH]] | [[kvcomm-selective-kv-sharing\|KVComm]] | Efficient KV-cache selection |
| [[google-deepmind\|Google DeepMind]] | [[kv-cache-alignment-shared-space\|KV Cache Alignment]], [[scaling-agent-systems\|Scaling paper]] | Scalable shared spaces |
| [[google-research\|Google Research]] | [[thinking-states-latent-reasoning\|Thinking States]] | Production-viable latent reasoning |

Additional contributors include [[harvard|Harvard]] (AC, iCoT, Du et al. debate), [[princeton-uiuc-stanford|Princeton/UIUC/Stanford]] ([[latentmas-collaboration|LatentMAS]], [[agent-primitives-building-blocks|Agent Primitives]]), [[purdue|Purdue]] ([[vision-wormhole-heterogeneous|Vision Wormhole]]), [[mit|MIT]] ([[multiagent-debate-du-et-al|Multiagent Debate]], [[platonic-representation-hypothesis|Platonic Representation Hypothesis]]), [[mbzuai|MBZUAI]] (ThoughtComm), and **[[amazon|Amazon]]** ([[latent-reasoning-supervision-analysis|Latent Reasoning Supervision Analysis]] — the first systematic empirical critique of the field's central BFS hypothesis, in collaboration with Michigan State University). The [[paper-timeline|paper timeline]] shows the field's acceleration from theoretical foundations (2022-2023) through a 2025 Cambrian explosion to 2026 unification efforts and the first wave of diagnostic critique.

## Where This Is Heading

The distinction between "thinking" and "communicating" is dissolving. Both are continuous representation flow — within a model or between models. The unified frameworks ([[latentmas-collaboration|LatentMAS]], [[vision-wormhole-heterogeneous|Vision Wormhole]], [[agent-primitives-building-blocks|Agent Primitives]]) are early instances of a future where multi-agent systems operate entirely in continuous space, with discrete language used only at the human interface.

The practical timeline depends on solving two problems: [[catastrophic-forgetting|catastrophic forgetting]] (enabling latent reasoning on production models) and cross-architecture alignment (enabling heterogeneous agent teams). [[vision-wormhole-heterogeneous|Vision Wormhole]]'s architectural bypass and [[kv-cache-alignment-shared-space|KV Alignment]]'s shared spaces are the most promising current paths, but both face scaling barriers that remain untested beyond 14B parameters.

A third challenge is emerging: as these systems become practical, the safety and interpretability question moves from theoretical concern to deployment blocker. The field must develop auditing tools that work at the speed and information density of latent communication — [[thought-communication-multiagent|ThoughtComm]]'s identifiable factors and [[latentcompress-open-call|LatentCompress]]'s slot-attention probing are starting points, but the gap between current capability and deployment-grade trust is large.

For the complete method comparison across all dimensions, see [[method-comparison]]. For tensions and contradictions between papers, see [[contradictions]]. For benchmark coverage and blind spots, see [[benchmark-overlap]].

## Navigation

All 9 Maps of Content provide guided reading paths into specific themes:

- [[latent-reasoning]] — Intra-agent continuous reasoning, from pause tokens to Coconut
- [[latent-communication]] — Inter-agent information exchange across the depth spectrum
- [[communication-depth-spectrum]] — The 10-level depth-compatibility walkthrough
- [[unified-frameworks]] — Systems combining reasoning and communication
- [[theoretical-foundations]] — Complexity theory, representation geometry, convergence
- [[practical-systems]] — Engineering decisions, scaling constraints, deployment trade-offs
- [[cross-architecture]] — The compatibility problem and three strategies for solving it
- [[safety-interpretability]] — Auditability, adversarial risks, and the opacity-capability trade-off
- [[compression-information-theory]] — Bandwidth bounds, redundancy, and optimal latent codecs
