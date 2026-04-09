### GSM8K (Grade School Math) -- 14 papers

The most widely used benchmark in this collection. Results are difficult to compare directly because papers use different base models, scales, and evaluation protocols.

| Paper | Model | Method | GSM8K Acc. | Baseline | Notes |
|---|---|---|---|---|---|
| [[coconut-reasoning-latent-space\|Coconut]] | GPT-2 | Continuous thought | 34.1% | 42.9% (CoT) | Underperforms CoT on math |
| [[icot-internalize-cot\|iCoT]] | GPT-2 Small | Stepwise internalization | 30.0% | 41.0% (CoT) | Zero visible reasoning |
| [[icot-internalize-cot\|iCoT]] | Mistral 7B | Stepwise internalization | 51.0% | 68.0% (CoT) | Best iCoT result |
| [[pause-tokens\|Pause Tokens]] | 1B custom | Pause-pretrained | 8.5% | 7.5% (baseline) | Marginal gain |
| [[softcot-efficient-reasoning\|SoftCoT]] | LLaMA-3.1-8B-Inst | Soft thought tokens | 81.0% | 79.6% (Zero-Shot CoT) | Frozen backbone |
| [[softcot-efficient-reasoning\|SoftCoT]] | Qwen2.5-7B-Inst | Soft thought tokens | 85.8% | 83.7% (Zero-Shot CoT) | Best SoftCoT result |
| [[thinking-states-latent-reasoning\|Thinking States]] | Qwen2.5-1.5B | Chunk-recurrent | 42.2% | 60.5% (CoT) | -18pp gap; state ambiguity |
| [[cipher-multiagent-debate-embeddings\|CIPHER]] | LLaMA2-70B | Embedding debate | 66.0% | 60.0% (single) | 2 debaters, 3 rounds |
| [[state-delta-trajectory\|SDE]] | Qwen2.5-7B | Delta injection (debate) | 91.8% | 87.9% (single) | Best SDE debate result |
| [[state-delta-trajectory\|SDE]] | Qwen2.5-14B | Delta injection (debate) | 93.4% | 91.1% (single) | Largest model tested |
| [[activation-communication-harvard\|AC]] | LLaMA-3.2-3B->8B | Activation graft | 64.0% | 60.0% (8B alone) | NLD wins at 75% |
| [[kvcomm-duke-online-reuse\|KVCOMM-online]] | LLaMA-3.1-8B | Cache reuse (efficiency) | 66.6% | 68.0% (original) | <2.5% quality drop |
| [[thought-communication-multiagent\|ThoughtComm]] | Qwen-3-1.7B | Latent thought exchange | 85.0% | 67.4% (single) | +17.6pp over single |
| [[latentmas-collaboration\|LatentMAS]] | Qwen3-14B | KV-cache + latent thoughts | 95.2% | 83.7% (single) | Sequential MAS |
| [[agent-primitives-building-blocks\|Agent Primitives]] | Qwen3-8B | Composed primitives | 94.2% | 81.1% (single) | Best MAS result |
| [[vision-wormhole-heterogeneous\|Vision Wormhole]] | SmolVLM2+Gemma-4B | Vision injection | 85.4% | 67.8% (single) | +17.6pp |
| [[multiagent-debate-du-et-al\|Du et al.]] | ChatGPT (3.5-turbo) | NL debate | 85.0% | 77.0% (single) | Foundational result |
| [[latent-reasoning-supervision-analysis\|Cui et al. (Improved Coconut)]] | GPT-2 (117M) | Mixed-stage curriculum | 41.06% | 34.09% (orig. Coconut) | Pure data-sampling fix; first reported improvement to Coconut |
| [[latent-reasoning-supervision-analysis\|Cui et al. (CODI)]] | LLaMA-3.2-1B | Distillation + outcome loss | 55.57% | -- | Highest CODI accuracy at this scale |
| [[latent-reasoning-supervision-analysis\|Cui et al. (SIM-CoT)]] | LLaMA-3.2-1B | Decoder reconstruction loss | 56.03% | -- | Strong-supervision variant |
| [[latent-reasoning-supervision-analysis\|Cui et al. (CoLaR)]] | LLaMA-3.2-1B | Token-level compression alignment | 25.23% | -- | Strong supervision collapses latent capacity |
| [[inference-time-scaling-continuous-reasoning\|Wang et al. (deterministic COCONUT)]] | GPT-2 (117M) | Reproduction baseline | 31.08% | -- | Backbone for inference-time scaling study |
| [[inference-time-scaling-continuous-reasoning\|Wang et al. (Pass@32)]] | GPT-2 (117M) | Dropout-sampled COCONUT, oracle selection | 44.43% | 31.08% (det.) | Pass@N upper bound; exceeds GPT-2 text CoT |
| [[inference-time-scaling-continuous-reasoning\|Wang et al. (PRM-HE BoN)]] | GPT-2 (117M) | MATH-Shepherd-style PRM (hard) reranker | 33.36% | 31.08% (det.) | +2.28pp; recovers only 19.8% of Pass@N headroom |

