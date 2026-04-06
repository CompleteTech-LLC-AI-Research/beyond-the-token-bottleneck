---
type: source
title: "The Vision Wormhole: Latent-Space Communication in Heterogeneous Multi-Agent Systems"
source_file: "[[raw/pdf/arxiv-2602.15382.pdf]]"
latex_source: "[[raw/latex/arxiv-2602.15382.tar.gz]]"
venue_pdfs: ["[[raw/pdf/openreview-xTh4AwVKdw.pdf|OpenReview]]"]
author: "Xiaoze Liu, Ruowang Zhang, Weichen Yu, Siheng Xiong, Liu He, Feijie Wu, Hoin Jung, Matt Fredrikson, Xiaoqian Wang, Jing Gao"
date_published: "2026-02-17"
date_ingested: "2026-04-06"
created: "2026-04-06"
updated: "2026-04-06"
venue: "arXiv preprint (work in progress)"
arxiv: "2602.15382"
institution: "Purdue, Contextual AI, CMU, Georgia Tech"
tags: [latent-communication, heterogeneous, vision-language, cross-architecture]
---

# The Vision Wormhole: Latent-Space Communication in Heterogeneous Multi-Agent Systems

## Summary

The **Vision Wormhole** repurposes the **visual input pathway** of Vision-Language Models (VLMs) as a universal continuous communication channel between heterogeneous agents. The key insight: VLMs are explicitly trained to accept dense, continuous vectors through their visual encoders — unlike text-only LLMs whose embedding layers expect discrete token embeddings. By injecting sender reasoning traces into the receiver's vision-token span, the framework achieves cross-architecture latent communication without the "off-manifold" problem that plagues direct hidden-state injection into text-only models.

## Core Innovation: The Visual Pathway as Communication Port

Text-only LLMs reject continuous vectors injected at the text embedding layer because text embeddings are [[continuous-vs-discrete-representation|sparse/discrete]] — continuous vectors are "off-manifold" and cause generation collapse. VLMs, however, have a vision pathway designed for exactly this: processing dense continuous vectors as meaningful context. The Vision Wormhole repurposes this pathway not for image understanding but for **model-to-model information transfer**.

## Architecture (4-Stage Pipeline)

> [!diagram|left]
> ```mermaid
> graph LR
>     subgraph Sender["Sender (Frozen VLM)"]
>         S1["**Stage 1: Latent Rollout**<br>T=1024 steps<br>NormMatch rescaling"]
>         S2["**Stage 2: Universal Encoding**<br>Perceiver resampler<br>D=512 universal dim"]
>     end
>     subgraph Hub["Shared Space"]
>         S3["**Stage 3: Affine Alignment**<br>Hub-and-spoke<br>Ridge regression"]
>     end
>     subgraph Receiver["Receiver (Frozen VLM)"]
>         S4["**Stage 4: Vision Injection**<br>Decoder with gated residual<br>256 image queries"]
>         Out["**Text Output**<br>Conditioned on<br>sender's reasoning"]
>     end
> 
>     S1 -->|"Hidden states"| S2 -->|"Universal tokens"| S3 -->|"Reference tokens"| S4 --> Out
> 
>     style Sender fill:#dae8fc,stroke:#6c8ebf
>     style Hub fill:#fff2cc,stroke:#d6b656
>     style Receiver fill:#d5e8d4,stroke:#82b366
> ```

> [!notation|right]
> | Element | Notation |
> |---|---|
> | Latent rollout | $h_0 \to h_1 \to \ldots \to h_T$ |
> | Hidden states | $H_i = [x_0, \ldots, x_{T-1}] \in \R^{T \times d_i}$ |
> | Universal tokens | $U_i \in \R^{K_u \times D}$ |
> | Reference tokens | $U_{\text{ref}} = U_i \cdot W + b$ |
> | Affine alignment | $W_i^{\text{out}}, b_i^{\text{out}}$ with $O(N)$ parameters |
> | Vision injection | $\Delta_i \in \R^{K_{\text{img}} \times d_i}$, gate $g_i \in (0,1)$ |

### Stage 1: Latent Rollout Extraction (Sender)

