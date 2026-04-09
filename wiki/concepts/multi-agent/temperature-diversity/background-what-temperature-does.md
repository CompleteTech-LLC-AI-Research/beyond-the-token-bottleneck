![[temperature-scaling-behavior]]

Mechanistically, temperature $T$ controls the **sharpness** of the softmax distribution over the vocabulary:

$$p(v_i | T) = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$$

where $z_i$ are the logits (pre-softmax scores).

The critical insight for this concept is that temperature has **opposite effects** depending on the communication medium:

| Temperature | Natural Language (sampling) | Embedding Communication (averaging) |
|-------------|---------------------------|-------------------------------------|
| Low ($T < 0.5$) | Deterministic, confident | Peaked embeddings $\approx$ discrete tokens |
| Medium ($T \approx 1.0$) | Fluent, standard | Moderately blended embeddings |
| High ($T > 1.5$) | Incoherent, nonsensical | Information-rich soft tokens |

This asymmetry is the foundation of why temperature diversity behaves differently in [[cipher-multiagent-debate-embeddings|CIPHER]] versus natural language debate (NLD).
