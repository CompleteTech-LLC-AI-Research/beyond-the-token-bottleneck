### 1. The Multitask Scaling Hypothesis

> There are fewer representations that are competent for $N$ tasks than there are for $M < N$ tasks.

As models train on more diverse data and tasks, the set of valid representations shrinks. With internet-scale data, the solution set becomes very small. Mathematically: as models optimize empirical risk $\E_{x \sim \text{dataset}}[\Loss(f, x)]$ with more data, they better approximate the population risk $\E_{x \sim \text{reality}}[\Loss(f, x)]$, converging toward the true data-generating process.

### 2. The Capacity Hypothesis

> Bigger models are more likely to converge to a shared representation than smaller models.

If a globally optimal representation exists, larger function classes $\mathcal{F}$ are more likely to contain it. Two small models might find different local optima; two large models are more likely to find the same (better) solution. This is visualized as overlapping hypothesis spaces that increasingly cover the global optimum as they expand.

### 3. The Simplicity Bias Hypothesis

> Deep networks are biased toward finding simple fits to the data, and the bigger the model, the stronger the bias.

Even when many representations are consistent with training data, networks prefer simpler ones. This bias constrains the solution space and drives convergence. It also explains why models generalize: the simplest representation consistent with the training data is often the one that reflects the true underlying structure.
