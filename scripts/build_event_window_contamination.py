from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

EVENTS_PATH = PROCESSED_DIR / "political_events_processed.csv"
OUTPUT_PATH = PROCESSED_DIR / "event_window_contamination.csv"
SUMMARY_PATH = PROCESSED_DIR / "event_window_contamination_summary.csv"

WINDOW_DAYS = [30, 90, 180]
SUPPORTED_EVENT_PRECISIONS = {"day", "month"}


def build_event_anchor_date(events: pd.DataFrame) -> pd.Series:
    start_dates = pd.to_datetime(events["start_date"])
    end_dates = pd.to_datetime(events["end_date"])
    return start_dates + (end_dates - start_dates) / 2


def contamination_level(count: int) -> str:
    if count >= 3:
        return "alta"
    if count >= 1:
        return "moderada"
    return "baixa"


def build_contamination() -> pd.DataFrame:
    events = pd.read_csv(EVENTS_PATH)
    events["start_date"] = pd.to_datetime(events["start_date"])
    events["end_date"] = pd.to_datetime(events["end_date"])
    events["anchor_date"] = build_event_anchor_date(events)

    point_events = events[events["date_precision"].isin(SUPPORTED_EVENT_PRECISIONS)].copy()
    rows: list[dict[str, object]] = []

    for _, event in point_events.iterrows():
        same_country_events = point_events[
            (point_events["country_code"] == event["country_code"])
            & (point_events["event_id"] != event["event_id"])
        ].copy()
        same_country_events["distance_days"] = (
            same_country_events["anchor_date"] - event["anchor_date"]
        ).dt.days
        same_country_events["abs_distance_days"] = same_country_events["distance_days"].abs()

        for window_days in WINDOW_DAYS:
            nearby = same_country_events[
                same_country_events["abs_distance_days"] <= window_days
            ].sort_values(["abs_distance_days", "anchor_date"])
            nearby_names = "; ".join(nearby["event_name"].astype(str).tolist())
            nearby_ids = "; ".join(nearby["event_id"].astype(str).tolist())
            nearby_distances = "; ".join(
                str(int(value)) for value in nearby["distance_days"].tolist()
            )
            nearby_count = int(len(nearby))

            rows.append(
                {
                    "event_id": event["event_id"],
                    "country_code": event["country_code"],
                    "country_name": event["country_name"],
                    "event_name": event["event_name"],
                    "event_anchor_date": event["anchor_date"],
                    "event_date_precision": event["date_precision"],
                    "window_days": window_days,
                    "nearby_event_count": nearby_count,
                    "contamination_level": contamination_level(nearby_count),
                    "nearby_event_ids": nearby_ids,
                    "nearby_event_names": nearby_names,
                    "nearby_event_distance_days": nearby_distances,
                    "is_contaminated_window": nearby_count > 0,
                }
            )

    contamination = pd.DataFrame(rows).sort_values(
        ["country_code", "event_anchor_date", "event_id", "window_days"]
    )
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    contamination.to_csv(OUTPUT_PATH, index=False, date_format="%Y-%m-%d")

    summary = (
        contamination.groupby(["country_code", "window_days", "contamination_level"], as_index=False)
        .agg(events=("event_id", "nunique"), rows=("event_id", "size"))
        .sort_values(["country_code", "window_days", "contamination_level"])
    )
    summary.to_csv(SUMMARY_PATH, index=False)

    return contamination


if __name__ == "__main__":
    result = build_contamination()
    contaminated = result[result["is_contaminated_window"]]
    print(f"Linhas de contaminacao geradas: {len(result)}")
    print(f"Janelas com eventos proximos: {len(contaminated)}")
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
    print(f"Resumo salvo em: {SUMMARY_PATH}")
