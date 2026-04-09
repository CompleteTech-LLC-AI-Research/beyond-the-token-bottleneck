---
type: source
title: "Think Before You Speak: Training Language Models with Pause Tokens"
source_file: "[[raw/pdf/arxiv-2310.02226.pdf]]"
latex_source: "[[raw/latex/arxiv-2310.02226]]"
author: "Sachin Goyal, Ziwei Ji, Ankit Singh Rawat, Aditya Krishna Menon, Sanjiv Kumar, Vaishnavh Nagarajan"
date_published: "2023-10-03"
date_ingested: "2026-04-06"
created: "2026-04-06"
venue: "ICLR 2024"
arxiv: "2310.02226"
institution: "Carnegie Mellon University, Google Research"
tags: [latent-reasoning, pause-tokens, extra-compute, foundational]
---

# Think Before You Speak: Training Language Models with Pause Tokens

## One-liner

![[pause-tokens/one-liner]]

## Summary

The **minimal baseline** for "extra computation without language." Appending $M$ copies of a learnable `<pause>` token to the input gives the transformer $K+M$ vectors per layer instead of $K$, widening the computational pathway without meaningful new parameters (~1024 embedding parameters — a $10^{-6}$ fraction of 1B model parameters). Wins on **8/9 tasks** at 1B scale, with SQuAD improving by +19.5 EM points. Establishes the existence proof that transformers can exploit non-linguistic computation, and serves as the lower bound that all richer latent reasoning approaches ([[coconut-reasoning-latent-space|Coconut]], [[softcot-efficient-reasoning|SoftCoT]], [[thinking-states-latent-reasoning|Thinking States]]) must exceed.

## Core Mechanism

### Two-Phase Training

**Pause-pretraining**: During causal language modeling on C4 (200B tokens, ~1 epoch), $M_\text{pt}$ pause tokens are inserted at **uniformly random positions** within each 2048-token training sequence. The next-token prediction loss is **skipped** at positions where the next token is `<pause>`. The model sees the same total token count but ~10% are dummy pauses, so it actually sees fewer meaningful tokens than the baseline — yet still wins.

**Pause-finetuning**: On downstream tasks, $M_\text{ft}$ pause tokens are **appended** to the input prefix (not randomly inserted). Model output is ignored until after the last pause. Standard next-token loss on the target answer only. $M_\text{ft}$ is fixed per task (tuned from $\{10, 50\}$).

**Critical finding: both phases required.** PausePT+PauseFT is the clear winner. Introducing pauses only at finetuning (StdPT+PauseFT) gives inconsistent, "lukewarm" gains. Filler tokens (periods `.`) at inference give **zero gains** — the model must be **trained** to exploit the extra compute.

### The Pause Token

A **new vocabulary item** outside the standard vocabulary — not a filler character like `.` or `#`. Only ~1024 new embedding parameters. All pause tokens share the same learned embedding.

## Key Results (1B Model, Mean over 5 Finetuning Runs)

| Dataset | Metric | Baseline (StdPT+StdFT) | PausePT+PauseFT | Δ |
|---------|--------|------------------------|-----------------|---|
| SQuAD | EM | 36.4 ±2.5 | **55.9 ±1.0** | **+19.5** |
| CommonSenseQA | EM | 26.9 ±2.9 | **34.8 ±1.2** | **+7.9** |
| NaturalQA | EM | 23.6 ±1.2 | **26.9 ±0.4** | **+3.3** |
| LAMBADA | EM | 16.4 ±1.7 | **18.8 ±0.1** | **+2.4** |
| WebQA | EM | 13.7 ±2.1 | **16.0 ±1.6** | **+2.3** |
| GSM8k | Acc | 7.5 ±0.5 | **8.5 ±0.9** | **+1.0** |
| PhysicalIQA | F1 | 73.3 ±0.2 | **74.2 ±0.2** | **+0.9** |
| CoQA | F1 | 29.9 ±1.0 | **31.6 ±0.5** | **+1.7** |
| HellaSwag | F1 | 37.8 ±0.1 | 37.8 ±0.2 | ~0 |

**8 of 9 tasks improve.** SQuAD shows the largest gain (+19.5); HellaSwag is the sole exception. The 130M model shows gains on 6/9 tasks, but the SQuAD improvement disappears at smaller scale — **larger models benefit more**, counter-intuitively suggesting the model needs sufficient raw capacity to exploit the extra computation pathways.

## Ablation Findings

### Append > Prepend

| Dataset | Baseline | Prepend (PausePT+PauseFT) | **Append (PausePT+PauseFT)** |
|---------|----------|--------------------------|------------------------------|
| SQuAD | 36.4 | 44.0 | **55.9** |
| CommonSenseQA | 26.9 | 34.5 | **34.8** |
| GSM8k | 7.5 | 8.0 | **8.5** |

