
import json
from pathlib import Path

import joblib
import numpy as np

from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
)

from scripts.train_v2_logreg import (
    load_split,
    TABULAR_INPUTS,
    GRAPH_INPUTS,
)
from src.graph.features import FEATURE_COLUMNS


LOCK_PATH = Path("docs/v2-evaluation-lock.json")
RESULT_PATH = Path(".local/v2_models/v2_final_test.json")
REPORT_PATH = Path("docs/v2-final-test.md")

EXPECTED_INPUTS = {
    "lr_tabular": TABULAR_INPUTS,
    "lr_graph": GRAPH_INPUTS,
    "rf_tabular": TABULAR_INPUTS,
    "rf_graph": GRAPH_INPUTS,
    "rf_graph_only": list(FEATURE_COLUMNS),
}


def evaluate_model(item, test, labels):
    name = item["name"]
    inputs = EXPECTED_INPUTS[name]
    threshold = float(item["threshold"])

    # Kaydedilmiş modeli yeniden eğitmeden yükledik.
    pipeline = joblib.load(item["artifact"])

    if list(pipeline.feature_names_in_) != inputs:
        raise ValueError(f"Model girdileri uyuşmuyor: {name}")

    probabilities = pipeline.predict_proba(
        test[inputs]
    )[:, 1]

    if not np.isfinite(probabilities).all():
        raise ValueError(f"Geçersiz tahminler: {name}")

    # Validation'da sabitlediğimiz eşiği değiştirmedik.
    predictions = (probabilities >= threshold).astype(int)

    tp = int(((predictions == 1) & (labels == 1)).sum())
    fp = int(((predictions == 1) & (labels == 0)).sum())
    fn = int(((predictions == 0) & (labels == 1)).sum())
    tn = int(((predictions == 0) & (labels == 0)).sum())

    return {
        "model": name,
        "threshold": threshold,
        "average_precision": float(
            average_precision_score(labels, probabilities)
        ),
        "roc_auc": float(
            roc_auc_score(labels, probabilities)
        ),
        "precision": float(
            precision_score(labels, predictions, zero_division=0)
        ),
        "recall": float(
            recall_score(labels, predictions, zero_division=0)
        ),
        "f1": float(
            f1_score(labels, predictions, zero_division=0)
        ),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
    }


def main():
    # Final test sonuçlarının üzerine yanlışlıkla yazılmasını önledik.
    if RESULT_PATH.exists() or REPORT_PATH.exists():
        raise FileExistsError(
            "Final test sonuçları zaten mevcut. "
            "Önce kayıtlı sonuçları inceleyin."
        )

    lock = json.loads(
        LOCK_PATH.read_text(encoding="utf-8")
    )

    if lock["champion"] != "rf_tabular":
        raise ValueError("Beklenmeyen champion modeli.")

    if (
        lock["test_threshold_tuning_allowed"]
        or lock["test_model_selection_allowed"]
    ):
        raise ValueError("Final değerlendirme kilidi geçersiz.")

    models = lock["models"]

    if (
        len(models) != 5
        or {item["name"] for item in models}
        != set(EXPECTED_INPUTS)
    ):
        raise ValueError("Model listesi uyuşmuyor.")

    for item in models:
        if not 0 <= float(item["threshold"]) <= 1:
            raise ValueError("Geçersiz threshold.")

        if not Path(item["artifact"]).is_file():
            raise FileNotFoundError(item["artifact"])

    print("Frozen model configuration verified.", flush=True)
    print("Loading final test split...", flush=True)

    test = load_split("test")
    labels = test["label_fraud"].to_numpy()

    results = []

    for item in models:
        result = evaluate_model(item, test, labels)
        results.append(result)

        print(
            f"{result['model']}: "
            f"AP={result['average_precision']:.6f}, "
            f"F1={result['f1']:.6f}",
            flush=True,
        )

    output = {
        "champion": lock["champion"],
        "selection_metric": lock["primary_metric"],
        "test_transactions": len(test),
        "test_fraud": int(labels.sum()),
        "results": results,
    }

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Sonuçları JSON olarak kaydettik.
    RESULT_PATH.write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# V2 Final Holdout Evaluation",
        "",
        f"Frozen champion: **{lock['champion']}**",
        "",
        f"Test transactions: {len(test):,}",
        f"Test fraud: {int(labels.sum()):,}",
        "",
        "| Model | AP | ROC-AUC | Precision | Recall | F1 | TP | FP |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for r in results:
        lines.append(
            f"| {r['model']} "
            f"| {r['average_precision']:.6f} "
            f"| {r['roc_auc']:.6f} "
            f"| {r['precision']:.6f} "
            f"| {r['recall']:.6f} "
            f"| {r['f1']:.6f} "
            f"| {r['tp']} | {r['fp']} |"
        )

    lines += [
        "",
        "## Evaluation protocol",
        "",
        "- Champion selected using validation AP.",
        "- Thresholds selected using validation F1.",
        "- Models were not retrained on test data.",
        "- No threshold was optimized on the test split.",
        "- All other models are fixed secondary comparisons.",
        "- Test results did not change the frozen champion.",
        "- Class-weighted RF scores are not assumed calibrated.",
        "- Selection criteria were formalized after viewing validation results.",
    ]

    REPORT_PATH.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("\nFINAL HOLDOUT EVALUATION COMPLETED!")
    print(f"Champion remains: {lock['champion']}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
