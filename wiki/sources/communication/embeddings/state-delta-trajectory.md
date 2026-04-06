---
type: source
title: "Augmenting Multi-Agent Communication with State Delta Trajectory"
source_file: "[[raw/pdf/arxiv-2506.19209.pdf]]"
latex_source: "[[raw/latex/arxiv-2506.19209.tar.gz]]"
venue_pdfs: ["[[raw/pdf/acl-2025.emnlp-main.518.pdf|EMNLP 2025]]"]
author: "Yichen Tang, Weihang Su, Yujia Zhou, Yiqun Liu, Min Zhang, Shaoping Ma, Qingyao Ai"
date_published: "2025-06-23"
date_ingested: "2026-04-06"
created: "2026-04-06"
updated: "2026-04-06"
venue: "EMNLP 2025"
arxiv: "2506.19209"
institution: "Tsinghua University"
tags: [state-delta, steering-vectors, multi-agent, same-model]
---

# Augmenting Multi-Agent Communication with State Delta Trajectory

## Summary

**State Delta Encoding (SDE)**, from [[tsinghua|Tsinghua University]], augments natural language communication between same-model agents by injecting **hidden state deltas** -- the difference between adjacent token positions' hidden states during generation -- into the receiver's forward pass at selected layers. Each delta acts as a **steering vector** that nudges the receiver's representations to better understand the sender's reasoning trajectory. Unlike raw hidden state transfer, deltas are **context-agnostic**: they capture only the reasoning dynamics, stripped of the sender's context-specific baseline.  Evaluated across 3 models, 10 benchmarks, and 3 task types (information asymmetry, debate, agent workflows), SDE outperforms NL and [[cipher-multiagent-debate-embeddings|CIPHER]] baselines on nearly all tasks, with improvements up to **+17.3%** on complex reasoning.

## Formal Definitions

### State Trajectory

Consider two agents, Alice and Bob, built from the same transformer LLM. When Alice generates output tokens $t_1, t_2, \ldots, t_n$, the **state trajectory** at layer $l$ is the ordered sequence of hidden states:

> $$H^l_A = \{ h^l_{A,0}, h^l_{A,1}, \ldots, h^l_{A,n} \}$$

Here $h^l_{A,i}$ is the output of the $l$-th transformer layer for token $t_i$, conditioned on the input prompt and all previously generated tokens. $h^l_{A,0}$ corresponds to the **last token of Alice's input prompt** (the initial state before generation begins).

### State Delta Encoding

Rather than transferring the raw trajectory $H^l_A$ (which contains Alice's context-specific information -- system prompt, private documents), SDE computes the **inter-token differences**:

> $$S^l_A = \{ s^l_1, s^l_2, \ldots, s^l_n \}, \quad \text{where } s^l_i = h^l_{A,i} - h^l_{A,i-1}$$

Each $s^l_i$ is a **state delta**: the internal change associated with generating token $t_i$. The state delta trajectory is a **context-agnostic trace** of reasoning dynamics -- it strips out Alice's absolute context and retains only the differential reasoning signal.

### Injection into the Receiver

Bob's prompt takes the form $\text{prompt}_B = \{X, t_1, t_2, \ldots, t_n, Y\}$ where $X$ and $Y$ are task instructions, environment info, and other agents' responses. When Bob processes Alice's tokens, SDE injects the corresponding deltas at layer $l$:

> $$h'^l_{B,j} = \begin{cases} h^l_{B,j} + s^l_i & \text{if position } j \text{ corresponds to token } t_i \text{ from Alice's output} \\ h^l_{B,j} & \text{otherwise} \end{cases}$$

The modified $h'^l_{B,j}$ is passed to layer $l+1$ for continued inference. This is an **additive** injection -- Bob's own representations are nudged, not overwritten. The injection only occurs at positions corresponding to Alice's output tokens within Bob's prompt.

## Layer Selection Procedure

