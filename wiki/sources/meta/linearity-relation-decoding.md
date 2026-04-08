---
type: source
title: "Linearity of Relation Decoding in Transformer Language Models"
source_file: "[[raw/pdf/arxiv-2308.09124.pdf]]"
latex_source: "raw/latex/arxiv-2308.09124/"
author: "Evan Hernandez, Arnab Sen Sharma, Tal Haklay, Kevin Meng, Martin Wattenberg, Jacob Andreas, Yonatan Belinkov, David Bau"
date_published: "2023-08-17"
date_ingested: "2026-04-06"
created: "2026-04-06"
venue: "ICLR 2024"
arxiv: "2308.09124"
institution: "MIT, Northeastern, Technion IIT, Harvard"
tags: [interpretability, linear-relations, enriched-representations, foundational]
---

# Linearity of Relation Decoding in Transformer Language Models

## One-liner

![[linearity-relation-decoding/one-liner]]

## Summary

Establishes that transformers implement **linear relational embeddings (LREs)** for ~48% of their relational knowledge: the mapping from a subject's hidden representation to the predicted object can be approximated by a single affine transformation. The key finding for this wiki: **mid-layer representations are richer than final-layer representations** — the model enriches entities with relational knowledge at intermediate layers (~layer 7-17 of 28 in GPT-J), then **compresses** for next-token prediction in later layers. This is the mechanistic explanation for why [[activation-communication-harvard|AC]]'s layer-26 communication works and why [[kvcomm-kth-selective|KVComm]] finds intermediate layers most transferable.

## The LRE Formula

For a relation r (e.g., "plays the sport of"), the mapping from subject representation s at an intermediate layer to the object representation o:

> $$\text{LRE}(s) = \beta \cdot W_r \cdot s + b_r$$

Where $W_r$ is estimated as the mean Jacobian over $n=8$ examples within the same relation:

> $$W = \E_{s_i, c_i}\left[\frac{\partial F}{\partial s} \;\middle|\; (s_i, c_i)\right]$$

And $b_r = \E[F(s,c) - (\partial F / \partial s) \cdot s]$. This is a first-order Taylor approximation of the model's internal computation $F$.

**$\beta$ correction**: Layer normalization causes the Jacobian to underestimate magnitude by 2.5-4.3x. $\beta$ compensates: GPT-J $\beta=2.25$, LLaMA-13B $\beta=8.0$, GPT2-XL $\beta=2.25$. Selected to maximize faithfulness-causality correlation.

**Low-rank pseudoinverse**: For causal editing, uses $W_r^\dagger$ (low-rank pseudoinverse, rank $\rho_r$ per relation) instead of full inverse, preventing noisy small singular values from washing out meaningful ones.

## The 48%/52% Breakdown

47 relations across 4 categories (26 factual, 8 commonsense, 6 linguistic, 7 bias), covering 10,000+ facts.

### Linear Relations (>60% faithfulness) — 48% of tested relations

| Relation | Faithfulness |
|----------|-------------|
| Occupation-gender | 0.98 |
| Adjective comparative | 0.98 |
| Adjective superlative | 0.93 |
| Country largest city | 0.92 |
| Name birthplace | 0.92 |
| Country capital city | 0.88 |
| Country language | 0.88 |
| Substance phase of matter | 0.87 |
| Object superclass | 0.85 |
| Name religion | 0.80 |
| Name gender | 0.80 |

### Non-Linear Relations (<30% faithfulness) — 52% of tested relations

| Relation | Faithfulness | Range size |
|----------|-------------|------------|
| Company CEO | 0.06 | 287 entities |
| Person father | 0.07 | 968 entities |
| Person mother | 0.14 | 962 entities |
| Pokemon evolution | 0.15 | — |
| Company HQ | 0.21 | — |

Pattern: Relations with **large, person/company-name ranges** resist linear approximation. Relations with small, categorical ranges (adjective forms, countries, genders) are highly linear.

**Cross-model consistency**: GPT-J relation-wise performance correlates with GPT2-XL (Spearman $R = 0.85$) and LLaMA-13B ($R = 0.71$). The same relations are linear/nonlinear across architectures.

## Layer Dynamics: The Mode Switch

The paper's most important finding for latent communication:

**Faithfulness rises through early-to-middle layers, then drops sharply in later layers.** Example (GPT-J, "plays the sport of"): faithfulness peaks at ~layer 7-17, then plummets.

### Why: Dual-Purpose Hidden Representations

Hidden states serve two purposes simultaneously:
1. **Encoding entity attributes** (relational knowledge, facts about the subject)
2. **Preparing next-token prediction** (output-optimized representation)

At later layers, purpose #2 overwrites purpose #1. The model "throws away" relational knowledge not needed for the immediate next-token prediction.

### Evidence for the Mode Switch

When the object token immediately follows the subject (no relation-specific context), faithfulness does **not** drop in later layers — because there's no competing prediction task to overwrite the relational encoding.

**Causality drops earlier than faithfulness**: Because information leaks from pre-intervention layers through attention (layers 0 to l-1 retain original subject info).

## The Attribute Lens: Internal Knowledge > Expressed Knowledge

The attribute lens applies the LRE to decode relational attributes from any hidden state at any layer. Critical result: it reveals **facts the model "knows" but doesn't output**.

