### Hidden-State Feedback Loop ([[coconut-reasoning-latent-space|Coconut]])

The approach introduced by [[coconut-reasoning-latent-space|Coconut (Hao et al., 2024)]]:

> [!diagram|left]
> ```mermaid
> graph LR
>     A["Input"] --> B["Transformer"]
>     B --> C["Last hidden state"]
>     C -->|"fed back as<br>input embedding"| D["Transformer"]
>     D --> E["Next hidden state"]
>     E -->|"..."| F["..."]
> 
>     style A fill:#dae8fc,stroke:#6c8ebf
>     style B fill:#dae8fc,stroke:#6c8ebf
>     style C fill:#fff2cc,stroke:#d6b656
>     style D fill:#dae8fc,stroke:#6c8ebf
>     style E fill:#d5e8d4,stroke:#82b366
>     style F fill:#d5e8d4,stroke:#82b366
> ```

> [!notation|right]
> | Step | Notation |
> |---|---|
> | Last hidden state | $h(t)$ |
> | Next hidden state | $h(t+1)$ |
> | Feedback | $h(t)$ fed back as input embedding |

Each "continuous thought" is a $d$-dimensional vector (the last hidden state after layer norm) that is directly used as the next input embedding. Special tokens `<bot>` / `<eot>` bracket the latent mode. The model can switch between language and latent reasoning within a single inference pass.

**Key properties**:
- Each continuous thought requires a **full forward pass** through the transformer stack, so it adds effective depth (consistent with the theoretical analysis that CoT increases transformer expressivity by looping outputs back).
- The hidden state is processed by the **final layer norm** before feedback, keeping magnitudes in a reasonable range for the embedding layer to process.
- During training, the loss is computed only on language tokens — continuous thoughts are **unsupervised**. They are not trained to compress the language reasoning they replace, but to facilitate prediction of future tokens.

### Externalized Soft Thoughts ([[softcot-efficient-reasoning|SoftCoT]])

[[softcot-efficient-reasoning|SoftCoT (Xu et al., 2025)]] addresses a critical problem: Coconut's hidden-state feedback loop requires training the backbone LLM, which causes **[[catastrophic-forgetting]]** on instruction-tuned models (LLaMA-3.1-8B-Instruct drops from 79.61% to 76.12% on GSM8K when adapted with Coconut+LoRA). SoftCoT externalizes the continuous reasoning to a small frozen **assistant model** (e.g., 0.5B), whose hidden states are projected into the backbone's embedding space via a learned linear layer. The backbone remains completely frozen ([[raw/pdf/arxiv-2502.12134.pdf|SoftCoT Table 1]]).

**Key properties**:
- Only the projection layer is trained — the backbone never changes
- Soft thought tokens are ~**4× more information-dense** than discrete tokens (6 soft tokens $\approx$ 24 hard tokens)
- Assistant model size barely matters (0.5B nearly matches 7B)
- Soft thoughts **augment** standard CoT rather than replacing it — the LLM still generates a full discrete reasoning chain

### Supervised Compressed Thoughts ([[thinking-states-latent-reasoning|Thinking States]])

