The following table maps each major entity in the collection to its primary positioning axis, flagship contribution, and unique role in the field.

| Entity | Positioning Axis | Flagship Paper | Unique Contribution |
| --- | --- | --- | --- |
| [[fair-meta\|FAIR at Meta]] | Constructive (foundational method) | [[coconut-reasoning-latent-space\|Coconut]] | Defined latent reasoning as a field; controls LLaMA ecosystem used by most other groups |
| [[amazon\|Amazon]] | Diagnostic (breadth-first analysis) | [[latent-reasoning-supervision-analysis\|Cui et al.]] | First unified empirical critique of four latent reasoning methods; weak/strong supervision taxonomy |
| [[google-deepmind\|Google DeepMind]] | Systems (scalable architecture) | [[kv-cache-alignment-shared-space\|KV Cache Alignment]] | O(N) interlingua for cross-model communication; self-improvement effect discovery |
| [[google-research\|Google Research]] | Production (deployment-oriented) | [[thinking-states-latent-reasoning\|Thinking States]] | Most deployment-ready latent reasoning method; state ambiguity finding (15% causal loss) |
| [[harvard\|Harvard]] | Constructive (method + empirical validation) | [[activation-communication-harvard\|AC]] | Strongest empirical evidence for cross-model representation convergence (zero-shot cross-family) |
| [[monash\|Monash]] | Diagnostic (narrow instrumentation) | [[inference-time-scaling-continuous-reasoning\|Wang et al.]] | First geometric measurement framework for continuous thoughts; null result on latent reranking |
| [[princeton-uiuc-stanford\|Princeton/UIUC/Stanford]] | Constructive (unified frameworks) | [[latentmas-collaboration\|LatentMAS]] | First system unifying latent reasoning + latent communication; training-free, 95.2% GSM8K |
| [[cmu\|CMU]] | Theoretical (identifiability) | [[thought-communication-multiagent\|ThoughtComm]] | Only formal guarantees that recovered latent factors correspond to true generative factors |
| [[tsinghua\|Tsinghua]] | Systems (cross-architecture fusion) | [[cache-to-cache-semantic-communication\|C2C]] | Solved cross-architecture KV-cache communication; effective rank analysis |
| [[kth\|KTH]] | Systems (efficiency) | [[kvcomm-kth-selective\|KVComm]] | First systematic comparison showing KV > embeddings > text; selective sharing Skyline paradox |
| [[purdue\|Purdue]] | Constructive (architectural insight) | [[vision-wormhole-heterogeneous\|Vision Wormhole]] | Repurposed VLM visual pathways as universal cross-architecture communication channel |
| [[mbzuai\|MBZUAI]] | Theoretical (causal representation) | [[thought-communication-multiagent\|ThoughtComm]] (with CMU/FAIR) | Causal representation learning expertise applied to structured latent communication |
| [[mit\|MIT]] | Foundational (paradigm creation) | [[multiagent-debate-du-et-al\|Multiagent Debate]] | Origin point for the entire multi-agent debate paradigm; Platonic Representation Hypothesis |

The table reveals a clear division of labor. Industry labs ([[fair-meta|FAIR]], [[amazon|Amazon]], [[google-deepmind|Google DeepMind]], [[google-research|Google Research]]) span the full range from foundational method creation to deployment engineering, while academic groups specialize more narrowly — diagnostics ([[monash|Monash]]), theory ([[cmu|CMU]], [[mbzuai|MBZUAI]]), or unified constructive systems ([[princeton-uiuc-stanford|Princeton/UIUC/Stanford]]).
