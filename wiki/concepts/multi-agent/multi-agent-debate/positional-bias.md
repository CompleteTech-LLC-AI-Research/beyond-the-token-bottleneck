An underappreciated factor: the **order** in which other agents' responses are concatenated into the prompt affects outcomes. [[cipher-multiagent-debate-embeddings|CIPHER]] investigates this and finds:
- When debaters operate at **similar temperatures**, order effects are negligible.
- When debaters are **diverse** (different temperatures or capabilities), order matters significantly.
- Both NLD and CIPHER show this effect, suggesting it's a property of the debate protocol, not the communication medium.

This connects to the broader "lost in the middle" phenomenon in LLMs — information in certain positions of the context window is attended to more strongly.
