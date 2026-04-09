### Impossibility Without CoT (Theorems 3.1 and 3.2)

**Theorem 3.1 (Arithmetic).** Assume $\text{TC}^0 \neq \text{NC}^1$. For any prime $p$, any integer depth $L$, and any polynomial $Q$, there exists a problem size $n$ such that no log-precision autoregressive transformer with depth $L$ and hidden dimension $d \leq Q(n)$ can solve $\text{Arithmetic}(n, p)$.

**Theorem 3.2 (Equations).** Under the same assumption, for any prime $p$, depth $L$, and polynomial $Q$, there exists $m$ such that no log-precision transformer with depth $L$ and $d \leq Q(m)$ can solve $\text{Equation}(m, p)$.

**Proof strategy.** The proofs establish that both problems are $\text{NC}^1$-hard via reductions from known $\text{NC}^1$-complete problems. Merrill & Sabharwal (2023) showed that bounded-depth log-precision transformers of polynomial size can be simulated by $\text{TC}^0$ circuits. Since $\text{TC}^0 \subsetneq \text{NC}^1$ (under the assumption), the transformers provably lack the circuit depth to solve these problems. The bottleneck is fundamentally **parallel complexity** -- these tasks require $\Omega(\log n)$ sequential computational steps that cannot be parallelized into constant depth, regardless of how wide the model is.

**Problem formulations.** Both tasks operate over finite fields $\mathbb{F}_p$ (integers modulo a prime $p$), which simplifies the analysis by ensuring all numbers are tokens in a bounded dictionary. $\text{Arithmetic}(n, p)$ asks the model to evaluate arithmetic expressions (with $+, -, \times, \div$ and brackets) of input length up to $n$. $\text{Equation}(m, p)$ asks the model to solve systems of $m$ linear equations in $m$ variables.

### Sufficiency With CoT (Theorems 3.3 and 3.4)

**Theorem 3.3 (Arithmetic with CoT).** Fix any prime $p$. For any $n > 0$, there exists an autoregressive transformer with constant hidden size $d = O(\text{poly}(p))$ (independent of $n$), depth $L = 5$, and 5 heads per layer that generates the CoT solution for all inputs in $\text{Arithmetic}(n, p)$. All parameter values are bounded by $O(\text{poly}(n))$.

**Theorem 3.4 (Equations with CoT).** Fix any prime $p$. For any $m > 0$, there exists an autoregressive transformer with constant hidden size $d$ (independent of $m$), depth $L = 4$, and 5 heads per layer that generates the CoT solution for all inputs in $\text{Equation}(m, p)$.

The polynomial parameter bound ensures these constructions are implementable in log-precision without loss of accuracy.

### Construction Details for the Depth-5 Arithmetic Transformer

The constructive proof of Theorem 3.3 is the paper's most technically detailed result. It builds on a set of fundamental operations implementable by transformer components:

**Attention-level primitives:**
- **Conditional COPY** (Lemma B.1): A softmax attention head can extract the content of the unique previous position satisfying certain conditions. Achieved by constructing $Q, K, V$ matrices so that the dot-product score is zero for exactly the target position and negative elsewhere.
- **Conditional MEAN** (Lemma B.2): A softmax attention head can average values over all positions satisfying a condition -- a "scatter" operation in parallel computing.

**MLP-level primitives:**
- **Multiplication** (Lemma B.3): A 2-layer MLP with GeLU activation and hidden dimension 4 approximates scalar multiplication $f(a,b) \approx ab$ within error $\epsilon$, with weights bounded by $O(\text{poly}(M, 1/\epsilon))$. The construction uses the identity $ab = \frac{1}{4}[(a+b)^2 - (a-b)^2]$, approximated via GeLU's Taylor expansion.
- **Conditional selection** (Lemma B.4): A 2-layer MLP selects between two values based on a threshold condition.
- **Lookup table** (Lemma B.5): A 2-layer MLP with $d^k$ hidden units implements any $k$-dimensional lookup table over a discrete domain of size $d$.

**Layer-by-layer construction:**

