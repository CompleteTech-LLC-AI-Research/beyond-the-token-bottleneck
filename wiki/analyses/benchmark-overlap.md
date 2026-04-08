---
type: analysis
title: "Benchmark Overlap Analysis"
created: "2026-04-06"
updated: "2026-04-08"
tags: [synthesis, benchmarks, comparison]
---

# Benchmark Overlap Analysis

A systematic survey of which benchmarks appear across the 27 source papers, identifying evaluation convergence points, comparable results, and blind spots in the field's testing practices.

## Methodology

Each of the 27 source pages was examined for empirical benchmarks used, models tested, and key results reported. Papers that are purely theoretical (no empirical benchmarks on standard datasets) are excluded from the benchmark matrix but noted in the model coverage section. Of 27 papers, 20 report results on identifiable benchmarks; 7 are theoretical, framework-level, or use only synthetic/custom tasks. The 19th empirical paper is [[latent-reasoning-supervision-analysis|Cui et al. (2026)]], which tests four latent reasoning methods (Coconut, CODI, SIM-CoT, CoLaR) on GSM8K-Aug and ProsQA — results reported under the GSM8K and ProsQA-related entries below. The 20th is [[inference-time-scaling-continuous-reasoning|Wang et al. (2025)]], which tests inference-time scaling (dropout sampling + PRM/ORM reranking) on COCONUT/GPT-2 against GSM8K — results reported under the GSM8K entry.

---

## Master Benchmark x Paper Matrix

The following table shows which papers evaluate on which benchmarks. A dot indicates the paper reports results on that benchmark.

| Benchmark | [[coconut-reasoning-latent-space\|Coconut]] | [[icot-internalize-cot\|iCoT]] | [[pause-tokens\|Pause]] | [[softcot-efficient-reasoning\|SoftCoT]] | [[thinking-states-latent-reasoning\|ThinkSt]] | [[cipher-multiagent-debate-embeddings\|CIPHER]] | [[state-delta-trajectory\|SDE]] | [[activation-communication-harvard\|AC]] | [[interlat-latent-space-agents\|Interlat]] | [[thought-communication-multiagent\|ThoughtC]] | [[kvcomm-selective-kv-sharing\|KVComm]] | [[cache-to-cache-semantic-communication\|C2C]] | [[kvcomm-online-cross-context\|KVC-On]] | [[latentmas-collaboration\|LatMAS]] | [[agent-primitives-building-blocks\|AgPrim]] | [[vision-wormhole-heterogeneous\|VW]] | [[multiagent-debate-du-et-al\|Du]] | [[scaling-agent-systems\|Scale]] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **GSM8K** | * | * | * | * | * | * | * | * | | * | | | * | * | * | * | * | |
| **MATH** | | | | | | | | | * | * | | | | | * | | | |
| **MMLU** (any subset) | | | | | | * | * | * | | | | * | * | | | | * | |
| **HumanEval/+** | | | | | | | | | | | | | * | * | * | * | | |
| **MBPP/+** | | | | | | | | | | | | | | * | * | | | |
| **AIME 24/25** | | | | | | | | | | | | | | * | * | * | | |
| **GPQA-Diamond** | | | | | | | | | | | | | | * | * | | | |
| **MedQA** | | | | | | | | | | | | | | * | * | | | |
| **ARC-E/C** | | | | | | | | | | | | | | * | | | | |
| **HotpotQA** | | | | | | | | | | | * | | | | | | | |
| **StrategyQA** | | | | * | | | * | | | | | | | | | | | |
| **SQuAD** | | | * | | | | | | | | | | | | | | | |
| **Arithmetic** | | | | | | * | | | | | | | | | | | * | |
| **ALFWorld** | | | | | | | | | * | | | | | | | | | |
| **Biographies** | | | | | | | | * | | | | | | | | | * | |
| **FEVER** | | | | | | | * | | | | | | | | | | | |
| **Quasar-T** | | | | | | | * | | | | | | | | | | | |
| **CWQ** | | | | | | | * | | | | | | | | | | | |
| **ProsQA** | * | | | | | | | | | | | | | | | | | |
| **ProntoQA** | * | | | | | | | | | | | | | | | | | |
| **Multiplication** | | * | | | | | | | | | | | | | | | | |

