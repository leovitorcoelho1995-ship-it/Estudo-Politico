from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

IMPACT_PATH = PROCESSED_DIR / "event_economic_impact_normalized.csv"
INDICATORS_PATH = PROCESSED_DIR / "economic_indicators_normalized.csv"
OUTPUT_PATH = PROCESSED_DIR / "event_study_series.csv"
SUMMARY_PATH = PROCESSED_DIR / "event_study_series_summary.csv"

PRE_DAYS = 180
POST_DAYS = 365
SUPPORTED_FREQUENCIES = {"daily", "weekly", "monthly", "quarterly"}


def build_event_study_series() -> pd.DataFrame:
    impact = pd.read_csv(IMPACT_PATH)
    indicators = pd.read_csv(INDICATORS_PATH)

    impact["event_anchor_date"] = pd.to_datetime(impact["event_anchor_date"], errors="coerce")
    impact["abs_standardized_change"] = pd.to_numeric(impact["abs_standardized_change"], errors="coerce")
    indicators["date"] = pd.to_datetime(indicators["date"], errors="coerce")
    indicators["z_score"] = pd.to_numeric(indicators["z_score"], errors="coerce")
    indicators = indicators[
        indicators["frequency"].isin(SUPPORTED_FREQUENCIES)
        & indicators["date"].notna()
        & indicators["z_score"].notna()
    ].copy()

    event_indicators = (
        impact.dropna(subset=["event_anchor_date"])
        .sort_values("abs_standardized_change", ascending=False)
        .drop_duplicates(["event_id", "indicator_slug", "indicator_source"])
    )

    rows: list[pd.DataFrame] = []
    series_cache: dict[tuple[str, str, str], pd.DataFrame] = {}

    for _, event_indicator in event_indicators.iterrows():
        anchor_date = event_indicator["event_anchor_date"]
        key = (
            event_indicator["country_code"],
            event_indicator["indicator_slug"],
            event_indicator["indicator_source"],
        )
        if key not in series_cache:
            country_code, indicator_slug, source = key
            series_cache[key] = indicators[
                (indicators["country_code"] == country_code)
                & (indicators["indicator_slug"] == indicator_slug)
                & (indicators["source"] == source)
            ].sort_values("date")

        window = series_cache[key][
            (series_cache[key]["date"] >= anchor_date - pd.Timedelta(days=PRE_DAYS))
            & (series_cache[key]["date"] <= anchor_date + pd.Timedelta(days=POST_DAYS))
        ].copy()
        if window.empty:
            continue

        window["event_id"] = event_indicator["event_id"]
        window["event_name"] = event_indicator["event_name"]
        window["event_anchor_date"] = anchor_date
        window["event_date_precision"] = event_indicator["event_date_precision"]
        window["event_category"] = event_indicator["event_category"]
        window["event_subcategory"] = event_indicator["event_subcategory"]
        window["relative_day"] = (window["date"] - anchor_date).dt.days
        window["event_study_pre_days"] = PRE_DAYS
        window["event_study_post_days"] = POST_DAYS
        rows.append(
            window[
                [
                    "event_id",
                    "country_code",
                    "country_name",
                    "event_name",
                    "event_anchor_date",
                    "event_date_precision",
                    "event_category",
                    "event_subcategory",
                    "date",
                    "relative_day",
                    "frequency",
                    "indicator_group",
                    "indicator_slug",
                    "indicator_name",
                    "unit",
                    "source",
                    "value",
                    "z_score",
                    "event_study_pre_days",
                    "event_study_post_days",
                ]
            ]
        )

    event_study = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    if event_study.empty:
        raise ValueError("Nenhuma linha de event study foi gerada.")

    event_study = event_study.sort_values(
        ["country_code", "event_anchor_date", "event_id", "indicator_slug", "date"]
    )
    event_study.to_csv(OUTPUT_PATH, index=False, date_format="%Y-%m-%d")

    summary = (
        event_study.groupby(["country_code", "event_id", "indicator_slug"], as_index=False)
        .agg(
            rows=("date", "size"),
            min_relative_day=("relative_day", "min"),
            max_relative_day=("relative_day", "max"),
            peak_abs_z=("z_score", lambda values: values.abs().max()),
        )
        .sort_values(["country_code", "event_id", "indicator_slug"])
    )
    summary.to_csv(SUMMARY_PATH, index=False)
    return event_study


if __name__ == "__main__":
    result = build_event_study_series()
    print(f"Linhas de event study: {len(result)}")
    print(result.groupby("country_code")["event_id"].nunique().to_string())
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
    print(f"Resumo salvo em: {SUMMARY_PATH}")
