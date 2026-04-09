### Knowledge Transfer Tasks (MMLU)
C2C shows strongest gains when the Sharer encodes domain-specific knowledge the Receiver lacks. For a math-specialized Sharer → general Receiver pair, MMLU-STEM improves by +14.2% while MMLU-Humanities shows only +3.1% — the Receiver selectively absorbs the Sharer's domain expertise through the learned gate.

### Base Model as Sharer (Unique Capability)
When a pretrained base model (cannot follow instructions, produces incoherent text) serves as Sharer to an instruction-tuned Receiver, C2C achieves significant accuracy gains while text-to-text (T2T) communication **completely fails** (the base model's generated text is unusable). This demonstrates that KV-cache representations capture knowledge independently of the model's ability to articulate that knowledge in language — a direct validation of the [[continuous-vs-discrete-representation|continuous over discrete]] thesis.

### Long-Context Tasks (LongBench)
Across all sequence-length intervals on LongBench, C2C consistently outperforms T2T. The advantage grows with sequence length because T2T's sequential decoding cost scales linearly with context length while C2C's parallel cache fusion remains near-constant (~90ms).
