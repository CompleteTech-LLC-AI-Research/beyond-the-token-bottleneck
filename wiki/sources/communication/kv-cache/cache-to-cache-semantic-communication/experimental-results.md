### Cross-Configuration Performance

Tested across model families (Qwen, LLaMA, Gemma), sizes (0.6B-14B), specializations (general, code, math), generations (Qwen2.5, Qwen3), and training stages (pretrained, instruction-tuned):

| Configuration | Acc. Gain over Receiver | Acc. Gain over T2T |
|--------------|------------------------|-------------------|
| Same family, different size | +6.4-14.2% | +3.1-5.4% |
| Different families | Consistent gains | Consistent gains |
| Base model as Sharer (can't follow instructions) | Significant gains | **C2C works; T2T fails** |
| Specialized → General | Effective knowledge transfer | Superior to T2T |

The "base model as Sharer" result is especially notable: a weaker instruction-tuned Receiver can leverage a stronger base model's knowledge via C2C even when the base model produces unusable text outputs. C2C bypasses the language bottleneck entirely.

### Effective Rank Analysis

After fusion, the KV-cache's **effective rank increases** (measured by rank of K and V matrices), indicating C2C enriches the Receiver's representations with new semantic dimensions rather than just reinforcing existing information.

### Efficiency

Compared to text-to-text:
- **2.5× average speedup** — eliminates the Sharer's sequential token decoding, replacing it with parallel cache fusion (~90ms)
- The Sharer only needs to run prefill (single forward pass), not autoregressive generation

### Scaling Behavior

- **Sequence length**: C2C consistently outperforms T2T across all sequence-length intervals on LongBench, demonstrating advantages for long-context tasks
- **Model size**: Accuracy improvements of C2C scale faster than T2T as Sharer size increases — richer KV-cache representations in larger models translate to greater gains
