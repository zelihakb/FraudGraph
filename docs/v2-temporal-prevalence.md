# V2 Temporal Fraud Prevalence

Analysis of 24-time-step windows.

| Split | Transactions | Fraud | Fraud rate |
|---|---:|---:|---:|
| train | 1,938,484 | 3,633 | 0.1874% |
| validation | 415,628 | 560 | 0.1347% |

## Methodology

- Chronological split boundaries remained unchanged.
- Fraud labels were used for descriptive analysis only.
- The test split was not scanned in this analysis.
- Model selection must use validation data only.

## Window-level results

| split      |   window |   transactions |   fraud |   fraud_rate_pct |
|:-----------|---------:|---------------:|--------:|-----------------:|
| train      |        1 |         251083 |     271 |        0.107932  |
| train      |        2 |         202874 |     309 |        0.152311  |
| train      |        3 |            429 |     310 |       72.2611    |
| train      |        4 |           8766 |     262 |        2.98882   |
| train      |        5 |           2675 |     252 |        9.42056   |
| train      |        6 |         195910 |     228 |        0.11638   |
| train      |        7 |         186059 |     272 |        0.14619   |
| train      |        8 |         197042 |     278 |        0.141087  |
| train      |        9 |         181649 |     255 |        0.140381  |
| train      |       10 |         171830 |     282 |        0.164116  |
| train      |       11 |         182109 |     262 |        0.14387   |
| train      |       12 |         149340 |     298 |        0.199545  |
| train      |       13 |         188657 |     242 |        0.128275  |
| train      |       14 |          20061 |     112 |        0.558297  |
| validation |       14 |         152463 |     134 |        0.0878902 |
| validation |       15 |         173951 |     250 |        0.143719  |
| validation |       16 |          89214 |     176 |        0.197278  |

## Source-data verification

Unusual fraud prevalence was observed in several early time windows.

We independently compared selected time steps against the original
PaySim CSV, filtering to CASH_OUT and TRANSFER transactions.

Verified steps: 50, 60, 70, 93, 98, 118, 119.

Transaction and fraud counts matched the prepared model dataset
for all seven selected steps.

This confirms the observed anomaly exists in the source data
for the checked steps. It does not independently establish
that the entire processing pipeline is free of leakage.

The chronological split boundaries remain unchanged.
