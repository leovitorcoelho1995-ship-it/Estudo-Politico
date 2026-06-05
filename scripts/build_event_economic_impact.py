from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

EVENTS_PATH = PROCESSED_DIR / "political_events_processed.csv"
INDICATORS_PATH = PROCESSED_DIR / "economic_indicators_unified.csv"
OUTPUT_PATH = PROCESSED_DIR / "event_economic_impact.csv"
SUMMARY_PATH = PROCESSED_DIR / "event_economic_impact_summary.csv"

WINDOW_DAYS = [30, 90, 180, 365]
SUPPORTED_FREQUENCIES = {"daily", "weekly", "monthly", "quarterly"}
SUPPORTED_EVENT_PRECISIONS = {"day", "month"}


def pct_change(before_value: float | None, after_value: float | None) -> float | None:
    if before_value is None or after_value is None:
        return None
    if pd.isna(before_value) or pd.isna(after_value) or before_value == 0:
        return None
    return ((after_value - before_value) / abs(before_value)) * 100


def build_event_anchor_date(events: pd.DataFrame) -> pd.Series:
    start_dates = pd.to_datetime(events["start_date"])
    end_dates = pd.to_datetime(events["end_date"])
    return start_dates + (end_dates - start_dates) / 2


def summarize_window(
    event: pd.Series,
    indicator: pd.DataFrame,
    window_days: int,
) -> dict[str, object] | None:
    anchor_date = event["anchor_date"]
    before_start = anchor_date - pd.Timedelta(days=window_days)
    before_end = anchor_date - pd.Timedelta(days=1)
    after_start = anchor_date + pd.Timedelta(days=1)
    after_end = anchor_date + pd.Timedelta(days=window_days)

    before = indicator[(indicator["date"] >= before_start) & (indicator["date"] <= before_end)]
    after = indicator[(indicator["date"] >= after_start) & (indicator["date"] <= after_end)]

    before_count = len(before)
    after_count = len(after)
    if before_count == 0 or after_count == 0:
        return None

    before_mean = before["value"].mean()
    after_mean = after["value"].mean()
    absolute_change = after_mean - before_mean
    percentage_change = pct_change(before_mean, after_mean)

    return {
        "event_id": event["event_id"],
        "country_code": event["country_code"],
        "country_name": event["country_name"],
        "event_name": event["event_name"],
        "event_category": event["event_category"],
        "event_subcategory": event["event_subcategory"],
        "event_start_date": event["start_date"],
        "event_end_date": event["end_date"],
        "event_anchor_date": anchor_date,
        "event_date_precision": event["date_precision"],
        "window_days": window_days,
        "indicator_group": indicator["indicator_group"].iloc[0],
        "indicator_slug": indicator["indicator_slug"].iloc[0],
        "indicator_name": indicator["indicator_name"].iloc[0],
        "indicator_frequency": indicator["frequency"].iloc[0],
        "indicator_unit": indicator["unit"].iloc[0],
        "indicator_source": indicator["source"].iloc[0],
        "before_start": before_start,
        "before_end": before_end,
        "after_start": after_start,
        "after_end": after_end,
        "before_observations": before_count,
        "after_observations": after_count,
        "before_mean": before_mean,
        "after_mean": after_mean,
        "absolute_change": absolute_change,
        "percentage_change": percentage_change,
    }


def build_impact() -> pd.DataFrame:
    events = pd.read_csv(EVENTS_PATH)
    indicators = pd.read_csv(INDICATORS_PATH)

    events["start_date"] = pd.to_datetime(events["start_date"])
    events["end_date"] = pd.to_datetime(events["end_date"])
    events["anchor_date"] = build_event_anchor_date(events)

    indicators["date"] = pd.to_datetime(indicators["date"])
    indicators["value"] = pd.to_numeric(indicators["value"], errors="coerce")
    indicators = indicators[
        indicators["frequency"].isin(SUPPORTED_FREQUENCIES)
        & indicators["value"].notna()
    ].copy()

    point_events = events[events["date_precision"].isin(SUPPORTED_EVENT_PRECISIONS)].copy()
    rows: list[dict[str, object]] = []

    for _, event in point_events.iterrows():
        country_indicators = indicators[indicators["country_code"] == event["country_code"]]

        for _, indicator in country_indicators.groupby(["indicator_slug", "source"], sort=False):
            for window_days in WINDOW_DAYS:
                row = summarize_window(event, indicator, window_days)
                if row is not None:
                    rows.append(row)

    impact = pd.DataFrame(rows)
    if impact.empty:
        raise ValueError("Nenhuma combinacao evento-indicador foi gerada.")

    impact = impact.sort_values(
        ["country_code", "event_anchor_date", "event_id", "indicator_slug", "window_days"]
    )
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    impact.to_csv(OUTPUT_PATH, index=False, date_format="%Y-%m-%d")

    summary = (
        impact.groupby(["country_code", "indicator_slug", "window_days"], as_index=False)
        .agg(
            rows=("event_id", "size"),
            events=("event_id", "nunique"),
            first_event=("event_anchor_date", "min"),
            last_event=("event_anchor_date", "max"),
        )
        .sort_values(["country_code", "indicator_slug", "window_days"])
    )
    summary.to_csv(SUMMARY_PATH, index=False, date_format="%Y-%m-%d")

    return impact


if __name__ == "__main__":
    result = build_impact()
    print(f"Linhas de impacto geradas: {len(result)}")
    print(result.groupby("country_code")["event_id"].nunique().to_string())
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
    print(f"Resumo salvo em: {SUMMARY_PATH}")
