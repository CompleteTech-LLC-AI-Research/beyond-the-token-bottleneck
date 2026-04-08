---
type: analysis
title: "Contradictions & Tensions Between Papers"
created: "2026-04-06"
updated: "2026-04-08"
tags: [synthesis, contradictions, tensions]
---

# Contradictions & Tensions Between Papers

Systematic tracking of claims that conflict or exist in tension across papers in this wiki. Some are genuine contradictions; others are complementary findings that appear to conflict but operate in different regimes. Distinguishing between the two is important for identifying real research gaps.

---

## 1. The Catastrophic Forgetting Contradiction

**Claim A**: Coconut's multi-stage curriculum successfully trains [[latent-space-reasoning|latent reasoning]] on GPT-2, achieving 97% on ProsQA.
— [[coconut-reasoning-latent-space|Coconut (Hao et al., 2024)]]

**Claim B**: Coconut's curriculum approach **damages** instruction-tuned models. LLaMA-3.1-8B drops from 79.61% to 76.12% on GSM8K when trained with LoRA for latent reasoning.
— [[softcot-efficient-reasoning|SoftCoT (Xu et al., 2025)]]

**Status**: **Genuine tension, different regimes**. [[coconut-reasoning-latent-space|Coconut]] works on base models; it breaks instruction-tuned models. The gap is not a contradiction but a regime boundary — the instruction-tuning pipeline creates a delicate balance that curriculum training disrupts. However, Coconut's paper does not acknowledge this limitation, which [[softcot-efficient-reasoning|SoftCoT]] discovered.

**Resolution needed**: Can curriculum training be modified to work on instruction-tuned models, or is architectural innovation (frozen backbone, training-free) the only path? See [[catastrophic-forgetting]].

---

## 2. Raw States vs. Deltas

**Claim A**: Sharing raw hidden states outperforms text communication. AC shows activation replacement outperforms NLD on 48/57 MMLU topics.
— [[activation-communication-harvard|AC (Ramesh & Li, 2025)]]

**Claim B**: Raw hidden states sometimes **degrade below the natural language baseline**. Deltas (inter-token differences) consistently outperform raw states.
— [[state-delta-trajectory|SDE (Tang et al., 2025)]]

**Status**: **Genuine tension, same regime**. Both test on similar model sizes and benchmarks. The discrepancy may be due to:
- [[activation-communication-harvard|AC]] shares a single layer's activation; [[state-delta-trajectory|SDE]] shares multi-layer deltas — different information content
- AC uses replacement/sum/mean aggregation; SDE uses additive injection — different integration methods
- The tasks where raw states degrade in SDE may be tasks where AC would also struggle

**Resolution needed**: A controlled comparison using the same models, benchmarks, and injection method, varying only whether raw states or deltas are transmitted.

---

## 3. Scaling: More Agents Help vs. Hurt

**Claim A**: [[multi-agent-debate|Multi-agent debate]] consistently improves over single agents. Du et al. shows +8pp on GSM8K; LatentMAS shows +11.5pp; ThoughtComm scales positively with more rounds.
— [[multiagent-debate-du-et-al|Du et al.]], [[latentmas-collaboration|LatentMAS]], [[thought-communication-multiagent|ThoughtComm]]

**Claim B**: Multi-agent scaling is **task-contingent**, not monotonic. Benefits range from +80.9% (finance) to **-70%** (sequential planning). Capability saturation occurs at ~45% single-agent accuracy.
— [[scaling-agent-systems|Scaling Agent Systems (Kim et al., 2025)]]

**Status**: **Complementary, different task distributions**. The debate papers primarily test math/reasoning benchmarks where single-agent accuracy is in the 40–85% range — exactly the regime where the [[scaling-agent-systems|Scaling]] paper predicts multi-agent benefits. The -70% finding is for sequential planning tasks with strong error propagation, which debate papers don't test.

**Resolution needed**: Apply latent communication methods to the Scaling paper's full 180-configuration benchmark set, including the task types where text-based MAS fails. Latent communication's reduced information loss may shift the crossover points.

