**The signal**: [[interlat-latent-space-agents|Interlat]] shows that 500+ latent steps can be compressed to **8 steps** with only 4% accuracy drop and 46× speedup. [[softcot-efficient-reasoning|SoftCoT]] shows 6 soft tokens $\approx$ 24 hard tokens (4× compression). These suggest there's massive redundancy in both discrete and continuous communication.

**The gap**: Compression is explored only as an engineering optimization. Nobody has asked: **what is the minimum sufficient representation for inter-agent communication?** Is there a theoretical lower bound on the bandwidth needed to transmit a reasoning trajectory? What information-theoretic principles govern optimal latent compression?

**Why this could be paradigm-shifting**: If the theoretical minimum is much smaller than current methods transmit (which the 46× compression suggests), then latent communication could become essentially free — a few vectors per message, transmitted in microseconds. This would make latent multi-agent systems practical for real-time applications (robotics, dialogue, live coding assistance).

**Concrete next steps**:
- Establish information-theoretic bounds on minimum communication bandwidth for various task types
- Design rate-distortion optimal latent codecs (borrowing from neural compression literature)
- Test whether the minimum bandwidth varies with task complexity, model size, or number of agents

---
