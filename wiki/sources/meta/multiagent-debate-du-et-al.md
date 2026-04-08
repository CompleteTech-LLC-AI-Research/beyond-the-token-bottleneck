---
type: source
title: "Improving Factuality and Reasoning in Language Models through Multiagent Debate"
source_file: "[[raw/pdf/arxiv-2305.14325.pdf]]"
latex_source: "raw/latex/arxiv-2305.14325/"
author: "Yilun Du, Shuang Li, Antonio Torralba, Joshua B. Tenenbaum, Igor Mordatch"
date_published: "2023-05-23"
date_ingested: "2026-04-06"
created: "2026-04-06"
updated: "2026-04-06"
venue: "arXiv preprint (under review)"
arxiv: "2305.14325"
institution: "MIT CSAIL, Google Brain"
tags: [multiagent-debate, foundational, reasoning, factuality]
---

# Improving Factuality and Reasoning in Language Models through Multiagent Debate

## Summary

The **foundational paper** for LLM [[multiagent-debate|multiagent debate]]. Established for the first time that having multiple LLM instances debate each other -- sharing responses, critiquing, and revising over multiple rounds -- improves both reasoning accuracy and factual correctness across diverse tasks. Nearly every paper in this wiki benchmarks against "NLD" (natural language debate) as introduced here. All experiments use ChatGPT (gpt-3.5-turbo) with black-box API access only.

## Core Mechanism

### Protocol

1. **Independent generation**: $N$ copies of an LLM each independently generate a candidate answer with reasoning.
2. **Response sharing**: Each agent's response is concatenated and provided to every other agent via a consensus prompt.
3. **Iterative debate**: Each agent reads all others' responses, critiques them, generates a revised answer. Repeated for $R$ rounds.
4. **Convergence**: Agents empirically converge to consensus. Default configuration: **3 agents, 2 rounds**.

### Prompt Templates

The paper specifies distinct starting and debate prompts for each task. The debate prompt follows a consistent structure across all tasks:

**Arithmetic starting prompt:** *"What is the result of {expression}? Make sure to state your answer at the end of the response."*

**Arithmetic debate prompt:** *"These are the recent/updated opinions from other agents: \<other agent responses\>. Use these opinions carefully as additional advice, can you provide an updated answer? Make sure to state your answer at the end of the response."*

**GSM8K starting prompt:** *"Can you solve the following math problem? \<Problem\> Explain your reasoning. Your final answer should be a single numerical number, in the form \\boxed\{answer\}, at the end of your response."*

**GSM8K debate prompt:** *"These are the solutions to the problem from other agents: \<other agent responses\> Using the solutions from other agents as additional information, can you provide your answer to the math problem? The original math problem is \<Problem\>."*

**MMLU starting prompt:** *"Can you answer the following question as accurately as possible? \{question\}: A) {}, B) {}, C) {}, D) {} Explain your answer, putting the answer in the form (X) at the end of your response."*

**MMLU debate prompt:** *"These are the solutions to the problem from other agents: \<other agent responses\> Using the reasoning from other agents as additional advice, can you give an updated answer? Examine your solution and that of other agents. Put your answer in the form (X) at the end of your response."*

### Convergence Control via Prompt Stubbornness

The paper identifies two prompt regimes that control debate dynamics:

- **Short prompts** (agents adapt quickly): Faster convergence but potentially lower accuracy. Agents tend to agree with the first plausible-sounding response.
- **Long prompts** (agents hold their ground): Slower convergence but higher final accuracy. Agents are instructed to maintain their reasoning unless genuinely convinced by another's argument.

Debates using longer prompts lead to slower convergence to correct answers, but also lead to better final consensus accuracy. This reveals the **agreeableness bias** inherent in RLHF-tuned models -- they are predisposed to agree, which can amplify errors.

### Response Summarization

For debates with 5+ agents, directly concatenating all responses exceeds context limits. The paper introduces **LLM-based summarization**: before each round, all agent responses are summarized by ChatGPT into a single condensed response that is then provided to each agent. This approach actually **improves** performance beyond direct concatenation, suggesting that summarization filters noise and highlights key reasoning patterns.

## Full Experimental Results

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

## Scaling Analysis

### Number of Agents

Performance on arithmetic monotonically increases from 1 to 6 agents. For 5+ agents, summarization replaces concatenation due to context length constraints. The summarization-based approach at 6 agents outperforms direct concatenation at 4 agents, suggesting the technique is complementary.

### Number of Rounds

Accuracy increases with debate rounds up to approximately 4 rounds, then plateaus. The paper notes diminishing returns: the first 1-2 rounds capture most of the benefit, with rounds 3-4 providing marginal improvements. Beyond 4 rounds, agents have typically converged and further debate produces no change.

### Persona Initialization

Using different initialization prompts (instructing each agent to behave as a professor, doctor, or mathematician) improved MMLU accuracy from **71.1% to 74.2%** -- a 3.1-point gain from prompt diversity alone. This suggests that heterogeneous agent perspectives improve the quality of debate by reducing the correlation of initial errors.

### CoT Synergy

Debate composes with other prompting techniques. On GSM8K:
- CoT alone: ~77%
- Debate alone (no CoT): ~78%
- **Debate + CoT: ~85%**

The orthogonality of debate and CoT confirms they address different failure modes: CoT improves individual reasoning quality, while debate provides error correction through cross-examination.

