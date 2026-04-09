### For System Design

When designing multi-agent systems with [[embedding-space-communication]], temperature diversity should be a **first-class design parameter**, not an afterthought. The optimal configuration is not "all agents at the same settings" but a deliberate mix of confident and exploratory agents. The consistent anchor temperature (~0.25) across models provides a reasonable default, while the explorer temperature should be tuned per task.

### For Ensemble Theory

Temperature diversity in embedding communication creates a new type of ensemble — not the classic "independent models vote" but **interacting models with complementary information regimes**. The interaction is key: the high-temperature agent's contribution is only useful because the low-temperature agent can integrate the soft information into focused reasoning. This is distinct from bagging (independent models, majority vote) and boosting (sequential error correction) — it is a form of **cooperative specialization** where diversity is designed into the information channel rather than the model parameters.

### Connection to Mixture of Experts

There is a conceptual parallel to **Mixture of Experts (MoE)** architectures: different "experts" (agents at different temperatures) contribute differently to the final output, with the gating mechanism being the debate protocol itself. The low-temperature agent acts as a soft gate, selecting which information from the high-temperature agent to incorporate. Unlike MoE, where experts share parameters and are trained jointly, temperature diversity uses the same model with different inference-time settings — a zero-cost form of specialization.

### For Communication Medium Selection

Temperature diversity provides a concrete decision criterion for choosing between NL debate and embedding communication. If the task requires high temperature diversity (large spread between agents) for optimal performance, embedding communication is strongly preferred because NL cannot support high-temperature agents. If the task's optimal temperatures are both low (like Formal Logic in CIPHER's experiments), the advantage of embedding communication diminishes and NL debate may suffice.
