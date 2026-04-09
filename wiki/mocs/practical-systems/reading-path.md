### 1. When Does Multi-Agent Help at All?

Start with **[[scaling-agent-systems|Scaling Agent Systems]]** — the quantitative framework that prevents wasted effort. The core finding: MAS is **task-contingent**, not universally beneficial. Its best variant yields +80.8% on naturally decomposable tasks (Centralized on Finance-Agent) but the worst can degrade -70.1% on strictly sequential ones (Independent on PlanCraft). The **baseline paradox** (beta = -0.404) means that if a single agent already achieves >45% accuracy, coordination overhead often exceeds the gains. Read this before committing to any multi-agent architecture.

### 2. Which Latent Method Fits Your Constraints?

**[[method-comparison|Method Comparison]]** provides the unified table across all 18 empirical methods. The three spectra that matter most for deployment: **training requirements** (CIPHER and KVComm need zero training; Coconut and Interlat need heavy curriculum learning), **cross-architecture compatibility** (natural language is universal; KV-cache methods are same-architecture only; AC and C2C bridge families), and **information density vs. compatibility** (the frontier goal is upper-right — high density AND high compatibility). No single method dominates; the optimal choice depends on your specific constraints.

### 3. The Composable Architecture Approach

**[[agent-primitives-building-blocks|Agent Primitives]]** shows how to structure latent MAS using reusable building blocks — **Review**, **Voting**, and **Planning** primitives composed per-task by an Organizer agent. Key deployment facts: +6.3% to +16.5% over single agents across 5 model families, **fewer tokens than single agents** on smaller models, and only 1.3-1.6x latency overhead (vs. 3.5-5.3x for text-based MAS). Critical implementation detail: **RoPE positional re-encoding** is mandatory for LLaMA-based models (without it, ~27-60pp accuracy drops).

### 4. Training-Free Deployment with LatentMAS

**[[latentmas-collaboration|LatentMAS]]** is the fastest path to a working latent MAS — no training, no adapters, just ridge regression alignment and KV-cache transfer. 4x faster than text-based MAS, 70-84% token reduction. But it requires **homogeneous architecture** (same model family) and catastrophically fails on LLaMA (-10.1% average on DeepSeek-R1-Distill-Llama-70B, as measured by Agent Primitives' comparison). For Qwen-family models, this is the lowest-friction deployment option.

### 5. Systems-Level Efficiency

**[[kvcomm-duke-online-reuse|KVCOMM-online]]** tackles the compute bottleneck that appears when agents share overlapping context. Its anchor-based KV-cache reuse achieves up to **7.8x prefill speedup** (6.7x average) with <2.5% quality drop — a systems optimization orthogonal to the communication method itself. Composable with any KV-cache approach.

### 6. Compression Targets and Bandwidth Planning

**[[latentcompress-open-call|LatentCompress]]** establishes concrete bandwidth targets: **512 bytes** suffices for simple tasks (GSM8K matches 91% baseline), but hard reasoning tasks (GPQA) need MB-scale bandwidth. The bandwidth-accuracy S-curve and cumulative degradation model ($Q \propto e^{-T\varepsilon/C}$) provide the planning framework for sizing communication channels in production systems.

### 7. Collaboration and Research Opportunities

**[[latentcompress-collaboration-strategy]]** maps the gap between existing open-source efforts and the full research landscape. **[[frontier-research-directions]]** identifies the engineering-adjacent directions with highest near-term impact: scaling laws for latent MAS (#7) and learned compression bounds (#8).