**Papers with no standard benchmarks** (excluded from matrix): [[superposition-coconut-theory|Superposition Theory]] (synthetic graph reachability only), [[cot-expressivity-theory|CoT Expressivity]] (synthetic arithmetic only), [[platonic-representation-hypothesis|Platonic Rep]] (alignment metrics, not task accuracy), [[relative-representations-zero-shot|Relative Rep]] (stitching metrics), [[linearity-relation-decoding|Linearity]] (probing faithfulness), [[kv-cache-alignment-shared-space|KV Alignment]] (small-scale Gemma experiments), [[latentcompress-open-call|LatentCompress]] (GSM8K/ARC-C/GPQA but as a project report, not a peer-reviewed paper).

---

## Most Common Benchmarks: Focused Comparison Tables

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
| [[kvcomm-online-cross-context\|KVCOMM-online]] | LLaMA-3.1-8B | Cache reuse (efficiency) | 66.6% | 68.0% (original) | <2.5% quality drop |
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
| [[kvcomm-online-cross-context\|KVCOMM-online]] | Full MMLU | LLaMA-3.1-8B (5 agents) | 69.9% |
| [[multiagent-debate-du-et-al\|Du et al.]] | Full MMLU | ChatGPT | 71.1% |

### HumanEval/MBPP (Code Generation) -- 4 papers

| Paper | Model | HumanEval+ | MBPP+ |
|---|---|---|---|
| [[latentmas-collaboration\|LatentMAS]] | Qwen3-14B (Seq) | 86.5% | 75.7% |
| [[agent-primitives-building-blocks\|Agent Primitives]] | Qwen3-8B | 82.3% | 75.9% |
| [[vision-wormhole-heterogeneous\|Vision Wormhole]] | SmolVLM2+Gemma-4B | 59.1% | -- |
| [[kvcomm-online-cross-context\|KVCOMM-online]] | LLaMA-3.1-8B | Pass@1 maintained | -- |

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

## Benchmark Blind Spots

### Entirely Missing Benchmark Categories

1. **Long-context reasoning**: Only [[kvcomm-selective-kv-sharing|KVComm]] tests on long-context QA datasets (HotpotQA, QASPER, MuSiQue, MultiFieldQA). Most [[latent-space-reasoning|latent reasoning]] and communication papers ignore contexts beyond a few thousand tokens. [[vision-wormhole-heterogeneous|Vision Wormhole]] notes bandwidth bottlenecks at scale but does not test on dedicated long-context benchmarks.

2. **Open-ended generation / instruction following**: No paper evaluates on AlpacaEval, MT-Bench, WildBench, or similar instruction-following benchmarks. All results are on closed-form tasks (QA, math, code). Whether latent methods preserve generation quality and instruction adherence is unknown.

3. **Multilingual benchmarks**: Zero multilingual evaluation across all 27 papers. [[relative-representations-zero-shot|Relative Representations]] demonstrates cross-lingual stitching but on sentiment classification, not reasoning.

