1. **Initial round**: Each agent independently generates a response to the question.
2. **Debate rounds**: Each agent receives all other agents' responses concatenated with the original prompt, and generates a refined response.
3. **Final answer**: Agents typically converge to a consensus. When they don't, majority voting or selection of the lowest-temperature agent's response is used.

### Formal Description

Given *n* debaters D₁...Dₙ and *R* rounds:
- **Round 1**: resᵢ ← Dᵢ(prompt) for each agent *i*
- **Round r > 1**: prompt' ← concat(prompt, res₁, ..., resₙ); resᵢ ← Dᵢ(prompt') for each agent *i*
- **Output**: Aggregate(res₁, ..., resₙ) — typically majority vote or lowest-temperature selection

The protocol is identical for natural language and embedding communication; only the representation of `resᵢ` changes.
