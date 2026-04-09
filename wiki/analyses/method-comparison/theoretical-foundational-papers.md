These papers provide theoretical grounding rather than new methods:

| Paper | Key Contribution | Relevance |
|-------|-----------------|-----------|
| [[superposition-coconut-theory\|Superposition Theory]] | Proof: continuous CoT = parallel BFS in $D$ steps vs $O(n^2)$ discrete | Why Coconut works |
| [[cot-expressivity-theory\|CoT Expressivity]] | Proof: CoT increases effective depth ($\text{TC}^0 \to \text{NC}^1$) | Why reasoning steps help at all |
| [[platonic-representation-hypothesis\|Platonic Rep.]] | Models converge to shared statistical structure | Why cross-family AC works |
| [[relative-representations-zero-shot\|Relative Rep.]] | Latent spaces related by isometries; zero-shot stitching | Foundation for cross-model alignment |
| [[linearity-relation-decoding\|Linearity of Relations]] | Linear relational embeddings; mid-layer enrichment | Why layer ~26 is optimal for AC |
| [[scaling-agent-systems\|Scaling Framework]] | Task-contingent coordination; 5 architectures × 180 configs | When multi-agent helps vs hurts |
| [[latentcompress-open-call\|LatentCompress]] | 512-byte compression baseline; bandwidth-accuracy curves | Practical compression targets |
| [[latent-reasoning-supervision-analysis\|Latent Reasoning Supervision Analysis]] (Cui et al.) | Empirical test of Coconut's BFS hypothesis on 4 methods (Coconut, CODI, SIM-CoT, CoLaR); identifies the supervision–exploration trade-off and Improved Coconut variant | Falsifies the iterative-BFS claim while confirming the capacity claim; bounds the latent reasoning design space |