[[thinking-states-latent-reasoning|Thinking States (Amos et al., 2026)]] combines discrete and continuous reasoning: generate **natural-language thoughts** at chunk boundaries during input processing, then **compress** them into fixed-size continuous states injected at a shallow layer. This bridges the supervision problem (thoughts are supervisable because they're NL) with the compactness advantage (states are continuous).

**Key properties**:
- **Deep-to-shallow recurrence**: Thoughts extracted from layer 26 (of 28), injected at layer 1 — gives the compressed state maximum processing depth through the backbone ([[raw/pdf/arxiv-2602.08332.pdf|Thinking States §3]])
- **Teacher forcing**: Because ground-truth thoughts are available, all chunks process in a single parallel forward pass. No BPTT needed — training cost is **constant** regardless of recurrence depth (vs. Coconut's linear scaling)
- Matches CoT on 2-Hop QA (54.91% vs 54.79%) with 1.19× speedup; dramatically outperforms CoT on length generalization (Parity: 100% vs 64.38%)
- **State ambiguity**: When the question appears at the end of the input, the model may reason about the wrong intermediate quantity before seeing what's asked

### Multi-Agent Latent Reasoning ([[latentmas-collaboration|LatentMAS]])

[[latentmas-collaboration|LatentMAS (Zou et al., 2025)]] extends Coconut-style latent reasoning to multi-agent systems, creating the first framework that unifies **latent reasoning AND latent communication**: each agent generates latent thoughts via hidden-state feedback, then transfers its full KV caches (including the latent thoughts) to the next agent.

**Key properties**:
- **Training-free** — alignment via ridge regression on embedding matrices
- $471.4\times$ theoretical compression advantage over text ($d / \log|V|$ for Qwen3-14B)
- 4-4.3× faster end-to-end than TextMAS, 70.8-83.7% fewer tokens

### Precursors and Baselines (Now Ingested)

**[[icot-internalize-cot|iCoT (Deng et al., 2024)]]** — The direct precursor to Coconut. Progressive left-to-right removal of CoT tokens ([[raw/pdf/arxiv-2405.14838.pdf|iCoT §3]]), forcing the model to internalize reasoning into hidden states. Established two critical techniques Coconut adopted: **optimizer resets** between stages and **removal smoothing**. Limitation: no dedicated reasoning medium — internalization is limited to the model's fixed depth. Mistral 7B achieves 51% on GSM8K with zero visible reasoning (surpassing GPT-4's 44% no-CoT), but still 17 points below explicit CoT (68%).

**[[pause-tokens|Pause Tokens (Goyal et al., 2024)]]** — The **minimal baseline** for extra computation without language. A single learnable `<pause>` embedding appended to input gives the transformer more vectors per layer (width expansion). Wins on 8/9 tasks at 1B scale. But pause tokens add **width only**, not depth — they cannot encode information from the model's own reasoning. Coconut's continuous thoughts add both width AND depth AND carry rich continuous information. [[pause-tokens|Pause Tokens]] are the existence proof; [[coconut-reasoning-latent-space|Coconut]] is the mechanism.

**Filler tokens** (Pfau et al., 2024): Using "..." for extra computation. Works for parallelizable problems but doesn't extend expressivity like CoT.

### The Spectrum from Explicit to Implicit Reasoning

| Method | Reasoning medium | Supervision | Recurrence | Training cost | Backbone modified? | Interpretable? | Scale tested |
|--------|-----------------|-------------|------------|---------------|-------------------|---------------|-------------|
| Standard CoT | Discrete tokens | Direct | Sequential generation | Constant | No | Full | Any |
| **[[thinking-states-latent-reasoning\|Thinking States]]** | **NL → compressed states** | **Direct (teacher forcing)** | **Chunk-recurrent** | **Constant** | **Lightweight modules** | **Full (NL thoughts)** | **1.5B** |
| **[[softcot-efficient-reasoning\|SoftCoT]]** | **External soft tokens** | **Indirect (projection)** | **None (single pass)** | **Constant** | **No (frozen)** | **Via decoding** | **7-8B** |
| [[coconut-reasoning-latent-space\|Coconut]] | Continuous hidden states | Indirect (future token prediction) | Hidden-state feedback | Linear (BPTT) | Yes (full training) | Via probing | GPT-2 |
| **[[latentmas-collaboration\|LatentMAS]]** | **Hidden states + KV caches** | **None (training-free)** | **Hidden-state feedback** | **None** | **No** | **Via probing** | **4-14B** |
| [[icot-internalize-cot\|iCoT]] | Implicit (no output) | Curriculum | None | Curriculum overhead | Yes | None | 7B (51% GSM8K) |
| [[pause-tokens\|Pause tokens]] | Implicit (learnable embedding) | Indirect | None (width only) | Requires pretraining | Partial (new token) | None | 1B |
| No-CoT | Implicit (single pass) | Direct (answer only) | None | Constant | No | None | Any |