Given a prompt, the frozen VLM backbone produces a final hidden vector $h_0$ at the prompt boundary. The system then generates a **T-step latent rollout** by repeatedly feeding back a single continuous pseudo-token embedding derived from the previous hidden state, **reusing the prompt's attention cache** (keys/values remain fixed from the original prompt processing). At each step t:

- Form input embedding: $x_t = \text{NormMatch}(h_t)$
- **NormMatch** rescales hidden states to match the typical norm of the model's token embeddings: $\text{NormMatch}(h) = \mu_i \cdot h / (\|h\|_2 + \varepsilon)$, where $\mu_i = \E[\|E_i(w)\|_2]$ over the vocabulary. This prevents norm drift that would destabilize autoregressive continuation in embedding space.
- The rollout yields $H_i = [x_0, \ldots, x_{T-1}] \in \R^{T \times d_i}$, a compact continuous summary of the agent's reasoning state.
- Rollout length T is fixed at **1024 steps** (bounds message extraction cost).

### Stage 2: Universal Token Encoding

A **Perceiver-style resampler** (cross-attention from learned queries to the rollout) compresses $H_i$ into a fixed set of universal tokens $U_i \in \R^{K_u \times D}$.

**Encoder mechanism:**
1. Project rollout into universal dimension: $Z = H_i P_i \in \R^{T \times D}$ (learned $P_i \in \R^{d_i \times D}$)
2. Maintain learned queries $Q^0 \in \R^{K_u \times D}$, updated through $L$ cross-attention blocks:
   - $Q^{\ell+1} = Q^\ell + \text{MHA}(\text{LN}(Q^\ell), \text{LN}(Z), \text{LN}(Z))$
   - $Q^{\ell+1} = Q^{\ell+1} + \text{FFN}(\text{LN}(Q^{\ell+1}))$ for $\ell = 0, \ldots, L-1$

**Token composition** ($K_u = K + 2 = 1024$ total):
- **$K$ semantic tokens**: carry the message content
- **1 global token**: for pooling/aggregation
- **1 style token**: encodes distributional statistics of the rollout via $s(H_i) = [\text{mean}(H_i), \text{std}(H_i), \sqrt{(1/T) \sum \|H_{i,t}\|^2}] \in \R^3$, mapped by a small MLP into $\R^D$ and added to the style token. This stabilizes cross-prompt and cross-role transfer by communicating coarse distributional properties.

**Shared universal dimension: $D = 512$** across all agents.

### Stage 3: Affine Alignment (Hub-and-Spoke)

Per-agent affine transformations map universal tokens to a shared reference space $U_\text{ref}$. Fix a reference agent $r$, then for each agent $i$:

- **Outbound**: $U_\text{ref} = U_i W_i^{\text{out}} + b_i^{\text{out}}$
- **Inbound**: $U_i = U_\text{ref} W_i^{\text{in}} + b_i^{\text{in}}$
- Where $W \in \R^{D \times D}$ and $b \in \R^D$

This yields **$O(N)$ alignment parameters** (one map per model to/from the hub) instead of $O(N^2)$ pairwise adapters.

**Ridge regression fitting:** Given shared anchor texts $\{m_j\}$, compute universal tokens $U_i(m_j)$ for every model $i$ using the trained encoder. Flatten across anchors and token positions to form $X_i \in \R^{(M \cdot K_u) \times D}$ and $Y_r \in \R^{(M \cdot K_u) \times D}$. Solve the closed-form regularized least-squares problem:

$$\min_{W,b} \|X_i W + \mathbf{1}b - Y_r\|_F^2 + \lambda\|W\|_F^2$$

Standard solution after mean-centering. Both forward ($A^{\text{out}}$) and reverse ($A^{\text{in}}$) maps are fit this way. Because ridge regression is inexpensive, alignment can be **re-fit whenever new models join** without retraining.

**Why affine works:** The hypothesis is $U_i(m) \approx \text{reshape}(z(m) \cdot R_i + \text{noise})$, where $z(m)$ is a shared semantic representation and $R_i$ is a model-specific invertible linear transform. Ridge regression estimates $R_i^{-1}$. The encoder's bottleneck discards idiosyncratic nuisance variation, making the remaining cross-model mismatch closer to an affine change-of-basis.

