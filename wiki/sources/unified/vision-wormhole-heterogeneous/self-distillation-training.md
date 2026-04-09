The codec is trained via **label-free self-distillation** — no human annotation required. The text-based communication path acts as "Teacher" and the vision wormhole acts as "Student."

**Setup:** Anchor messages m (short text strings) are used. The teacher prompt includes m explicitly as text. The student prompt omits m but contains a dummy image whose image-token span is overwritten by the injection computed from the teacher-side rollout.

**Loss function** (Eq. 3, three terms):

$$\Loss_\text{codec} = \lambda_h \|h_\text{vis} - \text{stopgrad}(h_\text{text})\|^2 + \lambda_\text{kl} \cdot \text{KL}(\text{softmax}(z_\text{text}/\tau) \| \text{softmax}(z_\text{vis}/\tau)) + \lambda_\text{rms} (\text{RMS}(\Delta_\text{inj}) - \text{RMS}(\bar{X}_\text{img}))^2$$

- **Hidden-state MSE** (weight 1.0): Enforces representational fidelity at the prompt boundary
- **KL divergence** (weight 0.25, temperature $\tau = 1.0$): Enforces output-distribution fidelity over the full vocabulary — especially informative because it provides rich gradient over the entire vocabulary distribution, not just a single target token
- **RMS matching** (weight 0.1): Stabilizes injection magnitude in the visual embedding manifold

Only codec parameters ($E_i$, $D_i$) are updated. Backbone remains frozen. Gradient clipping at max-norm 1.0.
