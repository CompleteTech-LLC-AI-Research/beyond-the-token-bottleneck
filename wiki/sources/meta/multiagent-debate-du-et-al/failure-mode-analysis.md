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
