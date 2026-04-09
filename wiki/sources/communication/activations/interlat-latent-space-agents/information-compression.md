### Compression via Latent-Space Reasoning

Full-length latents $H_L \in \R^{L \times d}$ are highly expressive but $L$ can be hundreds of steps, causing communication latency. The compression mechanism trains a separate **reasoning model $M$** to produce compact latents $H_K \in \R^{K \times d}$ where $K \ll L$.

The key mechanism is an **autoregressive latent-space reasoning loop** — the reasoning model feeds its last hidden state back as the next input embedding through a lightweight projection ("bridge module"):

> $$M(E_i) \to h_i, \quad E_{i+1} = E_i \;\|\; \text{Proj}(h_i)$$

This loop runs $K$ times, generating $K$ latent vectors entirely in latent space without ever decoding to tokens. The actor model and its communication adapter are **frozen** during compression training — only the reasoning model parameters are updated.

### Compression Training Objective

$\Loss_\text{compress} = \lambda_\text{task} \cdot \Loss_\text{task} + \lambda_\text{pref} \cdot \Loss_\text{pref} + \lambda_\text{geom} \cdot \Loss_\text{geom}$ (all weights = 1.0 in practice)

Three paths through the frozen actor:
- **Path A** (compressed latents $H_K$): the generated compressed message
- **Path D** (full-length latents $H_L$): reference from instruction-tuned model
- **Path B** (no latents): baseline with no communication

$\Loss_\text{task}$: Cross-entropy on frozen actor's predictions conditioned on $H_K$ — ensures compressed latents are useful.

$\Loss_\text{pref}$ **(Uncertainty-weighted agreement)**: Per-token weights $w_t = \max(H(p_t^B) - H(p_t^D), 0)$ emphasize positions where full latents actually reduce predictive uncertainty. The agreement loss is:

> $$\Loss_\text{pref} = \frac{T^2}{\sum w_t} \sum_{t \in S} w_t \cdot \text{KL}(p_t^D \| p_t^A)$$

This teaches $H_K$ to reproduce the informative behavioral effects of $H_L$ while ignoring positions where latents are unhelpful.

$\Loss_\text{geom}$ **(Latent direction alignment)**: Aligns global direction of actor-side latent features. Step-averaged directions $\bar{z}^A$ and $\bar{z}^D$ are computed, then:

> $$\Loss_\text{geom} = 1 - \cos(\bar{z}^A, \bar{z}^D)$$

This preserves geometric consistency between compressed and uncompressed latent spaces. Empirically the most critical compression loss.

Compression training: 64 A100-80GB GPUs, AdamW with learning rate 5e-5, warmup ratio 3%.
