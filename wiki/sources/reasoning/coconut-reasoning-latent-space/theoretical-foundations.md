### Why Language Is Not Optimal for Reasoning

The paper opens with a neuroscience argument: human brain imaging studies (Amalric & Dehaene 2019; Monti et al. 2007, 2009, 2012; Fedorenko et al. 2011, 2024) consistently show that **the language network remains largely inactive during reasoning tasks**. Language is optimized for communication, not computation. Forcing LLMs to reason in language space imposes an artificial constraint.

### Compute Allocation Problem

In CoT, every token gets roughly the same compute budget (one forward pass). But reasoning difficulty varies enormously across token positions:
- Most tokens are for **fluency** ("Let's", "we", "therefore") — trivially predicted, no reasoning needed.
- A few critical tokens encode the **actual reasoning steps** — these may require complex planning and deserve far more compute.

Coconut addresses this: in latent mode, each continuous thought gets a full forward pass dedicated to reasoning, with no compute wasted on fluency tokens.

### Connection to Expressivity Theory

Feng et al. (2023) showed that CoT increases the **effective depth** of transformers by looping outputs back as inputs. Coconut preserves this property — each continuous thought adds an effective transformer depth — while removing the information bottleneck of passing through the discrete token layer.
