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
