# V2 Graph Feature Definitions

Each transaction receives five features describing the receiver's prior incoming transactions.

- receiver_prior_tx_count
- receiver_prior_total_amount
- receiver_prior_avg_amount
- receiver_prior_7d_tx_count
- receiver_prior_7d_total_amount

Temporal rules:

- Historical transactions must satisfy past.time_step < current.time_step.
- The seven-day window uses past.time_step >= current.time_step - 168.
- Transactions from the same time step are excluded.
- Fraud labels and balance fields are not used to construct these features.

These rules help prevent future-information leakage.
