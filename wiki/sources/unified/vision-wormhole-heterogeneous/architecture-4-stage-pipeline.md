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