Appending is consistently better, especially on SQuAD (+11.9 over prepend). Pause-pretraining induces positional biases about where delays are useful.

### $M_\text{ft}$ Sensitivity (Optimal Pause Count Is Task-Dependent)

- **GSM8k**: Peaks at $M_\text{ft}=10$ (8.5%), drops back to ~7.5% baseline at $M_\text{ft}=50$ — inverted-U pattern
- **SQuAD**: Peaks at $M_\text{ft}=50$ (55.9%); $M_\text{ft}=10$ gives only 40.2% — monotonically increasing
- No single $M_\text{ft}$ is universally optimal. This makes practical deployment harder.

### Graceful Degradation ($M_\text{inf} \neq M_\text{ft}$)

When $M_\text{ft}=10$ but $M_\text{inf}$ varies at inference time:
- $M_\text{inf}=5$ (half): performance stays above baseline — graceful degradation
- $M_\text{inf} \in [5, 25]$: reasonable performance maintained
- **$M_\text{inf}=0$**: **catastrophic failure** — performance drops "spectacularly." A model pretrained and finetuned with pauses **cannot function without them** at inference.
- As few as 2 pause tokens restores reasonable performance.

## Width vs. Depth: The Compute Spectrum

The paper provides the conceptual framework (informal, not a formal theorem) that positions pause tokens relative to CoT and latent reasoning:

| Method | Computational expansion | Extra operations |
|--------|------------------------|-----------------|
| **Pause tokens** | **Width only**: $K+M$ vectors per layer | $M \times L$ additive (parallel per layer) |
| Chain-of-thought | **Width + depth**: $M$ tokens $\times$ $L$ layers | $M \times L$ multiplicative (sequential) |
| [[coconut-reasoning-latent-space\|Coconut]] | **Width + depth + continuous**: $K$ latent steps $\times$ $L$ layers | $K \times L$ multiplicative + superposition |

CoT's computational depth is larger by a **multiplicative factor $M$** vs pause tokens' **additive width gain**. This is why CoT produces much larger reasoning improvements — it adds effective depth ([[cot-expressivity-theory|Feng et al. prove this is the key bottleneck]]). Pause tokens add only width, which provides extra computation per layer but cannot break the $\text{TC}^0$ expressivity barrier.

## Model Architecture

| | 130M | 1B |
|---|------|-----|
| Parameters | 136M | 1.345B |
| Layers | 12 | 24 |
| Attention Heads | 12 | 32 |
| Embedding Dim | 768 | 2048 |
| Hidden Dim | 3072 | 8092 |

Pretrained on C4 English, 200B tokens. Pause token embedding: 1024 dims = $10^{-6}$ fraction of model parameters.

## Why This Matters for Latent Reasoning

Pause tokens are the **existence proof** that transformers can learn to use extra compute that carries zero semantic content, provided they are trained to do so from the start. This establishes three baselines:

1. **Lower bound on gains**: Any richer latent reasoning approach (Coconut, SoftCoT, Thinking States) that doesn't exceed pause token performance on a given task is providing no value beyond extra compute.
2. **Width-only is not enough**: The modest gains (1-19 points) vs CoT's much larger gains show that depth, not just width, is the critical resource. This motivates Coconut's feedback loop (which adds depth).
3. **Training is required**: Filler tokens at inference give zero gains. The model must learn during pretraining how to use the extra computation — this is a structural requirement, not something that emerges from prompting.

Coconut and Thinking States both use pause tokens as an ablation baseline, confirming that their continuous thoughts carry real information beyond mere extra compute: Coconut 34.1% vs pause-as-thought 24.1% on GSM8K (GPT-2 scale).

## Why Pause Tokens Work: Mechanistic Analysis

### The Extra Computation Hypothesis

Each pause token at position $t$ provides $L$ additional attention operations (one per layer) that can attend to all preceding tokens. Unlike CoT tokens, which carry semantic content through the vocabulary bottleneck, pause tokens carry **no input-side information** — they contribute only through the learned embedding (shared across all positions). The model must learn to use the pause positions as **scratch space** within attention: pause keys and values are populated via the embedding and the attention mechanism, then subsequent query tokens can attend to these positions to retrieve intermediate computation results.

This is analogous to register allocation in computer architecture: pause tokens provide additional "registers" (KV-cache entries) that the model can write intermediate results to via the attention mechanism and read from in later layers. The SQuAD result (+19.5 EM) suggests that extractive QA particularly benefits from this pattern — the model uses pause positions to pre-compute query-passage alignments before committing to an extraction span.

