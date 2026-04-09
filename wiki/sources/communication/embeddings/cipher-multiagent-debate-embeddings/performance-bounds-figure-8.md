Upper and lower bounds of 2-agent CIPHER debate on GSM8K:

**LLaMA2-7B:** Random debater → 11.3%, Misalignment debater → 15.0%, Single Answer → 17.5%, CIPHER → (not reported separately), Expert debater → (higher). Debate can be **detrimental** for low-capacity models when paired with bad debaters.

**LLaMA2-70B:** Random debater → 52.3%, Misalignment debater → 59.2%, Single Answer → 61.5%, CIPHER → 63.3% (with normal debater), Expert debater → 68.0% (upper bound when one debater always gives ground truth), and Expert upper bound reaches 87.8%. A more powerful model is robust against bad debaters — even random/misaligned feedback causes only modest degradation.