SDE is applied to only **1-3 carefully selected layers** per model. Layers are chosen via a single preliminary experiment on the **2WikiMultihopQA** dataset (300 questions, information asymmetry setting). Each layer is evaluated individually; the top-k layers (by combined EM + F1) are selected and **fixed for all subsequent experiments**. 2WikiMultihopQA is excluded from all main evaluations.

**Selected layers per model** (from Appendix A, Table 6):

| Model | Total Layers | Layers Selected | Top-5 Layers (by EM+F1) |
|-------|-------------|-----------------|------------------------|
| Qwen2.5-7B | 28 | **Layer 22** (1 layer) | 22, 24, 9, 20, 12 |
| Llama3.1-8B | 32 | **Layers 17, 20** (2 layers) | 17, 20, 5, 8, 30 |
| Qwen2.5-14B | 48 | **Layers 21, 23, 33** (3 layers) | 33, 21, 23, 19, 36 |

The most effective layers tend to fall in **middle-to-late** positions (e.g., Layer 22 of 28 for Qwen-7B, Layer 17 of 32 for Llama-8B). However, some early layers also perform well (Layers 5 and 8 in Llama-8B), indicating flexibility. The number of selected layers scales with model size: 1 for 7B, 2 for 8B, 3 for 14B.

## Full Results

### Information Asymmetry (IA): 2 Agents, up to 5 Rounds

Agents hold disjoint private document corpora (3 passages each from BM25 top-6 retrieval) and must collaborate through Q&A to answer multi-hop questions. Greedy decoding throughout.

| Model | Method | Quasar-T EM | Quasar-T F1 | CWQ EM | CWQ F1 | StrategyQA Acc |
|-------|--------|------------|------------|--------|--------|---------------|
| **Qwen2.5-7B** | Single | 0.237 | 0.279 | 0.297 | 0.363 | 0.170 |
| | NL | 0.305 | 0.375 | 0.312 | 0.430 | 0.443 |
| | CIPHER | 0.282 | 0.357 | 0.297 | 0.404 | 0.373 |
| | **SDE** | **0.315** | **0.377** | **0.317** | **0.444** | **0.455** |
| **Llama3.1-8B** | Single | 0.233 | 0.281 | 0.247 | 0.324 | 0.150 |
| | NL | 0.285 | 0.350 | 0.325 | 0.429 | 0.497 |
| | CIPHER | 0.277 | 0.349 | 0.342 | 0.453 | 0.503 |
| | **SDE** | **0.305** | **0.367** | **0.352** | **0.464** | **0.548** |
| **Qwen2.5-14B** | Single | 0.327 | 0.385 | 0.347 | 0.426 | 0.453 |
| | NL | 0.372 | 0.445 | 0.375 | 0.497 | 0.673 |
| | CIPHER | 0.352 | 0.421 | 0.350 | 0.484 | 0.643 |
| | **SDE** | **0.372** | **0.444** | **0.382** | **0.498** | **0.682** |

Improvements are larger on multi-hop datasets (CWQ, StrategyQA) than simple factual QA (Quasar-T), confirming SDE is more effective for complex, multi-step reasoning. Llama-8B shows the largest gains, especially on StrategyQA (+4.5pp over CIPHER).

### Multi-Agent Debate (IS): 2 Agents, 3 Rounds

All agents share identical information. Default sampling with model-specific temperatures; results averaged over 3 independent runs.

| Model | Method | GSM8K | Abstract Algebra | College Math | Formal Logic |
|-------|--------|-------|-----------------|-------------|-------------|
| **Qwen2.5-7B** | Single | 0.879 | 0.477 | 0.390 | 0.450 |
| | NL | 0.906 | 0.458 | 0.362 | 0.476 |
| | CIPHER | 0.893 | 0.485 | 0.370 | 0.488 |
| | **SDE** | **0.918** | **0.517** | **0.443** | **0.520** |
| **Llama3.1-8B** | Single | 0.787 | 0.227 | 0.217 | 0.357 |
| | NL | 0.833 | 0.283 | 0.227 | 0.389 |
| | CIPHER | 0.817 | 0.215 | 0.195 | 0.353 |
| | **SDE** | **0.845** | **0.302** | **0.242** | **0.422** |
| **Qwen2.5-14B** | Single | 0.911 | 0.567 | 0.507 | 0.566 |
| | NL | 0.931 | 0.710 | 0.635 | 0.609 |
| | CIPHER | 0.930 | 0.650 | 0.635 | 0.568 |
| | **SDE** | **0.934** | **0.753** | **0.695** | **0.657** |

