# V2 Final Holdout Evaluation

Frozen champion: **rf_tabular**

Test transactions: 416,297
Test fraud: 4,020

| Model | AP | ROC-AUC | Precision | Recall | F1 | TP | FP |
|---|---:|---:|---:|---:|---:|---:|---:|
| lr_tabular | 0.059106 | 0.748491 | 0.265943 | 0.048756 | 0.082405 | 196 | 541 |
| lr_graph | 0.157694 | 0.830146 | 0.627907 | 0.053731 | 0.098992 | 216 | 128 |
| rf_tabular | 0.257431 | 0.776231 | 0.965517 | 0.174129 | 0.295047 | 700 | 25 |
| rf_graph | 0.239632 | 0.877991 | 0.400816 | 0.195522 | 0.262832 | 786 | 1175 |
| rf_graph_only | 0.027465 | 0.729161 | 0.033651 | 0.674129 | 0.064103 | 2710 | 77822 |

## Evaluation protocol

- Champion selected using validation AP.
- Thresholds selected using validation F1.
- Models were not retrained on test data.
- No threshold was optimized on the test split.
- All other models are fixed secondary comparisons.
- Test results did not change the frozen champion.
- Class-weighted RF scores are not assumed calibrated.
- Selection criteria were formalized after viewing validation results.
