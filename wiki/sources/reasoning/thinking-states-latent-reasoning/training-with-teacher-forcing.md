### Parallel Training

Because ground-truth reasoning annotations $Z_i^*$ are available for each chunk, gold states $S_i^* = C(Z_i^*)$ can be **precomputed** for all chunks simultaneously. All chunks can then be processed in a **single parallel forward pass** through $M_\theta$:

$$\tilde{X}_i = X_i + S_i^*, \quad \forall i$$

This eliminates sequential dependencies during training entirely. The Thinking Block is then trained to predict $Z_i^*$ via standard next-token prediction, in parallel over all chunks. Each $H_i^{out}$ is computed under the gold state history $S_1^*, \ldots, S_i^*$, so predicting $Z_{i+1}$ is implicitly conditioned on all prior gold reasoning steps.

### Training Objective

$$\Loss = \Loss_{\text{LM}} + \sum_{i=1}^{K} \Loss_T(Z_i, Z_i^*)$$

where $\Loss_{\text{LM}}$ is the standard language modeling loss and $\Loss_T$ is cross-entropy over thinking sequences.

### Training Cost Comparison

The paper directly measures wall-clock time for forward + backward passes:

| Recurrent Steps | BPTT (Coconut) | Teacher Forcing (Thinking States) |
|----------------|---------------|----------------------------------|
| 1 | ~1x | ~1x |
| 5 | ~5x | ~1.1x |
| 10 | ~10x | ~1.1x |
| 20 | ~20x | ~1.1x |

BPTT cost grows **linearly** with recurrence depth. Thinking States maintains **approximately constant** training time regardless of reasoning depth. At 10 steps, BPTT incurs a **~10x cost penalty**.

### Fast Prefill with Speculative Thinking

While training is fully parallel, naive inference is sequential across chunks. The paper introduces an exact prefill algorithm exploiting the observation that most chunks produce **trivial states** (EOS-only thoughts):

1. Perform parallel forward pass over all chunks, speculating all states are trivial
2. Generate thinking states for each chunk using T and C
3. Identify earliest chunk $i_1$ with non-trivial state -- all chunks before $i_1$ are correctly computed
4. Cache positions up to $i_1$ and repeat from step 1 for remaining chunks

The algorithm completes in $|R| + 1$ rounds, where $|R|$ is the number of chunks with non-trivial states. When $|R| \ll K$ (typical regime), prefill latency is substantially reduced.
