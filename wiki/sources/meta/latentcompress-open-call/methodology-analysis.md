### Slot-Attention Compressor Architecture

The compression module uses a **slot-attention** mechanism (Locatello et al., 2020) with 4 learned slot vectors of dimension 64. Each slot attends to the full hidden-state sequence via iterative competitive attention: slots compete to "explain" different parts of the hidden-state sequence, naturally partitioning the information into disjoint groups.

The total message size is:

$$4 \text{ slots} \times 64 \text{ dim} \times 2 \text{ bytes (FP16)} = 512 \text{ bytes}$$

This yields a ~1/2000 compression ratio relative to full KV-cache transfer at MB scale.

The slot structure has an important connection to [[coconut-reasoning-latent-space|Coconut]]'s BFS discovery: if continuous thoughts encode superposed reasoning paths, slot-attention may **naturally disentangle** those paths (each slot capturing a distinct reasoning branch). This is untested but would connect compression research to the deepest theoretical finding in [[latent-space-reasoning]]. See [[latentcompress-collaboration-strategy]] for a proposed experimental test.

### Training on Inference Distribution (Key Methodological Insight)

The single largest improvement in compression quality came not from loss function design but from **collecting training hidden states on the inference distribution** rather than the training distribution. When hidden states are gathered during standard training (teacher forcing), the distribution of internal representations diverges from what the model produces during autoregressive inference.

Aligning the compressor's training data to the inference distribution eliminates this mismatch. This finding echoes the exposure bias problem well-known in sequence modeling and has implications for all methods that train auxiliary modules on frozen model representations:

- [[cache-to-cache-semantic-communication|C2C]]'s cache fuser — trained on prefill-derived KV-caches, which may differ from caches produced during interactive multi-round use
- [[interlat-latent-space-agents|Interlat]]'s communication adapter — trained on hidden states from standard generation
- [[softcot-efficient-reasoning|SoftCoT]]'s projection module — trained on frozen assistant model outputs

### Information Bottleneck + Style Adversarial Training

Experiment 4 combines two regularization strategies:

**Information bottleneck (IB)**: Adds a KL penalty encouraging the compressed representation to retain only task-relevant information, following the IB principle:

$$\min I(Z; X) - \beta I(Z; Y)$$

where $Z$ is the compressed state, $X$ the input, and $Y$ the target. The $\beta$ parameter controls the trade-off between compression and task utility.

**Style adversarial training**: A discriminator attempts to predict the sender's identity/style from the compressed message. The compressor is trained adversarially to prevent this leakage:

| Metric | Without adversarial | With adversarial |
|--------|-------------------|-----------------|
| Task accuracy | 99.97% | 99.95% |
| Style leakage | 35.2% | 13.5% |

This combination addresses a concern unique to latent communication: without adversarial debiasing, compressed representations could leak sender-specific information (model identity, training data artifacts) that has no communicative value but could be exploited.

### The Cumulative Degradation Model

The quality degradation formula models how compression error compounds across agent chains:

$$Q \propto e^{-T\varepsilon/C}$$

where $T$ is the number of agents in the chain, $\varepsilon$ is the per-step information loss rate, and $C$ is the channel capacity (in bytes). At 512 bytes, the measured $\varepsilon \approx 0.15$ across 8-agent chains.

This provides a principled framework for setting bandwidth budgets: given a target quality floor $Q_\text{min}$ and chain length $T$, the minimum required capacity is:

$$C_\text{min} = \frac{-T\varepsilon}{\ln(Q_\text{min})}$$

No other paper in the field provides an equivalent degradation model for multi-hop latent communication. The model also predicts that longer agent chains (higher $T$) require proportionally higher bandwidth — a finding consistent with [[latentmas-collaboration|LatentMAS]]'s observation that sequential 4-agent pipelines require substantial KV-cache transfer to maintain accuracy.
