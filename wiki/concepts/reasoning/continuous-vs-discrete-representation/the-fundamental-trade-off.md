LLMs are internally continuous systems (dense vector representations in $\R^d$ at every layer) that are forced to interface with the world through a discrete bottleneck (token sampling). This creates a fundamental trade-off:

| Property | Discrete (tokens) | Continuous (vectors) |
|----------|-------------------|---------------------|
| Information density | ${\sim}\log_2(V)$ bits per position ($V$ = vocab size) | $d$ floating-point values per position |
| Expressiveness | One choice per position | Superpositions of choices |
| Composability | Symbolic, combinatorial | Geometric, algebraic |
| Interpretability | Human-readable | Requires probing/decoding |
| Universality | Any system can process text | Requires compatible architecture |
| Error properties | Discrete errors (wrong token) | Continuous errors (drift, distortion) |
