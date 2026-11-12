
import json
from pathlib import Path

import pandas as pd


DATA_DIR = Path(".local/v2_model_data")
REPORT_PATH = Path("docs/v2-temporal-prevalence.md")
CSV_PATH = DATA_DIR / "temporal_prevalence_train_val.csv"

COLUMNS = ["time_step", "label_fraud"]


def analyze_split(split, expected):
    paths = sorted((DATA_DIR / split).glob("part_*.csv"))

    if not paths:
        raise FileNotFoundError(f"Split dosyaları bulunamadı: {split}")

    parts = []
    total_rows = 0
    total_fraud = 0

    for path in paths:
        # Yalnızca analiz için gerekli iki sütunu okuduk.
        frame = pd.read_csv(path, usecols=COLUMNS)

        total_rows += len(frame)
        total_fraud += int(frame["label_fraud"].sum())

        # İşlemleri 24 zaman adımlık pencerelere ayırdık.
        frame["window"] = (frame["time_step"] - 1) // 24 + 1

        summary = frame.groupby("window").agg(
            transactions=("label_fraud", "size"),
            fraud=("label_fraud", "sum"),
        )

        parts.append(summary)

    # Dosyalardaki parçalı sonuçları birleştirdik.
    result = pd.concat(parts).groupby(level=0).sum()

    if total_rows != expected["rows"]:
        raise AssertionError(f"{split}: işlem sayısı uyuşmuyor.")

    if total_fraud != expected["fraud"]:
        raise AssertionError(f"{split}: fraud sayısı uyuşmuyor.")

    result = result.reset_index()
    result.insert(0, "split", split)

    result["fraud_rate_pct"] = (
        100 * result["fraud"] / result["transactions"]
    )

    return result


def main():
    manifest = json.loads(
        (DATA_DIR / "manifest.json").read_text(
            encoding="utf-8"
        )
    )

    results = []

    # Final test verisini bu analizde okumadık.
    for split in ("train", "validation"):
        result = analyze_split(
            split,
            manifest["counts"][split],
        )
        results.append(result)

    combined = pd.concat(results, ignore_index=True)

    # Ayrıntılı zaman penceresi verilerini yerelde sakladık.
    combined.to_csv(CSV_PATH, index=False)

    lines = [
        "# V2 Temporal Fraud Prevalence",
        "",
        "Analysis of 24-time-step windows.",
        "",
        "| Split | Transactions | Fraud | Fraud rate |",
        "|---|---:|---:|---:|",
    ]

    for split in ("train", "validation"):
        counts = manifest["counts"][split]
        rate = 100 * counts["fraud"] / counts["rows"]

        lines.append(
            f"| {split} | {counts['rows']:,} | "
            f"{counts['fraud']:,} | {rate:.4f}% |"
        )

    lines += [
        "",
        "## Methodology",
        "",
        "- Chronological split boundaries remained unchanged.",
        "- Fraud labels were used for descriptive analysis only.",
        "- The test split was not scanned in this analysis.",
        "- Model selection must use validation data only.",
        "",
        "## Window-level results",
        "",
        combined.to_markdown(index=False),
        "",
    ]

    REPORT_PATH.parent.mkdir(
        parents=True, exist_ok=True
    )

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("\nTEMPORAL PREVALENCE ANALYSIS COMPLETED!")
    print(combined.to_string(index=False))
    print(f"\nReport: {REPORT_PATH}")
    print("Test split was not accessed.")


if __name__ == "__main__":
    main()
