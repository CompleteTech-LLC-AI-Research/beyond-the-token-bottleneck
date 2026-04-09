Catastrophic forgetting is one face of the **stability-plasticity dilemma** (Abraham & Robins, 2005): a system that is plastic enough to learn new information rapidly will be unstable enough to lose old information, and vice versa. This is not merely an engineering failure but a fundamental tension in any fixed-capacity learning system. The dilemma is particularly acute for LLMs because:

- **High plasticity is needed** to learn latent reasoning — a fundamentally new mode of operation
- **High stability is needed** to preserve instruction following, format compliance, factual knowledge, and reasoning patterns acquired through millions of training steps
