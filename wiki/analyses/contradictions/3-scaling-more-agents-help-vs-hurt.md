**Claim A**: [[multi-agent-debate|Multi-agent debate]] consistently improves over single agents. Du et al. shows +8pp on GSM8K; LatentMAS shows +11.5pp; ThoughtComm scales positively with more rounds.
— [[multiagent-debate-du-et-al|Du et al.]], [[latentmas-collaboration|LatentMAS]], [[thought-communication-multiagent|ThoughtComm]]

**Claim B**: Multi-agent scaling is **task-contingent**, not monotonic. Benefits range from +80.9% (finance) to **-70%** (sequential planning). Capability saturation occurs at ~45% single-agent accuracy.
— [[scaling-agent-systems|Scaling Agent Systems (Kim et al., 2025)]]

**Status**: **Complementary, different task distributions**. The debate papers primarily test math/reasoning benchmarks where single-agent accuracy is in the 40–85% range — exactly the regime where the [[scaling-agent-systems|Scaling]] paper predicts multi-agent benefits. The -70% finding is for sequential planning tasks with strong error propagation, which debate papers don't test.

**Resolution needed**: Apply latent communication methods to the Scaling paper's full 180-configuration benchmark set, including the task types where text-based MAS fails. Latent communication's reduced information loss may shift the crossover points.

---
