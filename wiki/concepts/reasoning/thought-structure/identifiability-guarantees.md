[[thought-communication-multiagent|ThoughtComm]] provides theoretical guarantees ([[raw/pdf/arxiv-2510.20733.pdf|ThoughtComm Theorems 1-3]]) that under minimal assumptions (invertible generating function, sparsity regularization):

1. Shared thoughts can be **disentangled** from private and irrelevant thoughts
2. Private thoughts can be **disentangled** from all other thoughts
3. The full incidence structure $B(J_f)$ can be **recovered** up to relabeling

These guarantees are **pairwise** — they hold for any pair of agents — and global structure is reconstructed by composing pairwise results. The key assumption is sparsity: each thought must have sparse influence on agent states (not every thought affects every dimension).
