# V2 Model Selection Protocol

## Selection decision

Primary selection metric: validation Average Precision (AP).

Selected model: **rf_tabular**.
Validation AP: **0.158758**.
Frozen threshold: **0.959629183138**.

## Validation comparison

| Model | AP | F1 | Frozen threshold |
|---|---:|---:|---:|
| lr_tabular | 0.003293 | 0.012476 | 0.012590 |
| lr_graph | 0.012020 | 0.039672 | 0.051077 |
| rf_tabular | 0.158758 | 0.257016 | 0.959629 |
| rf_graph | 0.035169 | 0.097306 | 0.923898 |
| rf_graph_only | 0.003964 | 0.009573 | 0.773469 |

## Methodological notes

- The primary metric was formally documented after reviewing validation results; this was not a preregistered selection rule.
- Model selection used validation results, not test results.
- Decision thresholds were optimized for validation F1.
- The selected model and all comparator thresholds are frozen before final test evaluation.
- No model retraining or test-based threshold optimization is permitted during final evaluation.
- Other models may be reported as fixed secondary comparisons, not used to change the selected champion.
- RF probabilities with class weighting are not assumed to be calibrated fraud probabilities.
- Test prevalence differs substantially from train and validation and must be acknowledged when interpreting final results.

## Interpretation

RF Tabular leads in validation AP and F1.
RF Combined leads in validation ROC-AUC but has lower AP.
Graph-only RF has high recall at its selected threshold but generates many false positives.
Negative graph-ablation results will be reported without changing the frozen selection.