### Cross-Model Debate

ChatGPT and Bard jointly debated on 20 GSM8K problems:
- ChatGPT alone: 14/20
- Bard alone: 11/20
- **Joint debate: 17/20**

In qualitative analysis, cases where both agents initially answered incorrectly were resolved through cross-examination, with ChatGPT leveraging information from Bard's (incorrect) reasoning to arrive at the correct answer. This demonstrates that debate benefits from **diversity of model capabilities**, not just diversity of random initialization.

## Compute Overhead Analysis

The default configuration (3 agents, 2 rounds) requires approximately **9x** the compute of a single agent query:
- Round 0 (initial): 3 generations
- Round 1: 3 generations (each reading 2 other responses)
- Round 2: 3 generations (each reading 2 other responses)
- Total: 9 generation calls, plus the cost of concatenating/processing context

The context length grows substantially across rounds as agent responses accumulate. With summarization, context growth is controlled but an additional summarization call is required per round. The paper acknowledges this as the primary practical limitation.

## Failure Mode Analysis

### False Consensus

Agents can converge on incorrect answers with high confidence. Despite answers being wrong, language models confidently affirm consistency with all other agents. The paper attributes this partly to the fact that LLMs do not correctly express uncertainty when generating responses.

### Agreeableness Bias

RLHF-tuned models are predisposed to agree with other agents, which can amplify errors rather than correct them. When agents were asked about their confidence directly, they consistently reported high confidence regardless of actual accuracy. However, the **ease of persuasion** during debate provides a more reliable signal -- on facts the model was confident about, agents strongly resisted changing their opinion, while uncertain facts led to rapid opinion shifts.

### Context Degradation

As debates grow longer, agents tend to focus on the most recent generations and lose track of earlier reasoning. The summarization approach partially mitigates this but does not fully solve it. The paper suggests that longer-context models or more sophisticated summarization strategies would help.

### Limited Model and Sample Diversity

- Only tested on ChatGPT (one cross-model experiment with Bard on 20 problems)
- **100 samples per benchmark** -- relatively small evaluation, with wide variance bars
- Zero-shot evaluation only (no in-context learning or fine-tuning for debate)

## What This Paper Established for the First Time

1. **First empirical proof that LLM debate improves reasoning and factuality** -- prior work (Irving et al. 2018) was theoretical with human judges
2. **Debate is not just voting** -- cross-examination of reasoning enables error correction even when all agents start wrong
3. **The "society of minds" framing for LLMs** -- drawing on Minsky, introduced the idea of LLM instances as a deliberative group
4. **Black-box composability** -- same prompts and procedure across all tasks, API access only
5. **The experimental template** -- systematically varied agents, rounds, prompts, summarization, cross-model, CoT compatibility. Nearly all subsequent papers follow this template.

## Limitations

- **Small model set**: All main experiments use a single model (ChatGPT / gpt-3.5-turbo). The only cross-model experiment (ChatGPT + Bard) uses 20 GSM8K problems — far too small for statistical reliability. No experiments with open-weight models, no analysis of how model scale affects debate dynamics.
- **Limited benchmark diversity**: Six tasks across arithmetic, math word problems, chess, biographies, MMLU, and chess move validity. No code generation, no scientific reasoning, no open-ended generation. The 100-sample evaluation size per benchmark yields wide confidence intervals (e.g., $\pm$ 4.7pp on arithmetic).
- **No cost-controlled comparisons**: The 9x compute overhead (3 agents x 3 rounds) is acknowledged but never compared against baselines at equivalent compute budgets. Self-consistency with 9 samples, or a single agent with 9x the thinking tokens, could provide fairer baselines. The paper does not establish that debate is compute-efficient relative to alternatives.
- **Text-only communication**: All inter-agent exchange is natural language — the information loss, context degradation, and agreeableness bias problems identified by the paper are inherent to this communication channel. The paper does not consider whether richer communication (embeddings, activations, KV-cache) could mitigate these failure modes.
- **Zero-shot only**: No in-context learning or fine-tuning experiments. Whether debate benefits change with few-shot prompting or task-specific fine-tuning is unknown.
- **No analysis of failure distribution**: The paper reports aggregate accuracy but does not analyze which problem types benefit most from debate, whether debate introduces new failure modes, or whether the improvement is uniform or concentrated on specific problem subtypes.

## Why Every Other Paper References This

This paper defined the problem, the protocol, and the evaluation framework. When [[cipher-multiagent-debate-embeddings|CIPHER]] proposes embedding-based debate, when [[kvcomm-kth-selective|KVComm]] benchmarks against NLD, when [[activation-communication-harvard|AC]] compares compute efficiency to debate, when [[scaling-agent-systems|Scaling Agent Systems]] formalizes "Decentralized MAS" -- they are all benchmarking against Du et al.'s protocol.

The limitations of this paper are exactly what motivated the latent communication research line: the **information loss** in natural language exchange (motivating [[cipher-multiagent-debate-embeddings|CIPHER]]), the **compute cost** of sequential token generation (motivating [[activation-communication-harvard|AC]]), the **agreeableness bias** in text debate (motivating ThoughtComm's structured routing), and the **context degradation** over rounds (motivating KV-cache approaches).

## Source Materials

- [[raw/pdf/arxiv-2305.14325.pdf|PDF]] (`raw/latex/arxiv-2305.14325/`)