### Adversarial Prompt Results (GPT-J, 11,891 prompts per condition)

| Condition | Model Output R@1 | **Attribute Lens R@1** | Attribute Lens R@3 |
|-----------|-----------------|----------------------|-------------------|
| Repetition-distracted | 0.02 | **0.54** | 0.71 |
| Instruction-distracted | 0.03 | **0.63** | 0.78 |

The model outputs the wrong answer almost every time (R@1 = 0.02-0.03), but the attribute lens recovers the correct fact from internal representations within top-3 predictions 71-78% of the time. **The model knows the right answer internally but outputs the wrong one** — latent communication would transmit the correct knowledge.

### Adversarial Setup
- **Repetition-distracted**: States a falsehood twice, asks model to complete a third time ("The capital city of England is Oslo" ×2 → "The capital city of England is...")
- **Instruction-distracted**: States falsehood, then "Repeat exactly."

## Causal Editing

The LRE inverse enables **causal steering** of model outputs by editing internal representations:

> $$\delta_s = W_r^\dagger(o' - o), \quad \tilde{s} = s + \delta_s$$

To change prediction from object o to target o'. Uses low-rank pseudoinverse W_r^†. Closely matches oracle performance (direct subject-representation substitution) across layers.

**Faithfulness-causality correlation**: $R = 0.84$ (GPT-J), $R = 0.85$ (GPT2-XL), $R = 0.83$ (LLaMA-13B). The linear approximation is not just descriptive — it's **causally real**. Editing via LRE inverse changes model outputs as predicted.

## Why This Matters for Latent Communication

### 1. Justifies mid-layer communication
The enriched representation finding explains why [[activation-communication-harvard|AC]] (layer 26/32), [[kvcomm-kth-selective|KVComm]] (intermediate layer selection with Gaussian prior), and [[state-delta-trajectory|SDE]] (middle-to-late layers) all find intermediate layers carry the most useful information. That's where the richest relational knowledge lives, before output compression discards it.

### 2. Internal knowledge > expressed knowledge
The attribute lens shows models encode facts they don't output. Latent communication (sharing activations/KV-cache) can transmit knowledge that would **never appear in natural language output** — a fundamental advantage over text-based communication that no amount of prompt engineering can close.

### 3. Linear structure enables simple alignment
If relational knowledge is encoded linearly, cross-model alignment ([[activation-communication-harvard|AC]]'s W, [[kv-cache-alignment-shared-space|KV Cache Alignment]]'s affine transforms, [[vision-wormhole-heterogeneous|Vision Wormhole]]'s affine alignment) is theoretically justified — the representations have the right geometric structure for linear projection.

### 4. But 52% of relations are NOT linear
This heterogeneity means some knowledge requires **deeper, nonlinear** communication. Linear projections may fail on relations with large ranges (company CEOs, person parents). This motivates richer approaches like [[thought-communication-multiagent|ThoughtComm]]'s autoencoder or [[cache-to-cache-semantic-communication|C2C]]'s neural fuser with dynamic head weighting.

### Connection to the Platonic Representation Hypothesis

The linearity findings provide mechanistic evidence for the [[platonic-representation-hypothesis|Platonic Representation Hypothesis]] at the **intra-model** level. PRH claims that different models converge to approximately isometric representations of reality; this paper shows that *within* a single model, relational knowledge is encoded as linear structure in the representation space. These are complementary claims:

- **PRH (inter-model)**: The mapping between Model A's and Model B's representations of the same entity is approximately linear.
- **LRE (intra-model)**: The mapping from a subject representation to its relational attributes within a single model is approximately linear.

Together, they predict that a linear projection from Model A's subject representation should recover relational attributes in Model B's space — exactly the operation performed by [[activation-communication-harvard|AC]]'s mapping matrix $W$ and [[kv-cache-alignment-shared-space|KV Cache Alignment]]'s affine adapters.

The 48%/52% split also refines PRH's predictions. PRH posits convergence toward a shared representation, but this paper shows that convergence is **relation-dependent**. Relations with small, categorical ranges (countries, languages, genders) are linearly encoded and therefore likely to be well-aligned across models. Relations with large, idiosyncratic ranges (company CEOs, person parents) are nonlinearly encoded and may require richer cross-model alignment mechanisms. This suggests that the "platonic representation" is not uniformly accessible — some aspects of shared reality are geometrically simpler than others.

The cross-model consistency result (Spearman $R = 0.85$ between GPT-J and GPT2-XL, $R = 0.71$ with LLaMA-13B) provides direct evidence: the same relations are linear in the same models. This is a non-trivial prediction of PRH — if models converge to similar representations, they should encode the same knowledge with similar geometric structure.

## Limitations

- Only first-token evaluation (coarse for multi-token entities)
- Layer normalization requires ad-hoc $\beta$ correction per model
- Single-state patching for causality — information leaks through earlier attention states
- Hyperparameter sensitivity (per-relation grid search over layer and pseudoinverse rank)
- Template-based prompts only; natural language diversity not captured
- Tested on GPT-J (6B), GPT2-XL (1.5B), LLaMA-13B — no frontier models

## Source Materials

- [[raw/pdf/arxiv-2308.09124.pdf|PDF]] (`raw/latex/arxiv-2308.09124/`)
