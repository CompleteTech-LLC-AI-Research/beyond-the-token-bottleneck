- **Low absolute alignment** (~0.16 on mutual k-NN): May reflect fundamental limits of cross-modal information overlap, not just noise. Different modalities genuinely contain different information.

- **Different modalities contain different information**: Language can't fully describe a solar eclipse; images can't convey "freedom of speech." The bijective observation function assumption is idealized; real sensors are lossy and partial. This limits how far convergence can go.

- **Not all modalities converging**: Robotics and other physical interaction modalities lack standardized data infrastructure. Convergence is most evident in vision and language, which have the most training data.

- **Sociological bias**: The AI community's preference for human-like reasoning and human-generated training data may drive convergence toward human representations specifically, not "reality." If we trained models on alien data, would they converge to the same representation?

- **Simplicity bias as alternative explanation**: Convergence could partly reflect shared inductive biases in deep networks (similar optimizers, architectures, initialization schemes) rather than convergence on a true model of reality. Similar architectures might find similar solutions regardless of what those solutions represent.

- **Kernel alignment $\neq$ pointwise alignment**: PRH demonstrates that similarity *structure* is shared; [[activation-communication-harvard|AC]] requires individual activation *vectors* to be substitutable -- a stronger requirement that may still need at minimum an affine correction. The gap between kernel-level agreement and vector-level compatibility is non-trivial.

- **Selection bias in evidence**: The 78 vision models all use deep learning with SGD-type optimizers on GPU hardware. Whether convergence persists across fundamentally different learning paradigms (symbolic AI, neuromorphic computing) is unknown.

- **Convergence rate uncertainty**: The linear relationship between scale and alignment suggests convergence will continue, but the ultimate ceiling is unknown. The ~0.16 alignment score could be near the true maximum or far from it.
