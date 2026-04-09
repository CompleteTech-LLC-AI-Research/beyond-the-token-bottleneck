### Number of Rounds (Figure 4a)

2 LLaMA2-70B debaters on Arithmetic dataset. Approximate values from the plot:

| Rounds | CIPHER | NLD |
|---|---|---|
| 1 | ~79% | ~79% |
| 2 | ~82% | ~78% |
| 3 | ~85% | ~81% |
| 4 | ~84% | ~82% |
| 5 | ~84% | ~82% |
| 6 | ~85% | ~83% |

Both methods show diminishing returns beyond round 3. CIPHER maintains a consistent ~2-3% advantage at every round count.

**Temperatures for extended rounds (Table 6):** NLD uses (0.013, 1.072); CIPHER uses (0.498, 1.725).

### Number of Debaters (Figure 4b)

LLaMA2-70B on GSM8K dataset, 3 rounds. Approximate values from the plot:

| Debaters | CIPHER | NLD |
|---|---|---|
| 2 | ~66% | ~65% |
| 3 | ~70% | ~68% |
| 4 | ~72% | ~70% |

More debaters help both methods, with CIPHER maintaining its edge.

**Temperatures for debater scaling (Table 7):**

| Debaters | NLD | CIPHER |
|---|---|---|
| 2 | (0.100, 0.500) | (0.250, 0.600) |
| 3 | (0.300, 0.500, 0.700) | (0.001, 0.725, 1.067) |
| 4 | (0.442, 0.176, 0.745, 0.539) | (0.641, 0.464, 0.507, 0.202) |
