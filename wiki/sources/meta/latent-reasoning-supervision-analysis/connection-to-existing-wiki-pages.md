### Direct experimental tests

- **[[coconut-reasoning-latent-space|Coconut (Hao et al., 2024)]]**: Cui et al. test the *same model* on the *same datasets*. The Improved Coconut variant (+7pp on GSM8K-Aug) is a direct follow-up. The shortcut analysis is the strongest mechanistic critique of Coconut to date.
- **[[superposition-coconut-theory|Superposition Theory (Zhu et al., 2025)]]**: Cui et al. **partially confirm** the theory (latent vectors do encode multiple candidates) but **falsify the iterative-BFS extension** (the process exhibits implicit pruning, not breadth-first expansion). The theoretical bound is achievable in capacity but not in dynamics.
- **[[icot-internalize-cot|iCoT]]**: Same GPT-2 backbone, related stage-wise curriculum. The collapse-mitigation insight (mix earlier-stage data) plausibly transfers to iCoT's progressive removal schedule.

### Concept page updates

- **[[latent-space-reasoning]]**: The "Emergent BFS" section needs a major caveat — capacity ≠ use. The "Three Solutions to the Training Challenge" table should add a fourth row for the supervision–exploration trade-off as an orthogonal failure mode.
- **[[catastrophic-forgetting]]**: Add the supervision–exploration trade-off as a *complementary* training-time barrier. The two trade-offs together explain why the latent reasoning design space is so constrained.
- **[[continuous-vs-discrete-representation]]**: The Pass@100 / Maj@100 gap is a quantitative instance of the discrete bottleneck — discrete tokens can't represent the multi-candidate state, but the multi-candidate state alone is insufficient.

### Analysis page updates

- **[[contradictions]]**: New tension #9 — "BFS as faithful structured search vs. implicit pruning" (Coconut/Zhu et al. vs. Cui et al.). Status: **partially resolved by Cui et al.** — capacity confirmed, dynamics falsified.
- **[[frontier-research-directions]]**: Direction #1 (superposition reasoning at frontier scale) and #2 (disentangling superposed paths) need a new "blockers" subsection — Cui et al. show the optimization process actively destroys the property both directions try to exploit.
- **[[benchmark-overlap]]**: Add to the "<2B latent reasoning cluster" and the GSM8K table.
- **[[open-questions]]**: Add the supervision–exploration trade-off as an open question; add the Pass@100 / Maj@100 amplification gap.

### MOC updates

- **[[latent-reasoning]]**: Add as a "critical empirical analysis" entry following Coconut and Superposition Theory.
- **[[theoretical-foundations]]**: Add as the empirical counterpoint to Zhu et al.'s superposition proof — together they bracket what is and isn't true about parallel BFS in latent space.
- **[[safety-interpretability]]**: The shortcut and noise-injection findings are directly relevant — latent reasoning that bypasses its own reasoning is a safety concern (you cannot audit a process that isn't being used).
