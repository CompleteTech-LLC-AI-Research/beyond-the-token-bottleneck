---
type: source
title: "Towards a Science of Scaling Agent Systems"
source_file: "[[raw/pdf/arxiv-2512.08296.pdf]]"
latex_source: "[[raw/latex/arxiv-2512.08296.tar.gz]]"
author: "Yubin Kim, Ken Gu, Chanwoo Park, et al."
date_published: "2025-12-17"
date_ingested: "2026-04-06"
created: "2026-04-06"
venue: "arXiv preprint"
arxiv: "2512.08296"
institution: "Google Research, Google DeepMind, MIT"
tags: [scaling, multi-agent, coordination, theoretical-framework]
---

# Towards a Science of Scaling Agent Systems

## One-liner

![[scaling-agent-systems/one-liner]]

## Summary

This paper provides the first **quantitative scaling framework** for multi-agent LLM systems, modeling performance as an interplay of agent quantity, coordination topology, model capability, and task properties. Through controlled experiments across **180 configurations** (5 architectures x 9 LLM models x 4 benchmarks), it challenges the "more agents is better" claim and establishes that multi-agent coordination is **task-contingent** — it can improve performance by +80.9% or degrade it by -70%.

## Nine LLM Models Tested

All models span an Intelligence Index range of 42-71 (composite capability score integrating reasoning, coding, and knowledge benchmarks). Cross-family scaling slopes differ by at most delta_max = 0.023, with CV < 0.02.

| Family | Model | Intelligence Index |
|--------|-------|--------------------|
| OpenAI | GPT-5-nano | 59 |
| OpenAI | GPT-5-mini | 68 |
| OpenAI | GPT-5 | 71 |
| Google | Gemini 2.0 Flash | 47 |
| Google | Gemini 2.5 Flash | 58 |
| Google | Gemini 2.5 Pro | 65 |
| Anthropic | Claude Sonnet 3.7 | 42 |
| Anthropic | Claude Sonnet 4.0 | 47 |
| Anthropic | Claude Sonnet 4.5 | 55 |

Best MAS variant vs. SAS at same Intelligence Index: OpenAI +8.7%, Google +8.1%, Anthropic -4.6%.

## Five Canonical Architectures (Formal Definitions)

The system S = (A, E, C, O) consists of agents A = {a_1, ..., a_n}, shared environment E, communication topology C, and orchestration policy O.

### Single-Agent System (SAS)
- |A| = 1, zero communication overhead
- Complexity: O(T) where T = max iterations
- Memory: O(T), sequential processing only

### Independent MAS
- C = {(a_i, agg) : all i} — agent-to-aggregator only, **no peer communication**
- Policy: synthesis_only (concatenates sub-agent outputs without cross-validation)
- LLM calls: O(nT) + O(1), sequential depth = 1, parallelization factor = n
- Memory: O(n * T), maximal parallelization but minimal coordination

### Centralized MAS
- C = {(orch, a_i) : all i} — orchestrator-to-agents only (hub-spoke)
- Policy: hierarchical — orchestrator decomposes tasks, coordinates R rounds across n sub-agents
- LLM calls: O(nT) + O(nR), sequential depth = R, parallelization factor = n
- Memory: O(n * T * R), creates validation bottleneck at orchestrator

### Decentralized MAS
- C = {(a_i, a_j) : all i,j where i != j} — all-to-all topology
- Policy: consensus — agents debate in D sequential rounds
- LLM calls: O(nT) + O(1), sequential depth = D
- Memory: O(n * T * D), each agent stores own debate history

### Hybrid MAS
- C = star_edges + peer_edges — orchestrator plus limited peer-to-peer
- Policy: hierarchical + lateral — combines orchestrator control with directed peer communication
- LLM calls: O(nT) + O(nR) + O(nP) where P = peer rounds
- Memory: O(n * T * R + n * P), inherits orchestrator control while enabling lateral exchange

## Full Coordination Metrics (Table 5)

All systems matched for total reasoning tokens (mean T_budget = 4,800 per trial), n = 180 configurations, 15,750 total instance runs.

| Metric | SAS | Independent | Decentralized | Centralized | Hybrid |
|--------|-----|-------------|---------------|-------------|--------|
| Success Rate (S) | 0.466 | 0.370 | 0.477 | 0.463 | 0.452 |
| Turns (T) | 7.2 +/- 2.1 | 11.4 +/- 3.2 | 26.1 +/- 7.5 | 27.7 +/- 8.1 | 44.3 +/- 12.4 |
| Overhead (Delta%) | 0% | 58% | 263% | 285% | 515% |
| Message Density (mu) | 0.00 | 0.00 | 0.41 | 0.39 | 0.24 |
| Redundancy (rho) | 0.00 | 0.48 +/- 0.09 | 0.50 +/- 0.06 | 0.41 +/- 0.06 | 0.46 +/- 0.04 |
| Efficiency (eta) | 0.466 | 0.234 | 0.132 | 0.120 | 0.074 |
| Error Amplification (alpha) | 1.0x | 17.2x | 7.8x | 4.4x | 5.1x |
| Success/1K tokens | 67.7 | 42.4 | 23.9 | 21.5 | 13.6 |

