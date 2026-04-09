This paper completes the [[kv-cache-communication]] picture by introducing the **scalable shared space** approach — a fundamentally different architecture from pairwise methods. The interlingua analogy is powerful: just as a universal interlingua would eliminate the need for O(N²) translation pairs between N languages, a shared KV-cache space eliminates the need for O(N²) cross-model adapters.

The module portability finding opens a new direction not explored by other papers in this collection: **skill transfer** between models via latent space, going beyond just communication to knowledge sharing.

The self-improvement effect (cyclic translation improves the original model) connects to [[cache-to-cache-semantic-communication|C2C]]'s effective rank increase and [[kvcomm-kth-selective|KVComm]]'s finding that selective sharing can exceed the skyline — all suggesting that latent-space mediation acts as a form of beneficial regularization.
