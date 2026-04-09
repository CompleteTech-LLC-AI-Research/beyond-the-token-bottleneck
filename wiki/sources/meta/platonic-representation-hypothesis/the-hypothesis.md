Drawing on Plato's Allegory of the Cave: training data are "shadows on the cave wall" (projections of an underlying reality $Z$), yet models are recovering ever-better representations of the actual world outside. There exists an underlying joint distribution $P(Z)$ over events in the real world. Images, text, audio are all projections of $Z$ through different observation functions. As models scale, their learned representations increasingly approximate this shared latent structure.

The hypothesis is stated formally:

> **The Platonic Representation Hypothesis:** Neural networks, trained with different objectives on different data and modalities, are converging to a shared statistical model of reality in their representation spaces.

The related **"Anna Karenina scenario"** (Bansal et al., 2021): all well-performing nets represent the world the same way. The PRH adds the claim that the representation they converge on is specifically a statistical model of underlying reality -- not just any shared solution, but one grounded in the causal structure of the world.
