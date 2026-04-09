The paper introduces **ProsQA** (Proof with Search Question-Answering), a logical reasoning dataset built on directed acyclic graphs (DAGs):

- ~23 nodes, ~36 edges per graph
- Average shortest path length: 3.8 steps
- ~1.6 shortest paths on average (multiple valid routes)
- Binary questions: "Is [Entity] a [Concept A] or [Concept B]?"
- Key challenge: **distractor branches** — the DAG structure creates many plausible-looking wrong paths

ProsQA is specifically designed to test planning ability — a model must navigate a graph with many dead ends, requiring look-ahead or backtracking. This is exactly where CoT's greedy nature fails and Coconut's emergent BFS excels.
