A spectrum of compatibility requirements:

| Approach | What's needed |
|----------|--------------|
| [[activation-communication-harvard|AC]] (no W) | Roughly aligned activation spaces — works across LLaMA/Qwen/Gemma |
| [[activation-communication-harvard|AC]] (with W) | Learned linear mapping (3072 C4 sentences, one-time) |
| [[interlat-latent-space-agents|Interlat]] | Trained communication adapter (MHA + projection) |
| [[latentmas-collaboration|LatentMAS]] | Same model architecture (training-free alignment) |
| [[state-delta-trajectory|SDE]] | Same model weights (deltas only meaningful in shared space) |
| [[agent-primitives-building-blocks|Agent Primitives]] | Same model weights (KV-cache concatenation assumes shared layers) |

Why does cross-model activation communication work at all? The answer is the shared framing used across every deep-stage method:

![[representation-alignment]]

Two activation-specific corollaries follow directly from this foundation. First, [[relative-representations-zero-shot|Moschella et al.]] report roughly **two orders of magnitude** improvement in stitching quality over absolute representations — a concrete quantitative floor for how much alignment buys you in practice. Second, [[linearity-relation-decoding|Hernandez et al.]] show that the faithfulness of linear relational decoding **peaks at mid-layers (~20-26) then drops in later layers**: the model enriches representations with relational knowledge before compressing them for next-token prediction. This is the mechanistic explanation for why [[activation-communication-harvard|AC]]'s layer-26 is optimal and why [[kvcomm-kth-selective|KVComm]] finds intermediate layers most transferable — it's where the richest information lives, before the output layers discard it.

Together these pin down not just *whether* cross-model activation sharing should work, but *where* in the stack it works best. The five approaches above navigate this alignment problem differently: some assume it ([[latentmas-collaboration|LatentMAS]], [[state-delta-trajectory|SDE]], [[agent-primitives-building-blocks|Agent Primitives]] stay in-model), some exploit it directly without any learned map ([[activation-communication-harvard|AC]] cross-family), and some learn an explicit bridge on top of it ([[interlat-latent-space-agents|Interlat]]'s communication adapter, [[activation-communication-harvard|AC]]'s optional linear W).
