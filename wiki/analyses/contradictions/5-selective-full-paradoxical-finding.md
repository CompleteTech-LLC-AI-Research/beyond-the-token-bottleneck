**Claim A**: More information transfer should produce better results — sharing full KV-cache or full hidden states should outperform selective sharing.
— Implicit assumption across the field

**Claim B**: Selective KV sharing (30% of layers) **matches or exceeds** sharing all layers. Sometimes exceeds the Skyline (full context, no communication needed).
— [[kvcomm-kth-selective|KVComm (Shi et al., 2025)]]

**Claim C**: Cyclic translation (A → shared space → A) **improves** model A beyond its original performance.
— [[kv-cache-alignment-shared-space|KV Alignment (Dery et al., 2026)]]

**Status**: **Paradox suggesting deeper principle**. Both findings suggest that intermediate representation spaces act as **beneficial regularizers** — filtering noise while preserving signal. This contradicts the naive "more = better" assumption and suggests an information-theoretic principle: optimal communication transmits *task-relevant* information, not maximum information.

**Resolution needed**: Theoretical framework explaining when and why selective/mediated transfer outperforms full transfer. Rate-distortion theory may apply — there may be a task-specific "channel capacity" beyond which additional information introduces harmful noise.

---
