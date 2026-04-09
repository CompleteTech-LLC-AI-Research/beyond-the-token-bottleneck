### Why Non-Contiguous Selection Outperforms Contiguous Blocks

KVComm's selection strategy can pick layers like {8, 12, 15, 19, 23} rather than a contiguous block like {10, 11, 12, 13, 14}. This outperforms contiguous selection because the **most informative layers are scattered** across the network. The Gaussian prior centers the selection around intermediate layers, but the attention-importance score overrides this when specific early or late layers carry unusually high semantic content for a given model.

The non-contiguous finding aligns with C2C's learnable gate results: when C2C's Gumbel-sigmoid gates converge to binary values, the "on" layers are typically non-contiguous, confirming that the beneficial fusion layers do not cluster.

### The Attention Importance Score in Practice

The selection score $\hat{S}_{al}$ measures how much each layer's attention mechanism focuses on context tokens (as opposed to self-attention on the query). Layers with high $\hat{S}_{al}$ are those where the model is actively retrieving and integrating contextual information — these are precisely the layers whose KV-cache carries the most transferable semantic content.

The Gaussian prior $P_l$ serves as a **regularizer**: without it, selection based purely on attention scores can produce unstable results (different calibration samples may yield very different layer sets). The prior smooths the selection toward the theoretically motivated intermediate layer range, and the mixing weight $\alpha$ controls the balance between data-driven and prior-driven selection.

### Single-Sample Calibration: Why It Works

The finding that **one calibration sample** generalizes to the full test set is surprising and important for practical deployment. The explanation: layer-level attention patterns are a property of the **model architecture and weights**, not of individual inputs. While per-input attention distributions vary, the **average** attention importance across layers is remarkably stable. A single sufficiently diverse input activates enough of the model's attention patterns to produce a representative layer ranking.

This contrasts sharply with C2C's approach, where the learnable gate must be trained on hundreds of thousands of samples (OpenHermes2.5, 500K samples) to learn per-layer fusion decisions. The difference is that KVComm's selection is a simple ranking over a fixed model property, while C2C's gating must learn input-dependent behavior.
