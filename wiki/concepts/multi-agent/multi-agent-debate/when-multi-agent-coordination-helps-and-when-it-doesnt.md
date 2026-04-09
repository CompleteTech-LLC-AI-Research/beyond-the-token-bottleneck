[[scaling-agent-systems|Towards a Science of Scaling Agent Systems]] provides the most systematic analysis of when MAS helps, with controlled experiments across 180 configurations ([[raw/pdf/arxiv-2512.08296.pdf|Kim et al. §4, Figure 2]]):

### Task-Contingent Value

| Task type | Best architecture | MAS effect | Why |
|-----------|------------------|------------|-----|
| Decomposable (Finance) | Centralized MAS | **+80.9%** | Naturally splits into parallel subtasks |
| Dynamic navigation (BrowseComp) | Decentralized MAS | **+9.2%** | Benefits from diverse exploration |
| Sequential state-dependent (PlanCraft) | **Single Agent** | **-39% to -70%** | Sequential reasoning cannot be parallelized; coordination overhead dominates |
| Tool-heavy (Workbench) | Single Agent | Marginal | Tool-coordination trade-off: 16-tool tasks suffer from overhead |

### Key Scaling Principles

- **Capability saturation**: When single-agent baselines exceed ~45% accuracy, coordination yields diminishing or negative returns
- **Error amplification**: Independent agents amplify errors 17.2×; centralized limits to 4.4× via validation bottlenecks
- **Agent count ceiling**: Beyond 3-4 agents under fixed budgets, per-agent reasoning quality degrades sharply (reasoning turns scale as $T = 2.72 \times (n+0.5)^{1.724}$)
- **Optimal overhead band**: 200-300% communication overhead; below = under-coordinated, above = diminishing returns

### Composable Primitives

[[agent-primitives-building-blocks|Agent Primitives]] addresses the task-architecture mismatch by making the structure composable: an Organizer selects from Review/Voting/Planning primitives per query, achieving +12-16.5% over single-agent across diverse benchmarks. This avoids the one-size-fits-all problem.