**Anchor count:** Default uses 3,000 anchors (1,000 each from CoS-E, OpenCodeReasoning, PRM800K). Weakly supervised variant uses only **90 anchors** (30 per source).

### Stage 4: Vision-Span Injection (Receiver)

The decoder $D_i$ maps universal tokens to a vision-span perturbation and scalar gate:

$$(\Delta_i, g_i) = D_i(U_i), \quad \Delta_i \in \R^{K_\text{img} \times d_i}, \; g_i \in (0,1)$$

**Decoder architecture:** Mirrors the resampler pattern. A learned set of $K_\text{img} = $ **256 image queries** attends to the universal tokens to produce $K_\text{img}$ vectors, linearly projected into $\R^{d_i}$ to form $\Delta_i$. The gate $g_i$ is predicted from a pooled representation of the universal tokens.

**Dummy-image baseline:** A fixed dummy image is processed once per model to produce baseline visual embeddings $\bar{X}_\text{img} \in \R^{L_\text{img} \times d_i}$. The perturbation is resampled to the required image-span length via **linear interpolation** along the token index, then injected residually:

$$X_\text{img} = \bar{X}_\text{img} + g_i \cdot \text{Resample}(\Delta_i;\; L_\text{img})$$

The **gated residual** serves two roles: (i) prevents over-injection when memory is empty or low-confidence, and (ii) adapts injection strength per example. Residual writing relative to $\bar{X}_\text{img}$ keeps injected context near the visual embedding manifold, improving stability.

## Self-Distillation Training

The codec is trained via **label-free self-distillation** — no human annotation required. The text-based communication path acts as "Teacher" and the vision wormhole acts as "Student."

**Setup:** Anchor messages m (short text strings) are used. The teacher prompt includes m explicitly as text. The student prompt omits m but contains a dummy image whose image-token span is overwritten by the injection computed from the teacher-side rollout.

**Loss function** (Eq. 3, three terms):

$$\Loss_\text{codec} = \lambda_h \|h_\text{vis} - \text{stopgrad}(h_\text{text})\|^2 + \lambda_\text{kl} \cdot \text{KL}(\text{softmax}(z_\text{text}/\tau) \| \text{softmax}(z_\text{vis}/\tau)) + \lambda_\text{rms} (\text{RMS}(\Delta_\text{inj}) - \text{RMS}(\bar{X}_\text{img}))^2$$

- **Hidden-state MSE** (weight 1.0): Enforces representational fidelity at the prompt boundary
- **KL divergence** (weight 0.25, temperature $\tau = 1.0$): Enforces output-distribution fidelity over the full vocabulary — especially informative because it provides rich gradient over the entire vocabulary distribution, not just a single target token
- **RMS matching** (weight 0.1): Stabilizes injection magnitude in the visual embedding manifold

Only codec parameters ($E_i$, $D_i$) are updated. Backbone remains frozen. Gradient clipping at max-norm 1.0.

## Codec Architecture Details

| Parameter | Value |
|---|---|
| Universal token dimension $D$ | 512 |
| Number of universal tokens $K_u$ | 1024 |
| Image injection tokens $K_\text{img}$ | 256 |
| Transformer layers | 6 |
| Attention heads | 8 |
| Dropout | 0.10 |
| Latent rollout length $T$ | 1024 |
| Training steps | 400 |
| Batch size | 2 |
| Optimizer | AdamW, lr = $2 \times 10^{-4}$ |
| Codec parameter count | ~0.05B |
| Effective dataset coverage (default) | ~0.27× (800 draws / 3000 anchors) |
| Effective dataset coverage (weak) | ~8.9× (800 draws / 90 anchors) |

## Results

### Small Models (1.6B–4B): Full Table

Five two-backbone configs + one four-backbone config, 9 benchmarks each. Macro-averaged: **+6.3pp accuracy, 1.87× speedup** over TextMAS.

**Two-backbone configurations (Planner/Refiner → Critic/Judger):**
- Gemma-3-4B + Qwen3-VL-2B
- LFM2.5-VL-1.6B + Gemma-3-4B
- LFM2.5-VL-1.6B + Qwen3-VL-2B
- SmolVLM2-2.2B + Gemma-3-4B
- SmolVLM2-2.2B + Qwen3-VL-2B

