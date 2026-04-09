### Token Usage (averages across 8 benchmarks)

| Model | Single | TextMAS | LatentMAS | Primitives MAS |
|-------|--------|---------|-----------|----------------|
| Qwen3-4B | 5,238 | 14,343 (+174.0%) | 3,280 (-37.4%) | 3,350 (-36.0%) |
| Qwen3-8B | 5,411 | 14,923 (+175.8%) | 3,457 (-36.1%) | 3,558 (-34.3%) |
| Qwen3-14B | 4,572 | 13,752 (+200.8%) | 4,330 (-5.3%) | 4,221 (-7.7%) |
| DS-R1-Qwen-32B | 4,854 | 11,396 (+134.8%) | 4,028 (-17.0%) | 4,195 (-13.6%) |
| DS-R1-Llama-70B | 5,268 | 16,268 (+208.7%) | 4,533 (-14.0%) | 4,922 (-6.6%) |

TextMAS uses **2-3x more tokens** than single agent. Primitives MAS uses **fewer tokens than single agent** on smaller models and comparable tokens on larger ones. LatentMAS is slightly more token-efficient but at the cost of stability.

### Inference Latency (averages across 8 benchmarks, seconds per query)

| Model | Single | TextMAS | Primitives MAS |
|-------|--------|---------|----------------|
| Qwen3-4B | 448 | 2,365 (+428%) | 692 (+54.5%) |
| Qwen3-8B | 571 | 2,915 (+411%) | 871 (+52.5%) |
| Qwen3-14B | 1,138 | 5,134 (+351%) | 1,634 (+43.6%) |
| DS-R1-Qwen-32B | 1,456 | 4,570 (+214%) | 1,511 (+3.8%) |

Primitives MAS introduces **~1.3-1.6x latency overhead** vs. single agent, while TextMAS introduces **~3.5-5.3x overhead**. On the larger DeepSeek-R1-Distill-Qwen-32B, the overhead is only 3.8%.
