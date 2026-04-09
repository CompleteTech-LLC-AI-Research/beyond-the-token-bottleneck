| Dataset | Metric | Baseline (StdPT+StdFT) | PausePT+PauseFT | Δ |
|---------|--------|------------------------|-----------------|---|
| SQuAD | EM | 36.4 ±2.5 | **55.9 ±1.0** | **+19.5** |
| CommonSenseQA | EM | 26.9 ±2.9 | **34.8 ±1.2** | **+7.9** |
| NaturalQA | EM | 23.6 ±1.2 | **26.9 ±0.4** | **+3.3** |
| LAMBADA | EM | 16.4 ±1.7 | **18.8 ±0.1** | **+2.4** |
| WebQA | EM | 13.7 ±2.1 | **16.0 ±1.6** | **+2.3** |
| GSM8k | Acc | 7.5 ±0.5 | **8.5 ±0.9** | **+1.0** |
| PhysicalIQA | F1 | 73.3 ±0.2 | **74.2 ±0.2** | **+0.9** |
| CoQA | F1 | 29.9 ±1.0 | **31.6 ±0.5** | **+1.7** |
| HellaSwag | F1 | 37.8 ±0.1 | 37.8 ±0.2 | ~0 |

**8 of 9 tasks improve.** SQuAD shows the largest gain (+19.5); HellaSwag is the sole exception. The 130M model shows gains on 6/9 tasks, but the SQuAD improvement disappears at smaller scale — **larger models benefit more**, counter-intuitively suggesting the model needs sufficient raw capacity to exploit the extra computation pathways.
