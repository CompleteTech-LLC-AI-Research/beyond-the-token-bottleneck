1. **GSM8K is the de facto universal benchmark** but is saturating. 14 of 18 empirical papers test on it. At 7B+ scale with multi-agent methods, accuracy exceeds 90%, limiting discriminative power.

2. **No benchmark is tested by more than 14 papers**. The field lacks a truly universal evaluation suite. MATH, GPQA, and code generation benchmarks are severely underrepresented relative to their importance.

3. **Scale confounds all comparisons**. Papers test at wildly different scales (GPT-2 117M to DeepSeek-R1 70B), making cross-paper accuracy comparisons misleading. Controlled comparisons on the same base model are rare.

4. **Communication papers test more broadly than reasoning papers**. Reasoning papers ([[coconut-reasoning-latent-space|Coconut]], [[icot-internalize-cot|iCoT]], [[pause-tokens|Pause Tokens]]) test on 2-4 benchmarks; communication papers ([[state-delta-trajectory|SDE]], [[agent-primitives-building-blocks|Agent Primitives]], [[latentmas-collaboration|LatentMAS]]) test on 6-10. This reflects different maturity levels: reasoning methods are still proving basic viability; communication methods are demonstrating generality.

5. **Critical blind spots**: open-ended generation, multilingual tasks, safety benchmarks, long-context reasoning, and real-world agent environments are all untested. These gaps mean the field cannot yet claim that latent methods work "in general" -- only on closed-form reasoning tasks.

6. **The Qwen family dominates recent work**. 10 papers use Qwen models, making it the most common evaluation platform. This introduces a risk of method overfitting to Qwen-specific architectural properties (e.g., Qwen's resilience to RoPE misalignment vs. LLaMA's catastrophic sensitivity, as documented by [[agent-primitives-building-blocks|Agent Primitives]]).
