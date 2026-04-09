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
