| Consideration | Low diversity (similar $T$) | High diversity (spread $T$) |
|--------------|---------------------------|---------------------------|
| Individual agent quality | All agents are reasonable | Explorer agent produces poor standalone output |
| Information complementarity | Low — redundant signals | High — anchor provides focus, explorer provides alternatives |
| Sensitivity to medium | Works in both NL and embedding | Only works in embedding communication |
| Optimization difficulty | Fewer hyperparameters | Bayesian optimization over temperature pairs needed |
| Robustness | Degrades gracefully | Sensitive to exact temperature values (narrow optimal region on some tasks) |
| Interpretability | Both agents' outputs are human-readable | Only anchor agent's output is interpretable |