## Full Benchmark Results

Overall mean MAS improvement: -3.5% (95% CI: [-18.6%, +25.7%]), sigma = 45.2%.

### Finance-Agent (naturally decomposable: revenue/cost/market subtasks)
- SAS: 0.349 mean
- Independent: +57% (0.548)
- Decentralized: +74.5% (0.609)
- Centralized: **+80.8%** (0.631)
- Hybrid: +73.1% (0.604)
- Error absorption peaks at 31.4% for this benchmark

### BrowseComp-Plus (dynamic web navigation, highest variability CV = 0.32)
- SAS: 0.318 mean
- Independent: **-35%**
- Decentralized: **+9.2%** (0.347)
- Centralized: +0.2%
- Hybrid: +6%

### PlanCraft (strictly sequential state-dependent reasoning)
- SAS: 0.568 mean
- Independent: **-70.1%** (0.170)
- Decentralized: -41.5% (0.332)
- Centralized: -50.3% (0.282)
- Hybrid: -39.1% (0.346)

### Workbench (deterministic tool use, lowest variability CV = 0.12)
- SAS: 0.629 mean
- Independent: -11%
- Decentralized: +5.7% (0.664)
- Centralized: -1.2%
- Hybrid: -1.2%

## Mixed-Effects Regression Model (Equation 1)

Twenty parameters, all predictors standardized (mu = 0, sigma = 1). Log transformations applied to right-skewed variables (Delta%: 0-515%; t_tools: 4-16; n: 1-4; alpha: 1.0-17.2).

**S = beta_0 + beta_1(I - I_bar) + beta_2(I - I_bar)^2 + beta_3 log(1+t) + beta_4 log(1+n) + beta_5 log(1+Delta%) + beta_6 eta + beta_7 mu + beta_8 rho + beta_9 log(1+alpha) + beta_10 S_SA + beta_11(S_SA * log(1+n)) + beta_12(eta * t) + beta_13(Delta% * t) + beta_14(alpha * t) + beta_15(rho * n) + beta_16(alpha * S_SA) + beta_17(mu * I) + beta_18(I * log(1+t)) + beta_19(eta * alpha) + epsilon**

### Independent Variables (4 categories)
1. **Base model capability**: Intelligence Index (I), centered at I_bar = 56.9
2. **System configuration**: agent count (n)
3. **Task properties**: tool count (t), single-agent baseline (S_SA)
4. **Coordination metrics**: efficiency (eta), overhead (Delta%), error amplification (alpha), message density (mu), redundancy (rho)

### Full Coefficient Table (Table 4)

| Predictor | beta_hat | 95% CI | p-value | Interpretation |
|-----------|----------|--------|---------|----------------|
| **Main Effects** | | | | |
| Intercept (beta_0) | 0.453 | [0.433, 0.472] | <0.001 | Baseline performance |
| Intelligence (I - I_bar) | 0.171 | [0.070, 0.272] | 0.001 | Linear capability effect |
| Intelligence^2 | 0.007 | [-0.013, 0.026] | 0.509 | Quadratic: NOT significant |
| log(1+t) tools | 0.411 | [0.291, 0.531] | <0.001 | Tool diversity benefit |
| log(1+n) agents | 0.052 | [-0.061, 0.166] | 0.367 | Agent count: NOT significant |
| S_SA baseline | 0.315 | [0.185, 0.445] | <0.001 | Task difficulty proxy |
| **Coordination** | | | | |
| log(1+Delta%) overhead | 0.034 | [0.011, 0.057] | 0.005 | Direct overhead cost |
| mu message density | -0.057 | [-0.110, -0.003] | 0.039 | Communication intensity |
| rho redundancy | -0.007 | [-0.052, 0.037] | 0.748 | NOT significant alone |
| eta efficiency | -0.043 | [-0.078, -0.007] | 0.021 | Coordination efficiency |
| log(1+alpha) error amp | -0.022 | [-0.077, 0.034] | 0.441 | NOT significant alone |
| **Critical Interactions** | | | | |
| S_SA * log(1+n) | **-0.404** | [-0.557, -0.252] | <0.001 | **Baseline paradox** |
| eta * t | **-0.267** | [-0.355, -0.178] | <0.001 | **Efficiency-tools trade-off** |
| Delta% * t | **-0.162** | [-0.241, -0.083] | <0.001 | **Overhead scales with complexity** |
| alpha * t | -0.019 | [-0.075, 0.037] | 0.506 | Not significant |
| rho * n | 0.047 | [0.019, 0.075] | 0.001 | Redundancy benefit with scale |
| alpha * S_SA | -0.022 | [-0.075, 0.030] | 0.404 | Not significant |
| mu * I | -0.065 | [-0.146, 0.015] | 0.114 | Not significant |
| I * log(1+t) | -0.011 | [-0.057, 0.034] | 0.626 | Not significant |
| eta * alpha | -0.069 | [-0.138, 0.000] | 0.053 | Borderline |

