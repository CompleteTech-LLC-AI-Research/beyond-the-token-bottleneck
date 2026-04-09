When choosing a latent communication method, the primary decision factors are: (1) whether you control the model weights, (2) whether agents share the same architecture, and (3) the deployment constraints.

**Do you need cross-architecture support?**
- *Yes, heterogeneous VLMs*: **[[vision-wormhole-heterogeneous|Vision Wormhole]]** — the only method supporting truly heterogeneous backbones with minimal training. Best for small-to-mid models (1.6B-4B); bandwidth bottleneck at 8B+.
- *Yes, heterogeneous text-only*: **[[activation-communication-harvard|AC]]** for zero-shot (no training, single-layer), or **[[cache-to-cache-semantic-communication|C2C]]** / **[[kv-cache-alignment-shared-space|KV Alignment]]** for richer transfer (requires trained fusers/adapters).
- *No, same model family*: Continue below.

**Can you train adapters or modify the pipeline?**
- *No training allowed*: **[[agent-primitives-building-blocks|Agent Primitives]]** (composable, task-adaptive, tested up to 70B), **[[kvcomm-kth-selective|KVComm]]** (selective layer sharing, calibration only), or **[[state-delta-trajectory|SDE]]** (delta-based, no calibration needed).
- *Minimal training OK*: **[[latentmas-collaboration|LatentMAS]]** (ridge regression, training-free but architecture-sensitive — avoid LLaMA backbones).
- *Training budget available*: **[[thought-communication-multiagent|ThoughtComm]]** (structured, disentangled) or **[[interlat-latent-space-agents|Interlat]]** (maximum bandwidth, $2600\times$).

**What is your primary optimization target?**
- *Accuracy*: Agent Primitives (+16.5pp avg at 8B), ThoughtComm (93.0% MATH), Interlat (ALFWorld 70.48%).
- *Latency/throughput*: KVCOMM-online (7.8x prefill speedup), LatentMAS (4-4.3x end-to-end), Vision Wormhole (up to 16.5x on mid-sized models).
- *Robustness to noise*: KV-cache methods (Agent Primitives demonstrates 93% vs 47% NL at 10 noise sentences).

**Important caveats**:
- LatentMAS catastrophically fails on LLaMA-based models ($-10.1$pp average on DeepSeek-R1-Distill-Llama-70B). Use Agent Primitives instead for LLaMA backbones. — [[agent-primitives-building-blocks]]
- Vision Wormhole accuracy degrades at 8B+ scale (up to $-33$pp on AIME) due to fixed visual-token bandwidth. Scaling bandwidth via multi-image injection is untested. — [[vision-wormhole-heterogeneous]]
- The scaling framework predicts MAS hurts on sequential planning tasks ($-70\%$) regardless of communication medium. Latent methods address lossy communication but not task-architecture mismatch. — [[scaling-agent-systems]]