4. **Safety and robustness**: No adversarial robustness testing (beyond [[agent-primitives-building-blocks|Agent Primitives]]' noise injection experiment). No evaluation on TruthfulQA, BBQ bias, or jailbreak resistance. [[latentcompress-open-call|LatentCompress]] raises the safety concern but provides no standard safety benchmark evaluation.

5. **Real-world agent benchmarks**: [[interlat-latent-space-agents|Interlat]] uses ALFWorld (a text-based household environment) and [[scaling-agent-systems|Scaling Agent Systems]] uses custom agent benchmarks (Finance-Agent, BrowseComp, PlanCraft, Workbench), but no paper tests on WebArena, SWE-bench, or other software engineering / web navigation benchmarks.

6. **Reading comprehension beyond SQuAD**: Only [[pause-tokens|Pause Tokens]] tests SQuAD and CoQA. No paper evaluates on DROP, QuALITY, or narrative understanding tasks.

### Underrepresented Benchmarks

| Benchmark | Papers Testing | Gap Significance |
|---|---|---|
| MATH | 3 | High -- standard math reasoning, should be universal |
| AIME | 3 | Medium -- competition math, only recent papers test it |
| GPQA-Diamond | 3 | High -- graduate-level reasoning, tests deeper capabilities |
| HumanEval/MBPP | 4 | Medium -- code generation increasingly important |
| StrategyQA | 2 | Medium -- commonsense multi-hop reasoning |
| ALFWorld | 1 | High -- embodied agent task, critical for latent MAS |

### Over-Represented but Saturating Benchmarks

**GSM8K** appears in 14 of 18 empirical papers but is approaching saturation at scale. Multi-agent methods on 7B+ models achieve 88-95%, leaving little room for differentiation. New papers should pair GSM8K with harder math benchmarks (MATH, AIME) to demonstrate meaningful gains.

---

## Model Coverage

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

## Cross-Paper Comparison: Communication Methods on Shared Benchmarks

Where multiple communication papers test on the same benchmark and model family, we can attempt normalized comparisons.

### GSM8K on Qwen 7B-Class Models (Debate Setting)

| Method | Model | GSM8K | Communication Type |
|---|---|---|---|
| Single agent | Qwen2.5-7B | 87.9% | None |
| NL debate | Qwen2.5-7B | 90.6% | Natural language |
| CIPHER | Qwen2.5-7B | 89.3% | Output embeddings |
| **SDE** | **Qwen2.5-7B** | **91.8%** | **State deltas** |

### GSM8K on Multi-Agent Systems (Qwen3 8B-Class)

| Method | Model | GSM8K | Agents |
|---|---|---|---|
| Single agent | Qwen3-8B | 81.1% | 1 |
| TextMAS | Qwen3-8B | 92.3% | 4 (sequential) |
| LatentMAS | Qwen3-8B | 93.8% | 4 (sequential) |
| **Agent Primitives** | **Qwen3-8B** | **94.2%** | **Variable (composed)** |

### Formal Logic (MMLU) on Qwen 7B-Class (Debate Setting)

| Method | Model | Formal Logic | Communication Type |
|---|---|---|---|
| Single agent | Qwen2.5-7B | 45.0% | None |
| NL debate | Qwen2.5-7B | 47.6% | Natural language |
| CIPHER | Qwen2.5-7B | 48.8% | Output embeddings |
| **SDE** | **Qwen2.5-7B** | **52.0%** | **State deltas** |

---

## Key Findings

1. **GSM8K is the de facto universal benchmark** but is saturating. 14 of 18 empirical papers test on it. At 7B+ scale with multi-agent methods, accuracy exceeds 90%, limiting discriminative power.

2. **No benchmark is tested by more than 14 papers**. The field lacks a truly universal evaluation suite. MATH, GPQA, and code generation benchmarks are severely underrepresented relative to their importance.

3. **Scale confounds all comparisons**. Papers test at wildly different scales (GPT-2 117M to DeepSeek-R1 70B), making cross-paper accuracy comparisons misleading. Controlled comparisons on the same base model are rare.

4. **Communication papers test more broadly than reasoning papers**. Reasoning papers ([[coconut-reasoning-latent-space|Coconut]], [[icot-internalize-cot|iCoT]], [[pause-tokens|Pause Tokens]]) test on 2-4 benchmarks; communication papers ([[state-delta-trajectory|SDE]], [[agent-primitives-building-blocks|Agent Primitives]], [[latentmas-collaboration|LatentMAS]]) test on 6-10. This reflects different maturity levels: reasoning methods are still proving basic viability; communication methods are demonstrating generality.

5. **Critical blind spots**: open-ended generation, multilingual tasks, safety benchmarks, long-context reasoning, and real-world agent environments are all untested. These gaps mean the field cannot yet claim that latent methods work "in general" -- only on closed-form reasoning tasks.

6. **The Qwen family dominates recent work**. 10 papers use Qwen models, making it the most common evaluation platform. This introduces a risk of method overfitting to Qwen-specific architectural properties (e.g., Qwen's resilience to RoPE misalignment vs. LLaMA's catastrophic sensitivity, as documented by [[agent-primitives-building-blocks|Agent Primitives]]).

## Source Materials

This analysis synthesizes data from all 27 source pages in `wiki/sources/`. No raw files were consulted.
