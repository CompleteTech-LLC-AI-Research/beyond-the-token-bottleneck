### Two-Phase Training

**Pause-pretraining**: During causal language modeling on C4 (200B tokens, ~1 epoch), $M_\text{pt}$ pause tokens are inserted at **uniformly random positions** within each 2048-token training sequence. The next-token prediction loss is **skipped** at positions where the next token is `<pause>`. The model sees the same total token count but ~10% are dummy pauses, so it actually sees fewer meaningful tokens than the baseline — yet still wins.

**Pause-finetuning**: On downstream tasks, $M_\text{ft}$ pause tokens are **appended** to the input prefix (not randomly inserted). Model output is ignored until after the last pause. Standard next-token loss on the target answer only. $M_\text{ft}$ is fixed per task (tuned from $\{10, 50\}$).

**Critical finding: both phases required.** PausePT+PauseFT is the clear winner. Introducing pauses only at finetuning (StdPT+PauseFT) gives inconsistent, "lukewarm" gains. Filler tokens (periods `.`) at inference give **zero gains** — the model must be **trained** to exploit the extra compute.

### The Pause Token

A **new vocabulary item** outside the standard vocabulary — not a filler character like `.` or `#`. Only ~1024 new embedding parameters. All pause tokens share the same learned embedding.
