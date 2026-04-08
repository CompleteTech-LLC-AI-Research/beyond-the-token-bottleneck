---
type: source
title: "SoftCoT: Soft Chain-of-Thought for Efficient Reasoning with LLMs"
source_file: "[[raw/pdf/arxiv-2502.12134.pdf]]"
latex_source: "[[raw/latex/arxiv-2502.12134.tar.gz]]"
author: "Yige Xu, Xu Guo, Zhiwei Zeng, Chunyan Miao"
date_published: "2025-02-17"
date_ingested: "2026-04-06"
created: "2026-04-06"
venue: "ACL 2025"
arxiv: "2502.12134"
institution: "Nanyang Technological University, Singapore"
tags: [latent-reasoning, continuous-thought, soft-tokens, catastrophic-forgetting]
---

# SoftCoT: Soft Chain-of-Thought for Efficient Reasoning with LLMs

## Summary

**SoftCoT** addresses a critical limitation of [[latent-space-reasoning]] approaches like [[coconut-reasoning-latent-space|Coconut]]: when applied to modern instruction-tuned LLMs (rather than GPT-2), continuous reasoning methods cause **[[catastrophic-forgetting|catastrophic forgetting]]** that degrades performance below the zero-shot baseline. SoftCoT solves this by **externalizing** the continuous reasoning to a small frozen assistant model, projecting the resulting "soft thought tokens" into the backbone LLM's embedding space via a lightweight trainable projection layer. The backbone LLM remains completely frozen.

## The Catastrophic Forgetting Problem

This paper provides the first systematic evidence that latent reasoning techniques break when applied to capable instruction-tuned models:

| Method | GSM8K (LLaMA-3.1-8B-Instruct) |
|--------|-------------------------------|
| Zero-Shot CoT | 79.61% |
| LoRA Fine-Tuning | 75.66% (−3.95) |
| Coconut (adapted with LoRA) | 76.12% (−3.49) |
| **SoftCoT** | **81.03% (+1.42)** |

Both LoRA fine-tuning and Coconut **fall below** the zero-shot baseline — the instruction-tuned model's carefully calibrated capabilities are damaged by any parameter modification. SoftCoT is the only trained method that improves over zero-shot CoT, because it never modifies the backbone.

This finding has significant implications for [[latent-space-reasoning]]: Coconut's results on GPT-2 (a small, non-instruction-tuned model) may not transfer to frontier models. The training curriculum that works for GPT-2 actively harms instruction-tuned models.

## Core Mechanism

> [!diagram|left]
> ```mermaid
> graph LR
>     subgraph Assistant["Frozen Assistant Model (e.g. 1B)"]
>         Q["Question +<br>N placeholder tokens"] --> AFWD["Forward Pass"] --> HID["Hidden states at<br>placeholder positions<br>(soft thought tokens)"]
>     end
> 
>     subgraph Projection["Trainable Projection"]
>         HID --> PROJ["Linear projection layer<br>(only trained component)"]
>     end
> 
>     subgraph Backbone["Frozen Backbone LLM (e.g. 8B)"]
>         PROJ --> CONCAT["Instruction + Question +<br>Projected Soft Thoughts"] --> BFWD["Forward Pass"] --> OUT["Discrete CoT +<br>Answer"]
>     end
> 
>     style Assistant fill:#dae8fc,stroke:#6c8ebf
>     style Projection fill:#fff2cc,stroke:#d6b656
>     style Backbone fill:#d5e8d4,stroke:#82b366
> ```

> [!notation|right]
> | Component | Notation |
> |---|---|
> | Question input | $Q$ |
> | Placeholder tokens | $N$ `[UNK]` tokens |
> | Projection layer | $W_p \in \R^{d_{\text{assist}} \times d_{\text{LLM}}}$ |
> | Assistant hidden dim | $d_{\text{assist}}$ |
> | Backbone hidden dim | $d_{\text{LLM}}$ |

### Three Components

**1. Assistant Model (frozen)**: A small LLM (e.g., LLaMA-3.2-1B-Instruct or Qwen2.5-0.5B-Instruct) receives:
- A task-specific instruction ("generate reasoning hints")
- The question Q
- N `[UNK]` placeholder tokens

