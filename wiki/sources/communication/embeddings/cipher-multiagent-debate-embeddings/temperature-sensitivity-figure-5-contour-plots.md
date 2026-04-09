2D contour plots show accuracy over all pairs of (temperature 1, temperature 2) for 2 LLaMA2-70B debaters. Three datasets analyzed: Arithmetic, GSM8K, Professional Psychology.

**NLD (top row of Figure 5):**
- Optimal performance occurs with both temperatures below 1.0.
- Higher temperatures cause LLMs to produce nonsensical natural language, harming the stronger debater.
- On Arithmetic: NLD optimal region clusters around temperatures (0.5–1.0, 0.5–1.0), peak ~81%.
- On GSM8K: NLD optimal region around (0.1–0.4, 0.2–0.8), peak ~65%.
- On Psychology: NLD optimal region around (0.0–0.4, 0.4–0.8), peak ~75%.

**CIPHER (bottom row of Figure 5):**
- Optimal regions appear on the **left side** of charts — low temperature 1 paired with high temperature 2.
- Temperature 1 (the agent whose response is used as final answer) should be low; temperature 2 can go well above 1.0.
- On Arithmetic: CIPHER peaks at ~85% with temperatures around (0.15, 1.75). The high-temperature agent's uniform distribution complements the confident low-temperature agent.
- On GSM8K: CIPHER peaks at ~66% with temperatures around (0.2, 0.9).
- On Psychology: CIPHER peaks at ~75% with temperatures around (0.1, 0.2) — more compact optimal region.

**Specific optimal temperature pairs (from Table 3):**

| Dataset | NLD temps | CIPHER temps |
|---|---|---|
| GSM8K (LLaMA2-70B) | (0.10, 0.20) | (0.22, 0.60) |
| H.S. Math | (0.30, 0.49) | (0.10, 0.82) |
| Psychology | (0.01, 0.51) | (0.10, 0.20) |
| Formal Logic | (0.10, 0.20) | (0.10, 0.20) |
| Arithmetic | (0.54, 1.00) | (0.15, 1.75) |

The Arithmetic result is most striking: CIPHER's optimal second temperature (1.75) is far above 1.0, which would produce gibberish in natural language but creates information-rich embeddings in CIPHER.
