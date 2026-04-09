[[latent-reasoning-supervision-analysis|Cui et al. (2026)]] provides the **empirical bracket** for Zhu et al.'s theory, separating two claims that the literature conflated:

| Claim | Source | Status |
|---|---|---|
| Latent vectors *can* encode normalized mixtures over the reachable set $V_c$ (see [[#Core Theoretical Results]]) | Zhu et al. (this paper) — proven by construction | **Confirmed** |
| The iterative latent process *does* expand the BFS frontier across steps | Implicit in Coconut's narrative | **Falsified** by Cui et al.'s diversity analysis (distinct outcomes *decrease* with depth) |
| The process *amplifies* the correct candidate before final readout | Implied | **Falsified** — Cui et al. find majority-vote accuracy 3-4 points below explicit reasoning |

The synthesis: Zhu et al.'s theoretical construction is achievable in **representational capacity** (a single continuous thought can be a uniform mixture over the reachable set), but the **gradient-based optimization process** of practically-trained latent reasoning models (Coconut, CODI, SIM-CoT, CoLaR) actively prunes that mixture as latent steps progress. The 2-layer, trained-from-scratch GPT-2 in Zhu et al.'s experiments demonstrates the achievable maximum; the practical methods Cui et al. test fall well short of it.

This is **not** a refutation of Zhu et al. — the construction stands and the capacity claim is independently confirmed by Cui et al.'s Pass@100 analysis. But it does mean the **realizable** advantage of latent reasoning over explicit CoT is much smaller than the construction suggests, and that closing the gap requires new training schemes, not just larger models. See the [[contradictions|contradictions analysis]] for the full discussion.
