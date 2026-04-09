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
