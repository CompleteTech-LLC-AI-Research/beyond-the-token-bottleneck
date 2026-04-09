### Soft Tokens Are ~4× More Efficient Than Hard Tokens

SoftCoT achieves optimal performance with **6 soft thought tokens**, while the hard-token variant (Assist-CoT, where the assistant generates discrete text) needs **24 tokens** for comparable performance. This ~4× compression ratio is consistent with CCoT's reported 5× ratio, providing further evidence for the [[continuous-vs-discrete-representation|continuous vs. discrete information density gap]].

The compression mechanism differs qualitatively from Coconut's. In Coconut, the continuous thought encodes a **superposition** of possible reasoning paths (enabling emergent BFS). In SoftCoT, the soft tokens encode **condensed reasoning cues** — hints that bias the backbone's attention patterns without dictating a specific reasoning path. The backbone retains full autonomy over its discrete reasoning chain; the soft tokens function more like a continuous "preamble" that primes relevant associations. This explains why 6 tokens suffice: they need only shift the probability landscape, not carry the full reasoning trajectory.

### Assistant Model Size Barely Matters

| Assistant size | SoftCoT accuracy (GSM8K) |
|---------------|-------------------------|
| 0.5B | 85.76% |
| 1.5B | 85.81% |
| 7B | 85.84% |

Even a 0.5B assistant is nearly as effective as a 7B one. The assistant's role is to provide **reasoning cues** in continuous space, not to solve the problem. The backbone LLM does the actual reasoning.

### [UNK] Tokens as Pause Tokens

Adding raw (untrained) `[UNK]` tokens slightly improves accuracy (68.21% → 68.49%) and reduces variance, consistent with the pause token literature (Goyal et al., 2024). The extra forward-pass compute alone provides marginal benefit; the trained projection provides the real gains.