In a single forward pass, the final-layer hidden states at the N `[UNK]` positions are extracted as **soft thought tokens** — continuous vectors encoding the assistant's reasoning about the problem.

**2. Projection Module (only trainable component)**: A linear layer maps from d_assist to d_LLM (e.g., 1B model's hidden dim → 8B model's hidden dim). This is the **only** trained component — a simple linear bridge between representation spaces.

**3. Backbone LLM (frozen)**: Receives the task instruction, question, and projected soft thought tokens as a continuous "preamble." Then generates standard discrete reasoning steps and an answer autoregressively.

### The Frozen Backbone Mechanism

The frozen backbone design is what distinguishes SoftCoT from all prior [[latent-space-reasoning]] methods. The projection module is a single linear layer $W_p \in \R^{d_\text{assist} \times d_\text{LLM}}$ that maps from the assistant's hidden dimension to the backbone's. Crucially, there is no nonlinear transformation, no multi-layer adapter, and no attention-based fusion — just an affine projection. This simplicity is possible because both models share the same tokenizer family and are trained on similar data distributions, so their representation spaces are related by approximately linear transforms (consistent with [[relative-representations-zero-shot|Moschella et al., 2022]]).

Because the backbone is never modified, it retains its full instruction-following capability, RLHF alignment, and safety properties. This is a practical advantage over [[coconut-reasoning-latent-space|Coconut]] that goes beyond accuracy: production deployments can add SoftCoT reasoning without re-validating the base model's safety alignment.

### Training

Only the projection module parameters are trained via standard next-token prediction loss on the reasoning + answer span. Both the assistant and backbone LLM are completely frozen. Trained on a single A100-80G.

## Key Results

### LLaMA-3.1-8B-Instruct (averages over 5 seeds)

| Benchmark | Zero-Shot CoT | SoftCoT | Δ |
|-----------|--------------|---------|---|
| GSM8K | 79.61% | 81.03% | +1.42 |
| ASDiv-Aug | 86.78% | 87.19% | +0.41 |
| AQuA | 54.65% | 56.30% | +1.65 |
| StrategyQA | 65.63% | 69.04% | +3.41 |
| Date Understanding | 54.40% | 59.04% | +4.64 |
| **Average** | **68.21%** | **70.52%** | **+2.31** |

### Qwen2.5-7B-Instruct

| Benchmark | Zero-Shot CoT | SoftCoT | Δ |
|-----------|--------------|---------|---|
| GSM8K | 83.70% | 85.81% | +2.11 |
| AQuA | 64.53% | 72.44% | +7.91 |
| StrategyQA | 49.65% | 60.61% | +10.96 |
| **Average** | **70.29%** | **75.06%** | **+4.77** |

Gains are especially large on tasks requiring commonsense reasoning (StrategyQA) and multiple-choice reasoning (AQuA). SoftCoT is orthogonal to self-consistency — combining them yields GSM8K 90.63%.

## Ablation Findings

### Soft Tokens Are ~4× More Efficient Than Hard Tokens

SoftCoT achieves optimal performance with **6 soft thought tokens**, while the hard-token variant (Assist-CoT, where the assistant generates discrete text) needs **24 tokens** for comparable performance. This ~4× compression ratio is consistent with CCoT's reported 5× ratio, providing further evidence for the [[continuous-vs-discrete-representation|continuous vs. discrete information density gap]].

The compression mechanism differs qualitatively from Coconut's. In Coconut, the continuous thought encodes a **superposition** of possible reasoning paths (enabling emergent BFS). In SoftCoT, the soft tokens encode **condensed reasoning cues** — hints that bias the backbone's attention patterns without dictating a specific reasoning path. The backbone retains full autonomy over its discrete reasoning chain; the soft tokens function more like a continuous "preamble" that primes relevant associations. This explains why 6 tokens suffice: they need only shift the probability landscape, not carry the full reasoning trajectory.

### Assistant Model Size Barely Matters

| Assistant size | SoftCoT accuracy (GSM8K) |
|---------------|-------------------------|
| 0.5B | 85.76% |
| 1.5B | 85.81% |
| 7B | 85.84% |

Even a 0.5B assistant is nearly as effective as a 7B one. The assistant's role is to provide **reasoning cues** in continuous space, not to solve the problem. The backbone LLM does the actual reasoning.

