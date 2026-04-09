47 relations across 4 categories (26 factual, 8 commonsense, 6 linguistic, 7 bias), covering 10,000+ facts.

### Linear Relations (>60% faithfulness) — 48% of tested relations

| Relation | Faithfulness |
|----------|-------------|
| Occupation-gender | 0.98 |
| Adjective comparative | 0.98 |
| Adjective superlative | 0.93 |
| Country largest city | 0.92 |
| Name birthplace | 0.92 |
| Country capital city | 0.88 |
| Country language | 0.88 |
| Substance phase of matter | 0.87 |
| Object superclass | 0.85 |
| Name religion | 0.80 |
| Name gender | 0.80 |

### Non-Linear Relations (<30% faithfulness) — 52% of tested relations

| Relation | Faithfulness | Range size |
|----------|-------------|------------|
| Company CEO | 0.06 | 287 entities |
| Person father | 0.07 | 968 entities |
| Person mother | 0.14 | 962 entities |
| Pokemon evolution | 0.15 | — |
| Company HQ | 0.21 | — |

Pattern: Relations with **large, person/company-name ranges** resist linear approximation. Relations with small, categorical ranges (adjective forms, countries, genders) are highly linear.

**Cross-model consistency**: GPT-J relation-wise performance correlates with GPT2-XL (Spearman $R = 0.85$) and LLaMA-13B ($R = 0.71$). The same relations are linear/nonlinear across architectures.
