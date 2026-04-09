### Where Thinking States Wins Over CoT

Approximately **12% of queries** correctly solved by Thinking States are *not* solved by CoT. Two representative failure modes of CoT:

**Hallucinated steps:** CoT generates an additional spurious reasoning step (e.g., "10*12=120, 120*2=240, 240*30=7200, 7200*6=43200" -- the final step is hallucinated). Thinking States produces the correct 3-step trajectory.

**Over-complex computation:** CoT attempts multiple operations in a single step and errs (e.g., "60-17-34=8" instead of computing each subtraction separately). Thinking States decomposes into atomic operations: "17*2=34", "17+34=51", "60-51=9".

Both models are fine-tuned from the same base model on identical training data, so these differences reflect the method's structural properties, not data advantages.

### The State Ambiguity Problem

The 18-point GSM8K gap is partly explained by **state ambiguity**: the question (what to compute) appears at the end of the input, but Thinking States processes left-to-right. The model may commit to reasoning about the wrong quantity before seeing the question.

**Example:** "Richard lives in a building with 15 floors. Each floor contains 8 units. [T: 15*8=120] Three quarters of the units are occupied. [T: (3/4)*120=90] What's the number of unoccupied units on **each floor**? [T: 120-90=30]" -- The model computes total unoccupied (30) rather than per-floor (2) because it cannot anticipate "on each floor" until the final clause.

**Disambiguation test:** Prepending the question to the start of the prompt ("What's the number of unoccupied units on each floor? Richard lives in a building...") improves accuracy from **42.22% to 48.65%** -- a 6.43-point gain. This is a zero-shot intervention (no retraining), confirming the hypothesis. Notably, this limitation stems from combining chunk-recurrence with a **causal autoregressive backbone**; bidirectional processing could identify the target quantity from the full input before committing to states.
