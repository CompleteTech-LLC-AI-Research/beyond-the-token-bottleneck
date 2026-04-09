**Sequential MAS** (4 agents): Planner → Critic → Refiner → Solver. Each agent receives the previous agent's latent working memory via KV-cache prepending. Only the Solver decodes text.

**Hierarchical MAS** (4 agents): Math Agent, Science Agent, and Code Agent operate in parallel on the same question. A Summarizer agent then receives all three agents' latent working memories (concatenated) and produces the final text answer.
