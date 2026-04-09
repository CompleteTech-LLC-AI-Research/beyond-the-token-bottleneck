Prior approaches to latent communication ([[cipher-multiagent-debate-embeddings|CIPHER]], [[activation-communication|activation sharing]]) treat communication as a uniform broadcast — every agent sends the same representation to every other agent. [[thought-communication-multiagent|ThoughtComm]] argues this is insufficient because:

1. **Not all thoughts are relevant to all agents**: In a multi-agent system, different agents may focus on different aspects of a problem. Sending irrelevant information wastes bandwidth and can confuse the receiver.
2. **Shared vs. private information serves different roles**: Common ground (shared thoughts) enables coordination; private thoughts enable novelty and complementary reasoning.
3. **Agreement level signals reliability**: A thought shared by 4 out of 5 agents is more likely to be correct than one held by a single agent — but the single agent's thought may also be the key insight everyone else missed.