**Four-backbone pool:** SmolVLM2-2.2B + LFM2.5-VL-1.6B + Gemma-3-4B + Qwen3-VL-2B

Selected highlights from Table 2:
- **AIME 2024** (SmolVLM2 + Qwen3-VL-2B): +10.0pp accuracy, **5.47× speedup** (2807s → 513s)
- **AIME 2025** (Gemma-3-4B + Qwen3-VL-2B): +10.0pp, 3.75× speedup
- **HumanEval-Plus** (SmolVLM2 + Gemma-3-4B): +26.2pp (32.9% → 59.1%), 1.64× speedup
- **GSM8K** (SmolVLM2 + Gemma-3-4B): +17.6pp (67.8% → 85.4%), 1.96× speedup
- Code generation average: **+13.2pp, 1.21× speedup**

### Weakly Supervised Variant (<100 Anchor Texts)

Trained with only **90 anchor texts** (30 per source). Tested on Gemma-3-4B + Qwen3-VL-2B and SmolVLM2-2.2B + Qwen3-VL-2B configs.

Macro average: **+6.5pp accuracy, 2.67× speedup** — remarkably data-efficient.

Selected results (SmolVLM2 + Qwen3-VL-2B, weakly supervised):
- **AIME 2024**: +23.4pp (13.3% → 36.7%), **7.20× speedup** (2807s → 390s)
- **AIME 2025**: +6.6pp, 4.80× speedup
- **GSM8K**: +12.7pp (64.3% → 77.0%), 2.49× speedup
- **HumanEval-Plus**: +11.6pp, 1.56× speedup

### Single-Agent vs MAS Comparison

| Model | Single-Agent Avg | TextMAS Avg | VW Avg | Δ Text | Δ VW |
|---|---|---|---|---|---|
| Qwen3-VL-2B | 50.8 | 49.4 | 52.6 | **-1.4pp** | +1.8pp |
| Gemma-3-4B | 55.7 | 52.5 | 56.0 | **-3.2pp** | +0.3pp |
| SmolVLM2-2.2B | 25.8 | 44.2 | 52.7 | +18.5pp | **+26.9pp** |
| LFM2.5-VL-1.6B | 40.2 | 46.8 | 52.2 | +6.6pp | **+12.0pp** |
| **Macro Avg** | 43.1 | 48.2 | 53.4 | +5.1pp | **+10.3pp** |

Key finding: For **strong backbones** (Qwen3-VL-2B, Gemma-3-4B), TextMAS **drops below** single-agent baselines (-1.4pp to -3.2pp), but VW stays at or above parity. For **weak backbones** (SmolVLM2, LFM2.5), both MAS variants help, but VW gains are much larger (+26.9pp vs +18.5pp for SmolVLM2). This indicates VW is more robust to heterogeneous orchestration effects — bounded latent communication reduces cross-role interference.

### Mid-Sized Models (4B–12B)

Two configs: Gemma-3-4B + Qwen3-VL-8B, and Qwen3-VL-8B + Gemma-3-12B.

**Dramatic speedups** (macro-average **5.92×**), with Qwen3-VL-8B + Gemma-3-12B seeing extreme speedups:
- AIME 2024: **16.54×** (1639s → 99s)
- MBPP-Plus: **13.51×** (238s → 18s)
- GPQA: **16.40×** (873s → 53s)
- ARC-Easy: 7.23×, ARC-Challenge: 7.34×

**But accuracy degrades** (macro-average **-5.3pp**), especially on complex tasks:
- AIME 2024 (8B+12B): -33.3pp (60.0% → 26.7%)
- AIME 2025 (8B+12B): -26.7pp (46.7% → 20.0%)
- GPQA (8B+12B): -21.7pp (61.6% → 39.9%)
- Simpler tasks hold: GSM8K +1.4pp (Gemma+Qwen8B), ARC-Easy +0.6pp

**Root cause:** The default fixed bandwidth (1024 latent steps, 256 visual tokens) becomes a bottleneck for stronger backbones that produce richer reasoning states. This is **not a hard limit** — bandwidth can be increased by stacking multiple images (e.g., four 224×224 images for ~1024 tokens) or using higher-resolution images (e.g., 1008px in Qwen-style prompts).

