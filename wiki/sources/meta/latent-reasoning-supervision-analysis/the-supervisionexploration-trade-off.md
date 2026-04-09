The paper's central conceptual contribution is identifying a **fundamental supervision-strength trade-off**:

| Supervision strength | Shortcut behavior | Latent diversity | Pass@100 ceiling | Practical accuracy |
|---|---|---|---|---|
| Weak (Coconut, CODI) | Severe (especially on simple tasks) | High | High | Limited by inability to amplify correct candidate |
| Strong (SIM-CoT, CoLaR) | Reduced or eliminated | Low | Low | Limited by loss of capacity |

This is **distinct from but complementary to** the [[catastrophic-forgetting|alignment trade-off]] identified by [[softcot-efficient-reasoning|SoftCoT]]:

| Trade-off | Tension | Mitigation in literature |
|---|---|---|
| Alignment trade-off | Backbone modification damages instruction-tuning | Frozen-backbone designs ([[softcot-efficient-reasoning|SoftCoT]], [[thinking-states-latent-reasoning|Thinking States]], [[latentmas-collaboration|LatentMAS]]) |
| **Supervision–exploration trade-off** | **Stronger supervision destroys latent capacity** | **None — open problem** |

Together, these two trade-offs **bound** the latent reasoning design space from both sides: too little supervision and the model takes shortcuts or fails to exploit its own representations; too much supervision and the latent state collapses to a deterministic compression of CoT.
