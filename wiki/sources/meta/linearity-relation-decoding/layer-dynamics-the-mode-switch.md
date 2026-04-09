The paper's most important finding for latent communication:

**Faithfulness rises through early-to-middle layers, then drops sharply in later layers.** Example (GPT-J, "plays the sport of"): faithfulness peaks at ~layer 7-17, then plummets.

### Why: Dual-Purpose Hidden Representations

Hidden states serve two purposes simultaneously:
1. **Encoding entity attributes** (relational knowledge, facts about the subject)
2. **Preparing next-token prediction** (output-optimized representation)

At later layers, purpose #2 overwrites purpose #1. The model "throws away" relational knowledge not needed for the immediate next-token prediction.

### Evidence for the Mode Switch

When the object token immediately follows the subject (no relation-specific context), faithfulness does **not** drop in later layers — because there's no competing prediction task to overwrite the relational encoding.

**Causality drops earlier than faithfulness**: Because information leaks from pre-intervention layers through attention (layers 0 to l-1 retain original subject info).
