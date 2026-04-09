### Base Models Used Across Papers

| Base Model Family | Papers Using It | Scale Range | Notes |
|---|---|---|---|
| **Qwen** (2.5/3) | 10 | 0.5B--32B | Most popular; used by [[state-delta-trajectory\|SDE]], [[interlat-latent-space-agents\|Interlat]], [[latentmas-collaboration\|LatentMAS]], [[agent-primitives-building-blocks\|AgPrim]], [[thought-communication-multiagent\|ThoughtComm]], [[softcot-efficient-reasoning\|SoftCoT]], [[thinking-states-latent-reasoning\|ThinkSt]] |
| **LLaMA** (2/3/3.1/3.2) | 9 | 3B--70B | Used by [[cipher-multiagent-debate-embeddings\|CIPHER]], [[activation-communication-harvard\|AC]], [[state-delta-trajectory\|SDE]], [[latentmas-collaboration\|LatentMAS]], [[agent-primitives-building-blocks\|AgPrim]], [[interlat-latent-space-agents\|Interlat]]; catastrophic failures noted on KV-cache methods |
| **GPT-2** | 3 | 117M--355M | [[coconut-reasoning-latent-space\|Coconut]], [[icot-internalize-cot\|iCoT]], CoT Expressivity; proof-of-concept scale only |
| **Gemma** (2/3) | 4 | 2B--12B | [[activation-communication-harvard\|AC]], [[kv-cache-alignment-shared-space\|KV Alignment]], [[vision-wormhole-heterogeneous\|Vision Wormhole]], [[agent-primitives-building-blocks\|AgPrim]] |
| **DeepSeek-R1-Distill** | 2 | 8B--70B | ThoughtComm, AgPrim |
| **Phi** (3/4-mini) | 2 | 3.8B | [[icot-internalize-cot\|iCoT]], [[thought-communication-multiagent\|ThoughtComm]] |
| **Mistral** | 1 | 7B | iCoT only |
| **Falcon** | 1 | 40B | CIPHER only |
| **MPT** | 1 | 30B | CIPHER only |
| **ChatGPT** (gpt-3.5-turbo) | 1 | -- | Du et al. (black-box) |
| **GPT-5/5.2** | 1 | -- | Scaling Agent Systems (black-box); AgPrim uses GPT-5.2 as Organizer |
| **VLMs** (SmolVLM2, LFM2.5, Gemma-3-VL, Qwen3-VL) | 1 | 1.6B--12B | Vision Wormhole only |

### Scale Distribution

| Scale Tier | Papers | Representative Methods |
|---|---|---|
| <1B | 5 | [[coconut-reasoning-latent-space\|Coconut]], [[icot-internalize-cot\|iCoT]], [[pause-tokens\|Pause Tokens]], [[kv-cache-alignment-shared-space\|KV Alignment]], [[interlat-latent-space-agents\|Interlat]] (0.5B) |
| 1B--4B | 5 | [[pause-tokens\|Pause Tokens]] (1B), [[softcot-efficient-reasoning\|SoftCoT]] (3.8B via Phi), [[latentmas-collaboration\|LatentMAS]] (4B), [[agent-primitives-building-blocks\|AgPrim]] (4B), [[vision-wormhole-heterogeneous\|VW]] (1.6-4B) |
| 7B--8B | 10 | Most communication papers |
| 14B--32B | 5 | [[state-delta-trajectory\|SDE]] (14B), [[latentmas-collaboration\|LatentMAS]] (14B), [[agent-primitives-building-blocks\|AgPrim]] (14B/32B) |
| 70B | 3 | [[cipher-multiagent-debate-embeddings\|CIPHER]], [[agent-primitives-building-blocks\|AgPrim]], [[activation-communication-harvard\|AC]] |
| Frontier (API) | 2 | Scaling Agent Systems, AgPrim (Organizer) |

**Critical gap**: No paper tests latent reasoning methods ([[coconut-reasoning-latent-space|Coconut]], [[icot-internalize-cot|iCoT]], [[thinking-states-latent-reasoning|Thinking States]]) at 7B+ scale. Coconut and iCoT are GPT-2 only; [[softcot-efficient-reasoning|SoftCoT]] tests at 7-8B but only the two-model variant (not Coconut-style self-contained loop); Thinking States tests at 0.5B-1.5B. [[latent-reasoning-supervision-analysis|Cui et al. (2026)]] tests four methods (Coconut, CODI, SIM-CoT, CoLaR) at GPT-2 and LLaMA-3.2-1B, joining the same <2B cluster. [[inference-time-scaling-continuous-reasoning|Wang et al. (2025)]] also tests COCONUT only at GPT-2 (117M), the same scale as the original COCONUT paper. Whether the BFS-via-superposition phenomenon persists at frontier scale — and whether the supervision–exploration trade-off Cui et al. document and the geometric homogeneity Wang et al. measure scale or relax — remains the single most important open experimental question in the field.

---