### [UNK] Tokens as Pause Tokens

Adding raw (untrained) `[UNK]` tokens slightly improves accuracy (68.21% → 68.49%) and reduces variance, consistent with the pause token literature (Goyal et al., 2024). The extra forward-pass compute alone provides marginal benefit; the trained projection provides the real gains.

## Theoretical Positioning

SoftCoT introduces a new point on the [[latent-space-reasoning]] spectrum:

| Method | Who reasons in latent space? | Backbone modified? | Scale tested |
|--------|----------------------------|-------------------|-------------|
| [[coconut-reasoning-latent-space\|Coconut]] | The model itself (hidden-state feedback loop) | Yes (full training) | GPT-2 |
| Coconut on instruction-tuned | The model itself | Yes (LoRA) | 7-8B (**degrades**) |
| **SoftCoT** | **External assistant model** | **No (frozen)** | **7-8B (improves)** |
| Standard CoT | The model itself (in token space) | No | Any |

SoftCoT trades Coconut's elegant self-contained loop for a **two-model architecture** that preserves the backbone — a pragmatic solution to the [[catastrophic-forgetting|catastrophic forgetting]] problem that may be the only viable approach for frontier instruction-tuned models.

### Comparison of Training Approaches

The three latent reasoning training paradigms reveal a progression in how the field handles the tension between continuous reasoning power and model integrity:

| Property | [[icot-internalize-cot\|iCoT]] | [[coconut-reasoning-latent-space\|Coconut]] | **SoftCoT** |
|----------|------|---------|---------|
| Training target | Full model | Full model | Projection only |
| Curriculum | Progressive CoT token removal | Multi-stage CoT → latent replacement | Single-stage next-token prediction |
| Optimizer reset needed | Yes (critical) | Yes (adopted from iCoT) | No (single-phase training) |
| Backbone modification | Complete retraining | Complete retraining | **None** |
| Scale demonstrated | GPT-2 (117M) | GPT-2 (small) | 7-8B instruction-tuned |
| Continuous thought source | Internalized within model | Self-generated hidden states | External assistant model |

iCoT and Coconut both require the delicate multi-stage curriculum with optimizer resets — a training procedure that is fragile and empirically shown to fail on instruction-tuned models. SoftCoT sidesteps this entirely by externalizing the reasoning to a separate model, requiring only standard supervised training of a small projection layer.

## Connections to the Wiki

- **[[latent-space-reasoning]]**: SoftCoT is a new approach to latent reasoning that avoids modifying the reasoning model. The soft thought tokens serve as a continuous "preamble" conditioning the LLM before it generates standard discrete CoT.
- **[[continuous-vs-discrete-representation]]**: The 4× compression ratio (soft vs. hard tokens) provides direct empirical evidence for the information density advantage of continuous representations.
- **[[embedding-space-communication]]**: The projection module that maps between assistant and backbone embedding spaces is analogous to cross-model communication — effectively a form of latent communication from a small "reasoning specialist" to a large "generalist."
- **[[kv-cache-alignment-shared-space|KV Cache Alignment]]**: Both use linear/learned projections to bridge representation spaces between models. KV Cache Alignment operates on KV-caches; SoftCoT operates on hidden-state embeddings.
- **[[catastrophic-forgetting]]**: SoftCoT is the first paper in this collection to systematically document this problem for latent reasoning methods on instruction-tuned LLMs.

## Limitations

- Soft thoughts **augment** standard CoT rather than replacing it — the LLM still generates a full discrete reasoning chain. No token savings at inference.
- Single forward pass through the assistant — no iterative refinement (unlike Coconut's multi-step loop).
- Tested only on 7-8B models. Scalability to 70B+ unverified.
- Requires task-specific training data with annotated reasoning steps for the projection module.
- The linear projection assumes approximately linear relationships between assistant and backbone representation spaces — may fail for very heterogeneous model families where the [[relative-representations-zero-shot|isometric assumption]] breaks down.

## Source Materials

- [[raw/pdf/arxiv-2502.12134.pdf|PDF]] ([[raw/latex/arxiv-2502.12134.tar.gz|LaTeX source]])
