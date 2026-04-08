---
type: analysis
title: "Open Questions"
created: "2026-04-06"
updated: "2026-04-08"
tags: [open-questions, synthesis]
---

# Open Questions

All open questions across the wiki, aggregated from concept pages and grouped by theme. For the 8 paradigm-shift research directions synthesized from these questions, see [[frontier-research-directions]].

---

## Scaling & Frontier Models

Questions about whether current findings hold at production scale. This is arguably the highest-priority cluster: if latent methods do not transfer to frontier-scale models, the entire research program risks being an artifact of small-model regimes.

- Does BFS emergence persist with larger, more capable models? [[coconut-reasoning-latent-space|Coconut]] tested only at GPT-2 scale; [[softcot-efficient-reasoning|SoftCoT]] and [[latentmas-collaboration|LatentMAS]] at 7–14B. — [[latent-space-reasoning]]
- Do KV-cache layer selection patterns and fusion benefits hold at 70B+ scale? Most experiments use 0.6B–14B models. — [[kv-cache-communication]]
- Does the advantage of embedding communication grow or shrink as models scale? Larger models may encode more in discrete tokens, narrowing the gap. — [[embedding-space-communication]], [[continuous-vs-discrete-representation]]
- [[activation-communication-harvard|AC]] finds layer 26/32 optimal for LLaMA. Is this consistent across architectures? Does it scale with model depth? — [[activation-communication]]
- [[agent-primitives-building-blocks|Agent Primitives]] tests up to 70B (DeepSeek-R1-Distill-Llama-70B) and finds that gains shrink from +16.5pp at 8B to +6.3pp at 70B. Is this a general pattern — do latent methods converge with single-agent performance at frontier scale? — [[agent-primitives-building-blocks]]
- The scaling framework from Kim et al. finds a **capability saturation threshold** at $\sim$45% single-agent accuracy, beyond which multi-agent coordination yields diminishing returns. Does latent communication shift this threshold upward? — [[scaling-agent-systems]], [[latentmas-collaboration]]
- [[vision-wormhole-heterogeneous|Vision Wormhole]]'s fixed bandwidth (256 visual tokens) becomes a bottleneck at 8B+ scale, causing accuracy drops of up to -33pp on hard tasks. What is the **bandwidth-model size scaling law** for latent communication channels? — [[vision-wormhole-heterogeneous]]
- Does the super-linear agent scaling exponent ($T \propto n^{1.724}$) change under latent communication, where coordination overhead is reduced? — [[scaling-agent-systems]]

The tension between these questions is sharp: [[agent-primitives-building-blocks|Agent Primitives]]' shrinking gains at 70B suggest diminishing returns, but the scaling framework's saturation threshold suggests the *type* of improvement may change (from accuracy to efficiency or robustness). Resolving this requires controlled experiments that hold task difficulty constant while varying model scale — currently no paper does this systematically.

## The Catastrophic Forgetting Barrier

The central unsolved tension for latent reasoning on instruction-tuned models.

- Can latent reasoning be trained **without damaging** instruction-tuned models? [[softcot-efficient-reasoning|SoftCoT]]'s externalization and [[latentmas-collaboration|LatentMAS]]'s training-free approach are workarounds — is there a fundamental fix? — [[latent-space-reasoning]], [[catastrophic-forgetting]]
- What's the optimal **hybrid discrete-continuous ratio**? [[thinking-states-latent-reasoning|Thinking States]] generates NL thoughts then compresses. Is this "best of both worlds" or an awkward compromise? — [[latent-space-reasoning]]
- LatentMAS catastrophically fails on LLaMA-based backbones (DeepSeek-R1-Distill-Llama-70B drops -10.1pp average) despite being training-free. Is this a failure of the ridge-regression alignment or a fundamental architectural sensitivity? [[agent-primitives-building-blocks|Agent Primitives]] shows LLaMA's extreme sensitivity to RoPE misalignment as a possible root cause. — [[latentmas-collaboration]], [[agent-primitives-building-blocks]]
- Could RL-based approaches (PPO/GRPO on latent thought quality) enable latent reasoning on instruction-tuned models without the curriculum training that causes forgetting? — [[frontier-research-directions]]
- **Solving the supervision–exploration trade-off**: Stronger supervision eliminates [[latent-reasoning-supervision-analysis|shortcut behavior]] but **destroys latent diversity** (CoLaR collapses to ~3 distinct outcomes vs. ~16 for Coconut). Is there a training scheme that prevents shortcut behavior without collapsing the multi-candidate capacity? Candidates: information-bottleneck objectives, contrastive losses on latent diversity, hybrid curricula combining strong and weak supervision phases. — [[catastrophic-forgetting]], [[latent-reasoning-supervision-analysis]]
- **Closing the Pass@100 / Maj@100 gap**: [[latent-reasoning-supervision-analysis|Cui et al.]] show that latent reasoning preserves correct candidates (Pass@100 ~70-82%) but fails to amplify them at decode time (Maj@100 ~40%, *below* explicit reasoning). [[inference-time-scaling-continuous-reasoning|Wang et al. (2025)]] *implemented* the obvious fix — train PRM (hard + soft) and ORM via MATH-Shepherd MC annotation on dropout-sampled COCONUT trajectories — and recovered only 19.8% of the available headroom (33.36% best vs. 42.61% Pass@N upper bound at N=16); PRM/ORM classification F1 hovers near chance (54%/52%). The diagnosis: continuous-thought representations exhibit IsoScore$\star \approx 0.013$ (extreme anisotropy) and produce statistically indistinguishable values across compactness, curvature, local smoothness, and straightness metrics for correct vs. incorrect thoughts. **The remaining open question is no longer "can a reranker work?" but "what training-time inductive biases (isotropy regularization, contrastive losses on latent diversity, trajectory-diversity objectives) would produce continuous thoughts that *can* be discriminated?"** — [[latent-space-reasoning]], [[latent-reasoning-supervision-analysis]], [[inference-time-scaling-continuous-reasoning]]

