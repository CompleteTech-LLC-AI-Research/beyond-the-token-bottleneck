Ground-truth thinking sequences are synthesized by aligning existing CoT annotations with input chunks. For each task:

- **State tracking (Parity, Vars)**: Reasoning annotations correspond naturally to state updates at each operation
- **GSM8K**: CoT steps are parsed and mapped to the input chunks where the relevant quantities first appear (~400K problems)
- **2-Hop QA**: Intermediate reasoning steps are mapped to chunks containing the relevant facts

The process uses existing CoT data without requiring new annotation -- the key innovation is the **chunk-to-thought mapping** that determines which reasoning should occur at which input position.