### Connection to Coconut's Latent Reasoning

Pause tokens and [[coconut-reasoning-latent-space|Coconut]]'s continuous thoughts share the insight that transformers can exploit non-linguistic computation, but differ fundamentally in mechanism:

| Property | Pause Tokens | Coconut Continuous Thoughts |
|----------|-------------|---------------------------|
| Information content | Zero (shared embedding) | Rich (full hidden-state feedback) |
| Compute added | Width only ($M$ extra vectors per layer) | Width + depth ($K$ extra forward passes) |
| Recurrence | None — single forward pass | Yes — each thought is a full forward pass |
| Expressivity class | Still $\text{TC}^0$ (constant depth) | Breaks $\text{TC}^0$ barrier via depth extension |
| Superposition | Not possible (fixed embedding) | Enabled — continuous vectors support [[superposition-coconut-theory|BFS via superposition]] |

Coconut's ablation directly quantifies the gap: on GSM8K at GPT-2 scale, Coconut achieves 34.1% vs. pause-as-thought at 24.1%. The 10pp difference represents the **information carried by continuous thoughts beyond mere extra compute**. This gap is expected to widen on tasks requiring search or planning (ProsQA: Coconut 97.0% vs. pause baseline 75.9%), where the depth advantage becomes critical.

### Why the 1B Model Benefits More Than 130M

The scale-dependent benefit is counter-intuitive: one might expect smaller models to benefit more from extra compute. The paper hypothesizes that exploiting pause tokens requires **sufficient capacity** to learn the complex attention patterns needed to write useful intermediate results to pause positions and read them back in later layers. At 130M parameters (12 layers, 12 heads), the attention mechanism may lack the capacity to develop these patterns. At 1B (24 layers, 32 heads), the doubled depth and head count provide enough representational space for the model to learn multi-step scratch-space computation across pause positions.

This connects to [[cot-expressivity-theory|Feng et al.]]'s theoretical framework: even within the $\text{TC}^0$ class, the constant factor matters. More layers and heads allow the model to implement more complex constant-depth circuits, and pause tokens expand the effective width of each layer's computation, making previously infeasible circuits achievable.

## Detailed Ablation Analysis

### Filler Tokens vs. Learned Pause (Critical Distinction)

Using period characters (`.`) as filler tokens at inference gives **exactly zero gain** on all 9 tasks. This rules out the hypothesis that simply having more positions for attention is sufficient — the model must be **trained from scratch** to use the extra positions. The learned pause embedding (1024 parameters) encodes the model's "intention" to use these positions for computation, and this intention must be established during pretraining so that the entire model co-adapts.

### The $M_\text{inf} = 0$ Catastrophe

When a model pretrained and finetuned with pauses is run with zero pauses at inference, performance drops "spectacularly" — well below the baseline model that was never trained with pauses. This indicates that pause-pretraining fundamentally restructures the model's computation: the model **allocates** intermediate results to pause positions during its forward pass, and removing those positions eliminates the results those later computations depend on. The model cannot gracefully degrade because its computation graph is structurally dependent on the pause positions existing.

This fragility contrasts with Coconut, where reducing the number of latent thoughts produces graceful degradation (fewer thoughts = less reasoning depth, but the model can still function). The difference stems from the recurrence: each Coconut thought is an independent forward pass with its own complete computation, while pause tokens are woven into a single forward pass where removing them breaks internal dependencies.

## Limitations

- Requires pretraining from scratch — cannot be applied to existing models (contrast with [[softcot-efficient-reasoning|SoftCoT]] which freezes the backbone entirely)
- Zero-delay fragility: pause-trained models break without pauses at inference, unlike [[coconut-reasoning-latent-space|Coconut]] which degrades gracefully
- Only tested at 130M and 1B; no experiments on larger models or encoder-decoder architectures. [[softcot-efficient-reasoning|SoftCoT]]'s [[catastrophic-forgetting]] finding suggests that applying pause-pretraining to instruction-tuned models at larger scale may face additional challenges.
- No formal theoretical result (Section 6 is explicitly informal — no theorems despite the discussion of computational width). [[cot-expressivity-theory|Feng et al.]] later provided the formal framework that pause tokens' intuitions pointed toward.
- Optimal $M_\text{ft}$ is task-dependent with no principled selection method — the inverted-U pattern on GSM8K ($M_\text{ft}=10$ optimal, $M_\text{ft}=50$ harmful) vs. monotonic improvement on SQuAD suggests fundamentally different compute demands across tasks

## Source Materials

- [[raw/pdf/arxiv-2310.02226.pdf|PDF]] (`raw/latex/arxiv-2310.02226/`)
