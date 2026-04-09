### Append > Prepend

| Dataset | Baseline | Prepend (PausePT+PauseFT) | **Append (PausePT+PauseFT)** |
|---------|----------|--------------------------|------------------------------|
| SQuAD | 36.4 | 44.0 | **55.9** |
| CommonSenseQA | 26.9 | 34.5 | **34.8** |
| GSM8k | 7.5 | 8.0 | **8.5** |

Appending is consistently better, especially on SQuAD (+11.9 over prepend). Pause-pretraining induces positional biases about where delays are useful.

### $M_\text{ft}$ Sensitivity (Optimal Pause Count Is Task-Dependent)

- **GSM8k**: Peaks at $M_\text{ft}=10$ (8.5%), drops back to ~7.5% baseline at $M_\text{ft}=50$ — inverted-U pattern
- **SQuAD**: Peaks at $M_\text{ft}=50$ (55.9%); $M_\text{ft}=10$ gives only 40.2% — monotonically increasing
- No single $M_\text{ft}$ is universally optimal. This makes practical deployment harder.

### Graceful Degradation ($M_\text{inf} \neq M_\text{ft}$)

When $M_\text{ft}=10$ but $M_\text{inf}$ varies at inference time:
- $M_\text{inf}=5$ (half): performance stays above baseline — graceful degradation
- $M_\text{inf} \in [5, 25]$: reasonable performance maintained
- **$M_\text{inf}=0$**: **catastrophic failure** — performance drops "spectacularly." A model pretrained and finetuned with pauses **cannot function without them** at inference.
- As few as 2 pause tokens restores reasonable performance.
