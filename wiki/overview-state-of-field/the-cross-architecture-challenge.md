The central tension, mapped in detail by [[cross-architecture]], is that **deeper communication channels carry more information but demand tighter architectural coupling**. Natural language works between any two models; KV-cache sharing requires identical architectures; state deltas require identical weights.

The field is bending this curve through three strategies:

1. **Learned linear maps** — AC shows that a single task-agnostic projection trained on 3,072 C4 sentences bridges model families. The cost scales $O(N^2)$ with pool size, but the maps are cheap to compute.
2. **Shared interlingua spaces** — KV Cache Alignment trains two adapters per model (into and out of a global shared space), scaling $O(N)$. New models join by training two adapters; untrained paths work zero-shot. Currently validated only at 100M-400M scale.
3. **Architectural bypass** — [[vision-wormhole-heterogeneous|Vision Wormhole]] routes communication through VLM visual input pathways, which are explicitly designed to accept dense continuous vectors. Hub-and-spoke alignment via ridge regression on anchor texts scales $O(N)$ and achieves +6.3pp accuracy and 1.87x speedup over text MAS across fully heterogeneous pools (Gemma, Qwen, SmolVLM, LFM at 1.6B-4B scale). At mid-scale (4B-12B), speedups reach 5.92x but accuracy degrades, suggesting a fixed bandwidth bottleneck.

The counter-example matters: [[latentmas-collaboration|LatentMAS]] demonstrates what happens when cross-architecture compatibility is ignored. Its training-free KV-cache transfer works well within Qwen-family models but catastrophically fails on LLaMA (-10.1% average), illustrating how same-architecture assumptions break down across families.
