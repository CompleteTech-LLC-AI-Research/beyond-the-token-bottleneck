**Models tested:**
- **LLaMA2-70B** (Touvron et al., 2023b) — primary model, 4096-token context window
- **LLaMA-65B** (Touvron et al., 2023a) — shares tokenizer with LLaMA2, different embedding matrices
- **Falcon-40B-Instruct** (Penedo et al., 2023)
- **MPT-30B** (MosaicML, 2023)
- **WizardMath-70B-V1.0** (Luo et al., 2023)
- **LLaMA2-Chat-70B** — also tested in cross-model experiments

**Five benchmarks:**
1. **GSM8K** — grade school math word problems (Cobbe et al., 2021)
2. **Arithmetic** — mathematical expressions with six two-digit numbers using +, *, - (following Du et al., 2023)
3. **MMLU Formal Logic** — from the Humanities category (Hendrycks et al., 2020)
4. **MMLU High School Math** — from the STEM category
5. **MMLU Professional Psychology** — from the Social Science category

**Sampling and evaluation:** For large datasets (GSM8K, Professional Psychology, Arithmetic), temperatures were tuned on a validation set of 200 sampled questions, then evaluated on a separate test set of 200 questions. All debates used 3 rounds with 2 debaters (following Du et al., 2023). Each debate produces 5 responses per question for the debate methods; self-consistency baselines (Major@5) also use 5 responses for fair comparison.

**Prompting strategy:** Few-shot chain-of-thought (CoT) prompting combined with zero-shot instruction ("Let's think step by step"). GSM8K uses 3-shot examples for LLaMA/Falcon/MPT; WizardMath uses its own CoT prompt. MMLU datasets use 3-shot examples with step-by-step explanations. Debate round prompts instruct agents to incorporate other agents' solutions.

**Temperature selection:** Bayesian optimization (Nogueira, 2014) was used to select optimal temperature pairs for each method on each dataset. Hardware: 4x NVIDIA A100 SXM 80GB GPUs for LLaMA family debates.

**Baseline methods:**
- **Single Answer:** one LLM, one response
- **Self-Consistency (Major@5):** one LLM generates 5 independent responses, majority vote (Wang et al., 2023b)
- **Natural Language Debate (NLD):** multiagent debate using natural language communication (Du et al., 2023)
