Total reasoning turns follow power-law growth with agent count:

**T = 2.72 * (n + 0.5)^1.724**, R^2 = 0.974, 95% CI on exponent: [1.685, 1.763], p < 0.001

The super-linear exponent (1.724 > 1) reflects quadratic message complexity tempered by practical bandwidth limits. Empirical turn multipliers vs. SAS (7.2 turns):
- Independent: 1.6x (11.4 turns)
- Decentralized: 3.6x (26.1 turns)
- Centralized: 3.8x (27.7 turns)
- Hybrid: **6.2x** (44.3 turns, t(178) = 16.8, p < 0.001)

Beyond 3-4 agents under fixed budgets, per-agent reasoning capacity becomes prohibitively thin — a hard resource ceiling where communication cost dominates reasoning capability. Extrapolation to n = 6: predicted 12.8-20.1 turns for base, but Centralized would reach ~85-130 turns.

Message density saturates logarithmically: S = 0.73 + 0.28 * ln(mu), R^2 = 0.68, p < 0.001. Performance plateaus near mu = 0.39 messages/turn (Decentralized: 0.41, Centralized: 0.39).
