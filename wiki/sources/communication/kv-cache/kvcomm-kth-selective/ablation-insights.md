### Random vs Importance-Based Layer Selection

The paper's selection strategy combines an attention-importance score $\hat{S}_{al}$ with a Gaussian prior $P_l$. Compared to baselines:

- **Random layer selection** at the same budget (e.g., 30% of layers chosen uniformly at random) performs significantly worse than importance-based selection, often falling below NLD on complex tasks. This confirms that the information content of KV-caches varies dramatically across layers — not all layers carry transferable semantic knowledge, and including uninformative layers can inject noise that degrades the receiver's processing.
- **Attention-only selection** (no Gaussian prior, $\alpha = 1$) produces unstable results: different calibration samples may yield very different layer sets because per-input attention distributions are noisy. The Gaussian prior smooths this instability by biasing selection toward the theoretically motivated intermediate layer range.
- **Prior-only selection** (no attention score, $\alpha = 0$) performs reasonably on average but misses model-specific deviations — some models have unusually informative early or late layers that the fixed Gaussian cannot capture.

The combined score with $\alpha$ balancing data-driven and prior-driven components gives the most robust performance across model pairs and tasks, which is why a single calibration sample suffices for generalization.

### Contiguous vs Non-Contiguous Layer Patterns

A key finding: constraining selection to **contiguous blocks** (e.g., layers 10-19) consistently underperforms the unconstrained non-contiguous selection (e.g., layers 8, 12, 15, 19, 23) at the same budget. The most informative layers are scattered across the network rather than clustered in a single block. For example, a model may have high attention importance at layers 8 and 23 alongside the expected intermediate-layer peaks — a contiguous block centered at layer 15 would miss both.

This non-contiguity finding is independently corroborated by [[cache-to-cache-semantic-communication|C2C]]'s learnable Gumbel-sigmoid gates, which converge to binary "on/off" decisions at non-contiguous layers. The convergence across two very different selection mechanisms (calibration-based ranking vs. gradient-trained gating) strengthens the conclusion that the beneficial fusion layers do not cluster.

The practical implication: any KV-cache sharing protocol that imposes contiguous-block constraints (e.g., "share the middle third of layers") leaves significant performance on the table compared to a principled non-contiguous selection strategy.
