# V2 Temporal Splits

The PaySim V2 dataset contains 2,770,409 transactions.

| Split | Time steps | Transactions | Fraud |
|---|---|---:|---:|
| Train | 1-322 | 1,938,484 | 3,633 |
| Validation | 323-376 | 415,628 | 560 |
| Test | 377-743 | 416,297 | 4,020 |

Splits are chronological and were not adjusted using fraud labels.

The natural fraud prevalence is preserved.
The final test set remains reserved for final evaluation.
