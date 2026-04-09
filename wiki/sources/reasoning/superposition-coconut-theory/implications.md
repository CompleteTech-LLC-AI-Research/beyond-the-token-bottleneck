1. **[[continuous-vs-discrete-representation|Continuous]] latent reasoning is provably more efficient** than discrete CoT for graph-structured problems: $D$ steps vs $O(n^2)$, potentially exponential gap for sparse graphs (where $D$ can be $O(\log n)$ while $n^2$ remains quadratic).

2. **Superposition is a computational mechanism**, not just a metaphor -- the quantum analogy is mathematically precise. Each continuous thought literally encodes a probability distribution over reachable states.

3. **2-layer continuous CoT outperforms 12-layer discrete CoT** on graph reachability -- latent reasoning substitutes for model depth, confirming and extending the depth-expressivity connection from [[cot-expressivity-theory|Feng et al. (2023)]].

4. **Many reasoning problems** (planning, knowledge graphs, multi-hop QA) reduce to graph reachability, so the superposition advantage may generalize broadly.

5. **BFS emerges without explicit supervision** -- models discover efficient algorithms never demonstrated in training data, suggesting that continuous thought representations have an inductive bias toward parallel search strategies.