---

## 4. Cross-Architecture Compatibility: Easy vs. Hard

**Claim A**: Cross-family [[activation-communication|activation communication]] works **without learned projections**. LLaMA ↔ Qwen ↔ Gemma activation transfer succeeds zero-shot.
— [[activation-communication-harvard|AC (Ramesh & Li, 2025)]]

**Claim B**: Cross-architecture [[kv-cache-communication|KV-cache communication]] requires **learned fusers** or a **shared representation space**. Direct KV transfer across architectures fails.
— [[cache-to-cache-semantic-communication|C2C]], [[kv-cache-alignment-shared-space|KV Alignment]]

**Status**: **Complementary, different representation depths**. Activations (single-layer residual stream) may converge across models per the [[platonic-representation-hypothesis|Platonic Representation Hypothesis]], but KV-caches (per-layer, per-head attention memory) have more architecture-specific structure. The contradiction highlights that **representation convergence varies by layer/component** — final-layer activations converge; attention-specific KV pairs do not.

**Resolution needed**: Systematic measurement of cross-model representation similarity at different transformer components (embeddings, layer-wise activations, KV-cache entries, attention patterns) to map where convergence holds and where it breaks.

---

## 5. Selective > Full: Paradoxical Finding

**Claim A**: More information transfer should produce better results — sharing full KV-cache or full hidden states should outperform selective sharing.
— Implicit assumption across the field

**Claim B**: Selective KV sharing (30% of layers) **matches or exceeds** sharing all layers. Sometimes exceeds the Skyline (full context, no communication needed).
— [[kvcomm-kth-selective|KVComm (Shi et al., 2025)]]

**Claim C**: Cyclic translation (A → shared space → A) **improves** model A beyond its original performance.
— [[kv-cache-alignment-shared-space|KV Alignment (Dery et al., 2026)]]

**Status**: **Paradox suggesting deeper principle**. Both findings suggest that intermediate representation spaces act as **beneficial regularizers** — filtering noise while preserving signal. This contradicts the naive "more = better" assumption and suggests an information-theoretic principle: optimal communication transmits *task-relevant* information, not maximum information.

**Resolution needed**: Theoretical framework explaining when and why selective/mediated transfer outperforms full transfer. Rate-distortion theory may apply — there may be a task-specific "channel capacity" beyond which additional information introduces harmful noise.

---

## 6. Training-Free vs. Trained: Which Is Better?

**Claim A**: Training-free methods ([[latentmas-collaboration|LatentMAS]], [[kvcomm-kth-selective|KVComm]], [[agent-primitives-building-blocks|Agent Primitives]], [[state-delta-trajectory|SDE]]) achieve competitive or superior results without model modification.
— Multiple papers

**Claim B**: Trained methods (C2C, Interlat, ThoughtComm) achieve richer cross-architecture communication and structured representations that training-free methods cannot.
— [[cache-to-cache-semantic-communication|C2C]], [[interlat-latent-space-agents|Interlat]], [[thought-communication-multiagent|ThoughtComm]]

**Status**: **Genuine trade-off, not contradiction**. Training-free methods are faster to deploy and don't risk [[catastrophic-forgetting|catastrophic forgetting]], but they're limited to homogeneous architectures or shallow communication. Trained methods enable cross-architecture and structured communication at the cost of training overhead. The tension is real but represents a design choice, not conflicting findings.

**Resolution needed**: Quantify the exact performance gap between training-free and trained approaches in controlled settings to determine when the training overhead is justified.

---

## 7. Coconut's Strength Varies by Task Type

**Claim A**: Coconut achieves 97.0% on ProsQA (planning/search) — dramatically outperforming CoT's 77.5%.
— [[coconut-reasoning-latent-space|Coconut]]

**Claim B**: Coconut achieves only 34.1% on GSM8K (math) — **underperforming** CoT's 42.9%.
— [[coconut-reasoning-latent-space|Coconut]] (same paper)