The LLaMA sensitivity finding from Agent Primitives is particularly important because it suggests the forgetting barrier may be architecture-dependent, not universal. A systematic study comparing Qwen, LLaMA, Gemma, and Mistral families under identical latent reasoning training would clarify whether some architectures are inherently more amenable to latent-space modification.

The supervision–exploration trade-off is **orthogonal** to the alignment trade-off: it concerns the new latent capability rather than pre-existing instruction-tuning. Together they bound the latent reasoning design space from both sides — see [[catastrophic-forgetting#The Second Barrier: The Supervision–Exploration Trade-Off|catastrophic forgetting's second barrier]] for the joint discussion.

## Cross-Architecture Compatibility

The fundamental trade-off: deeper communication = tighter coupling.

- How to communicate between models with **different tokenizers** or embedding spaces? The major unsolved problem. — [[embedding-space-communication]]
- Are there modality-specific pathways beyond vision (e.g., audio) that could serve as universal communication ports? — [[activation-communication]]
- Can thought structure be inferred from **observable outputs** (text, logits) for closed-source models? — [[thought-structure]]
- Is there an **optimal compression point** between full continuous and full discrete that captures most information with broad compatibility? — [[continuous-vs-discrete-representation]]
- Can models learn to communicate in a compressed continuous space that preserves **task-relevant** information while being compatible across architectures? — [[continuous-vs-discrete-representation]]
- [[vision-wormhole-heterogeneous|Vision Wormhole]] demonstrates that VLM visual pathways serve as a natural cross-architecture port with $O(N)$ alignment. Can **non-VLM modalities** (audio encoders, code embeddings) similarly be repurposed as universal communication interfaces? — [[vision-wormhole-heterogeneous]]
- [[agent-primitives-building-blocks|Agent Primitives]] require same-model configurations to satisfy the input-output alignment assumption. Can this assumption be relaxed with lightweight adapters while preserving the composable-primitive design? — [[agent-primitives-building-blocks]]
- The Platonic Representation Hypothesis predicts that model representations converge as scale increases. At what scale threshold does cross-architecture latent communication become reliable **without** learned adapters? — [[platonic-representation-hypothesis]], [[activation-communication-harvard]]
- [[activation-communication-harvard|AC]] succeeds zero-shot across LLaMA/Qwen/Gemma families at the activation level, but [[cache-to-cache-semantic-communication|C2C]] and [[kv-cache-alignment-shared-space|KV Alignment]] require learned components at the KV-cache level. Is this because activations converge faster than KV representations, or is it an artifact of evaluation setup? — [[contradictions]]

The cross-architecture picture is evolving rapidly. Six months ago, cross-family latent communication required heavy training (C2C). Now, AC demonstrates zero-shot cross-family transfer, and Vision Wormhole achieves heterogeneous VLM communication with weak supervision ($<100$ anchors). The trend suggests that cross-architecture compatibility may be a solved problem within 1-2 years for models above a certain scale — but the theoretical understanding of *why* it works (beyond the Platonic hypothesis) remains thin.

## Information Theory & Capacity Bounds

Theoretical gaps in understanding the communication spectrum.

- What is the theoretical **information capacity** of embedding communication vs. natural language? — [[embedding-space-communication]]
- What's the theoretical **minimum bandwidth** for lossless activation communication? [[interlat-latent-space-agents|Interlat]] compresses to 8 latent steps with 4% drop. — [[activation-communication]]
- When does discrete win? Are there tasks where discretization's structure is actually helpful — compositional generalization, symbolic reasoning, error correction? — [[continuous-vs-discrete-representation]]
- [[latentcompress-open-call|LatentCompress]] achieves 512-byte communication matching GSM8K baseline but needs MB-scale bandwidth for GPQA. What is the **bandwidth-task complexity relationship** — can it be predicted from task properties (e.g., number of reasoning hops, answer entropy)? — [[latentcompress-open-call]]
- [[latentmas-collaboration|LatentMAS]] proves a $d / \log|V|$ theoretical compression bound ($\sim$471x for Qwen3-14B). Is this bound tight, or can structured latent representations exceed it via superposition? — [[latentmas-collaboration]], [[superposition-coconut-theory]]
- Cumulative degradation across agent chains follows $Q \propto e^{-T\varepsilon/C}$. Can error-correcting codes or redundant latent dimensions break this exponential decay? — [[latentcompress-open-call]]
- What is the **rate-distortion optimal** compression for inter-agent communication at a given task complexity? Neural compression literature may provide frameworks but they assume i.i.d. sources, not structured reasoning trajectories. — [[frontier-research-directions]]

The information-theoretic questions are especially important because they connect to practical engineering decisions. If the bandwidth-task complexity relationship can be characterized, system designers could adaptively select communication depth per query (e.g., use 512-byte compressed latents for simple arithmetic, full KV-cache for multi-hop reasoning). This is what [[agent-primitives-building-blocks|Agent Primitives]]' Organizer does at the topology level; an analogous mechanism at the bandwidth level does not yet exist.

## Iterative & Multi-Round Communication

Most methods are tested in single-round or limited settings.

- How does KV-cache communication work in **iterative debate** settings? All papers evaluate single-round. — [[kv-cache-communication]]
- Could iterative activation grafting (multiple rounds) combine AC's information density with debate's iterative refinement? — [[activation-communication]]
- [[agent-primitives-building-blocks|Agent Primitives]]' Review primitive implements a 2-round latent feedback loop (Solver $\to$ Critic $\to$ Solver). How does performance scale with additional rounds, and is there a point of diminishing returns analogous to the message density saturation ($\mu \approx 0.39$) found by the scaling framework? — [[agent-primitives-building-blocks]], [[scaling-agent-systems]]
- KV Alignment's self-improvement effect (A $\to$ $\Omega$ $\to$ A improves model A) suggests that iterative cycling could be beneficial. Does this improvement saturate or continue monotonically? — [[kv-cache-alignment-shared-space]], [[frontier-research-directions]]

## Structure & Interpretability

How to organize, audit, and debug latent communication. This cluster connects directly to safety (opaque communication cannot be audited) and to scaling (structured communication may scale better than unstructured). [[thought-communication-multiagent|ThoughtComm]]'s identifiability theorems provide the strongest formal foundation, but they assume a specific generative model that may not hold for all methods.

- How many latent thought dimensions are needed? Can this be determined **automatically** via variational or information-theoretic criteria? — [[thought-structure]]
- Does thought structure **evolve across debate rounds** as agents update reasoning? Can the framework adapt in real time? — [[thought-structure]]
- Can disentangled latent thoughts serve as an **interpretability tool** — revealing *why* agents disagree? — [[thought-structure]]
- Can the framework distinguish between **informative thoughts and noise**? — [[thought-structure]]
- Does pairwise identifiability composition remain robust with **dozens or hundreds of agents**? — [[thought-structure]]
- How do we **audit, debug, and verify** reasoning in opaque continuous space? — [[latent-space-reasoning]]
- [[agent-primitives-building-blocks|Agent Primitives]] introduce a meta-level structure (Review/Voting/Planning primitives) selected by an Organizer. Can this structural decomposition be learned end-to-end rather than pre-specified, and could the Organizer itself operate in latent space? — [[agent-primitives-building-blocks]]
- [[vision-wormhole-heterogeneous|Vision Wormhole]]'s style token encodes distributional statistics $[\text{mean}, \text{std}, \text{RMS}]$ of the latent rollout. Could richer structural metadata (e.g., attention entropy, layer-wise activation norms) improve cross-model alignment without additional training? — [[vision-wormhole-heterogeneous]]

## Design Combinations

Unexplored combinations of existing techniques. The methods in this wiki address orthogonal dimensions (what to share, how to fuse, how to select layers, how to structure). The most promising near-term research may not be new methods but systematic combinations of existing ones.

- Can [[kvcomm-kth-selective|KVComm]]'s attention-based layer selection improve C2C's gating, or vice versa? — [[kv-cache-communication]]
- Could **token-level** KV selection (which positions to share) further improve efficiency beyond layer selection? — [[kv-cache-communication]]
- Could disentangled thought extraction be applied **specifically to KV-caches**, combining [[thought-communication-multiagent|ThoughtComm]]'s structure with KV's attention-native integration? — [[kv-cache-communication]]
- Could [[agent-primitives-building-blocks|Agent Primitives]]' composable primitive design be combined with [[vision-wormhole-heterogeneous|Vision Wormhole]]'s cross-architecture channel to create **heterogeneous composable MAS** where different primitives use different backbone models? — [[agent-primitives-building-blocks]], [[vision-wormhole-heterogeneous]]
- Can [[state-delta-trajectory|SDE]]'s delta-based communication be composed with [[latentmas-collaboration|LatentMAS]]'s KV-cache transfer — e.g., transmitting **KV-cache deltas** between rounds rather than full caches? — [[state-delta-trajectory]], [[latentmas-collaboration]]
- Could [[interlat-latent-space-agents|Interlat]]'s 3-loss training framework ($\Loss_{\text{task}} + \Loss_{\text{sep}} + \Loss_{\text{align}}$) be applied to train KV-cache fusers, potentially improving C2C's cross-architecture performance? — [[interlat-latent-space-agents]], [[cache-to-cache-semantic-communication]]
- Agent Primitives' Knowledge Pool stores 45 MAS configurations. Could this be expanded with **latent-space benchmarks** that encode when each communication depth (embedding, KV, activation) is optimal per task type? — [[agent-primitives-building-blocks]], [[scaling-agent-systems]]

## Beyond Reasoning Benchmarks

Generalization to broader tasks and settings. Nearly every method in this collection is evaluated on math reasoning (GSM8K, MATH, AIME) or multiple-choice QA. The narrow benchmark focus creates a selection bias — we do not know whether the advantages of latent communication generalize to the long-form, open-ended tasks that dominate real-world deployment.

- Can these methods scale to **open-ended tasks** (summarization, creative writing, dialogue)? — [[embedding-space-communication]]
- Can latent-space reasoning apply to **creative generation, dialogue**, or other non-reasoning tasks? — [[latent-space-reasoning]]
- [[thinking-states-latent-reasoning|Thinking States]] identifies reasoning about the wrong quantity before seeing the question. Can **bidirectional architectures** solve state ambiguity generally? — [[latent-space-reasoning]]
- No latent communication system supports **tool calling**. Can a learned router decide when to stay in latent space vs. decode to tokens for tool invocation? — [[latentcompress-open-call]]
- [[agent-primitives-building-blocks|Agent Primitives]] test on math, code, and QA but not on **agentic tasks** (web navigation, software engineering). Do composable KV-cache primitives generalize to tasks requiring environment interaction? — [[agent-primitives-building-blocks]]
- The scaling framework finds -70% degradation on sequential planning tasks with text-based MAS. Could latent communication's reduced error propagation make MAS viable for these currently-hostile task types? — [[scaling-agent-systems]]
- [[interlat-latent-space-agents|Interlat]] is the only method evaluated on an **agentic benchmark** (ALFWorld, 70.48%). Can other latent methods (Agent Primitives, Vision Wormhole) match or exceed this on interactive tasks that require grounded environment feedback? — [[interlat-latent-space-agents]]
- [[vision-wormhole-heterogeneous|Vision Wormhole]] shows +13.2pp on code generation, but code tasks involve structured outputs where partial errors can cascade. Does latent communication's richer signal help or hurt on tasks where **output structure** is critical? — [[vision-wormhole-heterogeneous]]

## Diversity & Temperature

- Should temperatures **change across debate rounds** (start diverse, converge)? — [[temperature-diversity]]
- With 3+ agents, what's the **optimal distribution** of temperatures? — [[temperature-diversity]]
- Could an agent **dynamically adjust** temperature based on position-level uncertainty? — [[temperature-diversity]]
- In latent communication, diversity is controlled not just by temperature but by the **communication channel itself** — embedding averages smooth over uncertainty, while raw activations preserve it. Does the optimal temperature setting depend on the communication depth? — [[continuous-vs-discrete-representation]], [[temperature-diversity]]
- [[agent-primitives-building-blocks|Agent Primitives]]' Voting primitive generates $N$ independent KV caches and selects in latent space. How does the diversity of these caches compare to temperature-based diversity in text-based voting, and is latent-space selection more robust to the "mode collapse" problem where diverse agents converge to the same wrong answer? — [[agent-primitives-building-blocks]], [[temperature-diversity]]

## Pretraining and Native Integration

All current methods add latent communication capabilities to models that were pretrained for text-only processing. This raises fundamental questions about whether post-hoc adaptation can ever be optimal.

- Would models pretrained with **native latent communication objectives** (e.g., multi-agent communication loss during pretraining) develop fundamentally different and better communication protocols? — [[latentcompress-open-call]]
- The NormMatch rescaling in [[vision-wormhole-heterogeneous|Vision Wormhole]] and the alignment matrix $M$ in [[latentmas-collaboration|LatentMAS]] both address the off-manifold problem — latent representations that fall outside the model's expected input distribution. Is this inherently a consequence of post-hoc adaptation, and would natively trained models avoid it entirely? — [[vision-wormhole-heterogeneous]], [[latentmas-collaboration]]
- Current compression results (512 bytes matching GSM8K baseline) are achieved with modules trained on top of frozen models. Could end-to-end training with a communication bottleneck during pretraining achieve **orders of magnitude** better compression? — [[latentcompress-open-call]], [[frontier-research-directions]]
- If native latent communication is integrated into pretraining, what is the right **curriculum** — should models first learn language, then latent communication (sequential), or both simultaneously (joint)? The curriculum question mirrors the Coconut training challenge but at pretraining scale. — [[coconut-reasoning-latent-space]], [[catastrophic-forgetting]]
- Vision Wormhole's self-distillation training (text path as teacher, vision path as student) suggests a bridge: models could be pretrained normally, then fine-tuned with self-distillation to develop latent channels without [[catastrophic-forgetting|catastrophic forgetting]]. Is self-distillation a **general solution** to the post-hoc adaptation problem? — [[vision-wormhole-heterogeneous]], [[softcot-efficient-reasoning]]

## Safety & Robustness

Safety questions become increasingly urgent as latent communication moves toward deployment. The fundamental tension: latent channels are more information-dense and more robust to noise, but they are also more opaque and harder to monitor. Every gain in communication efficiency creates a corresponding loss in auditability.

- Can a malicious agent craft embedding vectors that **exploit the receiver's processing** in ways discrete tokens cannot? — [[embedding-space-communication]]
- [[agent-primitives-building-blocks|Agent Primitives]] show KV-cache communication is dramatically more robust to noise injection than natural language (93% vs 47% accuracy at 10 noise sentences). Does this robustness hold against **adversarial** noise specifically crafted to exploit continuous communication? — [[agent-primitives-building-blocks]]
- As latent communication becomes more opaque (hidden states > KV-cache > embeddings > text), the **auditability surface** shrinks. What minimum monitoring hooks are needed to detect anomalous latent communication patterns? — [[contradictions]]
- [[latentcompress-open-call|LatentCompress]]'s information bottleneck + adversarial training reduces style leakage from 35.2% to 13.5%. Can similar techniques prevent **model fingerprinting** through latent channels — i.e., prevent receivers from identifying which model sent a message? — [[latentcompress-open-call]]
- [[vision-wormhole-heterogeneous|Vision Wormhole]] injects sender reasoning through the visual pathway while the text pathway remains untouched. Could this architectural separation be **exploited** — e.g., a sender injecting adversarial visual tokens that override text-based safety guardrails? — [[vision-wormhole-heterogeneous]]
- Multi-agent latent systems create **emergent communication protocols** not designed by humans. How do we verify that these protocols do not encode harmful coordination strategies (e.g., agents colluding to produce plausible but wrong answers)? — [[thought-structure]], [[latent-space-reasoning]]
- What happens when a latent MAS includes a **compromised agent** with modified weights? In text-based debate, bad-faith arguments can be detected by other agents; in latent communication, malicious representations may be indistinguishable from legitimate ones. — [[embedding-space-communication]], [[activation-communication]]

These safety questions are not merely theoretical. As latent MAS moves toward production ([[agent-primitives-building-blocks|Agent Primitives]] is tested at 70B with frontier-class Organizers like GPT-5.2 and Claude-4), the attack surface expands. The combination of opaque communication, dynamic topology selection, and cross-model latent injection creates novel threat vectors that have no analogue in text-based systems.

A promising direction: [[thought-communication-multiagent|ThoughtComm]]'s disentanglement framework could provide post-hoc interpretability of latent channels — decomposing opaque continuous messages into identifiable latent factors that can be monitored and audited. Whether this scales to production bandwidth remains an open question.
