Debates between LLaMA2-70B and LLaMA-65B (different models sharing a tokenizer but with distinct embedding matrices). Agreement = percentage of cases where both debaters produce the same final answer.

### Arithmetic

| | Round 1 | Round 2 | Round 3 |
|---|---|---|---|
| **NLD — LLaMA2-70B** | 73.0 | 69.0 | 72.0 |
| **NLD — LLaMA-65B** | 32.5 | 56.0 | 60.5 |
| **NLD — Agreement** | 31.5 | 61.5 | 77.5 |
| **CIPHER — LLaMA2-70B** | 73.5 | 70.0 | 74.5 |
| **CIPHER — LLaMA-65B** | 35.0 | 61.5 | 62.5 |
| **CIPHER — Agreement** | 34.5 | 69.0 | 78.0 |

### GSM8K

| | Round 1 | Round 2 | Round 3 |
|---|---|---|---|
| **NLD — LLaMA2-70B** | 61.0 | 58.8 | 61.8 |
| **NLD — LLaMA-65B** | 51.3 | 57.5 | 59.0 |
| **NLD — Agreement** | 51.5 | 77.5 | 88.8 |
| **CIPHER — LLaMA2-70B** | 61.5 | 64.3 | 64.8 |
| **CIPHER — LLaMA-65B** | 48.0 | 60.3 | 63.3 |
| **CIPHER — Agreement** | 44.0 | 70.3 | 83.8 |

Key observations: LLaMA-65B gains most dramatically — from 35.0% to 62.5% on Arithmetic via CIPHER. Cross-model CIPHER uses the receiver's embedding matrix for weighted averaging, ensuring outputs remain in the receiver's embedding space. CIPHER achieves higher per-debater accuracy than NLD despite slightly lower agreement rates in some rounds, suggesting CIPHER preserves individual model quality better.
