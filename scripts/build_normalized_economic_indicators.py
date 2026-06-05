from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

INPUT_PATH = PROCESSED_DIR / "economic_indicators_unified.csv"
OUTPUT_PATH = PROCESSED_DIR / "economic_indicators_normalized.csv"
SUMMARY_PATH = PROCESSED_DIR / "economic_indicators_normalized_summary.csv"


GROUP_COLUMNS = ["country_code", "indicator_slug", "source"]


def add_normalized_columns(group: pd.DataFrame) -> pd.DataFrame:
    group = group.sort_values("date").copy()
    first_value = group["value"].dropna().iloc[0]
    mean_value = group["value"].mean()
    std_value = group["value"].std(ddof=0)

    group["index_base_100"] = (group["value"] / first_value) * 100 if first_value > 0 else pd.NA
    previous_value = group["value"].shift(1)
    group["pct_change_from_previous"] = (
        (group["value"] - previous_value) / previous_value.abs()
    ) * 100
    group.loc[previous_value.abs() < 1e-9, "pct_change_from_previous"] = pd.NA
    group["absolute_change_from_previous"] = group["value"].diff()
    group["series_mean"] = mean_value
    group["series_std"] = std_value
    group["z_score"] = (group["value"] - mean_value) / std_value if std_value != 0 else pd.NA

    return group


def build_normalized() -> pd.DataFrame:
    df = pd.read_csv(INPUT_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"]).copy()

    normalized = pd.concat(
        [add_normalized_columns(group) for _, group in df.groupby(GROUP_COLUMNS)],
        ignore_index=True,
    )

    normalized = normalized.sort_values(["country_code", "indicator_slug", "source", "date"])
    normalized.to_csv(OUTPUT_PATH, index=False, date_format="%Y-%m-%d")

    summary = (
        normalized.groupby(["country_code", "indicator_slug", "source"], as_index=False)
        .agg(
            rows=("value", "size"),
            start_date=("date", "min"),
            end_date=("date", "max"),
            mean_value=("value", "mean"),
            std_value=("value", "std"),
            min_z_score=("z_score", "min"),
            max_z_score=("z_score", "max"),
        )
        .sort_values(["country_code", "indicator_slug", "source"])
    )
    summary.to_csv(SUMMARY_PATH, index=False, date_format="%Y-%m-%d")

    return normalized


if __name__ == "__main__":
    result = build_normalized()
    print(f"Linhas normalizadas: {len(result)}")
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
    print(f"Resumo salvo em: {SUMMARY_PATH}")
