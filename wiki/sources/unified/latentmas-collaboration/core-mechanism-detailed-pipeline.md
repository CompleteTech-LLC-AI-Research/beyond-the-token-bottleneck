> [!diagram|left]
> ```mermaid
> graph LR
>     subgraph AgentI["Current Agent (e.g. Planner)"]
>         FWD["**Forward Pass**<br>Input through N layers<br>to last-layer hidden state"]
>         ALN["**Alignment**<br>Ridge regression<br>d×d matrix"]
>         LAT["**Latent Thoughts**<br>K steps (40-80)<br>Feed aligned state back<br>No decoding/softmax"]
>     end
>     KV["**Extract Working Memory**<br>All N layers: KV caches<br>T input + K latent positions"]
>     subgraph AgentNext["Next Agent (e.g. Critic)"]
>         PRE["**KV Prepend**<br>Prepend predecessor caches<br>at every layer<br>via past_key_values"]
>         GEN["**Generate**<br>Latent thoughts<br>or final text"]
>     end
> 
>     FWD -->|"hidden state"| ALN -->|"aligned state"| LAT -->|"KV caches"| KV -->|"working memory"| PRE --> GEN
>     LAT -.->|"repeat K times"| FWD
> 
>     style AgentI fill:#dae8fc,stroke:#6c8ebf
>     style AgentNext fill:#f5f5f5,stroke:#666666
>     style KV fill:#ffe6cc,stroke:#d79b00
> ```

> [!notation|right]
> | Step | Notation |
> |---|---|
> | Current Agent | $A_i$ |
> | Next Agent | $A_{i+1}$ |
> | Last-layer hidden state | $h_T$ |
> | Alignment matrix | $M$ |
> | Aligned hidden state | $h'_T = M \cdot h_T$ |
> | Working memory of agent | $\M_i$ |
> | KV caches at layer $l$ | $(K_\text{cache}^{(l)}, V_\text{cache}^{(l)})$ |

### Step 1 — Latent Thought Generation

Each agent generates K latent steps via auto-regressive hidden-state recurrence:

1. **Forward pass**: Given input embeddings $X = [x_1, \ldots, x_T]$, the agent runs all $N$ transformer layers to produce last-layer hidden state $h_T$.
2. **Alignment**: Apply the alignment matrix $M$ to produce $h'_T = M h_T$, mapping the output-space vector back into a valid input-space embedding.
3. **Feedback loop**: Insert $h'_T$ as the input embedding for position $T+1$ (replacing normal token-embedding lookup). No decoding, no softmax, no vocabulary projection.
4. **Repeat**: Run the full transformer forward pass again with the extended sequence $[x_1, \ldots, x_T, h'_T]$ to produce $h_{T+1}$. Apply $M$, feed back. Repeat for $K$ total latent steps.
5. **Result**: A sequence of $K$ new hidden states $\Theta = [h_{T+1}, h_{T+2}, \ldots, h_{T+K}]$ — the agent's "latent thoughts."

The number of latent steps $K$ is a hyperparameter drawn from $\{0, 10, 20, 40, 80\}$. No stopping condition is learned — $K$ is fixed per run.

### Step 2 — Input-Output Alignment Matrix M

Since last-layer hidden states live in the output embedding space (high-level, abstract) and input embeddings live in the token embedding space (shallow, distributional), directly feeding $h$ back as input causes **out-of-distribution activations**. $M$ bridges this gap.

**Formula**: $M$ approximates the pseudo-inverse mapping from output to input space:

> $M \approx W_\text{out}^{-1} W_\text{in}$

Since $W_\text{out}$ is non-square ($d \times |V|$), the true inverse does not exist. In practice $M$ is computed via **ridge regression**:

> $M = (W_\text{out}^\top W_\text{out} + \lambda I)^{-1} W_\text{out}^\top W_\text{in}$

This solves: $\min_M \{ \|W_\text{out} M - W_\text{in}\|_F^2 + \lambda\|M\|_F^2 \}$

**Key properties**:
- $M$ is a **$d \times d$ matrix** (e.g., $d=1024$ for Qwen3-0.6B). Small and cheap.
- Computed **once per model** and reused for all latent steps and all queries.
- $\lambda > 0$ is a small regularization hyperparameter for numerical stability (exact value not specified in paper).
- Computational cost: polynomial in $d$ — negligible relative to inference.

**Theoretical justification** (Theorem A.1): For any non-singular $M$, the Wasserstein distance between the aligned embedding distribution and the true token embedding distribution is upper-bounded by $\|W_\text{out} M - W_\text{in}\|_F$. The ridge regression solution minimizes this upper bound.

### Step 3 — Working Memory Transfer (KV-Cache Concatenation)

After agent $A_i$ completes $K$ latent steps, its working memory is extracted and passed to $A_{i+1}$:

1. **Extract**: Collect KV caches from **all $N$ transformer layers** of $A_i$. For layer $l$, this gives $K_\text{cache}^{(l)}$ and $V_\text{cache}^{(l)}$, each containing $T+K$ column vectors ($T$ from original input, $K$ from latent thoughts).
2. **Define working memory**: $\M_i = \{(K_\text{cache}^{(l)}, V_\text{cache}^{(l)}) \mid l = 1, 2, \ldots, N\}$. This captures both the original input context AND the generated latent thoughts — unlike [[cache-to-cache-semantic-communication|C2C]] and [[kvcomm-kth-selective|KVComm]] which share only input-derived KV caches.
3. **Prepend**: For each layer $l$ of agent $A_{i+1}$, prepend $A_i$'s $K_\text{cache}^{(l)}$ and $V_\text{cache}^{(l)}$ to $A_{i+1}$'s own caches. This is done via the `past_key_values` interface in HuggingFace Transformers.
4. **Conditioning**: When $A_{i+1}$ now generates (either latent thoughts or final text), its attention at every layer attends over both the predecessor's full working memory and its own representations.

**Positional encodings**: The paper does not explicitly discuss positional encoding adjustment during KV-cache concatenation. The prepending operation places predecessor KV entries before the successor's own entries in the sequence dimension, implying the predecessor's positional encodings are preserved as-is from their original computation.

**Information preservation** (Theorem 3.3): The outputs of an agent receiving latent working memory via KV-cache transfer are provably equivalent to what it would produce if the predecessor's full output were directly re-encoded as input. Proof is by induction over transformer layers — if keys and values are identical, attention outputs are identical, so the full forward pass is identical.
