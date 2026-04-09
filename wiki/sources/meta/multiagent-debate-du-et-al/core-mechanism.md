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
