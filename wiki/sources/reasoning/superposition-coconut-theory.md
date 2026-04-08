---
type: source
title: "Reasoning by Superposition: A Theoretical Perspective on Chain of Continuous Thought"
source_file: "[[raw/pdf/arxiv-2505.12514.pdf]]"
latex_source: "[[raw/latex/arxiv-2505.12514]]"
author: "Hanlin Zhu, Shibo Hao, Jiantao Jiao, Stuart Russell, Zhiting Hu, Yuandong Tian"
date_published: "2025-05-19"
date_ingested: "2026-04-06"
created: "2026-04-06"
updated: "2026-04-08"
venue: "NeurIPS 2025"
arxiv: "2505.12514"
institution: "UC Berkeley, UC San Diego, Meta AI"
tags: [latent-reasoning, superposition, theoretical, bfs, foundational]
---

# Reasoning by Superposition: A Theoretical Perspective on Chain of Continuous Thought

## Summary

The first rigorous theoretical formalization of **why continuous chain-of-thought ([[coconut-reasoning-latent-space|Coconut]]) outperforms discrete CoT**. Proves that continuous thoughts implement **parallel BFS via superposition** -- each latent vector encodes a normalized uniform mixture of all graph vertices reachable within $c$ steps. A 2-layer transformer with continuous CoT solves directed graph reachability in **$D$ steps** ($D$ = graph diameter), vs. **$O(n^2)$** for discrete CoT -- a quadratic-to-linear improvement.

