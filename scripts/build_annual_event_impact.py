from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

EVENTS_PATH = PROCESSED_DIR / "political_events_processed.csv"
INDICATORS_PATH = PROCESSED_DIR / "economic_indicators_normalized.csv"
OUTPUT_PATH = PROCESSED_DIR / "annual_event_impact.csv"
SUMMARY_PATH = PROCESSED_DIR / "annual_event_impact_summary.csv"


def value_for_year(indicator: pd.DataFrame, year: int, column: str) -> float | None:
    match = indicator[indicator["year"] == year]
    if match.empty:
        return None
    value = match[column].iloc[0]
    if pd.isna(value):
        return None
    return float(value)


def build_annual_impact() -> pd.DataFrame:
    events = pd.read_csv(EVENTS_PATH)
    indicators = pd.read_csv(INDICATORS_PATH)

    events["start_year"] = pd.to_numeric(events["start_year"], errors="raise").astype("int64")
    indicators = indicators[indicators["frequency"] == "annual"].copy()
    indicators["year"] = pd.to_numeric(indicators["year"], errors="raise").astype("int64")
    indicators["value"] = pd.to_numeric(indicators["value"], errors="coerce")
    indicators["z_score"] = pd.to_numeric(indicators["z_score"], errors="coerce")

    rows: list[dict[str, object]] = []

    for _, event in events.iterrows():
        country_indicators = indicators[indicators["country_code"] == event["country_code"]]
        event_year = int(event["start_year"])

        for _, indicator in country_indicators.groupby(["indicator_slug", "source"], sort=False):
            previous_value = value_for_year(indicator, event_year - 1, "value")
            event_value = value_for_year(indicator, event_year, "value")
            next_value = value_for_year(indicator, event_year + 1, "value")

            previous_z = value_for_year(indicator, event_year - 1, "z_score")
            event_z = value_for_year(indicator, event_year, "z_score")
            next_z = value_for_year(indicator, event_year + 1, "z_score")

            if event_value is None:
                continue

            change_from_previous = None if previous_value is None else event_value - previous_value
            change_to_next = None if next_value is None else next_value - event_value
            z_change_from_previous = None if previous_z is None or event_z is None else event_z - previous_z
            z_change_to_next = None if next_z is None or event_z is None else next_z - event_z

            rows.append(
                {
                    "event_id": event["event_id"],
                    "country_code": event["country_code"],
                    "country_name": event["country_name"],
                    "event_name": event["event_name"],
                    "event_category": event["event_category"],
                    "event_subcategory": event["event_subcategory"],
                    "event_start_date": event["start_date"],
                    "event_end_date": event["end_date"],
                    "event_year": event_year,
                    "event_date_precision": event["date_precision"],
                    "indicator_group": indicator["indicator_group"].iloc[0],
                    "indicator_slug": indicator["indicator_slug"].iloc[0],
                    "indicator_name": indicator["indicator_name"].iloc[0],
                    "indicator_unit": indicator["unit"].iloc[0],
                    "indicator_source": indicator["source"].iloc[0],
                    "previous_year": event_year - 1,
                    "event_year_value": event_value,
                    "next_year": event_year + 1,
                    "previous_year_value": previous_value,
                    "next_year_value": next_value,
                    "change_from_previous_year": change_from_previous,
                    "change_to_next_year": change_to_next,
                    "previous_year_z_score": previous_z,
                    "event_year_z_score": event_z,
                    "next_year_z_score": next_z,
                    "z_change_from_previous_year": z_change_from_previous,
                    "z_change_to_next_year": z_change_to_next,
                }
            )

    result = pd.DataFrame(rows)
    if result.empty:
        raise ValueError("Nenhum impacto anual foi gerado.")

    result = result.sort_values(["country_code", "event_year", "event_id", "indicator_slug"])
    result.to_csv(OUTPUT_PATH, index=False)

    summary = (
        result.groupby(["country_code", "indicator_slug"], as_index=False)
        .agg(
            rows=("event_id", "size"),
            events=("event_id", "nunique"),
            first_event_year=("event_year", "min"),
            last_event_year=("event_year", "max"),
            max_abs_z_change_from_previous=("z_change_from_previous_year", lambda s: s.abs().max()),
        )
        .sort_values(["country_code", "indicator_slug"])
    )
    summary.to_csv(SUMMARY_PATH, index=False)

    return result


if __name__ == "__main__":
    annual = build_annual_impact()
    print(f"Linhas anuais geradas: {len(annual)}")
    print(annual.groupby("country_code")["event_id"].nunique().to_string())
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
    print(f"Resumo salvo em: {SUMMARY_PATH}")
