### Small Models (1.6B–4B): Full Table

Five two-backbone configs + one four-backbone config, 9 benchmarks each. Macro-averaged: **+6.3pp accuracy, 1.87× speedup** over TextMAS.

**Two-backbone configurations (Planner/Refiner → Critic/Judger):**
- Gemma-3-4B + Qwen3-VL-2B
- LFM2.5-VL-1.6B + Gemma-3-4B
- LFM2.5-VL-1.6B + Qwen3-VL-2B
- SmolVLM2-2.2B + Gemma-3-4B
- SmolVLM2-2.2B + Qwen3-VL-2B

**Four-backbone pool:** SmolVLM2-2.2B + LFM2.5-VL-1.6B + Gemma-3-4B + Qwen3-VL-2B

Selected highlights from Table 2:
- **AIME 2024** (SmolVLM2 + Qwen3-VL-2B): +10.0pp accuracy, **5.47× speedup** (2807s → 513s)
- **AIME 2025** (Gemma-3-4B + Qwen3-VL-2B): +10.0pp, 3.75× speedup
- **HumanEval-Plus** (SmolVLM2 + Gemma-3-4B): +26.2pp (32.9% → 59.1%), 1.64× speedup
- **GSM8K** (SmolVLM2 + Gemma-3-4B): +17.6pp (67.8% → 85.4%), 1.96× speedup
- Code generation average: **+13.2pp, 1.21× speedup**

### Weakly Supervised Variant (<100 Anchor Texts)

Trained with only **90 anchor texts** (30 per source). Tested on Gemma-3-4B + Qwen3-VL-2B and SmolVLM2-2.2B + Qwen3-VL-2B configs.

Macro average: **+6.5pp accuracy, 2.67× speedup** — remarkably data-efficient.

Selected results (SmolVLM2 + Qwen3-VL-2B, weakly supervised):
- **AIME 2024**: +23.4pp (13.3% → 36.7%), **7.20× speedup** (2807s → 390s)
- **AIME 2025**: +6.6pp, 4.80× speedup
- **GSM8K**: +12.7pp (64.3% → 77.0%), 2.49× speedup
- **HumanEval-Plus**: +11.6pp, 1.56× speedup

### Single-Agent vs MAS Comparison

| Model | Single-Agent Avg | TextMAS Avg | VW Avg | Δ Text | Δ VW |
|---|---|---|---|---|---|
| Qwen3-VL-2B | 50.8 | 49.4 | 52.6 | **-1.4pp** | +1.8pp |
| Gemma-3-4B | 55.7 | 52.5 | 56.0 | **-3.2pp** | +0.3pp |
| SmolVLM2-2.2B | 25.8 | 44.2 | 52.7 | +18.5pp | **+26.9pp** |
| LFM2.5-VL-1.6B | 40.2 | 46.8 | 52.2 | +6.6pp | **+12.0pp** |
| **Macro Avg** | 43.1 | 48.2 | 53.4 | +5.1pp | **+10.3pp** |

Key finding: For **strong backbones** (Qwen3-VL-2B, Gemma-3-4B), TextMAS **drops below** single-agent baselines (-1.4pp to -3.2pp), but VW stays at or above parity. For **weak backbones** (SmolVLM2, LFM2.5), both MAS variants help, but VW gains are much larger (+26.9pp vs +18.5pp for SmolVLM2). This indicates VW is more robust to heterogeneous orchestration effects — bounded latent communication reduces cross-role interference.

### Mid-Sized Models (4B–12B)

Two configs: Gemma-3-4B + Qwen3-VL-8B, and Qwen3-VL-8B + Gemma-3-12B.

**Dramatic speedups** (macro-average **5.92×**), with Qwen3-VL-8B + Gemma-3-12B seeing extreme speedups:
- AIME 2024: **16.54×** (1639s → 99s)
- MBPP-Plus: **13.51×** (238s → 18s)
- GPQA: **16.40×** (873s → 53s)
- ARC-Easy: 7.23×, ARC-Challenge: 7.34×

**But accuracy degrades** (macro-average **-5.3pp**), especially on complex tasks:
- AIME 2024 (8B+12B): -33.3pp (60.0% → 26.7%)
- AIME 2025 (8B+12B): -26.7pp (46.7% → 20.0%)
- GPQA (8B+12B): -21.7pp (61.6% → 39.9%)
- Simpler tasks hold: GSM8K +1.4pp (Gemma+Qwen8B), ARC-Easy +0.6pp

**Root cause:** The default fixed bandwidth (1024 latent steps, 256 visual tokens) becomes a bottleneck for stronger backbones that produce richer reasoning states. This is **not a hard limit** — bandwidth can be increased by stacking multiple images (e.g., four 224×224 images for ~1024 tokens) or using higher-resolution images (e.g., 1008px in Qwen-style prompts).
