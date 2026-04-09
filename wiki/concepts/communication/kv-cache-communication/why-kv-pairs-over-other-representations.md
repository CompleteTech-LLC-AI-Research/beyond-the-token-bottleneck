[[kvcomm-kth-selective|KVComm]] provides the strongest empirical case for KV pairs as the optimal communication medium, by systematically comparing alternatives:

### vs. Natural Language (Tokens)

The standard [[multi-agent-debate]] approach. Natural language requires the sender to sequentially generate tokens (slow, lossy) and the receiver to parse them (ambiguous). KV-cache communication eliminates both steps — the sender only needs a single prefill pass, and the receiver integrates information through attention.

### vs. Output Embeddings ([[cipher-multiagent-debate-embeddings|CIPHER]])

[[cipher-multiagent-debate-embeddings|CIPHER]] shares weighted averages of output embeddings. This preserves output-level uncertainty but still requires sequential generation of embedding vectors. KV-cache communication provides **layer-specific representations** (not just the output layer) in a single forward pass.

### vs. Hidden States (Activations)

[[kvcomm-kth-selective|KVComm]]'s key finding: hidden states suffer from **information concentration bias** — the last token's hidden state dominates in later layers, making it the most critical for output but also the hardest to share without corrupting the receiver's own processing:
- **Replace** the receiver's last-token hidden state → destroys receiver's own context
- **Average** sender and receiver hidden states → dilutes both
- **Prepend** all tokens' hidden states → only works from early layers (minimal compute savings)

KV pairs avoid this dilemma because they integrate through **attention**, not by replacing hidden states. The receiver decides via attention weights how much to attend to the sender's information at each position — non-destructive by design.

### vs. Disentangled Thoughts ([[thought-communication-multiagent|ThoughtComm]])

[[thought-communication-multiagent|ThoughtComm]] adds **structure** (shared/private decomposition) but requires a trained autoencoder. KV-cache methods ([[kvcomm-kth-selective|KVComm]], KVCOMM-online) are training-free. [[cache-to-cache-semantic-communication|C2C]] requires training but provides cross-architecture compatibility that ThoughtComm doesn't address.
