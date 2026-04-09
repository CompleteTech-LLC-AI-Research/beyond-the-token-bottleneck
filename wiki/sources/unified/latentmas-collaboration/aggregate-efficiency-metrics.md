**Sequential MAS averages**:
- Accuracy: +14.6% over single, +2.8% over TextMAS
- Token reduction: 70.8% fewer than TextMAS
- Speed: 4.0× faster (range 2.6×-7.0×)

**Hierarchical MAS averages**:
- Accuracy: +13.3% over single, +4.6% over TextMAS
- Token reduction: 83.7% fewer than TextMAS
- Speed: 4.3× faster (range 2.0×-7.7×)

LatentMAS also uses **15.0%-60.3% fewer tokens than single agents** because it distributes the question across agents, with only the final agent decoding a short answer.

Per-benchmark speedup factors (Hierarchical, Qwen3-14B): ARC-E 3.8×, ARC-C 3.9×, GSM8K 2.3×, MedQA 6.1×, MBPP+ 3.7×, HumanEval+ 3.4×, AIME24 4.0×, AIME25 5.7×, GPQA 6.3×.