SDE enhances debate performance by **+0.3% to +13.7%** over best baseline. The largest gains appear on complex mathematical/logical reasoning (MMLU subsets), not arithmetic (GSM8K). CIPHER sometimes **underperforms NL** (e.g., Llama-8B Abstract Algebra: CIPHER 0.215 vs NL 0.283), while SDE consistently outperforms both.

### Agent Workflow (IS): Up to 7 Agents, Sequential (Qwen2.5-7B)

ReAct-style framework where agents collaborate sequentially: each agent generates a Thought + Action, receives an Observation from the environment (BM25-retrieved Wikipedia), then passes everything to the next agent. Up to 7 agents per question.

| Method | FEVER Acc | HotpotQA EM | HotpotQA F1 | StrategyQA Acc |
|--------|----------|------------|------------|---------------|
| Single | 0.007 | 0.157 | 0.219 | 0.157 |
| NL | 0.230 | 0.210 | 0.315 | 0.317 |
| CIPHER | 0.180 | 0.200 | 0.288 | 0.327 |
| **SDE** | **0.267** | **0.227** | **0.320** | **0.383** |

SDE achieves up to **+17.3%** over baselines (on StrategyQA: 0.383 vs NL 0.317). The workflow setting -- requiring more complex sequential reasoning -- benefits more from SDE than the IA setting with the same model on the same dataset (StrategyQA IA: +1.2pp; StrategyQA workflow: +5.6pp), confirming SDE is particularly effective for complex reasoning chains.

## Ablation Studies

### Deltas vs Raw Hidden States (Table 4)

Replacing state deltas with raw hidden states $h^l_{A,i}$ (the "w/o delta" variant) consistently degrades performance. In several cases, raw states fall **below the NL baseline**, demonstrating that unprocessed hidden states introduce noise from the sender's context:

| Model | Method | Quasar-T EM | CWQ EM | College Math | Formal Logic |
|-------|--------|------------|--------|-------------|-------------|
| **Qwen-7B** | NL | 0.305 | 0.312 | 0.362 | 0.476 |
| | w/o delta | 0.295 | 0.313 | 0.403 | 0.462 |
| | **SDE** | **0.315** | **0.317** | **0.443** | **0.520** |
| **Llama-8B** | NL | 0.285 | 0.325 | 0.245 | 0.389 |
| | w/o delta | 0.275 | **0.297** | 0.247 | 0.394 |
| | **SDE** | **0.305** | **0.352** | **0.297** | **0.422** |

Key findings: Llama-8B CWQ drops from NL 0.325 to raw states **0.297** (-2.8pp below NL), while SDE reaches **0.352** (+2.7pp above NL). This is the strongest evidence that deltas, not raw states, are the correct abstraction -- the differential signal captures reasoning dynamics while stripping context-specific noise.

### Layer Selection Strategies (Figure 2, Appendix C)

Tested on Qwen2.5-14B with StrategyQA (IA) and Formal Logic (debate):

- **Combined top-k** (k <= 4): Stable performance, little variation as k increases from 1 to 4. Best balance of robustness and generality.
- **Only top-k** (single layer at rank k): Inconsistent -- performance varies unpredictably across ranks and tasks. E.g., on Qwen-7B Formal Logic, performance decreases from rank-1 to rank-4 but unexpectedly rises at rank-5.
- **All layers**: Significant performance drop in all cases -- excessive disruption of the model's internal representations.

