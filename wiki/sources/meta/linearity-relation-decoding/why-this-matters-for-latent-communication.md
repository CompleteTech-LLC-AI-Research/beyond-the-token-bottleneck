### 1. Justifies mid-layer communication
The enriched representation finding explains why [[activation-communication-harvard|AC]] (layer 26/32), [[kvcomm-kth-selective|KVComm]] (intermediate layer selection with Gaussian prior), and [[state-delta-trajectory|SDE]] (middle-to-late layers) all find intermediate layers carry the most useful information. That's where the richest relational knowledge lives, before output compression discards it.

### 2. Internal knowledge > expressed knowledge
The attribute lens shows models encode facts they don't output. Latent communication (sharing activations/KV-cache) can transmit knowledge that would **never appear in natural language output** — a fundamental advantage over text-based communication that no amount of prompt engineering can close.

### 3. Linear structure enables simple alignment
If relational knowledge is encoded linearly, cross-model alignment ([[activation-communication-harvard|AC]]'s W, [[kv-cache-alignment-shared-space|KV Cache Alignment]]'s affine transforms, [[vision-wormhole-heterogeneous|Vision Wormhole]]'s affine alignment) is theoretically justified — the representations have the right geometric structure for linear projection.

### 4. But 52% of relations are NOT linear
This heterogeneity means some knowledge requires **deeper, nonlinear** communication. Linear projections may fail on relations with large ranges (company CEOs, person parents). This motivates richer approaches like [[thought-communication-multiagent|ThoughtComm]]'s autoencoder or [[cache-to-cache-semantic-communication|C2C]]'s neural fuser with dynamic head weighting.

### Connection to the Platonic Representation Hypothesis

The linearity findings provide mechanistic evidence for the [[platonic-representation-hypothesis|Platonic Representation Hypothesis]] at the **intra-model** level. PRH claims that different models converge to approximately isometric representations of reality; this paper shows that *within* a single model, relational knowledge is encoded as linear structure in the representation space. These are complementary claims:

- **PRH (inter-model)**: The mapping between Model A's and Model B's representations of the same entity is approximately linear.
- **LRE (intra-model)**: The mapping from a subject representation to its relational attributes within a single model is approximately linear.

Together, they predict that a linear projection from Model A's subject representation should recover relational attributes in Model B's space — exactly the operation performed by [[activation-communication-harvard|AC]]'s mapping matrix $W$ and [[kv-cache-alignment-shared-space|KV Cache Alignment]]'s affine adapters.

The 48%/52% split also refines PRH's predictions. PRH posits convergence toward a shared representation, but this paper shows that convergence is **relation-dependent**. Relations with small, categorical ranges (countries, languages, genders) are linearly encoded and therefore likely to be well-aligned across models. Relations with large, idiosyncratic ranges (company CEOs, person parents) are nonlinearly encoded and may require richer cross-model alignment mechanisms. This suggests that the "platonic representation" is not uniformly accessible — some aspects of shared reality are geometrically simpler than others.

The cross-model consistency result (Spearman $R = 0.85$ between GPT-J and GPT2-XL, $R = 0.71$ with LLaMA-13B) provides direct evidence: the same relations are linear in the same models. This is a non-trivial prediction of PRH — if models converge to similar representations, they should encode the same knowledge with similar geometric structure.
