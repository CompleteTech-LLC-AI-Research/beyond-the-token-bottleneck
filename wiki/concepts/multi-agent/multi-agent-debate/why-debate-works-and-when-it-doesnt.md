### The Mechanism

Debate works because it implements a form of **ensembling through interaction**. Unlike simple majority voting (where models generate independently), debate allows models to:
1. **See each other's reasoning chains**, not just final answers
2. **Correct specific errors** in each other's reasoning steps
3. **Converge** on correct answers through iterative refinement

The key difference from ensembling: debate is *sequential and interactive*, not parallel and independent. Each round conditions on the previous round's outputs, creating an iterative error-correction process.

### The Capability Threshold Problem

A central finding in the literature is that debate has a **capability threshold** — it only helps models that are already good enough:

| Model capability | Debate in natural language | Debate in embeddings | Debate via latent thoughts |
|-----------------|---------------------------|---------------------|--------------------------|
| Strong (GPT-4) | Significant improvement | Not tested (closed-source) | Not tested |
| Medium (GPT-3.5) | Moderate improvement | Not tested (closed-source) | Not tested |
| Weaker open-source (LLaMA-65B, Falcon-40B) | Often fails to beat majority voting | **Does beat majority voting** ([[cipher-multiagent-debate-embeddings|CIPHER]]) | Not tested |
| Small (0.6B-8B) | No improvement; may degrade | Limited evidence | **Significant improvement** ([[thought-communication-multiagent|ThoughtComm]]: +67% relative over single answer) |

The root cause: weaker models struggle to **parse and incorporate natural language feedback** in the specific format debate requires. They may fail to generate properly formatted responses, misinterpret other agents' reasoning, or be "persuaded" by confident-sounding wrong answers. [[embedding-space-communication|Embedding-space communication]] sidesteps the formatting/parsing problem entirely — the information is transmitted as vectors, not as text that must be correctly interpreted.

### Performance Bounds

[[cipher-multiagent-debate-embeddings|CIPHER]]'s experiments with "expert debaters" (always providing ground truth) and "dummy debaters" (providing nonsense) reveal the envelope:
- **Upper bound** (expert partner): LLaMA2-70B on GSM8K reaches ~88% — debate with a perfect partner nearly doubles the gap between single-answer and ceiling.
- **Lower bound** (nonsense partner): Performance degrades below single-answer baseline — bad partners actively hurt. This means debate is not a free lunch; the quality of the communication partner matters.
