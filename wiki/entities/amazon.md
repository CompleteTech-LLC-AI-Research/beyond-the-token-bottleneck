---
type: entity
title: "Amazon"
created: "2026-04-08"
updated: "2026-04-08"
aliases: [Amazon, Amazon Research, Amazon Science]
tags: [organization, company, industry-lab]
---

# Amazon

Industrial research organization contributing the first comprehensive empirical analysis of [[latent-space-reasoning|latent reasoning]] internal mechanisms. Amazon's contribution is **diagnostic, not constructive**: rather than proposing a new method, it dissects the assumptions underlying existing methods and identifies fundamental limitations in how the field trains and evaluates latent reasoning.

## Contribution Timeline

![[amazon/timeline]]

## Research Themes

Amazon's single contribution to this collection sits at the **mechanistic-analysis** end of latent reasoning research:

- **Shortcut diagnostics**: Tests whether [[latent-space-reasoning|latent reasoning]] methods actually use their latent steps via depth ablation, noise injection ($\sigma = 100$, $\sim 4 \times$ embedding norm), and attention-pattern analysis. Finds that most methods retain non-trivial accuracy even when latent reasoning is destroyed — they exploit input-side shortcuts rather than performing genuine multi-step computation.
- **BFS hypothesis testing**: Empirically separates two claims that the literature conflates: (a) latent vectors *can* encode multiple candidate trajectories (confirmed via Pass@100 advantage of 20+ points over explicit reasoning), and (b) the iterative latent process *does* perform breadth-first expansion (falsified — diversity decreases with depth, the opposite of BFS).
- **Supervision taxonomy**: Introduces the **weak/strong supervision** classification, showing that the design space of latent reasoning is bounded by a fundamental trade-off between shortcut resistance (strong supervision wins) and latent capacity (weak supervision wins). This complements [[catastrophic-forgetting|SoftCoT's alignment trade-off]] as a second axis of constraint.
- **Improved Coconut**: A drop-in modification to Coconut's stage-wise curriculum that mixes earlier-stage data into later stages, raising GPT-2 GSM8K-Aug accuracy from 34.09% to 41.06% — the first reported improvement to Coconut's training scheme since the original paper.

## Collaboration Network

Cui et al. is a collaboration between Amazon's research arm and [[#Indirect Connections to Other Entities|Michigan State University]] (Yingqian Cui's home institution; the work was completed during her Amazon internship). The other authors are Amazon researchers.

### Indirect Connections to Other Entities

Amazon has no direct co-authorship with other wiki entities, but Cui et al. is methodologically and intellectually connected to several:

- **[[fair-meta|FAIR at Meta]]**: Directly tests, critiques, and improves [[coconut-reasoning-latent-space|Coconut]]. The Improved Coconut variant should be cited by any future work building on Coconut. Amazon's findings constrain the credibility of FAIR's emergent-BFS narrative.
- **[[cmu|CMU]] / UC Berkeley / UC San Diego (via Zhu et al.)**: Empirically falsifies the *iterative* BFS extension of [[superposition-coconut-theory|Zhu et al.'s superposition theory]], while confirming the *capacity* claim. The two papers together bracket what is and isn't true about parallel BFS in latent space.
- **CODI / SIM-CoT / CoLaR authors** (Shen et al., Wei et al., Tan et al.): Cui et al. is the first paper to evaluate these methods side-by-side under a unified taxonomy. None of these methods currently have wiki source pages, but they are first-class objects in the supervision-strength comparison.
- See [[research-positioning-patterns|Research positioning patterns]] for analysis of Amazon's industry-lab role in the collection.

## Strategic Position

Cui et al.'s findings define **two open problems** that Amazon is well-positioned to address in follow-up work:

1. **Closing the Pass@100 / Maj@100 gap**: Latent reasoning preserves correct candidates (Pass@100 ~70-82%) but fails to amplify them at decode time (Maj@100 ~40%). A **latent-aware reranker or decoding strategy** could recover the latent diversity advantage. Amazon's experience with retrieval and ranking systems makes this a natural follow-up.
2. **Solving the supervision–exploration trade-off**: A training scheme that enforces shortcut resistance without collapsing latent diversity. Candidate approaches: information-bottleneck objectives, contrastive losses on latent diversity, or hybrid curricula combining strong and weak supervision phases.

Amazon's findings also directly inform the [[frontier-research-directions|frontier directions analysis]]: directions #1 (superposition reasoning at frontier scale) and #2 (disentangling superposed paths) need to factor in the supervision–exploration trade-off as a hard constraint, not just a technical detail.

## Research Trajectory

Amazon is a new entity in this collection with a single high-impact analytical paper. The natural next steps:

1. **Scale the analysis to 7B+ models**: Cui et al. tests only GPT-2 and LLaMA-3.2-1B. Whether the supervision–exploration trade-off persists at larger scales is the most pressing question.
2. **Test the [[softcot-efficient-reasoning|SoftCoT]] / [[latentmas-collaboration|LatentMAS]] family**: Cui et al. focuses on single-model latent reasoning. The frozen-backbone and training-free approaches might escape the trade-off by avoiding the supervision dilemma entirely.
3. **Build a latent-aware decoder**: The Pass@100 / Maj@100 gap is an exploitation problem, not a representation problem. Amazon's strength in production decoding systems makes this a natural application.
4. **Extend the diagnostics to inter-agent latent communication**: The shortcut behavior framework could be applied to [[activation-communication|activation communication]] and [[kv-cache-communication|KV-cache communication]] methods to test whether they also bypass their own communication channels.

## Key Researchers

![[amazon/researchers]]

## Why This Entity Matters

Amazon's diagnostic posture is rare in this collection — most papers propose methods, not critiques. Cui et al. is **the first paper** in the wiki that systematically asks "do these methods actually do what they claim?" rather than "can we improve their accuracy?" This kind of analytical work is essential for distinguishing fundamental insights from optimization tricks, and the field needs more of it.

The lack of follow-up work from Amazon on this topic (as of April 2026) is itself notable: the obvious next steps (scaling, mitigation) are open for any group to take.
