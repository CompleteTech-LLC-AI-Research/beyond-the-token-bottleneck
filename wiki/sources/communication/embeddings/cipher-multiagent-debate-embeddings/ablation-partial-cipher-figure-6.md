Tested on LLaMA2-70B pairs on the Arithmetic dataset. CIPHER is invoked only at token positions where the model exhibits high uncertainty, with greedy sampling used elsewhere.

**Two uncertainty measures:**
- **Max probability:** $U(t) = 1 - \max_i p(i)$ — high when the model is not confident in any single token
- **Entropy:** $U(t) = -\sum_i p(i) \log p(i)$ — high when probability is spread across many tokens

**Two reversed variants** invoke CIPHER when uncertainty is *low* ($U(t) \leq$ threshold):
- **Max reversed** and **Entropy reversed**

**Results across three temperature pairs:**

At temperature pair (0.15, 1.75):
- **Full CIPHER:** ~85%
- **Max (partial):** closely matches full CIPHER (~84-85%)
- **Entropy (partial):** closely matches full CIPHER (~84-85%)
- **Max reversed:** dramatic drop to ~50-55%
- **Entropy reversed:** dramatic drop to ~50-55%

At temperature pair (0.20, 0.90):
- **Full CIPHER:** ~82%
- **Max/Entropy (partial):** closely track full CIPHER
- **Max reversed/Entropy reversed:** drop to ~65-70%

At temperature pair (0.25, 0.60):
- **Full CIPHER:** ~80%
- **Max/Entropy (partial):** closely track full CIPHER
- **Max reversed/Entropy reversed:** drop to ~70-72%

The pattern is consistent: applying CIPHER at high-uncertainty positions captures nearly all the benefit, while applying it only at low-uncertainty positions (reversed) causes dramatic performance degradation. This confirms that CIPHER's advantage comes specifically from **preserving information during uncertain generation steps** — exactly the moments when token sampling loses the most information.
