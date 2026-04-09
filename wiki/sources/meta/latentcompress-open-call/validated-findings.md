1. Compressed latent communication **works** (16B: 12%→57% on communication-dependent accuracy)
2. Simple tasks need minimal bandwidth (GSM8K: 512B = baseline)
3. Hard tasks need more bandwidth (GPQA: 512B drops back to baseline; needs MB)
4. **Training alignment matters more than loss design** — collecting hidden states on inference distribution (not training distribution) is the biggest single improvement
5. Full text is not the upper bound (QASPER: 4.5% selected text > 100% full text)
6. Cumulative degradation follows $Q \propto e^{-T\varepsilon/C}$ — 512B yields $\varepsilon \approx 0.15$ across 8-agent chains
