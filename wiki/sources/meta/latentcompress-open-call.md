---
type: source
title: "LatentCompress: Open Call for Latent Communication Research"
source_file: "https://github.com/billion-token-one-task/latent-communication"
author: "billion-token-one-task"
date_published: "2026"
date_ingested: "2026-04-06"
created: "2026-04-06"
updated: "2026-04-08"
venue: "GitHub (open research project)"
tags: [latent-communication, compression, slot-attention, experimental, collaboration]
---

# LatentCompress: Open Call for Latent Communication Research

## One-liner

![[latentcompress-open-call/one-liner]]

## Summary

An open research project that has achieved **512-byte compressed latent communication** between LLM agents — matching baseline accuracy (91%) on GSM8K while replacing MB-scale KV-cache transfers. Uses a slot-attention architecture (4 slots × 64 dim = 512 bytes) trained on top of frozen Qwen3-14B in a 4-agent sequential pipeline. Claims to be the world's 4th team working on this problem and the most extreme compression ratio (~1/2000 vs full KV).

## Key Experimental Results

### Experiment 1: Extreme Compression (GSM8K, ARC-C, GPQA)

| Method | Message size | GSM8K | ARC-C | GPQA-Diamond |
|--------|-------------|-------|-------|-------------|
| Single agent | 0 | 91% | 92% | 8.1% |
| [[latentmas-collaboration\|LatentMAS]] (full KV) | ~MB | **95%** | 93% | **26.8%** |
| SlotMAS (trained) | **512 B** | **91%** | — | 19.1% |

Critical finding: **512 bytes matches baseline on GSM8K** but GPQA needs MB-scale bandwidth. Task-dependent bandwidth requirements are the key variable.

### Experiment 2: Hidden Profile (forced communication)
16-byte bottleneck raises communication-dependent accuracy from **12% → 57-65%**. Full mean pool (10 KB) reaches 80.7%.

### Experiment 3: Long Document QA (QASPER)
Carefully selected 1.35 KB text (4.5% of full) achieves **54%** vs. 33% for full text — models are **drowned by long context**. Latent high-bandwidth (2 KB) only reaches 31%.

### Experiment 4: Information Bottleneck + Style Adversarial
4× compression with IB + adversarial training: 99.95% accuracy, style leakage drops from 35.2% → 13.5%.

## Validated Findings

1. Compressed latent communication **works** (16B: 12%→57% on communication-dependent accuracy)
2. Simple tasks need minimal bandwidth (GSM8K: 512B = baseline)
3. Hard tasks need more bandwidth (GPQA: 512B drops back to baseline; needs MB)
4. **Training alignment matters more than loss design** — collecting hidden states on inference distribution (not training distribution) is the biggest single improvement
5. Full text is not the upper bound (QASPER: 4.5% selected text > 100% full text)
6. Cumulative degradation follows $Q \propto e^{-T\varepsilon/C}$ — 512B yields $\varepsilon \approx 0.15$ across 8-agent chains

## Three Proposed Directions

### Direction 1: Large-Scale Compressor Training
Current: trained on 300 samples, validated on GSM8K only. Goal: universal compressor across 50+ task families, curriculum learning (low→high compression), adaptive slot count. Target: $\leq$ 1KB with $\leq$ 3pp drop across all tasks.

### Direction 2: Native Latent Communication Pretraining
Currently all methods (including LatentMAS, Interlat, and this work) add modules to frozen models whose representations weren't designed for communication. Goal: integrate multi-agent communication objectives into pretraining itself. Target: 7B model natively supporting latent communication, 64 bytes with 90%+ information retention.

### Direction 3: Latent + Tool Use Hybrid Communication
No latent communication system supports tool calling. Goal: learned Router (hidden state → binary decision: stay latent or decode to tokens). 90% communication via latent channel, tool-critical outputs via tokens. Evaluation on ALFWorld, WebArena, SWE-bench.

## Safety & Auditability (Unique Contribution)

