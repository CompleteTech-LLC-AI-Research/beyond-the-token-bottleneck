### State Trajectory

Consider two agents, Alice and Bob, built from the same transformer LLM. When Alice generates output tokens $t_1, t_2, \ldots, t_n$, the **state trajectory** at layer $l$ is the ordered sequence of hidden states:

> $$H^l_A = \{ h^l_{A,0}, h^l_{A,1}, \ldots, h^l_{A,n} \}$$

Here $h^l_{A,i}$ is the output of the $l$-th transformer layer for token $t_i$, conditioned on the input prompt and all previously generated tokens. $h^l_{A,0}$ corresponds to the **last token of Alice's input prompt** (the initial state before generation begins).

### State Delta Encoding

Rather than transferring the raw trajectory $H^l_A$ (which contains Alice's context-specific information -- system prompt, private documents), SDE computes the **inter-token differences**:

> $$S^l_A = \{ s^l_1, s^l_2, \ldots, s^l_n \}, \quad \text{where } s^l_i = h^l_{A,i} - h^l_{A,i-1}$$

Each $s^l_i$ is a **state delta**: the internal change associated with generating token $t_i$. The state delta trajectory is a **context-agnostic trace** of reasoning dynamics -- it strips out Alice's absolute context and retains only the differential reasoning signal.

### Injection into the Receiver

Bob's prompt takes the form $\text{prompt}_B = \{X, t_1, t_2, \ldots, t_n, Y\}$ where $X$ and $Y$ are task instructions, environment info, and other agents' responses. When Bob processes Alice's tokens, SDE injects the corresponding deltas at layer $l$:

> $$h'^l_{B,j} = \begin{cases} h^l_{B,j} + s^l_i & \text{if position } j \text{ corresponds to token } t_i \text{ from Alice's output} \\ h^l_{B,j} & \text{otherwise} \end{cases}$$

The modified $h'^l_{B,j}$ is passed to layer $l+1$ for continued inference. This is an **additive** injection -- Bob's own representations are nudged, not overwritten. The injection only occurs at positions corresponding to Alice's output tokens within Bob's prompt.