| Layer | Purpose | Mechanism |
|-------|---------|-----------|
| **Layer 1** | Count equal signs, find position of last `=`, compute $i^2$ | MEAN head counts `=` frequency; COPY head retrieves last `=` position; MLP computes products |
| **Layer 2** | Compute distances to nearest/last `=`, count strictly-previous `=`, compute squared quantities | COPY from position $i-1$; MLP computes $(n^=)^2$, $(d^=)^2$ |
| **Layer 3** | Extract 5 context tokens from previous CoT step; determine if calculation needed | 5 parallel COPY heads with dot-product scores $-(n^= - \hat{n}^= - 1)^2 - (d^= - \hat{d}^= + t)^2$ ensuring unique retrieval; MLP implements arithmetic lookup table |
| **Layer 4-5** | Generate output: copy token, perform calculation, or emit result | Conditional selection between copy/compute modes; final lookup table for $+, -, \times, \div$ |

The key insight is that the CoT format reduces each generation step to examining a **fixed-size context window** (5 tokens from the previous derivation step), enabling a constant-size model to handle arbitrarily long expressions.

### Generalization to Dynamic Programming (Theorem 4.7)

**Theorem 4.7.** Consider any DP problem satisfying Assumptions 4.1-4.4. For any integer $n$, there exists an autoregressive transformer with constant depth $L$, hidden dimension $d$, and attention heads $H$ (all independent of $n$) that correctly generates the CoT solution for all input sequences of length up to $n$.

The DP framework is characterized by three ingredients:
- **State space** $\mathcal{I}_n \subset \mathcal{I}$: The finite set of subproblems, with a partial order (DAG) defining dependencies.
- **Transition function** $T$: $\text{dp}(i) = f(n, i, s_{g(n,i)}, \text{dp}(h(n,i)))$ -- each state depends on a constant number of input tokens ($J$) and previous states ($K$).
- **Aggregation function** $A$: Combines results, e.g., $\min$, $\max$, $\sum$ over a subset of states.

**Assumptions** (all verified for LIS, ED, and CFG problems):
1. $|\mathcal{I}_n| = O(\text{poly}(|s|))$ -- polynomial state space
2. Functions $f, g, h, u$ are approximable by constant-size GeLU MLPs with polynomial efficiency
3. The topological ordering function is similarly approximable
4. The aggregation indicator function is similarly approximable

**Impossibility complement (Theorem 4.8).** Context-Free Grammar (CFG) Membership Testing -- a $\text{P}$-complete DP problem -- cannot be solved by bounded-depth polynomial-size transformers without CoT (under $\text{TC}^0 \neq \text{NC}^1$). This establishes that CoT enables transformers to solve problems up to $\text{P}$-completeness, a dramatic jump from $\text{TC}^0$.

**DP examples analyzed:**

| Problem | State Space | Transition | Aggregation |
|---------|-------------|-----------|-------------|
| **LIS** (Longest Increasing Subsequence) | $(j, k)$ for $j \in [n], k \in \{0, \ldots, j-1\}$ | $\text{dp}(j,k) = \max(\text{dp}(j,k-1), \text{dp}(k,k-1) \cdot \mathbb{I}[s_j > s_k] + 1)$ | $\max_i \text{dp}(i, i-1)$ |
| **ED** (Edit Distance) | $(j, k) \in \{0,\ldots,n_1\} \times \{0,\ldots,n_2\}$ | $\min(\text{dp}(j,k-1)+a, \text{dp}(j-1,k)+b, \text{dp}(j-1,k-1)+c\mathbb{I}[s^{(1)}_j \neq s^{(2)}_k])$ | $\text{dp}(n_1, n_2)$ |

### RNN Impossibility

An important negative result: **constant-size RNNs cannot solve** any of these tasks with CoT, even given the same CoT format. The bottleneck is that RNNs lack attention's ability to **selectively retrieve** arbitrary previous intermediate results. The hidden state of an RNN can only carry a constant amount of information, while attention can access any position in the context. This distinction is critical for latent reasoning architectures.