The project makes a strong case that latent communication creates a **governance crisis**: if agents communicate in opaque continuous vectors, current Chain-of-Thought monitoring fails completely. Three proposed solutions:

1. **Interpretable compression** (current): Slot-attention slots can be probe-decoded to nearest NL descriptions. Extreme compression (512B) **forces** structured information organization, making it more auditable than high-bandwidth opaque transfer.
2. **Channel constraints** (architecture-level): Bandwidth budgets, semantic anchoring (require latent messages to be decodable to readable text as "audit shadow"), adversarial debiasing.
3. **Runtime monitoring** (long-term): Anomaly detection on latent communication distributions, information flow tracking, degradable "audit mode."

## Methodology Analysis

### Slot-Attention Compressor Architecture

The compression module uses a **slot-attention** mechanism (Locatello et al., 2020) with 4 learned slot vectors of dimension 64. Each slot attends to the full hidden-state sequence via iterative competitive attention: slots compete to "explain" different parts of the hidden-state sequence, naturally partitioning the information into disjoint groups.

The total message size is:

$$4 \text{ slots} \times 64 \text{ dim} \times 2 \text{ bytes (FP16)} = 512 \text{ bytes}$$

This yields a ~1/2000 compression ratio relative to full KV-cache transfer at MB scale.

The slot structure has an important connection to [[coconut-reasoning-latent-space|Coconut]]'s BFS discovery: if continuous thoughts encode superposed reasoning paths, slot-attention may **naturally disentangle** those paths (each slot capturing a distinct reasoning branch). This is untested but would connect compression research to the deepest theoretical finding in [[latent-space-reasoning]]. See [[latentcompress-collaboration-strategy]] for a proposed experimental test.

### Training on Inference Distribution (Key Methodological Insight)

The single largest improvement in compression quality came not from loss function design but from **collecting training hidden states on the inference distribution** rather than the training distribution. When hidden states are gathered during standard training (teacher forcing), the distribution of internal representations diverges from what the model produces during autoregressive inference.

Aligning the compressor's training data to the inference distribution eliminates this mismatch. This finding echoes the exposure bias problem well-known in sequence modeling and has implications for all methods that train auxiliary modules on frozen model representations:

- [[cache-to-cache-semantic-communication|C2C]]'s cache fuser — trained on prefill-derived KV-caches, which may differ from caches produced during interactive multi-round use
- [[interlat-latent-space-agents|Interlat]]'s communication adapter — trained on hidden states from standard generation
- [[softcot-efficient-reasoning|SoftCoT]]'s projection module — trained on frozen assistant model outputs

### Information Bottleneck + Style Adversarial Training

Experiment 4 combines two regularization strategies:

**Information bottleneck (IB)**: Adds a KL penalty encouraging the compressed representation to retain only task-relevant information, following the IB principle:

$$\min I(Z; X) - \beta I(Z; Y)$$

where $Z$ is the compressed state, $X$ the input, and $Y$ the target. The $\beta$ parameter controls the trade-off between compression and task utility.

**Style adversarial training**: A discriminator attempts to predict the sender's identity/style from the compressed message. The compressor is trained adversarially to prevent this leakage:

| Metric | Without adversarial | With adversarial |
|--------|-------------------|-----------------|
| Task accuracy | 99.97% | 99.95% |
| Style leakage | 35.2% | 13.5% |

This combination addresses a concern unique to latent communication: without adversarial debiasing, compressed representations could leak sender-specific information (model identity, training data artifacts) that has no communicative value but could be exploited.

### The Cumulative Degradation Model

The quality degradation formula models how compression error compounds across agent chains:

$$Q \propto e^{-T\varepsilon/C}$$

where $T$ is the number of agents in the chain, $\varepsilon$ is the per-step information loss rate, and $C$ is the channel capacity (in bytes). At 512 bytes, the measured $\varepsilon \approx 0.15$ across 8-agent chains.

This provides a principled framework for setting bandwidth budgets: given a target quality floor $Q_\text{min}$ and chain length $T$, the minimum required capacity is:

