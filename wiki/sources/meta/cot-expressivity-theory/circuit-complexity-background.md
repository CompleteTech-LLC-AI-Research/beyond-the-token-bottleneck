The paper frames transformer expressivity through the lens of **circuit complexity classes**, which classify Boolean functions by the resources required by families of circuits:

| Complexity Class | Definition | Relevant Computation |
|-----------------|-----------|---------------------|
| **$\text{TC}^0$** | Constant-depth, polynomial-size circuits with threshold gates | What bounded-depth log-precision transformers can compute |
| **$\text{NC}^1$** | $O(\log n)$-depth, polynomial-size circuits with bounded fan-in | Arithmetic expression evaluation, linear equation solving |
| **$\text{P}$** | Polynomial-time Turing machines (equivalent to polynomial-depth circuits) | General dynamic programming, CFG membership testing |

The key separation assumption is $\text{TC}^0 \neq \text{NC}^1$, widely believed since Yao (1989). This means constant-depth threshold circuits (and hence bounded-depth transformers) cannot simulate logarithmic-depth computations. The **log-precision transformer** model used throughout the paper restricts internal neurons to $O(\log n)$ bit precision, matching practical implementations where machine precision (16 or 32 bits) is much smaller than input length.
