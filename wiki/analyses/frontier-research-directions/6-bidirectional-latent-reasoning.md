**The signal**: [[thinking-states-latent-reasoning|Thinking States]] identifies a fundamental limitation of causal (left-to-right) latent reasoning: **state ambiguity**. When the question appears at the end of the input, the model may commit to reasoning about the wrong intermediate quantity before seeing what's being asked. Prepending the question improves accuracy from 42.22% to 48.65% — a 15% relative gain from a trivial change.

**The gap**: All latent reasoning methods in this collection are causal (left-to-right). Nobody has explored **bidirectional latent reasoning** — where continuous thoughts can attend to both past and future context. Encoder-decoder architectures or prefix-LM architectures could enable this, but the interaction with latent reasoning is unexplored.

**Why this could be paradigm-shifting**: Many real reasoning tasks require "look-ahead" — you need to know the goal before you can plan the path. Causal latent reasoning forces a commitment order that may be fundamentally wrong for planning tasks. Bidirectional latent reasoning would enable a model to encode the full problem context before beginning to reason, potentially eliminating the 18-point accuracy gap Thinking States observes on GSM8K.

**Concrete next steps**:
- Test encoder-decoder models (T5-style) with Coconut's hidden-state feedback in the decoder, conditioned on bidirectional encoder representations
- Design a "plan-then-reason" architecture where a bidirectional encoder produces a latent plan, then a causal decoder reasons step-by-step conditioned on it
- Measure whether state ambiguity disappears when the full input is encoded bidirectionally before latent reasoning begins

---
