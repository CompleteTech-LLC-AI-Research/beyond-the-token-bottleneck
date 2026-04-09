Tested on BrowseComp-Plus with high-capability (GPT-5, Sonnet 4.5, Gemini 2.5 Pro) and low-capability (GPT-5 nano, Sonnet 3.7, Gemini 2.0 Flash) models.

Key findings:
- **Centralized**: Sub-agent capability matters more than orchestrator capability across all families. Low orchestrator + high sub-agents outperforms high orchestrator + low sub-agents.
- **Anthropic uniquely benefits from heterogeneous centralized**: low-capability orchestrator + high-capability sub-agents (0.42) outperforms homogeneous high-capability (0.32) by 31%.
- **Decentralized mixed-capability approaches near-optimal**: OpenAI mixed 0.53 vs. homogeneous-high 0.50; Anthropic mixed 0.47 vs. 0.37; Google mixed 0.42 vs. 0.43.
- OpenAI and Google show performance degradation under heterogeneous centralized configurations.
