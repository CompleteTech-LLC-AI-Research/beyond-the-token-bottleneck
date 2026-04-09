| # | Tension | Papers | Status | Priority |
|---|---------|--------|--------|----------|
| 1 | Curriculum works (base) / breaks (instruct) | [[coconut-reasoning-latent-space\|Coconut]] vs [[softcot-efficient-reasoning\|SoftCoT]] | Different regimes | **High** — blocks production use |
| 2 | Raw states help / raw states hurt | [[activation-communication-harvard\|AC]] vs [[state-delta-trajectory\|SDE]] | Same regime, unresolved | **High** — fundamental design question |
| 3 | More agents help / more agents hurt | Debate papers vs Scaling | Different task distributions | Medium — understood but not tested with latent methods |
| 4 | Cross-arch easy (activations) / hard (KV) | AC vs C2C/KV Align | Different representation depths | Medium — regime-dependent |
| 5 | Selective > full (paradox) | [[kvcomm-kth-selective\|KVComm]], [[kv-cache-alignment-shared-space\|KV Alignment]] | Suggests deeper principle | **High** — potential paradigm insight |
| 6 | Training-free competitive / trained richer | Multiple | Design trade-off | Low — understood trade-off |
| 7 | BFS excels at search / fails at math | [[coconut-reasoning-latent-space\|Coconut]] (internal) | Task-dependent, acknowledged | Low — well understood |
| 8 | Interpretability needed / prevents superposition | [[thinking-states-latent-reasoning\|Thinking States]] vs [[coconut-reasoning-latent-space\|Coconut]] | Fundamental tension | Medium — needs creative resolution |
| 9 | BFS as faithful search / implicit pruning / geometrically structureless | [[coconut-reasoning-latent-space\|Coconut]], [[superposition-coconut-theory\|Zhu et al.]] vs [[latent-reasoning-supervision-analysis\|Cui et al.]] vs [[inference-time-scaling-continuous-reasoning\|Wang et al.]] | Substantially resolved — capacity confirmed, dynamics falsified, naive reranking falsified, geometric structure absent | **High** — redirects the agenda from scaling/decoding to training-time inductive biases |
