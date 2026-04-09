Given models A (sender with context/knowledge) and B (receiver generating the answer):

1. Run B's forward pass **up to layer $j$**, yielding post-layer activation $h_{B,j} \in \R^{t_B \times d_B}$
2. Run A's **partial** forward pass up to layer $k$, yielding $h_{A,k} \in \R^{t_A \times d_A}$
3. **Replace B's last-token activation only**: $(h_{B,j})_{t_B} \leftarrow f((h_{A,k})_{t_A}, (h_{B,j})_{t_B})$
4. Continue B's forward pass from layer j+1 through to decoding completion

### Combination Functions

Three non-learned options (assuming $d_A = d_B$):

| Function | Formula | Performance | Why |
|----------|---------|-------------|-----|
| **Replace** | $f(a,b) = a$ | **Best** | Output stays in B's activation space; B retains all context in other token positions |
| Mean | $f(a,b) = (a+b)/2$ | Moderate | Dilutes both signals |
| Sum | $f(a,b) = a+b$ | Worst | Roughly doubles activation norm, pushing out of distribution |

For cross-family models ($d_A \neq d_B$), a **task-agnostic linear mapping** $W \in \R^{d_B \times d_A}$ projects A's activations into B's space. $W$ is trained once per model pair on 3072 C4 sentences (MSE loss, 10 epochs, Adam lr=0.001). This introduces **zero task-specific parameters** — the same W is used across all benchmarks.

### Why Layer 26 (of 32)?

The paper provides a 2D contour plot scanning all $(k,j)$ pairs $\in \{1,\ldots,30\}^2$. The optimum at $k = j = 26$ corresponds to the "**enriched entity representation**" layers identified by Hernandez et al. (2024):

- **Early layers (1-12)**: Embeddings are still being contextualized. Not yet informative enough for communication.
- **Mid-late layers (~20-26)**: "Enriched entity representations" — entities in the prompt have been populated with additional facts about them from the model's weights. This is the **richest** representation of the input.
- **Final layers (27-32)**: Representations are optimized for next-token prediction — information not needed for that narrow objective is discarded. Richer contextual knowledge is "thrown away."

This layer-depth finding aligns with [[kvcomm-kth-selective|KVComm]]'s hypothesis H1 (intermediate layers encode the most transferable semantic knowledge), despite the two papers approaching the problem from different angles.
