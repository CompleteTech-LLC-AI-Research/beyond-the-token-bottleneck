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
