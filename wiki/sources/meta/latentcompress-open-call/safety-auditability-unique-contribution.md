The project makes a strong case that latent communication creates a **governance crisis**: if agents communicate in opaque continuous vectors, current Chain-of-Thought monitoring fails completely. Three proposed solutions:

1. **Interpretable compression** (current): Slot-attention slots can be probe-decoded to nearest NL descriptions. Extreme compression (512B) **forces** structured information organization, making it more auditable than high-bandwidth opaque transfer.
2. **Channel constraints** (architecture-level): Bandwidth budgets, semantic anchoring (require latent messages to be decodable to readable text as "audit shadow"), adversarial debiasing.
3. **Runtime monitoring** (long-term): Anomaly detection on latent communication distributions, information flow tracking, degradable "audit mode."
