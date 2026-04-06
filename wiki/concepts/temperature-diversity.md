---
type: concept
title: "Temperature Diversity"
created: "2026-04-06"
updated: "2026-04-06"
tags: [technique, multi-agent]
---

# Temperature Diversity

**Temperature diversity** is the practice of running agents at **different temperatures** in a [[multiagent-debate]] to encourage complementary information contributions. Rather than an implementation detail, temperature diversity is a first-class design parameter that accounts for a substantial portion of performance gains in [[embedding-space-communication|embedding-based communication]] systems like [[cipher-multiagent-debate-embeddings|CIPHER]].

## Background: What Temperature Does

Temperature $T$ controls the **sharpness** of the softmax distribution over the vocabulary:

$$p(v_i | T) = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$$

where $z_i$ are the logits (pre-softmax scores).

- **$T \to 0$ (greedy)**: All probability mass concentrates on the single most likely token. Output is deterministic and confident, but ignores all alternative possibilities.
- **$T = 1.0$ (standard)**: The raw learned distribution. Balanced between confidence and exploration.
- **$T > 1.0$ (high)**: Distribution flattens. More probability mass on less-likely tokens. In natural language, this produces increasingly incoherent text. In embedding space, this produces vectors that blend in more alternative tokens.
- **$T \to \infty$**: Uniform distribution. Every token equally weighted. Carries no information about the model's preference — essentially noise.

The critical insight is that temperature has **opposite effects** depending on the communication medium:

| Temperature | Natural Language (sampling) | Embedding Communication (averaging) |
|-------------|---------------------------|-------------------------------------|
| Low ($T < 0.5$) | Deterministic, confident | Peaked embeddings $\approx$ discrete tokens |
| Medium ($T \approx 1.0$) | Fluent, standard | Moderately blended embeddings |
| High ($T > 1.5$) | Incoherent, nonsensical | Information-rich soft tokens |

This asymmetry is the foundation of why temperature diversity behaves differently in [[cipher-multiagent-debate-embeddings|CIPHER]] versus natural language debate (NLD).

## Theoretical Foundations

### Connection to Ensemble Diversity Theory

Temperature diversity in multi-agent systems is an instance of a deeper principle from **ensemble learning**: diverse ensembles outperform homogeneous ones. The theoretical grounding comes from the **bias-variance-covariance decomposition** (Ueda & Nakano, 1996; Brown et al., 2005):

For an ensemble of $M$ estimators, the expected squared error decomposes as:

> $$\text{Error} = \overline{\text{bias}}^2 + \frac{1}{M}\overline{\text{variance}} + \left(1 - \frac{1}{M}\right)\overline{\text{covariance}}$$

The covariance term dominates for large $M$ and represents the **correlation between estimators' errors**. Reducing this covariance — making agents' errors more independent — is the primary mechanism by which diversity helps. Temperature diversity achieves this by placing agents in different regions of the probability landscape:

- A low-temperature agent makes systematic errors (always picks the greedy choice, even when wrong)
- A high-temperature agent makes stochastic errors (spreads probability to unlikely tokens, occasionally getting lucky on hard positions)
- These error patterns are **uncorrelated**, reducing the covariance term

### Negative Correlation Learning

The concept of **negative correlation learning** (Liu & Yao, 1999) provides additional insight: the ideal ensemble has members whose errors are not just uncorrelated but **negatively correlated** — when one is wrong, the other is more likely to be right. Temperature diversity approximates this because:

- Low-temperature agents are accurate on **easy positions** (high-confidence, where the greedy token is correct) but fail on **hard positions** (where the greedy choice is wrong and alternatives matter)
- High-temperature agents preserve information at **hard positions** (distributing weight across alternatives) but introduce noise at **easy positions**

The complementary failure modes create a natural negative correlation structure.

### The Expected SARSA Connection

CIPHER's theoretical framing draws an analogy to **Expected SARSA** in reinforcement learning ([[raw/pdf/arxiv-2310.06272.pdf|CIPHER §5]]). Autoregressive generation is modeled as a Markov decision process where the state is the generated sequence so far, the action is the next token, and the policy is the softmax distribution. CIPHER computes the **expected value** over all tokens (like Expected SARSA), while natural language generation samples a single token (like vanilla SARSA). Expected SARSA provably has lower variance than vanilla SARSA (Van Seijen et al., 2009). Temperature amplifies this advantage: at high temperature, the expectation (weighted average embedding) remains a valid signal, while the sample (a single token drawn from a flat distribution) becomes essentially random.

### Information-Theoretic Perspective

From an information-theoretic view, each token position carries two types of information:

1. **Mode information**: Which token is most likely (captured by low-temperature / greedy decoding)
2. **Distributional information**: The full shape of the probability distribution over alternatives — confidence level, runner-up tokens, uncertainty structure