Recommendation: Apply 1-3 combined top-ranking layers. Avoid single-layer selection (unstable) and all-layer modification (harmful).

### Agents and Rounds Scaling (Table 5, Formal Logic, Qwen2.5-7B)

**Varying agents** (3 rounds fixed):

| Agents | NL | CIPHER | SDE |
|--------|------|--------|------|
| 2 | 0.476 | 0.488 | **0.520** |
| 3 | 0.449 | 0.431 | **0.515** |
| 4 | 0.453 | 0.437 | **0.518** |
| 5 | 0.495 | 0.432 | **0.514** |

**Varying rounds** (2 agents fixed):

| Rounds | NL | CIPHER | SDE |
|--------|------|--------|------|
| 2 | 0.452 | 0.488 | **0.513** |
| 3 | 0.476 | 0.488 | **0.520** |
| 4 | 0.454 | 0.488 | **0.523** |
| 5 | 0.460 | 0.488 | **0.521** |

SDE maintains a **consistent advantage** across all configurations (0.513-0.523), while NL fluctuates significantly (0.449-0.495) and CIPHER stays flat (it produces identical embeddings across rounds when temperature is fixed). SDE is robust to variations in agent count and round count.

## Connection to Steering Vectors and Activation Engineering

SDE explicitly frames each state delta as a **steering vector** in the tradition of [[activation-communication-harvard|activation engineering]]. The connection to **ActAdd** (Turner et al., 2024) is direct: ActAdd derives steering vectors by computing hidden state differences under prompts with or without a target keyword, then adds these vectors during inference to steer generation. SDE does the same thing but at **token granularity** during inter-agent communication: each $s^l_i$ is the hidden state difference between generating token $t_i$ versus $t_{i-1}$, and it steers the receiver's processing of that specific token.

The key difference: ActAdd uses a fixed steering vector derived from a contrastive pair of prompts. SDE produces a **dynamic sequence** of steering vectors, one per generated token, capturing the evolving reasoning trajectory rather than a single static direction. This connects SDE to the broader literature on **Inference-Time Intervention** (Li et al., 2023) for truthfulness and **contrastive activation addition** (Rimsky et al., 2024) for behavior steering.

## Connections

- **[[activation-communication]]**: SDE is a refined version -- instead of transferring raw activations (which include context-specific noise), it transfers the **inter-token differences** (reasoning dynamics only).
- **[[activation-communication-harvard|AC]]**: AC replaces the last-token activation at one layer. SDE additively injects deltas across selected layers for **all tokens in the output sequence**. AC works cross-model; SDE is same-model only.
- **[[cipher-multiagent-debate-embeddings|CIPHER]]**: SDE outperforms CIPHER because probability distributions are "surface-level" -- deltas capture deeper hidden reasoning dynamics. CIPHER also fails to differentiate across debate rounds (identical embeddings at fixed temperature).
- **[[kv-cache-communication]]**: KV-cache methods transfer keys and values at all layers. SDE transfers only deltas at 1-3 layers -- lower bandwidth but also lower risk of interference.
- **[[continuous-vs-discrete-representation]]**: SDE demonstrates that not all continuous representations are equally useful -- the **differential** signal (deltas) outperforms raw states, suggesting the reasoning dynamics live in the inter-token transitions, not the absolute positions.

## Limitations

- **Same-model only**: Requires sender and receiver to share the same base LLM (same architecture, same weights). Cannot work with heterogeneous agent systems.
- **White-box access required**: Must extract hidden states from the sender and inject into the receiver -- incompatible with black-box API models.
- **Bandwidth overhead**: Even with only 1-3 layers, transmitting per-token state deltas increases communication cost, especially for long contexts or large models. Future work could explore selective transmission or compression of state deltas.

## Source Materials

- [[raw/pdf/arxiv-2506.19209.pdf|PDF]] ([[raw/latex/arxiv-2506.19209.tar.gz|LaTeX source]])