**Status**: **Internally consistent, task-dependent**. Superposition-based BFS excels at search/planning (where exploring multiple paths matters) but struggles with linear sequential math (where commitment to one calculation path is fine). The contradiction is within a single paper and is acknowledged.

**Implication**: Latent reasoning is not a universal improvement. It's specifically powerful for tasks requiring **search** or **parallel hypothesis evaluation**. For sequential computation, CoT may remain superior. This has implications for which tasks to target in future latent reasoning research.

---

## 8. Interpretability: Feature or Dealbreaker?

**Claim A**: Thinking States preserves interpretability by generating NL thoughts before compression. This is presented as a key advantage for safety and debugging.
— [[thinking-states-latent-reasoning|Thinking States (Amos et al., 2026)]]

**Claim B**: Coconut's opaque continuous thoughts enable qualitatively superior computation (BFS superposition) impossible with interpretable intermediate steps.
— [[coconut-reasoning-latent-space|Coconut]], [[superposition-coconut-theory|Superposition Theory]]

**Status**: **Genuine design tension**. Interpretability and superposition are fundamentally at odds — you cannot have a human-readable intermediate step that simultaneously encodes multiple hypotheses. This is not a contradiction to resolve but a fundamental trade-off to navigate.

**Resolution needed**: Can [[thought-communication-multiagent|ThoughtComm]]'s disentanglement provide post-hoc interpretability of opaque continuous thoughts? This would give the best of both worlds: opaque computation for power, structured decomposition for debugging.

---

## 9. BFS as Faithful Structured Search vs. Implicit Pruning

**Claim A**: Coconut's continuous thoughts implement **emergent breadth-first search** — each latent step expands a frontier of candidate reasoning paths, with weaker candidates pruned only as the model approaches a confident answer. Theoretically formalized by Zhu et al. (2025), who prove that a 2-layer transformer can encode the full reachable-vertex set as a normalized superposition.
— [[coconut-reasoning-latent-space|Coconut (Hao et al., 2024)]], [[superposition-coconut-theory|Zhu et al. (2025)]]

**Claim B**: Latent reasoning *can* encode multiple candidates (Pass@100 over 100 stochastic rollouts is 20+ points higher than explicit reasoning), but the *iterative* process exhibits **implicit pruning**, not BFS expansion. Distinct outcomes *decrease* monotonically with latent depth (avg. 18.75 → 15.84 from 1 to 5 latent steps), the opposite of true BFS. Majority-vote accuracy is *lower* than explicit reasoning by 3-4 points, meaning the larger candidate pool is not being concentrated on the correct answer.
— [[latent-reasoning-supervision-analysis|Cui et al. (2026)]]

**Claim C**: Even when the diverse candidates are externally available (dropout-sampled COCONUT trajectories yield Pass@32 = 44.43% on GPT-2 GSM8K, exceeding both deterministic COCONUT and text CoT), no standard reranker can recover the headroom. PRM (hard + soft, MATH-Shepherd-style) and ORM achieve only +2.28pp out of +13.35pp available, with PRM/ORM classification F1 hovering near chance (54%/52%). The diagnosis is geometric: continuous-thought representations exhibit IsoScore$\star \approx 0.013$ and produce statistically indistinguishable values across compactness, curvature, local smoothness, and straightness metrics for correct vs. incorrect thoughts.
— [[inference-time-scaling-continuous-reasoning|Wang et al. (2025)]]

**Status**: **Substantially resolved by Cui et al. + Wang et al. — capacity confirmed, dynamics falsified, naive reranking falsified, geometric structure absent**. The cleanest decomposition to date of five claims that the literature conflated:

| Sub-claim | Status | Evidence |
|---|---|---|
| Latent vectors can encode multiple candidates | Confirmed | Zhu et al. theoretical construction; Cui et al. Pass@100 advantage; Wang et al. Pass@32 = 44.43% |
| The iterative process expands the frontier | **Falsified** | Cui et al. distinct-outcome counts decrease with depth |
| The process amplifies the correct candidate | **Falsified** | Cui et al. majority-vote below explicit reasoning |
| Standard reranking (PRM/ORM/self-consistency) closes the gap | **Falsified** | [[inference-time-scaling-continuous-reasoning\|Wang et al.]] PRM-HE recovers only 19.8% of Pass@N headroom |
| The remaining diversity has discriminable geometric structure | **Falsified** | Wang et al. IsoScore$\star \approx 0.013$; correct/incorrect thoughts intermixed in t-SNE; F1 ≈ 54%/52% |