$$C_\text{min} = \frac{-T\varepsilon}{\ln(Q_\text{min})}$$

No other paper in the field provides an equivalent degradation model for multi-hop latent communication. The model also predicts that longer agent chains (higher $T$) require proportionally higher bandwidth — a finding consistent with [[latentmas-collaboration|LatentMAS]]'s observation that sequential 4-agent pipelines require substantial KV-cache transfer to maintain accuracy.

## Limitations and Gaps

1. **Extremely limited training data**: The compressor is trained on only 300 samples and validated on GSM8K alone. Generalization to diverse task families is unvalidated.
2. **Same-model only**: All experiments use Qwen3-14B for all agents. Cross-architecture compression is not addressed — contrast with [[cache-to-cache-semantic-communication|C2C]] and [[kv-cache-alignment-shared-space|KV Cache Alignment]] which handle heterogeneous model pairs.
3. **No layer selection analysis**: Compression operates on last-layer hidden states. [[kvcomm-kth-selective|KVComm]] and [[activation-communication-harvard|AC]] show that intermediate layers (~layer 26/32) often carry richer transferable information. Extracting from the optimal layer could improve compression efficiency.
4. **No comparison with delta-based communication**: [[state-delta-trajectory|SDE]] demonstrates that inter-token state deltas outperform raw hidden states for communication. Compressing deltas rather than raw states could reduce bandwidth requirements, since deltas strip context-specific baselines.
5. **No formal connection to rate-distortion theory**: The bandwidth-accuracy curves are empirical. A formal rate-distortion analysis (minimum bits required to achieve a given task accuracy) would ground the compression limits theoretically.
6. **Narrow literature awareness**: References only 3 peer works (LatentMAS, Interlat, Vision Wormhole). Does not cite [[kvcomm-kth-selective|KVComm]]'s layer selection, [[thought-communication-multiagent|ThoughtComm]]'s identifiability framework, [[cipher-multiagent-debate-embeddings|CIPHER]]'s embedding communication, or the [[softcot-efficient-reasoning|SoftCoT]] finding on [[catastrophic-forgetting]] that could affect their Direction 2 (native pretraining).

## Cross-References and Connections

### Relation to KV-Cache Communication Cluster
The slot-attention compressor addresses the same fundamental problem as [[kv-cache-communication]] — transferring internal model state between agents — but at a radically different compression point. Where [[kvcomm-kth-selective|KVComm]] transmits 30-70% of layers (~10-22 layers' KV pairs), and [[cache-to-cache-semantic-communication|C2C]] transmits full selected-layer caches with a learned fuser, LatentCompress compresses everything to 512 bytes. The bandwidth-accuracy trade-off is extreme: sufficient for GSM8K, insufficient for GPQA.

### Relation to Latent Reasoning
The QASPER finding (4.5% selected text > 100% full text) resonates with [[coconut-reasoning-latent-space|Coconut]]'s insight that language is not optimal for information transfer. Both suggest that intelligent compression/selection outperforms brute-force information quantity. The connection to [[cot-expressivity-theory|Feng et al.]]'s depth theory is unexplored: does slot-attention compression preserve the effective depth that [[latent-space-reasoning]] methods rely on?

### Relation to Safety and Interpretability
The safety framing is unique in the field. The "audit shadow" proposal (requiring latent messages to be decodable to readable text) directly addresses the governance gap identified by no other paper. This connects to [[thinking-states-latent-reasoning|Thinking States]]'s design choice to preserve natural language thoughts at chunk boundaries, enabling interpretability that pure latent methods ([[coconut-reasoning-latent-space|Coconut]], [[icot-internalize-cot|iCoT]]) sacrifice.

## Position in the Field

Self-described as the 4th team globally. References only LatentMAS, Interlat, and Vision Wormhole as peers. Does not reference the larger body of work in this wiki (CIPHER, ThoughtComm, KVComm, C2C, KV Cache Alignment, AC, SDE, etc.).

## Source Materials

- [GitHub repository](https://github.com/billion-token-one-task/latent-communication)
