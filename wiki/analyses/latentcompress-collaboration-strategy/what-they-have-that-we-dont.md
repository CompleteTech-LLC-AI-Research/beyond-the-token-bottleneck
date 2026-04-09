1. **Working code and experimental results** — 512-byte compression matching GSM8K baseline is a real result, not a thought experiment. Their slot-attention architecture, information bottleneck training, and style-adversarial debiasing are validated.

2. **The bandwidth-accuracy curve methodology** — their S-curve framework (sweep communication bandwidth from 0 to full-KV, find the "activation energy threshold" per task) is the right experimental paradigm for the field. Nobody else has this.

3. **The cumulative degradation model** — $Q \propto e^{-T\varepsilon/C}$ is a clean theoretical framework for understanding how compression loss compounds across agent chains. The $\varepsilon$ measurement methodology (fix task, vary chain length, extract per-step loss) is rigorous.

4. **Safety/auditability framing** — they're the only team in the entire field taking this seriously. Their argument is correct: if latent communication becomes standard, and it's opaque, current AI safety monitoring (CoT auditing) breaks completely. Slot-attention's interpretable structure is a genuine advantage.

5. **The QASPER finding** — 4.5% of full text outperforms 100% full text is a striking result that reframes the problem: it's not just "latent > text" but "the right compression > everything."