### Three Dominant Effects

1. **Baseline paradox** (beta = -0.404, p < 0.001): When S_SA > ~45%, coordination yields diminishing or negative returns. Decision boundary: S_SA = -beta_4/beta_17 = 0.052/0.404 = 0.129 standardized units, ~0.45 raw.
2. **Efficiency-tools trade-off** (beta = -0.267, p < 0.001): Tool-heavy tasks suffer disproportionately. For 16-tool tasks, penalty = -0.267 * eta * t, yielding -1.99 for SAS vs. -0.32 for MAS — single-agent paradoxically more effective.
3. **Overhead-complexity interaction** (beta = -0.162, p < 0.001): Critical threshold Delta%_max = (0.034/0.162) * log(1+Delta%) ~ 150% for t=16, ruling out all MAS except possibly decentralized.

## Predictive Model Validation

| Metric | Value |
|--------|-------|
| R^2_train | 0.613 |
| R^2_CV (5-fold) | **0.524** (+/- 0.033 SD) |
| MAE | 0.089 (+/- 0.011) |
| RMSE | 0.112 (+/- 0.014) |
| Train-CV gap | 0.076 |
| Correct architecture prediction | **87%** of held-out configs |
| Residual SE | 0.118 |
| Shapiro-Wilk p | 0.412 |
| Breusch-Pagan p | 0.298 |

Model comparison (R^2_CV): Intelligence only = 0.283, + tools/agents = 0.430, + architecture labels = 0.431, + coordination metrics = **0.524** (20% improvement over categorical labels).

Regularized alternatives: Lasso retained 16/20 predictors (R^2_CV = 0.506), Ridge (R^2_CV = 0.509). Full model retained for interpretability.

### GPT-5.2 Out-of-Sample Validation (released after study)

| Metric | Value | Status |
|--------|-------|--------|
| MAE | 0.071 | < 0.10 acceptable |
| MAPE | 15.8% | acceptable |
| Normalized MAE | 0.045 | |
| Qualitative findings validated | **4 of 5** | one partial |
| Kendall's tau (ranking) | 0.200 | weak |

GPT-5.2 Intelligence Index = 75. The one partially validated finding: architecture convergence at high capability means architecture distinctions narrow at frontier capability levels.

## Agent Scaling Power Law

Total reasoning turns follow power-law growth with agent count:

**T = 2.72 * (n + 0.5)^1.724**, R^2 = 0.974, 95% CI on exponent: [1.685, 1.763], p < 0.001

The super-linear exponent (1.724 > 1) reflects quadratic message complexity tempered by practical bandwidth limits. Empirical turn multipliers vs. SAS (7.2 turns):
- Independent: 1.6x (11.4 turns)
- Decentralized: 3.6x (26.1 turns)
- Centralized: 3.8x (27.7 turns)
- Hybrid: **6.2x** (44.3 turns, t(178) = 16.8, p < 0.001)

Beyond 3-4 agents under fixed budgets, per-agent reasoning capacity becomes prohibitively thin — a hard resource ceiling where communication cost dominates reasoning capability. Extrapolation to n = 6: predicted 12.8-20.1 turns for base, but Centralized would reach ~85-130 turns.

Message density saturates logarithmically: S = 0.73 + 0.28 * ln(mu), R^2 = 0.68, p < 0.001. Performance plateaus near mu = 0.39 messages/turn (Decentralized: 0.41, Centralized: 0.39).

## Three Coordination Regimes

| Regime | Overhead | Efficiency (eta) | Characteristics |
|--------|----------|-------------------|-----------------|
| Under-coordination | < 100% | ~0.234 | Minimal gains (+2-4%), coordination not engaged |
| **Optimal band** | 200-300% | ~0.16 | Highest success/cost ratio, strong error absorption. Dominated by Centralized (285%) and Decentralized (263%) |
| Over-coordination | > 400% | ~0.11 | Diminishing returns, Hybrid (515%) introduces coordination-failure modes (12.4% protocol failures) |

Error absorption in coordinated architectures: 22.7% average error reduction (95% CI: [20.1%, 25.3%]), peaking at 31.4% for Finance-Agent. Independent MAS shows +4.6% error amplification (no inter-agent verification).