**Key observations**: GSM8K results span from 8.5% ([[pause-tokens|Pause Tokens]] at 1B) to 95.2% ([[latentmas-collaboration|LatentMAS]] at Qwen3-14B). The benchmark saturates at scale -- multi-agent approaches on 7B+ models consistently achieve 85-95%. Reasoning-only methods ([[coconut-reasoning-latent-space|Coconut]], [[icot-internalize-cot|iCoT]]) at GPT-2 scale underperform CoT, while communication methods at 7B+ scale exceed it.

### MATH -- 3 papers

| Paper | Model | Method | MATH Acc. | Baseline |
|---|---|---|---|---|
| [[interlat-latent-space-agents\|Interlat]] | Qwen2.5-7B | Hidden-state transfer | 36.9% | 33.3% (No-Comm) |
| [[thought-communication-multiagent\|ThoughtComm]] | Qwen-3-1.7B | Latent thought exchange | 93.0% | 43.6% (single) |
| [[agent-primitives-building-blocks\|Agent Primitives]] | Qwen3-8B | Composed primitives | 63.7% | 60.8% (single) |

**Key observation**: MATH is severely underrepresented. Only 3 papers test on it despite being a standard reasoning benchmark. [[thought-communication-multiagent|ThoughtComm]]'s 93.0% on Qwen-3-1.7B is remarkably high and should be verified against other papers' baselines.

### MMLU (Various Subsets) -- 6 papers

Papers use different MMLU subsets, making direct comparison difficult.

| Paper | Subsets Used | Model | Best Result |
|---|---|---|---|
| [[cipher-multiagent-debate-embeddings\|CIPHER]] | Formal Logic, HS Math, Psychology | LLaMA2-70B | 52.4% (Formal Logic) |
| [[state-delta-trajectory\|SDE]] | Abstract Algebra, College Math, Formal Logic | Qwen2.5-14B | 75.3% (Abstract Algebra) |
| [[activation-communication-harvard\|AC]] | 57 datasets (full) | LLaMA-3.2-3B->8B | 62.7% average |
| [[cache-to-cache-semantic-communication\|C2C]] | Full MMLU | Various cross-model | Consistent gains |
| [[kvcomm-duke-online-reuse\|KVCOMM-online]] | Full MMLU | LLaMA-3.1-8B (5 agents) | 69.9% |
| [[multiagent-debate-du-et-al\|Du et al.]] | Full MMLU | ChatGPT | 71.1% |

### HumanEval/MBPP (Code Generation) -- 4 papers

| Paper | Model | HumanEval+ | MBPP+ |
|---|---|---|---|
| [[latentmas-collaboration\|LatentMAS]] | Qwen3-14B (Seq) | 86.5% | 75.7% |
| [[agent-primitives-building-blocks\|Agent Primitives]] | Qwen3-8B | 82.3% | 75.9% |
| [[vision-wormhole-heterogeneous\|Vision Wormhole]] | SmolVLM2+Gemma-4B | 59.1% | -- |
| [[kvcomm-duke-online-reuse\|KVCOMM-online]] | LLaMA-3.1-8B | Pass@1 maintained | -- |

### AIME 2024/2025 (Competition Math) -- 3 papers

| Paper | Model | AIME24 | AIME25 |
|---|---|---|---|
| [[latentmas-collaboration\|LatentMAS]] | Qwen3-14B (Hier) | 73.3% | 66.7% |
| [[agent-primitives-building-blocks\|Agent Primitives]] | Qwen3-8B | 76.7% | 73.3% |
| [[vision-wormhole-heterogeneous\|Vision Wormhole]] | SmolVLM2+Qwen3-VL-2B | 36.7% (weak sup.) | -- |

### GPQA-Diamond (Graduate-Level QA) -- 3 papers

| Paper | Model | GPQA-Diamond |
|---|---|---|
| [[latentmas-collaboration\|LatentMAS]] | Qwen3-14B (Hier) | 53.0% |
| [[agent-primitives-building-blocks\|Agent Primitives]] | Qwen3-8B | 59.6% |
| [[latentcompress-open-call\|LatentCompress]] | Qwen3-14B (SlotMAS) | 19.1% (512B bandwidth) |

---
