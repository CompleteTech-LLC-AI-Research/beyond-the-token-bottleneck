### Architecture Overview

The system operates in three stages at each communication round:

> [!diagram|left]
> ```mermaid
> graph TD
>     H["Agent hidden states"] --> AE["Sparsity-regularized autoencoder"]
>     AE --> Z["Latent thoughts"]
>     Z --> SR["Structure recovery"]
>     SR --> AW["Agreement-based reweighting"]
>     AW --> PA["Prefix adaptation per agent"]
>     PA --> GEN["Agents generate next response"]
> ```

> [!notation|right]
> | Step | Notation |
> |---|---|
> | Hidden states | $H_t$ |
> | Latent thoughts | $\hat{Z}_t$ |
> | Structure recovery | $B(J_{\hat{f}})$ |
> | Reweighting | $w_\sigma \cdot \hat{Z}_{t,\sigma}^{(i)}$ |
> | Prefix adaptation | $P_t^{(i)} = g(\tilde{Z}_t^{(i)})$ |

### Stage 1: Extracting Latent Thoughts

A sparsity-regularized autoencoder maps the concatenated agent hidden states into a latent space:

> $$\hat{Z}_t = \hat{f}^{-1}(H_t) \in \R^{n_z}$$

The autoencoder is trained with a reconstruction loss plus $\ell_1$ regularization on the Jacobian:

> $$\Loss_\text{rec} = \|H_t - \hat{f}(\hat{Z}_t)\|^2 + \lambda\|J_{\hat{f}}\|_1$$

The $\ell_1$ regularization (a practical relaxation of the $\ell_0$ in the theory) enforces **sparsity** in the Jacobian, which is the key ingredient enabling disentanglement. Without sparsity, the autoencoder would learn entangled representations where recovered "thoughts" are arbitrary mixtures of true thoughts.

### Stage 2: Structural Routing via Agreement

Once latent thoughts are extracted, the recovered Jacobian structure $B(J_{\hat{f}})$ determines which thoughts are relevant to which agents. For each agent $A_i$, the relevant thoughts $Z_{H_t^{(i)}}$ are identified, then partitioned by **agreement level** — how many agents share each thought:

> $$\sigma_j = \sum_{k=1}^{n_a} \mathbb{1}[\hat{Z}_{t,j} \in \hat{Z}_{H_t^{(k)}}]$$

Thoughts with high $\sigma$ (shared by many agents) represent **common ground**. Thoughts with low $\sigma$ (held by one or few agents) represent **private reasoning** or **novel perspectives**. Each agreement level gets a distinct weight $w_\sigma$, and the reweighted thoughts are concatenated into a personalized representation for each agent:

> $$\tilde{Z}_t^{(i)} = \text{concat}(w_\sigma \cdot \hat{Z}_{t,\sigma}^{(i)})$$

This is a crucial design choice: it doesn't just tell agents *what* others think, but structures the information by *how widely each thought is shared*. An agent receives its relevant thoughts annotated with "this is common ground" vs. "this is unique to you" vs. "this is unique to agent 3."

### Stage 3: Prefix Adaptation

The personalized latent representation is injected into each agent via a learned adapter function:

> $$P_t^{(i)} = g(\tilde{Z}_t^{(i)}) \in \R^{m \times d}$$

Where $m$ is the prefix length and $d$ is the embedding dimension. Following Li & Liang (2021), these prefix vectors are prepended to the agent's token embeddings in the next generation step — they modulate the agent's behavior without modifying model weights.

The adapter is trained with a lightweight objective: semantic similarity to a reference generation plus a fluency regularization term. The goal is not to replicate specific content but to ensure the prefix produces linguistically natural effects.

### Modularity and Efficiency

A key practical advantage: both the autoencoder and adapter are **task-agnostic** and can be pretrained once and reused across tasks. Their computational cost depends only on the embedding dimension (e.g., 1024 or 4096), not the model parameter count. This means ThoughtComm's overhead is identical for a 7B and a 405B model that share the same embedding dimension — a dramatic efficiency advantage over approaches like multiagent finetuning that require full-model training.
