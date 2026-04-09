### Entirely Missing Benchmark Categories

1. **Long-context reasoning**: Only [[kvcomm-kth-selective|KVComm]] tests on long-context QA datasets (HotpotQA, QASPER, MuSiQue, MultiFieldQA). Most [[latent-space-reasoning|latent reasoning]] and communication papers ignore contexts beyond a few thousand tokens. [[vision-wormhole-heterogeneous|Vision Wormhole]] notes bandwidth bottlenecks at scale but does not test on dedicated long-context benchmarks.

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
