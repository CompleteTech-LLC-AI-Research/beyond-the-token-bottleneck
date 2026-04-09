> [!diagram|left]
> ```mermaid
> graph TD
>     X["Question X"] --> S1["Latent step s_1<br>(dropout ON)"]
>     S1 --> S2["Latent step s_2<br>(dropout ON)"]
>     S2 --> S3["..."]
>     S3 --> ST["Latent step s_T"]
>     ST --> A["Answer decoding<br>(dropout OFF)"]
>     A --> R["Sampled answer a_n"]
>     R -->|"repeat N times"| X
>     R --> RM["PRM / ORM<br>reranker"]
>     RM --> FA["Final answer"]
>     style X fill:#dae8fc,stroke:#6c8ebf
>     style S1 fill:#fff2cc,stroke:#d6b656
>     style S2 fill:#fff2cc,stroke:#d6b656
>     style ST fill:#fff2cc,stroke:#d6b656
>     style A fill:#d5e8d4,stroke:#82b366
>     style RM fill:#ffe6cc,stroke:#d79b00
>     style FA fill:#e1d5e7,stroke:#9673a6
> ```

> [!notation|right]
> | Symbol | Meaning |
> |---|---|
> | $X$ | Input question prompt |
> | $\mathbf{s}_i \in \R^D$ | $i$-th continuous thought vector |
> | $T = c \cdot k$ | Total latent steps ($c=2$, $k=3$) |
> | $N$ | Number of stochastic samples per question |
> | $y^{HE}_{s_i}$ | Hard MC label for step $s_i$ |
> | $y^{SE}_{s_i}$ | Soft MC label for step $s_i$ |
> | $r^{OUT}$ | Outcome label for trajectory |

### Stochastic Sampling via Selective Dropout

COCONUT's reasoning is deterministic by construction — each latent step $\mathbf{s}_i = f_\theta(X, \mathbf{s}_{<i})$ is computed by a single forward pass with no sampling temperature, so applying temperature only at the answer-decoding stage cannot diversify the *trajectory*, only the *transcription* of a single trajectory.

The fix is minimal: enable dropout (at the same rate used during training) **only during the iterative hidden-state generation phase**, then disable it for the final-answer text generation. This confines stochasticity to the latent loop without compromising answer-decoding integrity. Each forward pass through the dropout-enabled COCONUT now produces a different continuous-thought trajectory, and Pass@N can be measured by drawing $N$ such trajectories and decoding each one's answer.

### MC Annotation for Continuous-Thought Reward Models

The reward modeling pipeline is a direct adaptation of MATH-Shepherd to continuous thoughts (Algo 1 in the paper). For each problem $X$ with ground-truth answer $a^*$:

1. Sample $M = 5$ continuous-thought trajectories via dropout, deduplicate by final answer (yielding $\sim$1.32 unique trajectories per problem).
2. For each step $\mathbf{s}_i$ in each unique trajectory, take the partial trajectory $\tau_{1:i}$ and Monte-Carlo sample $N = 10$ completions from it.
3. Compute step-wise labels:
   - **Hard estimation**: $y^{HE}_{s_i} = \mathbf{1}[\exists j: a_j = a^*]$ — does *any* completion from this prefix reach the correct answer?
   - **Soft estimation**: $y^{SE}_{s_i} = \frac{1}{N}\sum_{j=1}^{N} \mathbf{1}[a_j = a^*]$ — what *fraction* of completions reach it?
4. Compute trajectory-level outcome labels: $r^{OUT} = \mathbf{1}[\text{final answer correct}]$.

Annotation is run on the GSM8K training set, yielding 238K samples for PRM and 324K for ORM, balanced 1:1 between positive and negative. **Critical architectural constraint**: continuous thoughts are model-specific, so the reward model backbone *must* be COCONUT itself — a reward model trained on a different transformer cannot interpret COCONUT's latent representations. Wang et al. attach two-layer MLP heads (ReLU + sigmoid) to a COCONUT base for hard/soft PRM and ORM.

The PRM loss is the joint cross-entropy + MSE objective:

$$\mathcal{L}_{PRM} = \mathcal{L}_{CE}(y^{HE}_{s_i}, \hat{y}^{HE}_{s_i}) + \mathcal{L}_{MSE}(y^{SE}_{s_i}, \hat{y}^{SE}_{s_i})$$

ORM uses cross-entropy alone on the trajectory outcome.
