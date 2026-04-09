The wiki's [[frontier-research-directions]] document identifies "superposition reasoning at frontier scale" and "disentangling superposed reasoning paths" as the two highest-potential research directions. Both rest on Coconut's empirical claim of **emergent BFS** ([[raw/pdf/arxiv-2412.06769.pdf|Coconut §4.2]]) and Zhu et al.'s theoretical proof that continuous thoughts can encode reachability frontiers ([[superposition-coconut-theory|Zhu et al. Theorem 1]]). Cui et al. **separate these two claims**:

- **Capacity** (a latent vector can encode multiple candidates) — confirmed via Pass@100 analysis: latent reasoning's Pass@100 (62–82%) consistently exceeds explicit reasoning's (44–62%) by 20+ points.
- **Use** (the model actually performs BFS-like exploration across iterations) — falsified. Diversity *decreases* with more latent steps; majority-vote accuracy stays *below* explicit reasoning by 3–4 points.

This is the cleanest decomposition yet of the gap between Coconut's theoretical promise and its empirical reality.
