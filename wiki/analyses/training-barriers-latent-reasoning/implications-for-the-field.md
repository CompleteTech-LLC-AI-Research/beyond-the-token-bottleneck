### The Base-to-Aligned Gap

The gap between "works on GPT-2" and "works on LLaMA-3.1-8B-Instruct" is a recurring challenge across ML. Results at small scale on base models may not transfer to production-grade instruction-tuned models. This has profound implications:

- **Latent reasoning may require architectural innovation**, not just training tricks, to work with frontier models
- **Frozen-backbone approaches** ([[softcot-efficient-reasoning|SoftCoT]], [[thinking-states-latent-reasoning|Thinking States]]) may be the only viable path for instruction-tuned models
- Papers demonstrating latent reasoning on base models should be read with caution about transferability

### The Alignment Tax

Catastrophic forgetting creates an **alignment tax** for latent reasoning research: the more aligned and capable a model is, the harder it is to add new capabilities through fine-tuning. This is ironic — the models that would benefit most from enhanced reasoning (frontier instruction-tuned models) are exactly the ones where enhancement is hardest.

### Toward Modular Solutions

The trajectory across the three solutions — from [[coconut-reasoning-latent-space|Coconut]]'s full-model training to [[softcot-efficient-reasoning|SoftCoT]]'s external assistant to [[thinking-states-latent-reasoning|Thinking States]]' lightweight modules — shows a clear trend toward **modularity**. Future solutions will likely further separate "reasoning enhancement" from "core model capabilities," potentially through:

- Specialized reasoning co-processors that operate alongside frozen LLMs
- Standardized interfaces for injecting continuous reasoning signals (prefix tokens, KV-cache entries, activation injections)
- Training-free latent reasoning methods that exploit inference-time computation without any gradient-based learning
