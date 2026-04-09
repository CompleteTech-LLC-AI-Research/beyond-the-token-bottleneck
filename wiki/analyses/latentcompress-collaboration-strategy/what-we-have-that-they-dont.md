Their analysis references only 3 papers ([[latentmas-collaboration|LatentMAS]], [[interlat-latent-space-agents|Interlat]], [[vision-wormhole-heterogeneous|Vision Wormhole]]). Our wiki covers **27 papers** spanning the full research landscape. This gives us several insights they're missing:

### 1. Superposition Reasoning (Their Blind Spot)

They cite [[coconut-reasoning-latent-space|Coconut]]'s BFS finding in their "why this matters" section but don't connect it to their compression work. This is a critical gap:

**If continuous thoughts encode superposed reasoning paths (Coconut), what happens when you compress them to 512 bytes?** Do the superposed paths survive compression? If slot-attention forces disentanglement (each slot captures one path), this could be the accidental discovery of the "disentangling superposition" direction we identified as the #2 highest-potential research direction.

**Concrete experiment they should run**: After compressing to 4 slots, probe each slot to see if it corresponds to a distinct reasoning path (using Coconut's methodology of forcing language continuation from each slot independently). If yes, they've built a disentanglement machine.

### 2. State Deltas (Unexplored Communication Medium)

They compress raw hidden states. [[state-delta-trajectory|SDE]] shows that **inter-token deltas** outperform raw states — sometimes raw states degrade below NL baseline while deltas consistently improve. They should test compressing deltas instead of raw hidden states. This could dramatically reduce the bandwidth needed (deltas are already denoised of context-specific baselines).

### 3. The Self-Improvement Effect

Three papers in our collection find that mediating through a shared space improves the original model. Their slot-attention compressor IS a shared space. They should test: does passing a model's own hidden states through the compressor and back (cyclic: model → slots → model) improve the model's solo performance? If yes, their compressor doubles as a self-distillation module.

### 4. The Layer Selection Literature

[[kvcomm-kth-selective|KVComm]] and [[activation-communication-harvard|AC]] establish that intermediate layers (~layer 26/32) carry the richest information. Their compressor presumably operates on last-layer hidden states. Testing extraction from mid-late layers might improve compression efficiency — the information may already be more compact at the optimal layer.

### 5. Cross-Architecture Communication

Their work is same-model only (Qwen3-14B). [[cache-to-cache-semantic-communication|C2C]], [[kv-cache-alignment-shared-space|KV Cache Alignment]], and [[vision-wormhole-heterogeneous|Vision Wormhole]] address cross-architecture communication. Their slot-attention compressor could serve as a **universal codec** if trained on multiple model families — slots as the "interlingua."

### 6. The Catastrophic Forgetting Context

They train only the compression head (frozen backbone) — good. But they should be aware of [[softcot-efficient-reasoning|SoftCoT]]'s finding that any backbone modification destroys instruction-tuned capabilities. If Direction 2 (native pretraining) requires backbone modification, they'll hit this wall.