## Token Efficiency (Success per 1K Tokens)

| Architecture | Success/1K tokens | Relative to SAS |
|--------------|-------------------|-----------------|
| SAS | 67.7 | 1.0x |
| Independent | 42.4 | 0.63x |
| Decentralized | 23.9 | 0.35x |
| Centralized | 21.5 | 0.32x |
| Hybrid | 13.6 | 0.20x |

Dollar costs per 1% success gain: OpenAI Hybrid ~$0.008, Google ~$0.012, Anthropic Hybrid ~$0.024 (3x worse, reflecting Anthropic's sensitivity to coordination overhead).

## Heterogeneity Effects (Mixed-Capability Teams)

Tested on BrowseComp-Plus with high-capability (GPT-5, Sonnet 4.5, Gemini 2.5 Pro) and low-capability (GPT-5 nano, Sonnet 3.7, Gemini 2.0 Flash) models.

Key findings:
- **Centralized**: Sub-agent capability matters more than orchestrator capability across all families. Low orchestrator + high sub-agents outperforms high orchestrator + low sub-agents.
- **Anthropic uniquely benefits from heterogeneous centralized**: low-capability orchestrator + high-capability sub-agents (0.42) outperforms homogeneous high-capability (0.32) by 31%.
- **Decentralized mixed-capability approaches near-optimal**: OpenAI mixed 0.53 vs. homogeneous-high 0.50; Anthropic mixed 0.47 vs. 0.37; Google mixed 0.42 vs. 0.43.
- OpenAI and Google show performance degradation under heterogeneous centralized configurations.

## Significance for the Wiki

This paper contextualizes all the latent communication work: the information bottleneck of natural language communication (which CIPHER, KV-cache methods, ThoughtComm, etc. address) is one of several failure modes in MAS. Others include task decomposability mismatch, error amplification, and coordination overhead. Latent communication addresses the **lossy communication** problem but cannot fix **task-architecture mismatch** or **coordination overhead**.

The paper also suggests that latent communication methods could improve the coordination efficiency metrics — reducing overhead and error amplification by transmitting richer information per exchange.

## Limitations

- **Only 4 benchmarks**: Finance-Agent, BrowseComp-Plus, PlanCraft, and Workbench cover financial analysis, web navigation, sequential planning, and tool use — but omit math reasoning, code generation, scientific QA, and open-ended generation. The "task-contingent" finding is established on a narrow task sample; the regression model's generalizability to other domains is unvalidated.
- **No latent communication channels tested**: All inter-agent communication is natural language. The framework identifies "lossy communication" as a failure mode but never tests whether KV-cache, activation, or embedding-level communication would shift the coordination metrics. The efficiency (eta) and overhead (Delta%) numbers are specific to text-based exchange.
- **9 models from 3 providers**: OpenAI (GPT-5 family), Google (Gemini family), and Anthropic (Claude Sonnet family) — all proprietary, closed-weight API models. No open-weight models (LLaMA, Qwen, Mistral) are tested, which limits reproducibility and prevents analysis of architecture-specific effects. The Intelligence Index is a composite score that may not capture capability dimensions relevant to coordination.
- **Limited heterogeneity analysis**: Mixed-capability teams are tested only on BrowseComp-Plus with a single decomposition (high/low orchestrator x high/low sub-agents). The interaction between model heterogeneity and task type is unexplored — the Anthropic-specific benefit of heterogeneous centralized configurations could be an artifact of the single benchmark.
- **Fixed agent count ceiling (n=4)**: The power law $T = 2.72 \cdot (n + 0.5)^{1.724}$ is fit on n=1 to n=4 only. Extrapolation to larger teams is speculative. The "3-4 agent ceiling" may reflect experimental design constraints rather than fundamental limits.
- **No cost-controlled comparisons**: Token efficiency (success/1K tokens) is reported but not cost-equalized across providers. The dollar cost estimates ($0.008-$0.024 per 1% success gain) depend on provider pricing at time of study and are not informative about compute-equivalent comparisons.

## Connections

- **[[multiagent-debate]]**: Decentralized MAS implements debate. This paper quantifies when debate helps (+9.2% on web navigation) and when it hurts (-41.5% on sequential planning).
- **[[embedding-space-communication]]**: All communication in this framework is natural language. The "lossy communication" problem it identifies is exactly what latent methods address.
- **[[thought-structure]]**: The information gain metric (Bayesian posterior variance reduction) quantifies how much actionable information agents exchange — related to ThoughtComm's agreement-based routing.

## Source Materials

- [[raw/pdf/arxiv-2512.08296.pdf|PDF]] ([[raw/latex/arxiv-2512.08296.tar.gz|LaTeX source]])
