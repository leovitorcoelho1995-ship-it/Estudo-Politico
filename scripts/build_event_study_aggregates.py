from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

EVENT_STUDY_PATH = PROCESSED_DIR / "event_study_series.csv"
OUTPUT_PATH = PROCESSED_DIR / "event_study_category_aggregates.csv"
SUMMARY_PATH = PROCESSED_DIR / "event_study_category_aggregates_summary.csv"


def build_event_study_aggregates() -> pd.DataFrame:
    study = pd.read_csv(EVENT_STUDY_PATH)
    study["z_score"] = pd.to_numeric(study["z_score"], errors="coerce")
    study["relative_day"] = pd.to_numeric(study["relative_day"], errors="coerce")
    study = study.dropna(subset=["z_score", "relative_day"]).copy()
    study["relative_day"] = study["relative_day"].astype(int)

    aggregates = (
        study.groupby(["country_code", "country_name", "event_category", "relative_day"], as_index=False)
        .agg(
            mean_z_score=("z_score", "mean"),
            median_z_score=("z_score", "median"),
            p25_z_score=("z_score", lambda values: values.quantile(0.25)),
            p75_z_score=("z_score", lambda values: values.quantile(0.75)),
            observations=("z_score", "size"),
            events=("event_id", "nunique"),
            indicators=("indicator_slug", "nunique"),
        )
        .sort_values(["country_code", "event_category", "relative_day"])
    )
    aggregates.to_csv(OUTPUT_PATH, index=False)

    summary = (
        aggregates.groupby(["country_code", "event_category"], as_index=False)
        .agg(
            days=("relative_day", "size"),
            min_events=("events", "min"),
            median_events=("events", "median"),
            max_events=("events", "max"),
            median_observations=("observations", "median"),
            peak_abs_mean_z=("mean_z_score", lambda values: values.abs().max()),
        )
        .sort_values(["country_code", "event_category"])
    )
    summary.to_csv(SUMMARY_PATH, index=False)
    return aggregates


if __name__ == "__main__":
    result = build_event_study_aggregates()
    print(f"Linhas agregadas de event study: {len(result)}")
    print(result.groupby(["country_code", "event_category"])["events"].max().to_string())
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
    print(f"Resumo salvo em: {SUMMARY_PATH}")
