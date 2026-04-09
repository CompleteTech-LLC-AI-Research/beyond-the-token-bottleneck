The protocol is simple:

1. **Sender ($M_s$)** processes context $C$, runs one forward pass (prefill), generates KV pairs at all layers
2. **Selection**: Top $M$ layers chosen by the selection strategy
3. **Transmission**: Selected KV pairs $\{(k^s_{l_i}, v^s_{l_i})\}$ sent to receiver
4. **Receiver ($M_r$)** processes query $Q$. At each selected layer $l_i$, sender's KV pairs are concatenated with receiver's own: $k^r_l \leftarrow [k^s_{l_i}; k^r_l]$, $v^r_l \leftarrow [v^s_{l_i}; v^r_l]$
5. **Generation**: Receiver generates output attending to both its own and sender's cached context

No learned projections, no training. Pure concatenation + attention.
