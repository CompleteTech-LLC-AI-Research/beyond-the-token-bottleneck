### Deltas vs Raw Hidden States (Table 4)

Replacing state deltas with raw hidden states $h^l_{A,i}$ (the "w/o delta" variant) consistently degrades performance. In several cases, raw states fall **below the NL baseline**, demonstrating that unprocessed hidden states introduce noise from the sender's context:

| Model | Method | Quasar-T EM | CWQ EM | College Math | Formal Logic |
|-------|--------|------------|--------|-------------|-------------|
| **Qwen-7B** | NL | 0.305 | 0.312 | 0.362 | 0.476 |
| | w/o delta | 0.295 | 0.313 | 0.403 | 0.462 |
| | **SDE** | **0.315** | **0.317** | **0.443** | **0.520** |
| **Llama-8B** | NL | 0.285 | 0.325 | 0.245 | 0.389 |
| | w/o delta | 0.275 | **0.297** | 0.247 | 0.394 |
| | **SDE** | **0.305** | **0.352** | **0.297** | **0.422** |

Key findings: Llama-8B CWQ drops from NL 0.325 to raw states **0.297** (-2.8pp below NL), while SDE reaches **0.352** (+2.7pp above NL). This is the strongest evidence that deltas, not raw states, are the correct abstraction -- the differential signal captures reasoning dynamics while stripping context-specific noise.

### Layer Selection Strategies (Figure 2, Appendix C)

Tested on Qwen2.5-14B with StrategyQA (IA) and Formal Logic (debate):

- **Combined top-k** (k <= 4): Stable performance, little variation as k increases from 1 to 4. Best balance of robustness and generality.
- **Only top-k** (single layer at rank k): Inconsistent -- performance varies unpredictably across ranks and tasks. E.g., on Qwen-7B Formal Logic, performance decreases from rank-1 to rank-4 but unexpectedly rises at rank-5.
- **All layers**: Significant performance drop in all cases -- excessive disruption of the model's internal representations.

Recommendation: Apply 1-3 combined top-ranking layers. Avoid single-layer selection (unstable) and all-layer modification (harmful).

### Agents and Rounds Scaling (Table 5, Formal Logic, Qwen2.5-7B)

**Varying agents** (3 rounds fixed):

| Agents | NL | CIPHER | SDE |
|--------|------|--------|------|
| 2 | 0.476 | 0.488 | **0.520** |
| 3 | 0.449 | 0.431 | **0.515** |
| 4 | 0.453 | 0.437 | **0.518** |
| 5 | 0.495 | 0.432 | **0.514** |

**Varying rounds** (2 agents fixed):

| Rounds | NL | CIPHER | SDE |
|--------|------|--------|------|
| 2 | 0.452 | 0.488 | **0.513** |
| 3 | 0.476 | 0.488 | **0.520** |
| 4 | 0.454 | 0.488 | **0.523** |
| 5 | 0.460 | 0.488 | **0.521** |

SDE maintains a **consistent advantage** across all configurations (0.513-0.523), while NL fluctuates significantly (0.449-0.495) and CIPHER stays flat (it produces identical embeddings across rounds when temperature is fixed). SDE is robust to variations in agent count and round count.
