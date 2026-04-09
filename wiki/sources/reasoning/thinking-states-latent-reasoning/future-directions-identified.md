1. **Extension to decoding phase**: Currently thoughts are generated only during input processing (prefill). Extending to the decoding phase could enable dynamic compute allocation during generation.

2. **RL warm-starting**: The supervised model could serve as initialization for reinforcement learning, allowing the model to optimize its thinking process beyond human-generated CoT traces. Starting from a model that already compresses reasoning into states could stabilize RL training.

3. **Bidirectional processing**: The state ambiguity problem would be resolved if the model could process the full input before committing to intermediate states. This motivates encoder-decoder or bidirectional variants.