This paper formalizes the most important finding in our entire research collection and is the theoretical backbone for our [[frontier-research-directions|#1 paradigm-shift direction]].

## Problem Formulation

### Graph Reachability Task

Given a directed graph $\mathcal{G} = (V, E)$ with vertices $V = \{v_1, \ldots, v_n\}$ and edges $E = \{e_1, \ldots, e_m\}$, a root node $s$, and two candidate destinations $t_1, t_2$ (exactly one reachable from $s$), determine which candidate is reachable.

### Input Format

The prompt follows a structured sequence: BOS token, followed by $3m$ tokens representing $m$ edges (each edge as source-target-edge_marker triplet), a query token with two candidates $t_1, t_2$, a reasoning token with root $s$, then $C$ continuous thought steps, and finally an answer token. Total prompt length: $t_0 = 3m + 6$ tokens before thoughts begin.

### Embedding Structure

Token embeddings $u_v \in \R^d$ with $d = O(|V|)$ are partitioned into four subspaces:
- **Content space** ($d_{te}$ dimensions): Stores the token identity via orthonormal embeddings ($U^T U = I_V$)
- **Buffer 1** ($d_{te}$ dimensions): Scratch space for intermediate computations (source nodes)
- **Buffer 2** ($d_{te}$ dimensions): Scratch space for intermediate computations (target nodes)
- **Positional encoding space** ($d_{pe}$ dimensions): Sinusoidal positional encodings

The orthonormality assumption ($\langle u_a, u_b \rangle = \delta_{ab}$) is critical -- it ensures that superpositions of different vertex embeddings are distinguishable and that inner products between a continuous thought and vertex embeddings cleanly measure membership in the reachable set.

### Chain of Continuous Thought

Unlike discrete CoT (which samples a token and feeds back its embedding), continuous CoT skips the sampling step: $h_{t_0+c} = \text{Transformer}_\theta(h_1, \ldots, h_{t_0+c-1})$. The raw output embedding becomes the next input. This preserves the continuous superposition state that would be destroyed by sampling.

## Core Theoretical Results

### Attention Chooser (Lemma 1)

A building block used throughout the construction. Under sinusoidal positional encoding, for any token $x \in V$ and relative position $\ell \geq 0$, there exist query/key matrices $Q, K \in \R^{2d_{pe} \times d}$ such that position $i$ attends to position $i - \ell$ if $h_i = u_x$, and attends to position 1 otherwise.

**Construction:** The query matrix is designed so that:
$$q_i = \begin{bmatrix} \bar{p}_i \\ \xi \langle \tilde{u}_{\bar{x}}, \tilde{h}_i \rangle \bar{p}_1 \end{bmatrix}, \quad k_j = \begin{bmatrix} \eta \bar{p}_{j+\ell} \\ \eta \bar{p}_j \end{bmatrix}$$

where $\tilde{u}_{\bar{x}} = \sum_{v \neq x} \tilde{u}_v$ is the superposition of all tokens except $x$. When $h_i = u_x$, the inner product $\langle \tilde{u}_{\bar{x}}, \tilde{h}_i \rangle = 0$, so attention is governed by positional similarity $\langle \bar{p}_i, \bar{p}_{j+\ell} \rangle$, which is maximized at $j = i - \ell$ by properties of sinusoidal encodings. When $h_i \neq u_x$, the second term dominates and redirects attention to position 1.

This mechanism enables **token-conditioned relative attention** -- the same parameters work for any input length.

### BFS Construction Diagram

> [!diagram|left]
> ```mermaid
> graph TD
>     subgraph Input["Input: Edge Tokens + Root"]
>         EDGES["Edge tokens"]
>         ROOT["Root node"]
>     end
> 
>     subgraph Layer1["Layer 1: Information Gathering (5 heads)"]
>         H0["Head 0-1:<br>Edge tokens attend to<br>source & target nodes"]
>         H2["Head 2-3:<br>Reasoning token attends<br>to candidates"]
>         H4["Head 4:<br>Answer token attends<br>to current thought"]
>     end
> 
>     subgraph Layer2["Layer 2: BFS Expansion (1 head)"]
>         ATT["Attention: current thought<br>queries edge tokens where<br>inner product > 0"]
>         RETRIEVE["Retrieve targets of<br>edges with source in<br>visited set"]
>     end
> 
>     subgraph MLP["MLP: Signal Filter"]
>         THRESH["Threshold + LayerNorm<br>→ clean uniform superposition"]
>     end
> 
>     subgraph Output["Output: Updated Superposition"]
>         TC["Normalized superposition<br>of all vertices in<br>next visited set"]
>     end
> 
>     EDGES --> H0
>     ROOT --> H2
>     H0 --> ATT
>     H2 --> ATT
>     H4 --> ATT
>     ATT --> RETRIEVE
>     RETRIEVE --> THRESH
>     THRESH --> TC
>     TC -.->|"feeds back as<br>next thought"| ATT
> 
>     style Input fill:#dae8fc,stroke:#6c8ebf
>     style Layer1 fill:#fff2cc,stroke:#d6b656
>     style Layer2 fill:#ffe6cc,stroke:#d79b00
>     style MLP fill:#f8cecc,stroke:#b85450
>     style Output fill:#d5e8d4,stroke:#82b366
> ```

> [!notation|right]
> | Component | Notation |
> |---|---|
> | Edge tokens | $e_1, \ldots, e_m$ |
> | Root node | $s$, with $t_0 = u_s$ |
> | Candidates | $t_1, t_2$ |
> | Current thought | $t_c$ (superposition over $V_c$) |
> | Visited set | $V_c$ |
> | Next thought | $t_{c+1}$ (superposition over $V_{c+1}$) |

### Lemma 2: Continuous Thought Maintains Superposition States

The central result. Define $V_c$ as the set of vertices reachable from $s$ within $c$ steps.

**Lemma 2.** There exists a construction of a two-layer transformer such that:
$$t_c = h_{t_0+c} = \frac{1}{\sqrt{|V_c|}} \sum_{v \in V_c} u_v$$

The $c$-th continuous thought is the **normalized superposition** of all vertices reachable within $c$ steps -- literally encoding the complete BFS frontier at step $c$.

**Proof by induction:**

*Base case ($c = 0$):* $V_0 = \{s\}$ and $t_0 = u_s = \frac{1}{\sqrt{|V_0|}} \sum_{v \in V_0} u_v$. Trivially satisfied.

*Inductive step:* Assuming the superposition holds for steps $0, \ldots, c$, the two-layer transformer produces the superposition for step $c+1$:

**First layer (5 attention heads):** Each head is an attention chooser:
- $h_0 = (\text{edge\_token}, 2)$: Edge tokens attend to their source node (2 positions back)
- $h_1 = (\text{edge\_token}, 1)$: Edge tokens attend to their target node (1 position back)
- $h_2 = (\text{reasoning}, 2)$: Reasoning token attends to second candidate
- $h_3 = (\text{reasoning}, 1)$: Reasoning token attends to first candidate
- $h_4 = (\text{answer}, 1)$: Answer token attends to the current thought

After Layer 1, each edge token $\langle e \rangle$ has its source node in Buffer 1 and target node in Buffer 2. This is the **information gathering** step -- it distributes edge endpoint information to the edge marker positions.

**Second layer (1 attention head):** The current continuous thought $t_c$ (a superposition of $V_c$) attends to all edge tokens. The query-key construction ensures:
$$\langle q_{t_c}, k_{\langle e_i \rangle} \rangle \propto \langle t_c, u_{s_i} \rangle$$

Since $t_c$ is a superposition of $V_c$, this inner product is positive if and only if $s_i \in V_c$ (because embeddings are orthonormal). The attention therefore concentrates on edges whose source is in the current reachable set, and retrieves their targets from Buffer 2. This is exactly **one BFS expansion step**: $V_{c+1} = V_c \cup \{v : \exists u \in V_c, (u,v) \in E\}$.

**MLP as signal filter:** After the attention layer, the raw superposition has non-uniform weights and noise (since softmax attention scores are never exactly zero). The MLP implements a threshold-and-equalize operation:

For a superposition $h = \sum_{v} \lambda_v u_v$, setting $W_1 = [u_1, \ldots, u_V]^T$ (rotating to standard basis), applying a threshold nonlinearity $\sigma(x) = \mathbb{1}\{x \geq \varepsilon\}$ coordinate-wise, and setting $W_2 = W_1^T$ (rotating back) produces $\sum_v \mathbb{1}\{\lambda_v \geq \varepsilon\} u_v$. After **layer normalization**, this yields the clean uniform superposition $\frac{1}{\sqrt{|V_{c+1}|}} \sum_{v \in V_{c+1}} u_v$.

### Theorem 1: Main Result

**Theorem 1.** Fix $T_{\max} > 0$. There exists a two-layer transformer with parameters $\theta$ and readout matrix $W_{\text{read}} \in \R^{|V| \times d}$ (where $d = O(|V|)$), both independent of the specific graph, such that for any directed graph with at most $n_{\max}$ nodes, root $s$, and candidates $t_1, t_2$, for any $C$ exceeding the graph diameter $D$, the model correctly outputs the reachable candidate.

**Prediction mechanism.** The answer token "measures" the superposition state $t_C$ by computing inner products with the candidate embeddings $u_{t_1}$ and $u_{t_2}$. Since the reachable candidate is in the superposition (positive inner product) and the unreachable one is not (approximately zero inner product), argmax over the readout scores identifies the correct answer.

### The Quantum Mechanics Analogy (Made Precise)

| Property | Continuous CoT | Discrete CoT |
|----------|---------------|-------------|
| Thought state | **Superposition** (weighted sum of multiple vertex embeddings) | **Collapsed** (single sampled token) |
| Search strategy | **Parallel BFS** (all frontier nodes expanded simultaneously) | **Sequential DFS/greedy** (one path at a time) |
| Complexity | $D$ steps (graph diameter) | $O(n^2)$ steps (best known, Merrill & Sabharwal 2023) |
| Final answer | **Measurement** (answer token projects superposition onto candidates) | Direct output |

The analogy is explicit and precise: continuous thoughts are superposition states, token sampling is measurement/collapse, and the answer token performs a projective measurement.

### Role of Buffer Spaces

The buffer subspaces store intermediate information (source/target of edges) without interfering with the content space used for superposition. In practice, these could be jointly projected into a lower-dimensional space using (approximately) orthogonal rotations $R^{(i)} \in \R^{d \times d}$, where each rotation's column space forms a subspace. Different subspaces need only be approximately orthogonal, and within each subspace, vectors need only be approximately orthonormal.

### Compatibility with RoPE

The paper also provides a construction using Rotary Positional Embeddings (RoPE), demonstrating the results are not specific to sinusoidal encodings. The attention chooser mechanism works with RoPE by exploiting the rotation property: $\text{RoPE}(q, i)^T \text{RoPE}(k, j)$ depends only on relative position $i - j$.

## Empirical Validation

### Training Setup

- **Model**: GPT-2 style decoder, 2 layers, $d_{\text{model}} = 768$, $n_{\text{heads}} = 8$, trained from scratch
- **Dataset**: ProsQA (subset requiring 3-4 reasoning hops), from Hao et al. (2024)
  - Train: 14,785 problems, avg $|V| = 22.8$, avg $|E| = 36.5$, avg solution length 3.5
  - Val: 257 problems; Test: 419 problems
- **Training**: AdamW ($\beta_1 = 0.9$, $\beta_2 = 0.95$, weight decay $10^{-2}$), constant lr $= 10^{-4}$, multi-stage curriculum (stage $i$ trains with $i$ continuous thoughts), 25 epochs per stage, 300 epochs total
- **Compute**: ~24 hours on 2 NVIDIA A100 80GB GPUs

### Overall Accuracy

| Method | Accuracy |
|--------|----------|
| No CoT (2-layer) | ~75% |
| CoT (2-layer) | ~75% |
| CoT* (12-layer, 12 heads) | ~83% |
| **Coconut (2-layer)** | **~99%** |

A 2-layer Coconut model achieves near-perfect accuracy on ProsQA while both CoT baselines (including a much larger 12-layer model) fail to reliably solve the task. Random guessing baseline is 50%.

### Layer 1 Attention Patterns

Attention maps confirm the theoretical construction: edge tokens $\langle e \rangle$ attend almost exclusively to their source and target nodes, placing nearly all attention mass on exactly the predicted positions. This validates that the model has learned the information-gathering mechanism from the construction.

### Layer 2 Attention Scores by Edge Category

| Edge Category | Step 1 | Step 2 | Step 3 | Step 4 |
|---------------|--------|--------|--------|--------|
| **Not Reachable** | 0.04 $\pm$ 0.07 | 0.03 $\pm$ 0.09 | 0.08 $\pm$ 0.17 | 0.12 $\pm$ 0.20 |
| **Reachable** | 2.12 $\pm$ 1.07 | 0.71 $\pm$ 0.92 | 0.38 $\pm$ 0.72 | 0.29 $\pm$ 0.66 |
| **-- Frontier** | 2.12 $\pm$ 1.07 | 1.00 $\pm$ 0.96 | 0.67 $\pm$ 0.87 | 0.61 $\pm$ 0.95 |
| **-- Optimal** | 2.54 $\pm$ 1.03 | 1.72 $\pm$ 1.13 | 1.67 $\pm$ 1.20 | 2.23 $\pm$ 1.35 |

The model sharply concentrates attention on **Reachable** edges (mean score ~2.12 vs ~0.04 for Not Reachable at step 1), exactly as the theory predicts. Additional biases toward **Frontier** and **Optimal** edges emerge from training signals.

### Representation Analysis (Inner Products)

Inner products between continuous thought vectors $t_i$ and node embeddings $u_v$ show clear hierarchical separation across 3 random seeds:

| Node Category | Step 1 | Step 2 | Step 3 | Step 4 |
|---------------|--------|--------|--------|--------|
| **Not Reachable** | -0.37 to -0.25 | -0.26 to -0.04 | -0.09 to 0.02 | -0.27 to -0.23 |
| **Reachable** | 3.59 to 3.71 | 1.37 to 1.55 | 0.62 to 0.80 | 0.53 to 0.66 |
| **-- Frontier** | 5.09 to 5.38 | 2.45 to 2.69 | 1.95 to 2.11 | 2.12 to 2.29 |
| **-- Optimal** | 6.41 to 6.84 | 4.67 to 5.11 | 5.44 to 6.43 | 8.98 to 9.58 |

The separation pattern (Not Reachable $\ll$ Reachable $<$ Frontier $<$ Optimal) is consistent across all 3 runs, confirming the superposition representation is a stable, reproducible phenomenon.

### BFS Emerges Without Multi-Path Supervision

**COCONUT-BFS experiment.** When training supervision is drawn uniformly from frontier nodes (not just the optimal path), the model achieves the same near-perfect accuracy. Crucially, comparing inner product distributions between standard Coconut and Coconut-BFS reveals:

- **Coconut-BFS** learns expected BFS behavior (uniform attention to frontier nodes)
- **Standard Coconut** (trained only on optimal paths) **still** assigns elevated weight to non-optimal frontier nodes compared to non-frontier reachable nodes

This means **BFS emerges from training dynamics, not from explicit supervision**. The model discovers that parallel frontier exploration is the efficient algorithm for reachability, even when training data only shows single optimal paths.

## Implications

1. **[[continuous-vs-discrete-representation|Continuous]] latent reasoning is provably more efficient** than discrete CoT for graph-structured problems: $D$ steps vs $O(n^2)$, potentially exponential gap for sparse graphs (where $D$ can be $O(\log n)$ while $n^2$ remains quadratic).

2. **Superposition is a computational mechanism**, not just a metaphor -- the quantum analogy is mathematically precise. Each continuous thought literally encodes a probability distribution over reachable states.

3. **2-layer continuous CoT outperforms 12-layer discrete CoT** on graph reachability -- latent reasoning substitutes for model depth, confirming and extending the depth-expressivity connection from [[cot-expressivity-theory|Feng et al. (2023)]].

4. **Many reasoning problems** (planning, knowledge graphs, multi-hop QA) reduce to graph reachability, so the superposition advantage may generalize broadly.

5. **BFS emerges without explicit supervision** -- models discover efficient algorithms never demonstrated in training data, suggesting that continuous thought representations have an inductive bias toward parallel search strategies.

## Limitations

- **No proven lower bound for discrete CoT**: The gap is between an upper bound ($D$ for continuous) and a best-known result ($O(n^2)$ for discrete), not a proven separation. It remains possible that discrete CoT could solve reachability in fewer steps with a clever construction.
- **Only graph reachability**: General reasoning tasks are not addressed. The theory applies cleanly to problems with graph structure but extensions to natural language reasoning are speculative.
- **Constructive proof, not a learning theory result**: No proof that gradient descent converges to these solutions. The experiments show it does empirically on small models, but scaling behavior is unknown.
- **Linear embedding dimension** $O(|V|)$: Real models have $d \ll |V|$. In practice, the orthonormality assumption is only approximate, and superpositions would interfere. The paper acknowledges this but notes buffer spaces can share dimensions via approximate orthogonality.
- **GPT-2 scale experiments only**: All experiments use a small 2-layer model trained from scratch on synthetic data. Whether frontier LLMs exhibit similar superposition behavior is untested.

## Connection to Our Research Directions

This paper is the theoretical foundation for [[frontier-research-directions|direction #1 (superposition reasoning at frontier scale)]] and [[frontier-research-directions|direction #2 (disentangling superposed paths)]]. If [[latentcompress-open-call|LatentCompress]]'s slot-attention compression naturally disentangles these superposition states into individual slots, it would connect compression research to this theory directly -- each slot might correspond to one BFS frontier vertex.

The relationship to [[cot-expressivity-theory|Feng et al.]] is complementary: Feng et al. prove CoT adds **depth** (breaking the $\text{TC}^0$ barrier); Zhu et al. prove continuous CoT additionally exploits **width** (superposition). Together they explain why continuous thoughts outperform discrete CoT on planning tasks -- continuous thoughts leverage both depth (through recurrence) and width (through superposition) simultaneously.

## Empirical Counterpart: Cui et al. (2026)

[[latent-reasoning-supervision-analysis|Cui et al. (2026)]] provides the **empirical bracket** for Zhu et al.'s theory, separating two claims that the literature conflated:

| Claim | Source | Status |
|---|---|---|
| Latent vectors *can* encode normalized mixtures over the reachable set $V_c$ (see [[#Core Theoretical Results]]) | Zhu et al. (this paper) — proven by construction | **Confirmed** |
| The iterative latent process *does* expand the BFS frontier across steps | Implicit in Coconut's narrative | **Falsified** by Cui et al.'s diversity analysis (distinct outcomes *decrease* with depth) |
| The process *amplifies* the correct candidate before final readout | Implied | **Falsified** — Cui et al. find majority-vote accuracy 3-4 points below explicit reasoning |

The synthesis: Zhu et al.'s theoretical construction is achievable in **representational capacity** (a single continuous thought can be a uniform mixture over the reachable set), but the **gradient-based optimization process** of practically-trained latent reasoning models (Coconut, CODI, SIM-CoT, CoLaR) actively prunes that mixture as latent steps progress. The 2-layer, trained-from-scratch GPT-2 in Zhu et al.'s experiments demonstrates the achievable maximum; the practical methods Cui et al. test fall well short of it.

This is **not** a refutation of Zhu et al. — the construction stands and the capacity claim is independently confirmed by Cui et al.'s Pass@100 analysis. But it does mean the **realizable** advantage of latent reasoning over explicit CoT is much smaller than the construction suggests, and that closing the gap requires new training schemes, not just larger models. See the [[contradictions|contradictions analysis]] for the full discussion.

## Source Materials

- [[raw/pdf/arxiv-2505.12514.pdf|PDF]] ([[raw/latex/arxiv-2505.12514|LaTeX source]])
