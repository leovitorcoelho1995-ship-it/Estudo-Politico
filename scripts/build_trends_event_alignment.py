from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

INPUT_PATH = PROCESSED_DIR / "trends_normalized.csv"
OUTPUT_PATH = PROCESSED_DIR / "trends_event_alignment.csv"

OUTPUT_COLUMNS = [
    "event_id",
    "country_code",
    "country_name",
    "event_name",
    "event_start_date",
    "event_end_date",
    "term",
    "peak_date",
    "peak_interest",
    "peak_z_score",
    "days_from_event",
    "timing",
]


def timing_label(days_from_event: int) -> str:
    if days_from_event < 0:
        return "antes"
    if days_from_event > 0:
        return "depois"
    return "no evento"


def build_alignment() -> pd.DataFrame:
    if not INPUT_PATH.exists():
        result = pd.DataFrame(columns=OUTPUT_COLUMNS)
        result.to_csv(OUTPUT_PATH, index=False)
        return result

    trends = pd.read_csv(INPUT_PATH)
    if trends.empty:
        result = pd.DataFrame(columns=OUTPUT_COLUMNS)
        result.to_csv(OUTPUT_PATH, index=False)
        return result

    trends["date"] = pd.to_datetime(trends["date"], errors="coerce")
    trends["event_start_date"] = pd.to_datetime(trends["event_start_date"], errors="coerce")
    trends["event_end_date"] = pd.to_datetime(trends["event_end_date"], errors="coerce")
    trends["interest"] = pd.to_numeric(trends["interest"], errors="coerce")
    trends["z_score"] = pd.to_numeric(trends["z_score"], errors="coerce")
    trends = trends.dropna(subset=["date", "event_start_date", "interest", "z_score"]).copy()

    rows = []
    for (_, term), group in trends.groupby(["event_id", "term"]):
        group = group.sort_values(["z_score", "interest"], ascending=False)
        peak = group.iloc[0]
        days_from_event = int((peak["date"] - peak["event_start_date"]).days)
        rows.append(
            {
                "event_id": peak["event_id"],
                "country_code": peak["country_code"],
                "country_name": peak["country_name"],
                "event_name": peak["event_name"],
                "event_start_date": peak["event_start_date"],
                "event_end_date": peak["event_end_date"],
                "term": term,
                "peak_date": peak["date"],
                "peak_interest": peak["interest"],
                "peak_z_score": peak["z_score"],
                "days_from_event": days_from_event,
                "timing": timing_label(days_from_event),
            }
        )

    result = pd.DataFrame(rows, columns=OUTPUT_COLUMNS)
    result = result.sort_values(["country_code", "event_id", "peak_z_score"], ascending=[True, True, False])
    result.to_csv(OUTPUT_PATH, index=False, date_format="%Y-%m-%d")
    return result


if __name__ == "__main__":
    alignment = build_alignment()
    print(f"Alinhamentos Trends: {len(alignment)}")
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
