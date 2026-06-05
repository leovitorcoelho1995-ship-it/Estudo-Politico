from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "bcb_sgs_indicators.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "bcb_sgs_summary.csv"


def build_summary(input_path: Path = INPUT_PATH, output_path: Path = OUTPUT_PATH) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    summary = (
        df.groupby(["series_slug", "series_code", "series_name"], as_index=False)
        .agg(
            rows=("value", "size"),
            start_date=("date", "min"),
            end_date=("date", "max"),
            missing_values=("value", lambda values: values.isna().sum()),
            min_value=("value", "min"),
            max_value=("value", "max"),
            latest_value=("value", "last"),
        )
        .sort_values("series_slug")
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_path, index=False, date_format="%Y-%m-%d")
    return summary


if __name__ == "__main__":
    result = build_summary()
    print(result.to_string(index=False))
    print(f"\nResumo salvo em: {OUTPUT_PATH}")
