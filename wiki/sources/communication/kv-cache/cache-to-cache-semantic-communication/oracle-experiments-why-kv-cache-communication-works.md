C2C's design is motivated by three oracle experiments:

### 1. Cache Enrichment

Few-shot prompting improves accuracy — but why? Is it because the model attends to more context tokens, or because the exemplars **enrich the KV-cache semantics** of the question tokens?

The oracle test: prefill with exemplars + question, then **discard the exemplar cache** and decode with only the question-aligned slice (same cache size as no exemplars). Result: **accuracy improves at the same cache length**. The exemplars permanently alter how the question is encoded in the KV-cache — richer embeddings, not just more attention targets.

### 2. Layer-Wise Variation

Cache enrichment has dramatically different effects across layers — some layers benefit, others are harmed. Selectively enriching only the **top-performing layers** (top-5) yields slightly higher accuracy than enriching all layers, while targeting the worst layers degrades performance. This motivates C2C's per-layer gating mechanism.

### 3. Cross-Model Cache Convertibility

A 3-layer MLP can successfully project KV-cache from Qwen3-4B into the representation space of Qwen3-0.6B. T-SNE visualizations show the transformed cache falls within the target model's representation space. However, the transformed cache occupies only a **subset** of the target's space — reflecting that one model's semantics cannot fully cover another's. The correct-answer sets of different models show limited overlap despite comparable aggregate accuracy, confirming **complementary strengths**.
