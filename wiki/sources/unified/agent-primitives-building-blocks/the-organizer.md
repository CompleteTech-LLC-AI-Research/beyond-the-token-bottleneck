The Organizer is an LLM (default: **GPT-5.2**) that automates MAS construction. It does not solve the task itself.

### Selection Process

Given an input query, the Organizer:
1. Analyzes task requirements and complexity
2. Retrieves relevant entries from the Knowledge Pool based on the input query
3. Abstracts retrieved MAS systems into primitive compositions, replacing task-specific agents with corresponding Agent Primitives
4. Determines (i) which primitive types to instantiate and (ii) their execution structure / composition order
5. Outputs a primitive composition plan specifying instantiated primitives and their composition in code

The number of agents is **not fixed** — it is determined per query by the Organizer (unlike baselines which use 4 agents).

### Knowledge Pool

The Knowledge Pool stores **45 MAS structures** collected from 5 existing MAS frameworks:
- **Multi-Agent Debate** (Du et al., 2023)
- **DyLAN** (Liu et al., 2024)
- **Self-Refine** (Madaan et al., 2023)
- **AFlow** (Zhang et al., 2024a)
- **MAS-GPT** (Ye et al., 2025)

Each entry associates a query pattern with a corresponding system-level reasoning strategy. The Organizer uses these as structural guidance, not as direct reuse of full agent-level designs.
