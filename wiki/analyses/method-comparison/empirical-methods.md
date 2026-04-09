### Reasoning Methods (Intra-Agent)

| Method | Channel | Training | Cross-Arch | Compute vs NL | Scale Tested | Key Result |
|--------|---------|----------|------------|---------------|-------------|------------|
| [[coconut-reasoning-latent-space\|Coconut]] | Hidden-state feedback | Yes (multi-stage curriculum) | No | 3–10× fewer tokens | GPT-2 | ProsQA 97.0% (+19.5pp vs CoT) |
| [[icot-internalize-cot\|iCoT]] | Implicit compression | Yes (progressive removal) | No | 11× inference speedup | GPT-2 Small, Mistral 7B | GSM8K 51% no visible reasoning |
| [[softcot-efficient-reasoning\|SoftCoT]] | Soft embeddings | Yes (projection only, frozen backbone) | Yes (any backbone) | 4× token compression | LLaMA-3.1-8B, Qwen2.5-7B | +2.31pp avg, preserves instruction tuning |
| [[thinking-states-latent-reasoning\|Thinking States]] | Compressed NL → states | Yes (teacher forcing) | No | 2.66× speedup | Qwen2.5-0.5B/1.5B | OOD generalization 97.71% |
| [[pause-tokens\|Pause Tokens]] | Learnable embeddings | Yes (pretraining + finetune) | No | Minimal (width only) | 130M, 1B | SQuAD +19.5 EM pts |

### Diagnostic & Inference-Time Augmentations

| Method | Target | Training | What It Tests | Scale | Key Result |
|---|---|---|---|---|---|
| [[latent-reasoning-supervision-analysis\|Cui et al. (Improved Coconut)]] | COCONUT, CODI, SIM-CoT, CoLaR | Modified curriculum (Coconut only) | Shortcut behavior + BFS hypothesis + supervision–exploration trade-off | GPT-2, LLaMA-3.2-1B | Improved Coconut +7pp on GSM8K-Aug; falsifies iterative BFS |
| [[inference-time-scaling-continuous-reasoning\|Wang et al. (PRM/ORM Reranking)]] | COCONUT | PRM (hard + soft) + ORM via MATH-Shepherd MC annotation | Whether discrete-space inference-time scaling transfers to continuous space | GPT-2 | Pass@32 = 44.43%; best reranker recovers only 19.8% of headroom; geometric homogeneity diagnosed (IsoScore$\star \approx 0.013$) |

### Communication Methods (Inter-Agent)

| Method | Channel | Training | Cross-Arch | Compute vs NL | Scale Tested | Key Result |
|--------|---------|----------|------------|---------------|-------------|------------|
| [[multiagent-debate-du-et-al\|Du et al. NLD]] | Natural language | No | Yes (universal) | 9× cost (baseline) | ChatGPT | GSM8K +8pp over single |
| [[cipher-multiagent-debate-embeddings\|CIPHER]] | Output embeddings | No | Shared tokenizer | ~Same | LLaMA-65B, Falcon-40B | +0.5–5.0% over NLD |
| [[state-delta-trajectory\|SDE]] | Hidden-state deltas | No | Same model only | Selective (1–3 layers) | Qwen2.5-7B/14B, LLaMA-8B | College Math +7.3pp over CIPHER |
| [[thought-communication-multiagent\|ThoughtComm]] | Disentangled latents | Yes (autoencoder + prefix) | Same embedding dim | Independent of model size | 0.6B–8B (5 models) | MATH 93.0% (vs 43.6% single) |
| [[activation-communication-harvard\|AC]] | Single-layer activation | Optional (3K samples) | Yes (cross-family) | <¼ compute | 1.5B–9B (3 families) | 48/57 MMLU > NLD |
| [[interlat-latent-space-agents\|Interlat]] | Full hidden-state seq. | Yes (curriculum + 3-loss) | Yes (with adapter) | $2600\times$ bandwidth, $46\times$ speedup | Qwen2.5-7B | ALFWorld 70.48%/65.42% |
| [[kvcomm-kth-selective\|KVComm]] | KV-cache (selected) | No (calibration only) | Same architecture | 30% layers $\approx$ full | 3B–8B (9 pairs) | HotpotQA F1 0.57 vs NLD 0.43 |
| [[cache-to-cache-semantic-communication\|C2C]] | KV-cache (fused) | Yes (per-pair fuser) | Yes (cross-family) | 2.5× speedup | 0.6B–14B (3 families) | +6.4–14.2% vs receiver alone |
| [[kv-cache-alignment-shared-space\|KV Alignment]] | KV-cache (shared space) | Yes (per-model adapter) | Yes (via shared space) | ~¼ model size adapter | Gemma-2 100M–400M | Self-improvement effect; zero-shot extensibility |
| [[kvcomm-duke-online-reuse\|KVCOMM-online]] | KV-cache (offset reuse) | No | Same model | 6.7× prefill speedup | Multi-agent systems | 7.8× speedup, <2.5% quality drop |

### Unified Methods (Reasoning + Communication)

| Method | Channel | Training | Cross-Arch | Compute vs NL | Scale Tested | Key Result |
|--------|---------|----------|------------|---------------|-------------|------------|
| [[latentmas-collaboration\|LatentMAS]] | Hidden-state + KV-cache | No (ridge regression) | Homogeneous only | $4\text{--}4.3\times$ faster | Qwen3-4B/8B/14B | GSM8K 95.2% (+11.5pp vs single) |
| [[vision-wormhole-heterogeneous\|Vision Wormhole]] | VLM visual pathway | Weak (<100 anchors) | Yes (heterogeneous) | 1.87–5.47× speedup | 1.6B–12B | +6.3pp vs TextMAS, +13.2pp code |
| [[agent-primitives-building-blocks\|Agent Primitives]] | KV-cache + RoPE | No (in-context learning) | Yes (cross-family) | 3–4× token reduction | 8B–70B | 75.3% vs 58.8% single (+16.5pp) |
