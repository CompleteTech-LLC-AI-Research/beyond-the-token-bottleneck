**The signal**: [[vision-wormhole-heterogeneous|Vision Wormhole]] discovers that VLM visual pathways are a natural "continuous communication port" because they're explicitly trained to process dense vectors. Text-only LLMs reject continuous injections (the "off-manifold" problem); VLMs accept them natively through their image-token span.

**The gap**: Vision Wormhole uses this for inter-agent communication only, and is tested only on small models (1.6B-4B). Nobody has explored:
- Using the visual pathway for **intra-model latent reasoning** (feed continuous thoughts through the image input rather than the text input, potentially solving the off-manifold problem that makes Coconut-style approaches difficult)
- **Multi-modal latent reasoning** — could a VLM reason about images, code, and math in a unified latent space by routing everything through the visual pathway?
- **Scaling the bandwidth** — the 256 visual token budget limits larger models. Multi-image injection, higher-resolution tokens, or variable-length visual spans could dramatically expand capacity.

**Why this could be paradigm-shifting**: VLMs are becoming the default architecture (most frontier models are multimodal). If the visual pathway can be repurposed as a universal continuous interface, it eliminates the key architectural barrier to latent communication — every VLM already has the "port" built in. No special training needed.

**Concrete next steps**:
- Test Coconut-style latent reasoning through a VLM's visual pathway (feed continuous thoughts as "images" rather than through the text embedding layer)
- Benchmark whether visual-pathway injection avoids the [[catastrophic-forgetting|catastrophic forgetting]] problem (since the text pathway remains untouched)
- Design a "latent reasoning image" — a learned representation that compresses a reasoning trajectory into a single image-format input

---
