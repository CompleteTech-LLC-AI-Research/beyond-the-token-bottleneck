At each generation step $t$, instead of sampling a token, CIPHER computes:

> $$\text{emb}(t) = \sum_i p(\text{vocab}_i) \cdot \text{emb}(\text{vocab}_i)$$

This weighted average stays within the convex hull of the tokenizer's embedding space, so the receiving model can process it as input.

**Stopping criterion:** Generation terminates when the nearest-neighbor embedding (over the vocabulary set) to the newly generated embedding is the EOS token, or when the maximum sequence length is reached. This replaces the standard "sampled token = EOS" check with a geometric proximity test in embedding space.

**Debate protocol (Algorithm 1):**

```mermaid
graph LR
    subgraph Init["Initialization"]
        style Init fill:#dae8fc,stroke:#6c8ebf
        Q["Question +<br>instructions"] --> EMB["Convert to<br>embeddings"]
    end
    subgraph R1["Round 1"]
        style R1 fill:#fff2cc,stroke:#d6b656
        EMB --> D1A["Debater A<br>generates CIPHER<br>response"]
        EMB --> D1B["Debater B<br>generates CIPHER<br>response"]
    end
    subgraph RN["Rounds 2...N"]
        style RN fill:#ffe6cc,stroke:#d79b00
        D1A --> CAT["Concatenate prompt +<br>all CIPHER responses"]
        D1B --> CAT
        CAT --> DNA["Debater A<br>refined CIPHER"]
        CAT --> DNB["Debater B<br>refined CIPHER"]
        DNA -.->|"next round"| CAT
        DNB -.->|"next round"| CAT
    end
    subgraph Out["Post-processing"]
        style Out fill:#d5e8d4,stroke:#82b366
        DNA --> NN["Nearest-neighbor<br>decode to NL"]
        DNB --> NN
        NN --> SEL["Select lowest-temp<br>debater's answer"]
    end
```

1. Convert question + instructions into embeddings via the tokenizer.
2. Each debater independently generates an initial CIPHER response (embedding sequence).
3. For each subsequent debate round, concatenate prompt embeddings with all debaters' CIPHER responses, then each debater generates a refined CIPHER response.
4. Post-processing: convert final embedding responses back to natural language via nearest-neighbor search, then aggregate. The response from the lowest-temperature debater is selected as the final answer.
