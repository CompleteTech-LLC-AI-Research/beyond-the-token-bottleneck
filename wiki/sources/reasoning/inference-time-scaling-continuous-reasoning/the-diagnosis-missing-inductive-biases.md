Wang et al.'s discussion section pinpoints a single root cause: **COCONUT's training objective applies supervision only to the final text answer**, not to the latent thoughts themselves. The continuous-thought representations are therefore optimized solely for end-task accuracy, with no pressure to develop *structural* properties that would let an external verifier discriminate correct from incorrect reasoning.

Three concrete mitigations are proposed but not tested:

1. **Isotropy regularization** during training to spread latent representations across more dimensions, breaking the geometric homogeneity that prevents discrimination.
2. **Trajectory diversity objectives** that encourage geometrically varied reasoning paths for different problem types.
3. **Contrastive losses** that explicitly teach the model to produce *different* latent representations for correct versus incorrect reasoning patterns.

The general principle: **inference-time scaling cannot be retrofitted onto a representation that was never trained to support discrimination.** The solution must be in training, not decoding.
