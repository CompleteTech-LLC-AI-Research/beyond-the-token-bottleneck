### Reasoning Tasks (3 agents, 2 rounds)

| Task | Single Agent | Self-Reflection | Majority Vote (3 agents) | **Debate (3 agents, 2 rounds)** |
|------|-------------|-----------------|--------------------------|--------------------------------|
| Arithmetic | 67.0% $\pm$ 4.7 | 72.1% $\pm$ 4.5 | 69.0% $\pm$ 4.6 | **81.8% $\pm$ 2.3** |
| GSM8K | 77.0% $\pm$ 4.2 | 75.0% $\pm$ 4.3 | 81.0% $\pm$ 3.9 | **85.0% $\pm$ 3.5** |
| Chess ($\Delta$PS) | 91.4 $\pm$ 10.6 | 102.1 $\pm$ 11.9 | 102.2 $\pm$ 6.2 | **122.9 $\pm$ 7.6** |

The arithmetic task evaluates expressions with six two-digit numbers (addition, multiplication, subtraction). Chess move prediction uses the first 14 moves from grandmaster games in PGN notation, evaluated by Stockfish pawn score advantage ($\Delta$PS). All evaluations are zero-shot.

### Factuality Tasks (3 agents, 2 rounds)

| Task | Single Agent | Self-Reflection | **Debate (3 agents, 2 rounds)** |
|------|-------------|-----------------|--------------------------------|
| Biographies | 66.0% $\pm$ 2.2 | 68.3% $\pm$ 2.9 | **73.8% $\pm$ 2.3** |
| MMLU | 63.9% $\pm$ 4.8 | 57.7% $\pm$ 5.0 | **71.1% $\pm$ 4.6** |
| Chess Move Validity | 29.3% $\pm$ 2.6 | 38.8% $\pm$ 2.9 | **45.2% $\pm$ 2.9** |

The biography task evaluates 524 computer scientists' bullet-point biographies against ground truth. MMLU uses the standard multiple-choice exam benchmark. Chess move validity measures whether proposed moves are legal given the board state (BIG-Bench Chess-State Tracking).

### Critical Distinctions Established

**Debate is not majority voting.** Debate outperforms majority vote because agents can **change their minds** through cross-examination of reasoning. The paper shows cases where **all agents start wrong** but arrive at the correct answer through debate -- something majority voting cannot do. In qualitative examples on GSM8K, all three agents initially produce incorrect arithmetic, but through iterative critique of each other's reasoning steps, they identify and correct errors.

**Debate > self-reflection.** Single-agent self-reflection sometimes **hurts** performance (MMLU: 63.9% $\to$ 57.7%, a 6.2-point degradation). The paper hypothesizes this occurs because a single agent lacks genuine diversity of reasoning -- it tends to reinforce its own errors rather than discovering alternative solution paths. Debate provides genuine cognitive diversity through independent initial reasoning.