Natural language communication can only transmit mode information (a single sampled token). Embedding communication transmits both. Temperature controls the **mixing ratio** between these two types:

| Agent type | Mode info | Distributional info | Communication medium that benefits |
|-----------|-----------|--------------------|------------------------------------|
| Low-$T$ | Strong | Weak (peaked distribution, negligible alternatives) | Both NL and embedding |
| High-$T$ | Weak (diluted by alternatives) | Strong (rich distribution shape) | Embedding only |

Temperature diversity pairs agents with complementary information profiles, maximizing the total information available to the system.

## Mechanism in Detail

### The Low-Temperature Agent (Anchor)

- Produces sharp, confident outputs — essentially greedy generation
- Serves as the **final answer selector** because its outputs are closest to natural language and most interpretable (CIPHER selects the lowest-temperature debater's response as the final answer)
- Provides a strong "hypothesis" for the other agent to react to
- In CIPHER, its embeddings are close to actual token embeddings (since the distribution is peaked)
- Error profile: high accuracy on easy positions, systematic failures on hard positions

### The High-Temperature Agent (Explorer)

- In natural language debate: produces garbled text at high temperatures ($T > 1.5$), which **actively harms** the other agent. This is why NLD wants all temperatures below 1.0
- In CIPHER: produces embedding vectors that are **rich weighted averages** over many tokens. These vectors encode the model's nuanced beliefs, including uncertainty and alternative possibilities. The receiving model processes these as soft inputs that carry richer information than any single token could
- Error profile: noisy on easy positions, but preserves critical information on hard positions

### Why They Complement Each Other

The pair works because they contribute **different types of information**:
- The anchor contributes **decisive, focused reasoning** — strong on the tokens where the model is confident
- The explorer contributes **distributional information** — valuable precisely at positions where the model is uncertain and a single token would be misleading

This is analogous to **exploration vs. exploitation** in reinforcement learning. The low-temperature agent exploits known-good reasoning; the high-temperature agent explores the space of possibilities. Together they cover more of the information landscape.

## Experimental Evidence from CIPHER

### Temperature Sensitivity Contour Plots

CIPHER's experiments with Bayesian optimization over temperature pairs reveal distinct optimal regions for CIPHER vs. NLD ([[raw/pdf/arxiv-2310.06272.pdf|CIPHER Figure 5, §4.3]]):

**NLD optimal regions** (2 LLaMA2-70B debaters):
- Arithmetic: Both temperatures in the 0.5-1.0 range, peak ~81%
- GSM8K: Both temperatures in the 0.1-0.8 range, peak ~65%
- Psychology: Both temperatures in the 0.0-0.8 range, peak ~75%
- **Pattern**: Both agents must stay below or near 1.0. Higher temperatures produce nonsensical text that degrades debate quality.

**CIPHER optimal regions** (2 LLaMA2-70B debaters):
- Arithmetic: Low $T_1$ (~0.15) paired with high $T_2$ (~1.75), peak ~85%
- GSM8K: Low $T_1$ (~0.2) paired with higher $T_2$ (~0.9), peak ~66%
- Psychology: More compact region around (0.1, 0.2), peak ~75%
- **Pattern**: Optimal performance with temperatures **spread apart**. The contour plots show the best regions on the left side of the charts (low $T_1$, high $T_2$).

### Optimal Temperature Pairs Across Tasks

Specific Bayesian-optimized temperature pairs from ([[raw/pdf/arxiv-2310.06272.pdf|CIPHER Table 3]]):

| Dataset | NLD optimal $(T_1, T_2)$ | CIPHER optimal $(T_1, T_2)$ | Temperature spread |
|---------|--------------------------|----------------------------|--------------------|
| GSM8K | (0.10, 0.20) | (0.22, 0.60) | NLD: 0.10, CIPHER: 0.38 |
| H.S. Math | (0.30, 0.49) | (0.10, 0.82) | NLD: 0.19, CIPHER: 0.72 |
| Psychology | (0.01, 0.51) | (0.10, 0.20) | NLD: 0.50, CIPHER: 0.10 |
| Formal Logic | (0.10, 0.20) | (0.10, 0.20) | Both: 0.10 |
| Arithmetic | (0.54, 1.00) | (0.15, 1.75) | NLD: 0.46, CIPHER: 1.60 |

The Arithmetic result is the most striking: CIPHER's optimal second temperature (1.75) is far above 1.0, which would produce gibberish in natural language but creates information-rich embeddings. The temperature spread in CIPHER (1.60) is 3.5x larger than in NLD (0.46).

### Cross-Model Temperature Patterns

Temperature diversity patterns hold consistently across different LLM families ([[raw/pdf/arxiv-2310.06272.pdf|CIPHER Table 5]]):

| Model | CIPHER optimal $(T_1, T_2)$ |
|-------|----------------------------|
| LLaMA2-70B | (0.22, 0.60) |
| LLaMA2-Chat-70B | (0.25, 0.65) |
| LLaMA-65B | (0.25, 0.85) |
| Falcon-40B-Instruct | (0.25, 0.65) |
| MPT-30B | (0.23, 0.64) |
| WizardMath-70B | (0.26, 0.69) |

Remarkably, the anchor temperature clusters tightly around 0.22-0.26 across all models, while the explorer temperature varies more (0.60-0.85). This suggests that the optimal anchor temperature is a near-universal property of LLM softmax distributions, while the optimal explorer temperature is model-specific.

### Quantitative Impact of Diversity

The magnitude of temperature diversity's contribution can be isolated:

On the Arithmetic benchmark (LLaMA2-70B):
- NLD at optimal temperatures: ~81%
- CIPHER at non-diverse temperatures (both low): ~75%
- CIPHER at optimal (diverse) temperatures: ~85%

The ~10% gap between CIPHER-diverse and CIPHER-uniform shows that temperature diversity **accounts for a large portion of CIPHER's advantage**. Without diversity, CIPHER with embedding communication but uniform temperatures actually underperforms NLD on this task.

### Scaling Temperature Diversity to 3+ Agents

With more than two agents, temperature diversity becomes more nuanced ([[raw/pdf/arxiv-2310.06272.pdf|CIPHER Table 7]]):

| Debaters | NLD temperatures | CIPHER temperatures |
|----------|-----------------|---------------------|
| 2 | (0.100, 0.500) | (0.250, 0.600) |
| 3 | (0.300, 0.500, 0.700) | (0.001, 0.725, 1.067) |
| 4 | (0.442, 0.176, 0.745, 0.539) | (0.641, 0.464, 0.507, 0.202) |

For CIPHER with 3 agents, the optimal configuration is extreme: one near-zero agent (strong anchor), one medium agent, and one high-temperature explorer ($T > 1.0$). For 4 agents, the pattern becomes less regular, suggesting that with more agents the optimization landscape becomes more complex.

### The Partial CIPHER Ablation Connection

CIPHER's partial application experiment reinforces the temperature story ([[raw/pdf/arxiv-2310.06272.pdf|CIPHER Figure 6]]): applying CIPHER only at **high-uncertainty positions** (where the distribution is spread, mimicking high temperature) captures most of the benefit:

At temperature pair (0.15, 1.75):
- Full CIPHER: ~85%
- Partial CIPHER (high-uncertainty positions only): ~84-85%
- Reversed (low-uncertainty positions only): ~50-55%

The advantage is concentrated at exactly the positions where temperature diversity matters most — positions where the model is uncertain and a single token would lose the most information. At confident positions, embedding communication and token communication are essentially equivalent (both transmit the same dominant token).

## Temperature Diversity vs. Structured Alternatives

### [[thought-communication-multiagent|ThoughtComm]]'s Agreement Routing

[[thought-communication-multiagent|ThoughtComm]]'s agreement-based routing provides a **structured alternative** to temperature diversity. Rather than relying on temperature to create complementary information profiles, [[thought-communication-multiagent|ThoughtComm]] directly identifies and routes disentangled thoughts:

| Property | Temperature diversity | ThoughtComm agreement routing |
|----------|----------------------|------------------------------|
| **How diversity is created** | Different sampling temperatures produce different information profiles | Autoencoder disentangles thoughts; agreement scores annotate commonality |
| **What's complementary** | Mode info (anchor) vs. distributional info (explorer) | Shared thoughts (common ground) vs. private thoughts (unique perspectives) |
| **Control mechanism** | Temperature hyperparameter (continuous, per-agent) | Agreement weights $w_\sigma$ (learned, per-thought) |
| **Theoretical guarantee** | None — empirical optimization via Bayesian search | Identifiability theorems for shared/private thought recovery |
| **Scales with rounds** | Fixed temperatures across rounds | Adapts as thought structure evolves across rounds |
| **Requires training** | No | Yes (autoencoder + adapter) |

Temperature diversity is a **crude proxy** for what ThoughtComm achieves precisely: the high-temperature agent's role is essentially to provide "alternative perspectives" (via distributional information), while the low-temperature agent provides "confident conclusions." ThoughtComm makes this distinction explicit by formally separating shared thoughts (confident, widely held) from private thoughts (unique, potentially novel).

### Connection to [[thought-structure]]

The [[thought-structure]] concept reveals that temperature diversity operates on the wrong level of abstraction. Temperature modulates the **representation format** (peaked vs. spread distribution) rather than the **content** (which thoughts to share). Two agents at different temperatures may still think about the same thing — they just represent it differently. ThoughtComm disentangles the **content** of thoughts and routes them based on relevance and agreement, regardless of how they're represented.

However, temperature diversity has a significant practical advantage: it requires **zero training** and works with any model. ThoughtComm requires autoencoder training and access to hidden states. For rapid deployment or closed-source models, temperature diversity remains the most accessible diversity mechanism.

## Broader Implications

### For System Design

When designing multi-agent systems with [[embedding-space-communication]], temperature diversity should be a **first-class design parameter**, not an afterthought. The optimal configuration is not "all agents at the same settings" but a deliberate mix of confident and exploratory agents. The consistent anchor temperature (~0.25) across models provides a reasonable default, while the explorer temperature should be tuned per task.

### For Ensemble Theory

Temperature diversity in embedding communication creates a new type of ensemble — not the classic "independent models vote" but **interacting models with complementary information regimes**. The interaction is key: the high-temperature agent's contribution is only useful because the low-temperature agent can integrate the soft information into focused reasoning. This is distinct from bagging (independent models, majority vote) and boosting (sequential error correction) — it is a form of **cooperative specialization** where diversity is designed into the information channel rather than the model parameters.

### Connection to Mixture of Experts

There is a conceptual parallel to **Mixture of Experts (MoE)** architectures: different "experts" (agents at different temperatures) contribute differently to the final output, with the gating mechanism being the debate protocol itself. The low-temperature agent acts as a soft gate, selecting which information from the high-temperature agent to incorporate. Unlike MoE, where experts share parameters and are trained jointly, temperature diversity uses the same model with different inference-time settings — a zero-cost form of specialization.

### For Communication Medium Selection

Temperature diversity provides a concrete decision criterion for choosing between NL debate and embedding communication. If the task requires high temperature diversity (large spread between agents) for optimal performance, embedding communication is strongly preferred because NL cannot support high-temperature agents. If the task's optimal temperatures are both low (like Formal Logic in CIPHER's experiments), the advantage of embedding communication diminishes and NL debate may suffice.

