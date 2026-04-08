---
type: overview
title: "Practical Systems"
created: "2026-04-06"
updated: "2026-04-06"
tags: [moc, practical, scaling, deployment]
---

# Practical Systems

The engineering lens on latent multi-agent systems: when to use which method, what the scaling constraints are, and how to navigate deployment trade-offs. Where the other MOCs ask "what's possible?", this one asks "what should I build?"

## Reading Path

### 1. When Does Multi-Agent Help at All?

Start with **[[scaling-agent-systems|Scaling Agent Systems]]** — the quantitative framework that prevents wasted effort. The core finding: MAS is **task-contingent**, not universally beneficial. Its best variant yields +80.8% on naturally decomposable tasks (Centralized on Finance-Agent) but the worst can degrade -70.1% on strictly sequential ones (Independent on PlanCraft). The **baseline paradox** (beta = -0.404) means that if a single agent already achieves >45% accuracy, coordination overhead often exceeds the gains. Read this before committing to any multi-agent architecture.

### 2. Which Latent Method Fits Your Constraints?

**[[method-comparison|Method Comparison]]** provides the unified table across all 18 empirical methods. The three spectra that matter most for deployment: **training requirements** (CIPHER and KVComm need zero training; Coconut and Interlat need heavy curriculum learning), **cross-architecture compatibility** (natural language is universal; KV-cache methods are same-architecture only; AC and C2C bridge families), and **information density vs. compatibility** (the frontier goal is upper-right — high density AND high compatibility). No single method dominates; the optimal choice depends on your specific constraints.

### 3. The Composable Architecture Approach

**[[agent-primitives-building-blocks|Agent Primitives]]** shows how to structure latent MAS using reusable building blocks — **Review**, **Voting**, and **Planning** primitives composed per-task by an Organizer agent. Key deployment facts: +6.3% to +16.5% over single agents across 5 model families, **fewer tokens than single agents** on smaller models, and only 1.3-1.6x latency overhead (vs. 3.5-5.3x for text-based MAS). Critical implementation detail: **RoPE positional re-encoding** is mandatory for LLaMA-based models (without it, ~27-60pp accuracy drops).

### 4. Training-Free Deployment with LatentMAS

**[[latentmas-collaboration|LatentMAS]]** is the fastest path to a working latent MAS — no training, no adapters, just ridge regression alignment and KV-cache transfer. 4x faster than text-based MAS, 70-84% token reduction. But it requires **homogeneous architecture** (same model family) and catastrophically fails on LLaMA (-10.1% average on DeepSeek-R1-Distill-Llama-70B, as measured by Agent Primitives' comparison). For Qwen-family models, this is the lowest-friction deployment option.

### 5. Systems-Level Efficiency

**[[kvcomm-duke-online-reuse|KVCOMM-online]]** tackles the compute bottleneck that appears when agents share overlapping context. Its anchor-based KV-cache reuse achieves up to **7.8x prefill speedup** (6.7x average) with <2.5% quality drop — a systems optimization orthogonal to the communication method itself. Composable with any KV-cache approach.

### 6. Compression Targets and Bandwidth Planning

**[[latentcompress-open-call|LatentCompress]]** establishes concrete bandwidth targets: **512 bytes** suffices for simple tasks (GSM8K matches 91% baseline), but hard reasoning tasks (GPQA) need MB-scale bandwidth. The bandwidth-accuracy S-curve and cumulative degradation model ($Q \propto e^{-T\varepsilon/C}$) provide the planning framework for sizing communication channels in production systems.

### 7. Collaboration and Research Opportunities

**[[latentcompress-collaboration-strategy]]** maps the gap between existing open-source efforts and the full research landscape. **[[frontier-research-directions]]** identifies the engineering-adjacent directions with highest near-term impact: scaling laws for latent MAS (#7) and learned compression bounds (#8).

## Decision Guide

Use this table to narrow your method choice based on deployment constraints:

| Constraint | Recommended Methods | Avoid |
|---|---|---|
| **Zero training budget** | [[latentmas-collaboration\|LatentMAS]], [[agent-primitives-building-blocks\|Agent Primitives]], [[kvcomm-kth-selective\|KVComm]], [[state-delta-trajectory\|SDE]] | Coconut, Interlat, ThoughtComm |
| **Cross-architecture required** | [[activation-communication-harvard\|AC]], [[cache-to-cache-semantic-communication\|C2C]], [[vision-wormhole-heterogeneous\|Vision Wormhole]] | LatentMAS, KVComm, SDE |
| **Latency-critical (<2x single)** | Agent Primitives (1.3-1.6x latency), [[kvcomm-duke-online-reuse\|KVCOMM-online]] for prefill | Hybrid MAS (6.2x turns overhead), TextMAS (3.5-5.3x latency) |
| **LLaMA-family backbone** | Agent Primitives (with RoPE re-encoding) | LatentMAS (catastrophic on LLaMA) |
| **Maximum accuracy** | Agent Primitives composed (75.3% avg on Qwen3-8B) | Independent MAS (-70% on sequential tasks) |
| **Minimal bandwidth** | [[latentcompress-open-call\|LatentCompress]] slots (512B), [[cipher-multiagent-debate-embeddings\|CIPHER]] | Full KV-cache transfer (~MB) |
| **Safety/auditability required** | LatentCompress (slot-attention probing), [[thought-communication-multiagent\|ThoughtComm]] (identifiable factors) | Raw hidden-state transfer (opaque) |

### 8. Cross-Cutting Analyses

- **[[benchmark-overlap|Benchmark Overlap Analysis]]** — Maps which benchmarks appear across multiple papers, exposing where results are directly comparable and where claimed improvements may reflect benchmark selection rather than genuine gains. Essential context for interpreting the method comparison table above.
- **[[contradictions|Contradictions]]** — Documents deployment-relevant tensions across the literature, including conflicting claims about training-free viability, cross-architecture compatibility by depth, and when MAS helps vs. hurts. Read this to understand the caveats behind the Decision Guide.
- **[[paper-timeline|Paper Timeline]]** — Chronological view of all 27 papers showing the field's acceleration from theoretical foundations (2022-2023) through the 2025 Cambrian explosion to 2026 unification. Useful for understanding which results build on which, and for gauging the maturity of different approaches.

## Connections

- **[[latent-reasoning]]** — Intra-agent reasoning methods that feed into unified systems. The [[catastrophic-forgetting]] barrier is the main obstacle to deploying Coconut-style reasoning in production.
- **[[latent-communication]]** — The full depth spectrum of inter-agent communication options, organized by information density and compatibility.
- **[[communication-depth-spectrum]]** — 10-level walkthrough from natural language to full KV-cache + latent thoughts, useful for understanding the bandwidth-compatibility trade-off space.
- **[[unified-frameworks]]** — The three systems (LatentMAS, Vision Wormhole, Agent Primitives) that combine reasoning and communication.
