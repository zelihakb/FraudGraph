# V2 Model Reproduction Commands

The following commands reproduce the V2 model experiments.

## Unit Tests
python -m unittest discover -s tests -p "test_*.py" -v

## Dataset Preparation
python -m scripts.build_v2_splits

## Logistic Regression
python -m scripts.train_v2_logreg

## Random Forest
python -m scripts.train_v2_rf

## Graph-Only Ablation
python -m scripts.train_v2_graph_only

All model selection and threshold tuning must use validation data.
The test split is reserved for final evaluation.
