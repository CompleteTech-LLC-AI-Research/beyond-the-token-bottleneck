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
