The broader ML literature has developed several families of solutions to catastrophic forgetting, each with distinct trade-offs:

| Strategy | Key Methods | Mechanism | Trade-off |
|----------|-----------|-----------|-----------|
| **Regularization-based** | EWC (Kirkpatrick et al., 2017), Synaptic Intelligence (Zenke et al., 2017) | Penalize changes to parameters important for old tasks | Requires computing/storing parameter importance; slows new learning |
| **Replay-based** | Experience Replay, Generative Replay (Shin et al., 2017) | Interleave old-task data during new-task training | Requires storing or generating old data; computational overhead |
| **Architecture-based** | Progressive Neural Networks (Rusu et al., 2016), PackNet (Mallya & Lazebnik, 2018) | Allocate separate parameters for new tasks while freezing old | Growing model size; limited cross-task transfer |
| **Frozen-backbone** | Adapters, Prefix Tuning (Li & Liang, 2021), LoRA (Hu et al., 2022) | Train only a small set of new parameters; keep backbone frozen | Limited expressivity; may not capture complex new behaviors |
