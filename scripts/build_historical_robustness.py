from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

IMPACT_PATH = PROCESSED_DIR / "event_economic_impact_normalized.csv"
INDICATORS_PATH = PROCESSED_DIR / "economic_indicators_unified.csv"
OUTPUT_PATH = PROCESSED_DIR / "event_economic_impact_robustness.csv"
SUMMARY_PATH = PROCESSED_DIR / "event_economic_impact_robustness_summary.csv"

MIN_BASELINE_WINDOWS = 20


def summarize_change(series: pd.DataFrame, anchor_date: pd.Timestamp, window_days: int) -> tuple[float, int, int] | None:
    before_start = anchor_date - pd.Timedelta(days=window_days)
    before_end = anchor_date - pd.Timedelta(days=1)
    after_start = anchor_date + pd.Timedelta(days=1)
    after_end = anchor_date + pd.Timedelta(days=window_days)

    before = series[(series["date"] >= before_start) & (series["date"] <= before_end)]
    after = series[(series["date"] >= after_start) & (series["date"] <= after_end)]

    if before.empty or after.empty:
        return None

    return float(after["value"].mean() - before["value"].mean()), len(before), len(after)


def candidate_anchor_dates(series: pd.DataFrame, window_days: int) -> pd.Series:
    min_date = series["date"].min() + pd.Timedelta(days=window_days)
    max_date = series["date"].max() - pd.Timedelta(days=window_days)
    candidates = series[(series["date"] >= min_date) & (series["date"] <= max_date)]["date"]
    return candidates.drop_duplicates().sort_values()


def historical_distribution(series: pd.DataFrame, window_days: int, historical_std: float) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    if pd.isna(historical_std) or historical_std == 0:
        return pd.DataFrame(rows)

    series = series.sort_values("date").drop_duplicates(subset=["date"], keep="last")
    dates = series["date"].to_numpy(dtype="datetime64[ns]")
    values = series["value"].to_numpy(dtype="float64")
    cumulative = values.cumsum()

    def window_stats(start: pd.Timestamp, end: pd.Timestamp) -> tuple[float, int] | None:
        left = dates.searchsorted(start.to_datetime64(), side="left")
        right = dates.searchsorted(end.to_datetime64(), side="right")
        count = right - left
        if count <= 0:
            return None
        total = cumulative[right - 1] - (cumulative[left - 1] if left > 0 else 0.0)
        return float(total / count), int(count)

    for anchor_date in candidate_anchor_dates(series, window_days):
        before_start = anchor_date - pd.Timedelta(days=window_days)
        before_end = anchor_date - pd.Timedelta(days=1)
        after_start = anchor_date + pd.Timedelta(days=1)
        after_end = anchor_date + pd.Timedelta(days=window_days)

        before = window_stats(before_start, before_end)
        after = window_stats(after_start, after_end)
        if before is None or after is None:
            continue

        before_mean, before_count = before
        after_mean, after_count = after
        absolute_change = after_mean - before_mean
        standardized_change = absolute_change / historical_std
        rows.append(
            {
                "baseline_anchor_date": anchor_date,
                "baseline_before_observations": before_count,
                "baseline_after_observations": after_count,
                "baseline_standardized_change": standardized_change,
                "baseline_abs_standardized_change": abs(standardized_change),
            }
        )

    return pd.DataFrame(rows)


def classify_rarity(percentile: float | None, baseline_windows: int) -> str:
    if percentile is None or pd.isna(percentile) or baseline_windows < MIN_BASELINE_WINDOWS:
        return "insuficiente"
    if percentile >= 95:
        return "raro"
    if percentile >= 80:
        return "acima do comum"
    return "comum"


def build_historical_robustness() -> pd.DataFrame:
    impact = pd.read_csv(IMPACT_PATH)
    indicators = pd.read_csv(INDICATORS_PATH)

    impact["event_anchor_date"] = pd.to_datetime(impact["event_anchor_date"], errors="coerce")
    impact["abs_standardized_change"] = pd.to_numeric(impact["abs_standardized_change"], errors="coerce")
    impact["historical_std"] = pd.to_numeric(impact["historical_std"], errors="coerce")

    indicators["date"] = pd.to_datetime(indicators["date"], errors="coerce")
    indicators["value"] = pd.to_numeric(indicators["value"], errors="coerce")
    indicators = indicators.dropna(subset=["date", "value"]).copy()

    rows: list[dict[str, object]] = []
    distribution_cache: dict[tuple[str, str, str, int, float], pd.DataFrame] = {}

    for _, row in impact.dropna(subset=["event_anchor_date", "abs_standardized_change"]).iterrows():
        key = (
            row["country_code"],
            row["indicator_slug"],
            row["indicator_source"],
            int(row["window_days"]),
            float(row["historical_std"]) if not pd.isna(row["historical_std"]) else 0.0,
        )

        if key not in distribution_cache:
            country_code, indicator_slug, indicator_source, window_days, historical_std = key
            series = indicators[
                (indicators["country_code"] == country_code)
                & (indicators["indicator_slug"] == indicator_slug)
                & (indicators["source"] == indicator_source)
            ].copy()
            distribution_cache[key] = historical_distribution(series, window_days, historical_std)

        distribution = distribution_cache[key]
        observed_abs = float(row["abs_standardized_change"])
        baseline_windows = len(distribution)

        if baseline_windows:
            percentile = (distribution["baseline_abs_standardized_change"] <= observed_abs).mean() * 100
            median_baseline = distribution["baseline_abs_standardized_change"].median()
            p95_baseline = distribution["baseline_abs_standardized_change"].quantile(0.95)
        else:
            percentile = pd.NA
            median_baseline = pd.NA
            p95_baseline = pd.NA

        row_dict = row.to_dict()
        row_dict.update(
            {
                "baseline_windows": baseline_windows,
                "baseline_median_abs_standardized_change": median_baseline,
                "baseline_p95_abs_standardized_change": p95_baseline,
                "historical_percentile": percentile,
                "rarity_label": classify_rarity(percentile, baseline_windows),
                "is_rare_movement": bool(
                    baseline_windows >= MIN_BASELINE_WINDOWS
                    and not pd.isna(percentile)
                    and percentile >= 95
                ),
            }
        )
        rows.append(row_dict)

    robustness = pd.DataFrame(rows)
    if robustness.empty:
        raise ValueError("Nenhuma linha de robustez foi gerada.")

    robustness = robustness.sort_values(
        [
            "country_code",
            "event_anchor_date",
            "event_id",
            "indicator_slug",
            "window_days",
        ]
    )
    robustness.to_csv(OUTPUT_PATH, index=False)

    summary = (
        robustness.groupby(["country_code", "window_days", "rarity_label"], as_index=False)
        .agg(
            rows=("event_id", "size"),
            events=("event_id", "nunique"),
            median_percentile=("historical_percentile", "median"),
            rare_movements=("is_rare_movement", "sum"),
        )
        .sort_values(["country_code", "window_days", "rarity_label"])
    )
    summary.to_csv(SUMMARY_PATH, index=False)

    return robustness


if __name__ == "__main__":
    result = build_historical_robustness()
    print(f"Linhas de robustez historica: {len(result)}")
    print(result.groupby("rarity_label").size().to_string())
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
    print(f"Resumo salvo em: {SUMMARY_PATH}")
