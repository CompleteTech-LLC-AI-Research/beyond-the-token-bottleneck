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