**Implication for the field**: Zhu et al.'s theoretical bound is achievable in *capacity* but not in *dynamics*, and the residual capacity is *geometrically structureless* — there is no signal a verifier can extract. Practical methods (Coconut, CODI, SIM-CoT, CoLaR) prune their own diversity during the latent loop, and the surviving thoughts produce statistically indistinguishable IsoScore$\star$, Hoyer sparsity, compactness, curvature, local smoothness, and straightness measurements regardless of correctness. The [[frontier-research-directions|frontier-scale superposition reasoning agenda]] must redirect from "scale up Coconut" or "build a better reranker" to **"build training-time inductive biases (isotropy regularization, contrastive losses, trajectory-diversity objectives) that produce continuous thoughts which are *structurally* discriminable from incorrect ones."** Wang et al. propose this trio of mitigations but test none of them; both the training-time and the inference-time gaps remain open.

**Resolution status**: The controlled comparison of best-of-N CoT, self-consistency CoT, and latent-aware best-of-N decoding is now done at GPT-2 scale ([[inference-time-scaling-continuous-reasoning|Wang et al.]]) and the latent-aware variants do *not* close the gap. The BFS hypothesis is therefore rescued in only its *weakest* form: capacity is real, but exploitation requires not just external machinery but also training-time intervention to make the latent state discriminable. Whether the geometric homogeneity finding persists at LLaMA-1B / Qwen-7B scale, and whether stronger-supervision methods (CODI, SIM-CoT, CoLaR) produce more discriminable representations, are the next two open questions.

---

## Summary Table

| # | Tension | Papers | Status | Priority |
|---|---------|--------|--------|----------|
| 1 | Curriculum works (base) / breaks (instruct) | [[coconut-reasoning-latent-space\|Coconut]] vs [[softcot-efficient-reasoning\|SoftCoT]] | Different regimes | **High** — blocks production use |
| 2 | Raw states help / raw states hurt | [[activation-communication-harvard\|AC]] vs [[state-delta-trajectory\|SDE]] | Same regime, unresolved | **High** — fundamental design question |
| 3 | More agents help / more agents hurt | Debate papers vs Scaling | Different task distributions | Medium — understood but not tested with latent methods |
| 4 | Cross-arch easy (activations) / hard (KV) | AC vs C2C/KV Align | Different representation depths | Medium — regime-dependent |
| 5 | Selective > full (paradox) | [[kvcomm-kth-selective\|KVComm]], [[kv-cache-alignment-shared-space\|KV Alignment]] | Suggests deeper principle | **High** — potential paradigm insight |
| 6 | Training-free competitive / trained richer | Multiple | Design trade-off | Low — understood trade-off |
| 7 | BFS excels at search / fails at math | [[coconut-reasoning-latent-space\|Coconut]] (internal) | Task-dependent, acknowledged | Low — well understood |
| 8 | Interpretability needed / prevents superposition | [[thinking-states-latent-reasoning\|Thinking States]] vs [[coconut-reasoning-latent-space\|Coconut]] | Fundamental tension | Medium — needs creative resolution |
| 9 | BFS as faithful search / implicit pruning / geometrically structureless | [[coconut-reasoning-latent-space\|Coconut]], [[superposition-coconut-theory\|Zhu et al.]] vs [[latent-reasoning-supervision-analysis\|Cui et al.]] vs [[inference-time-scaling-continuous-reasoning\|Wang et al.]] | Substantially resolved — capacity confirmed, dynamics falsified, naive reranking falsified, geometric structure absent | **High** — redirects the agenda from scaling/decoding to training-time inductive biases |
