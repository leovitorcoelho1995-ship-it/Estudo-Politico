from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

IMPACT_PATH = PROCESSED_DIR / "event_economic_impact_normalized.csv"
INDICATORS_PATH = PROCESSED_DIR / "economic_indicators_normalized.csv"
OUTPUT_PATH = PROCESSED_DIR / "event_shock_persistence.csv"
SUMMARY_PATH = PROCESSED_DIR / "event_shock_persistence_summary.csv"

HORIZON_DAYS = 365
NORMAL_Z_THRESHOLD = 1.0
SUPPORTED_FREQUENCIES = {"daily", "weekly", "monthly", "quarterly"}


def classify_persistence(
    peak_abs_z_after: float | None,
    days_until_normal_range: int | None,
    after_observations: int,
) -> str:
    if after_observations < 2 or peak_abs_z_after is None or pd.isna(peak_abs_z_after):
        return "insuficiente"
    if peak_abs_z_after < NORMAL_Z_THRESHOLD:
        return "sem choque relevante"
    if days_until_normal_range is None or pd.isna(days_until_normal_range):
        return "persistiu"
    if days_until_normal_range <= 90:
        return "reverteu rapido"
    return "decaiu lentamente"


def summarize_persistence(event_row: pd.Series, series: pd.DataFrame) -> dict[str, object]:
    anchor_date = pd.to_datetime(event_row["event_anchor_date"])
    horizon_end = anchor_date + pd.Timedelta(days=HORIZON_DAYS)
    after = series[(series["date"] > anchor_date) & (series["date"] <= horizon_end)].copy()

    base = event_row.to_dict()
    base["persistence_horizon_days"] = HORIZON_DAYS
    base["normal_z_threshold"] = NORMAL_Z_THRESHOLD
    base["after_horizon_observations"] = int(len(after))

    if after.empty:
        base.update(
            {
                "peak_abs_z_after": pd.NA,
                "peak_z_after": pd.NA,
                "peak_date_after": pd.NaT,
                "days_to_peak": pd.NA,
                "days_until_normal_range": pd.NA,
                "end_abs_z_after": pd.NA,
                "persistence_label": "insuficiente",
            }
        )
        return base

    after["abs_z_score"] = after["z_score"].abs()
    peak = after.sort_values("abs_z_score", ascending=False).iloc[0]
    normal_after_peak = after[
        (after["date"] >= peak["date"]) & (after["abs_z_score"] < NORMAL_Z_THRESHOLD)
    ].sort_values("date")
    days_until_normal = (
        int((normal_after_peak.iloc[0]["date"] - anchor_date).days)
        if not normal_after_peak.empty
        else pd.NA
    )
    end_abs_z = float(after.sort_values("date").iloc[-1]["abs_z_score"])
    peak_abs_z = float(peak["abs_z_score"])

    base.update(
        {
            "peak_abs_z_after": peak_abs_z,
            "peak_z_after": float(peak["z_score"]),
            "peak_date_after": peak["date"],
            "days_to_peak": int((peak["date"] - anchor_date).days),
            "days_until_normal_range": days_until_normal,
            "end_abs_z_after": end_abs_z,
            "persistence_label": classify_persistence(
                peak_abs_z,
                None if pd.isna(days_until_normal) else int(days_until_normal),
                len(after),
            ),
        }
    )
    return base


def build_shock_persistence() -> pd.DataFrame:
    impact = pd.read_csv(IMPACT_PATH)
    indicators = pd.read_csv(INDICATORS_PATH)

    impact["event_anchor_date"] = pd.to_datetime(impact["event_anchor_date"], errors="coerce")
    indicators["date"] = pd.to_datetime(indicators["date"], errors="coerce")
    indicators["z_score"] = pd.to_numeric(indicators["z_score"], errors="coerce")
    indicators = indicators[
        indicators["frequency"].isin(SUPPORTED_FREQUENCIES)
        & indicators["date"].notna()
        & indicators["z_score"].notna()
    ].copy()

    rows: list[dict[str, object]] = []
    series_cache: dict[tuple[str, str, str], pd.DataFrame] = {}

    for _, row in impact.dropna(subset=["event_anchor_date"]).iterrows():
        key = (row["country_code"], row["indicator_slug"], row["indicator_source"])
        if key not in series_cache:
            country_code, indicator_slug, source = key
            series_cache[key] = indicators[
                (indicators["country_code"] == country_code)
                & (indicators["indicator_slug"] == indicator_slug)
                & (indicators["source"] == source)
            ].sort_values("date")
        rows.append(summarize_persistence(row, series_cache[key]))

    persistence = pd.DataFrame(rows)
    if persistence.empty:
        raise ValueError("Nenhuma linha de persistencia foi gerada.")

    persistence = persistence.sort_values(
        ["country_code", "event_anchor_date", "event_id", "indicator_slug", "window_days"]
    )
    persistence.to_csv(OUTPUT_PATH, index=False, date_format="%Y-%m-%d")

    summary = (
        persistence.groupby(["country_code", "window_days", "persistence_label"], as_index=False)
        .agg(
            rows=("event_id", "size"),
            events=("event_id", "nunique"),
            median_days_to_peak=("days_to_peak", "median"),
            median_days_until_normal=("days_until_normal_range", "median"),
        )
        .sort_values(["country_code", "window_days", "persistence_label"])
    )
    summary.to_csv(SUMMARY_PATH, index=False)
    return persistence


if __name__ == "__main__":
    result = build_shock_persistence()
    print(f"Linhas de persistencia: {len(result)}")
    print(result.groupby("persistence_label").size().to_string())
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
    print(f"Resumo salvo em: {SUMMARY_PATH}")
