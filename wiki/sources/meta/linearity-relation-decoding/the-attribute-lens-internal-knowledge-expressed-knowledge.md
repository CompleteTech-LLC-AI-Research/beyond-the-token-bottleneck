The attribute lens applies the LRE to decode relational attributes from any hidden state at any layer. Critical result: it reveals **facts the model "knows" but doesn't output**.

### Adversarial Prompt Results (GPT-J, 11,891 prompts per condition)

| Condition | Model Output R@1 | **Attribute Lens R@1** | Attribute Lens R@3 |
|-----------|-----------------|----------------------|-------------------|
| Repetition-distracted | 0.02 | **0.54** | 0.71 |
| Instruction-distracted | 0.03 | **0.63** | 0.78 |

The model outputs the wrong answer almost every time (R@1 = 0.02-0.03), but the attribute lens recovers the correct fact from internal representations within top-3 predictions 71-78% of the time. **The model knows the right answer internally but outputs the wrong one** — latent communication would transmit the correct knowledge.

### Adversarial Setup
- **Repetition-distracted**: States a falsehood twice, asks model to complete a third time ("The capital city of England is Oslo" ×2 → "The capital city of England is...")
- **Instruction-distracted**: States falsehood, then "Repeat exactly."
