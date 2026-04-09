The following table collects concrete numbers from papers in this wiki, showing the accuracy and efficiency consequences of moving between discrete and continuous representations:

| Paper | Task | Discrete method | Continuous method | Discrete accuracy | Continuous accuracy | Compression factor |
|-------|------|----------------|-------------------|-------------------|--------------------|--------------------|
| [[coconut-reasoning-latent-space\|Coconut]] | ProsQA (graph reach.) | Discrete CoT | Continuous thoughts | 77.5% | 97.0% | $O(n^2) \to O(D)$ steps |
| [[coconut-reasoning-latent-space\|Coconut]] | GSM8K | Discrete CoT | Continuous thoughts | 34.3% | 34.1% | ~1x (no gain) |
| [[cipher-multiagent-debate-embeddings\|CIPHER]] | Arithmetic | NL debate ($T=0.54,1.0$) | Embedding debate ($T=0.15,1.75$) | ~81% | ~85% | 15 bits $\to$ $d \times 32$ bits/pos |
| [[cipher-multiagent-debate-embeddings\|CIPHER]] | GSM8K | NL debate | Embedding debate | ~65% | ~66% | 15 bits $\to$ $d \times 32$ bits/pos |
| [[thought-communication-multiagent\|ThoughtComm]] | MATH (Qwen-3-1.7B) | Multiagent finetune (NL) | Disentangled thoughts | 75.8% | 93.0% | $n_z$ latent dims |
| [[thought-communication-multiagent\|ThoughtComm]] | MATH (Phi-4-mini) | Multiagent finetune (NL) | Disentangled thoughts | 60.2% | 74.6% | $n_z$ latent dims |
| [[superposition-coconut-theory\|Zhu et al.]] | Graph reachability | Discrete CoT (sequential) | Superposition (parallel BFS) | $O(n^2)$ steps | $D$ steps | Quadratic $\to$ linear |

Key patterns: (1) The continuous advantage is **largest on tasks requiring parallel exploration** (ProsQA, MATH) and **smallest on sequential arithmetic** (GSM8K), consistent with the superposition hypothesis. (2) The advantage scales with model weakness — smaller models (Qwen-3-0.6B, 1.7B) gain more from continuous communication than larger ones, likely because weaker models lose more information at the discrete bottleneck. (3) [[thought-communication-multiagent|ThoughtComm]]'s structured continuous approach consistently outperforms [[cipher-multiagent-debate-embeddings|CIPHER]]'s unstructured continuous approach, suggesting that structure matters beyond raw information preservation.