## Trade-off Analysis

| Consideration | Low diversity (similar $T$) | High diversity (spread $T$) |
|--------------|---------------------------|---------------------------|
| Individual agent quality | All agents are reasonable | Explorer agent produces poor standalone output |
| Information complementarity | Low — redundant signals | High — anchor provides focus, explorer provides alternatives |
| Sensitivity to medium | Works in both NL and embedding | Only works in embedding communication |
| Optimization difficulty | Fewer hyperparameters | Bayesian optimization over temperature pairs needed |
| Robustness | Degrades gracefully | Sensitive to exact temperature values (narrow optimal region on some tasks) |
| Interpretability | Both agents' outputs are human-readable | Only anchor agent's output is interpretable |

## Open Questions

- **Optimal temperature schedules**: Should temperatures change across debate rounds? Starting diverse and converging toward low temperatures as consensus forms could combine exploration (early rounds) with exploitation (late rounds). No published work has explored this.
- **More than two temperatures**: With 3+ agents, what is the optimal distribution of temperatures? CIPHER's 3-agent result (0.001, 0.725, 1.067) suggests an extreme anchor + graduated explorers pattern, but the 4-agent result is less regular. Is there a principled allocation rule?
- **Adaptive temperature**: Could an agent dynamically adjust its temperature based on position-level uncertainty, combining the anchor and explorer roles in a single agent? This would be a form of **adaptive diversity** — explore where uncertain, exploit where confident — without requiring multiple agents.
- **Task-dependent diversity**: Why does Psychology's optimal CIPHER temperature pair (0.10, 0.20) show almost no diversity, while Arithmetic's (0.15, 1.75) shows extreme diversity? What properties of the task determine how much diversity helps?
- **Temperature diversity beyond softmax**: In models with alternative output distributions (e.g., discrete diffusion models, energy-based models), what is the analog of temperature diversity? The principle — complementary information profiles — should generalize, but the mechanism would differ.
- **Interaction with [[thought-structure]]**: Could temperature diversity and thought-structure routing be combined? For instance, the high-temperature agent's rich distributional embeddings might provide better input for ThoughtComm's autoencoder, enabling more informative disentanglement. Conversely, ThoughtComm's agreement routing could replace Bayesian temperature optimization with a principled, learned routing mechanism.
- **Diversity in reasoning vs. communication**: Temperature diversity operates at the communication interface. Is there an analog within single-model latent reasoning — e.g., varying the "temperature" of [[latent-space-reasoning|Coconut]]'s continuous thoughts to create diverse superpositions?
