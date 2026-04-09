Three lightweight modules augment a **frozen backbone LLM** (the backbone parameters are not updated):

### 1. Thinking Block (T)

A single-layer causal transformer decoder, initialized from the LLM's last layer. Autoregressively generates natural-language reasoning tokens from deep-layer representations. If no reasoning is needed for a given chunk, produces only an EOS token. The lightweight design ensures that thought generation is substantially faster than standard autoregressive decoding through the full backbone.

### 2. Compression Block (C)

A single-layer transformer encoder with a pooling layer, initialized from the LLM's first layer. Maps variable-length thought sequences into a fixed-size state $S \in \R^{c \times d}$, where $c$ is the chunk size and $d$ is the hidden dimension. The pooling operation ensures that thoughts of any length compress to the same-dimensional state, maintaining a fixed context size regardless of reasoning complexity.

### 3. Deep-to-Shallow Recurrence

The key architectural innovation. Thoughts are extracted from a **deep layer** (layer 26 of 28 in Qwen2.5-1.5B) and injected at a **shallow layer** (layer 1). This gives the compressed state maximum processing depth through the LLM backbone -- nearly all 27 layers process the reasoning state before the next chunk arrives. The design philosophy: let the heavyweight backbone do the computational work, while the lightweight modules handle thought generation and compression.

### Processing Loop (Diagram)

> [!diagram|left]
> ```mermaid
> graph LR
>     subgraph Input["Input Processing"]
>         X["Chunk tokens"]
>         S["State from previous chunk"]
>     end
> 
>     subgraph Processing["Backbone Forward Pass"]
>         INJ["1. Inject State<br>(additive, layer 1)"]
>         FWD["2. Forward Pass<br>(extract at layer 26)"]
>     end
> 
>     subgraph ThoughtGen["Thought Generation"]
>         THINK["3. Thinking Block<br>(NL thought tokens)"]
>         COMP["4. Compression Block<br>(fixed-size state)"]
>     end
> 
>     subgraph Output["Next Iteration"]
>         NEXT["5. Repeat for next chunk"]
>     end
> 
>     X --> INJ
>     S --> INJ
>     INJ --> FWD
>     FWD --> THINK
>     THINK --> COMP
>     COMP --> NEXT
>     NEXT -.->|"State feeds back"| S
> 
>     style Input fill:#dae8fc,stroke:#6c8ebf
>     style Processing fill:#fff2cc,stroke:#d6b656
>     style ThoughtGen fill:#d5e8d4,stroke:#82b366
>     style Output fill:#e1d5e7,stroke:#9673a6
> ```

> [!notation|right]
> | Step | Notation |
> |---|---|
> | Chunk tokens | $X_i$ ($c$ tokens) |
> | State from previous chunk | $S_i$ |
> | Inject State | $\tilde{X}_i = X_i + S_i$ |
> | Forward Pass | $H_i = M_\theta(\tilde{X}_i)$ |
> | Thinking Block | $Z_{i+1} = T(H_i)$ |
> | Compression Block | $S_{i+1} = C(Z_{i+1})$ |
> | Next chunk | $X_{i+1}$ |
> | State feedback | $S_{i+1}$ feeds back |

### Processing Loop (Formal)

Input is partitioned into $K$ non-overlapping chunks of size $c$ (e.g., 8 tokens): $X_1, \ldots, X_K$ where each $X_i \in \R^{c \times d}$.

At each step $i$:

1. **Inject state**: $\tilde{X}_i = X_i + S_i$ (additive injection at layer $L^{in} = 1$)
2. **Forward pass**: $H_i^{out} = M_\theta(\tilde{X}_i | \tilde{X}_{<i})$ (extract representations at layer $L^{out} = 26$, past chunks accessed via KV-cache)
3. **Generate thought**: $Z_{i+1} = T(H_i^{out})$ (Thinking Block produces variable-length NL thought)
4. **Compress thought**: $S_{i+1} = C(Z_{i+1}) \in \R^{c \times d}$ (Compression Block maps to fixed-size state)
5. Repeat for next chunk. Initial state: $S_1 = \mathbf{0}$.

Since the thought tokens are never appended to the backbone's context window, the **context length remains fixed** -- no context extension occurs regardless of how many reasoning steps are generated.