## Ablation Insights

### NormMatch Components

NormMatch rescaling ($\text{NormMatch}(h) = \mu_i \cdot h / (\|h\|_2 + \varepsilon)$) is critical for preventing norm drift during latent rollout. Without NormMatch, rollout hidden states diverge from the embedding manifold within ~50 steps, causing generation collapse. The per-model calibration constant $\mu_i = \E[\|E_i(w)\|_2]$ must be computed over the full vocabulary — approximating with a subset degrades rollout stability.

### Resampler Configuration

The Perceiver-style resampler uses 6 Transformer layers with 8 attention heads and dropout 0.10. Reducing to 3 layers drops accuracy by ~3-4pp on math benchmarks. Increasing to 12 layers shows diminishing returns (<1pp gain) while doubling codec parameter count. The L=6 configuration represents the efficiency sweet spot at ~0.05B parameters per codec.

### Alignment Anchor Count

Default: **3,000 anchors** (1,000 each from CoS-E, OpenCodeReasoning, PRM800K). The weakly supervised variant uses only **90 anchors** (30 per source) yet achieves comparable or better results (+6.5pp accuracy, 2.67x speedup vs +6.3pp, 1.87x for full supervision). This remarkable data efficiency suggests that affine alignment via ridge regression is well-conditioned: the cross-model mismatch is low-rank enough that ~90 paired observations suffice to estimate the affine transform. However, the weakly supervised variant shows higher variance across benchmark pairs — reliability improves with more anchors even if average performance does not.

### Visual Token Budget

The default **256 image injection tokens** ($K_\text{img}$) suffice for small models (1.6B-4B) but become a bottleneck for mid-sized models (4B-12B). The accuracy degradation on complex tasks (AIME 2024: -33.3pp for 8B+12B config) is attributed to this fixed bandwidth. The paper notes this is not a hard limit: stacking multiple images (4x 224x224 for ~1024 tokens) or using higher-resolution images (1008px Qwen-style) can increase the visual token budget proportionally. No systematic ablation of $K_\text{img} \in \{64, 128, 256, 512, 1024\}$ is provided — this is a key gap for understanding the bandwidth-accuracy trade-off curve.

## Limitations

- Requires VLMs specifically (text-only models cannot be receivers)
- Fixed bandwidth bottleneck for large models (256 visual tokens insufficient for 8B+)
- Only tested on sequential Planner-Critic-Refiner-Judger workflows
- Could not reliably reproduce Cache-to-Cache or LatentMAS baselines on their heterogeneous configs (degenerate outputs), so comparison is only against TextMAS
- Preprint / work in progress

## Connections

- **[[embedding-space-communication]]**: Advances the spectrum by using the VLM visual pathway as a modality-grounded anchor for continuous communication — solving the off-manifold problem.
- **[[kv-cache-alignment-shared-space|KV Cache Alignment]]**: Both use hub-and-spoke topology with $O(N)$ alignment. KV Cache Alignment uses a learned shared KV space; Vision Wormhole uses the visual embedding space as the "hub."
- **[[cache-to-cache-semantic-communication|C2C]]**: Both enable cross-architecture communication via learned projections, but C2C requires $O(N^2)$ pairwise fusers while VW needs $O(N)$ codecs. C2C adapters for Qwen3-0.6B↔Qwen2.5-0.5B occupy 818.4 MB — comparable to the 988 MB backbone itself. VW codecs are ~0.05B parameters.
- **[[latent-space-reasoning]]**: The latent rollout extraction is conceptually related to [[coconut-reasoning-latent-space|Coconut]]'s continuous thought — both feed back hidden states as pseudo-tokens. VW uses this for message extraction rather than reasoning itself.
- **[[softcot-efficient-reasoning|SoftCoT]]**: Both use self-distillation (text path as teacher, continuous path as student). VW distills at the communication boundary between agents rather than within a single model.

## Source Materials

- [[raw/pdf/arxiv-2602.15382.pdf|PDF]] ([[raw/latex/arxiv-2602.15382.tar.gz|LaTeX source]])
