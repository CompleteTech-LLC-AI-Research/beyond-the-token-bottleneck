The default configuration (3 agents, 2 rounds) requires approximately **9x** the compute of a single agent query:
- Round 0 (initial): 3 generations
- Round 1: 3 generations (each reading 2 other responses)
- Round 2: 3 generations (each reading 2 other responses)
- Total: 9 generation calls, plus the cost of concatenating/processing context

The context length grows substantially across rounds as agent responses accumulate. With summarization, context growth is controlled but an additional summarization call is required per round. The paper acknowledges this as the primary practical limitation.
