### Direction 1: Large-Scale Compressor Training
Current: trained on 300 samples, validated on GSM8K only. Goal: universal compressor across 50+ task families, curriculum learning (low→high compression), adaptive slot count. Target: $\leq$ 1KB with $\leq$ 3pp drop across all tasks.

### Direction 2: Native Latent Communication Pretraining
Currently all methods (including LatentMAS, Interlat, and this work) add modules to frozen models whose representations weren't designed for communication. Goal: integrate multi-agent communication objectives into pretraining itself. Target: 7B model natively supporting latent communication, 64 bytes with 90%+ information retention.

### Direction 3: Latent + Tool Use Hybrid Communication
No latent communication system supports tool calling. Goal: learned Router (hidden state → binary decision: stay latent or decode to tokens). 90% communication via latent channel, tool-critical outputs via tokens. Evaluation on ALFWorld, WebArena, SWE-bench.
