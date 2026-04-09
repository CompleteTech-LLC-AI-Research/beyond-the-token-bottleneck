### 1. Single-Vector Replacement (AC)

[[activation-communication-harvard|AC]] replaces B's last-token activation at one layer with A's activation from the same depth. Despite its simplicity — one vector, one layer — it outperforms natural language debate on **48/57 MMLU datasets** and **6/7 reasoning benchmarks** with **< ¼ the compute**.

**Key findings**:
- **Replace** function beats sum and mean (B retains context at other positions)
- Works **cross-family** (LLaMA ↔ Qwen ↔ Gemma) without learned projections ([[raw/pdf/arxiv-2501.14082.pdf|AC Table 2]]), supporting the Platonic Representation Hypothesis
- Exception: **GSM8K** — debate beats AC because multi-step math benefits from iterative refinement, not single-shot knowledge transfer
- One-shot sufficiency: one activation graft communicates "all of A's knowledge/beliefs about the prompt"

### 2. Full Hidden-State Sequences (Interlat)

[[interlat-latent-space-agents|Interlat]] transmits the **full temporal sequence** of last-layer hidden states from all generation steps — not a single vector but a matrix $H \in \R^{L \times d}$. A learned **communication adapter** (multi-head attention + layer norm + projection) bridges representation spaces.

**Key findings**:
- **2,600× bandwidth** increase per position vs. discrete tokens (~40,000 bits vs ~15 bits) ([[raw/pdf/arxiv-2511.09149.pdf|Interlat §4.1]])
- Best result is **cross-family** (Qwen→LLaMA: 70.95%/71.39% on ALFWorld)
- Beats CoT on **Level-5 MATH** (hardest) — 15.80% vs 15.05% — latent communication preserves "superposition of parallel hypotheses"
- Compression to **8 latent steps** with only 4% accuracy drop and **46× speedup**
- **Curriculum learning is critical** — without it, near-zero success (training instability)

### 3. Training-Free KV-Cache Transfer (LatentMAS)

[[latentmas-collaboration|LatentMAS]] goes beyond sharing input-processing KV-caches: it shares KV caches that include **generated latent thoughts** (hidden states fed back as input embeddings, [[coconut-reasoning-latent-space|Coconut]]-style). The full layer-wise KV cache constitutes a "latent working memory" transferred between agents.

**Key findings**:
- **Training-free** — only a $d \times d$ alignment matrix $M$ computed via ridge regression
- **4-4.3× faster** than TextMAS with **70.8-83.7% fewer tokens**
- Up to **+14.6% accuracy** over single-agent baselines
- Theoretical: latent thoughts can be **$d / \log|V|$ times** more efficient than text — $471.4\times$ for Qwen3-14B
- Unifies latent reasoning ([[coconut-reasoning-latent-space|Coconut]]) + latent communication (KV-cache transfer) in one framework

### 4. State Deltas as Steering Vectors (SDE)

[[state-delta-trajectory|SDE]] introduces a refined approach for **same-model** agents: instead of transmitting raw hidden states (which include context-specific noise from the sender's system prompt), transmit the **inter-token differences** (deltas):

> $s^l_i = h^l_{A,i} - h^l_{A,i-1}$

Each delta acts as a **steering vector** injected additively at 1-3 selected layers, nudging the receiver's representations.

**Key findings**:
- **Deltas outperform raw states** — raw states sometimes degrade below NL baseline; deltas consistently improve. Strongest evidence that deltas, not raw states, are the right abstraction for same-model communication.
- Up to **+17.3%** over NL baselines on agent workflow tasks
- Context-agnostic: deltas capture reasoning dynamics only, stripped of sender's context-specific baseline
- Applied to only 1-3 middle-to-late layers (all layers degrades performance)

### 5. Structured KV-Cache Primitives (Agent Primitives)

[[agent-primitives-building-blocks|Agent Primitives]] uses KV-cache concatenation not just for transmission but to implement **computation structures** — Review (iterative critique), Voting (consensus), Planning (decomposition) — all in latent space.

**Key findings**:
- **+12-16.5% average accuracy** over single-agent across 8 benchmarks
- **RoPE positional re-encoding is critical** — without it, LLaMA-based models catastrophically collapse (AIME25: 56.7% → 26.7%)
- Stable across all backbones (unlike LatentMAS which fails on LLaMA)
- KV-cache communication is **noise-resilient**: retains 93% accuracy at 10 noise sentences vs 47% for NL
