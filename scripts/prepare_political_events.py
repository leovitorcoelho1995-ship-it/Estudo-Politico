from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "political_events.csv"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "political_events_processed.csv"
SUMMARY_PATH = PROJECT_ROOT / "data" / "processed" / "political_events_summary.csv"

VALID_COUNTRIES = {"BRA", "USA", "ARG"}
VALID_PRECISIONS = {"day", "month", "year", "year_range"}


def prepare_events(raw_path: Path = RAW_PATH, processed_path: Path = PROCESSED_PATH) -> pd.DataFrame:
    df = pd.read_csv(raw_path)

    required_columns = {
        "event_id",
        "country_code",
        "country_name",
        "start_date",
        "end_date",
        "date_precision",
        "event_name",
        "event_category",
        "event_subcategory",
        "source_note",
    }
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Colunas ausentes: {sorted(missing_columns)}")

    if df["event_id"].duplicated().any():
        duplicated = df.loc[df["event_id"].duplicated(), "event_id"].tolist()
        raise ValueError(f"event_id duplicado: {duplicated}")

    unknown_countries = set(df["country_code"]) - VALID_COUNTRIES
    if unknown_countries:
        raise ValueError(f"Paises invalidos: {sorted(unknown_countries)}")

    unknown_precisions = set(df["date_precision"]) - VALID_PRECISIONS
    if unknown_precisions:
        raise ValueError(f"Precisao de data invalida: {sorted(unknown_precisions)}")

    df["start_date"] = pd.to_datetime(df["start_date"], errors="raise")
    df["end_date"] = pd.to_datetime(df["end_date"], errors="raise")

    invalid_ranges = df[df["end_date"] < df["start_date"]]
    if not invalid_ranges.empty:
        raise ValueError(f"Eventos com end_date antes de start_date: {invalid_ranges['event_id'].tolist()}")

    df["start_year"] = df["start_date"].dt.year
    df["end_year"] = df["end_date"].dt.year
    df["duration_days"] = (df["end_date"] - df["start_date"]).dt.days + 1

    df = df.sort_values(["country_code", "start_date", "event_id"])
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(processed_path, index=False, date_format="%Y-%m-%d")

    summary = (
        df.groupby(["country_code", "event_category"], as_index=False)
        .agg(
            events=("event_id", "size"),
            first_event=("start_date", "min"),
            last_event=("end_date", "max"),
        )
        .sort_values(["country_code", "event_category"])
    )
    summary.to_csv(SUMMARY_PATH, index=False, date_format="%Y-%m-%d")

    return df


if __name__ == "__main__":
    events = prepare_events()
    print(f"Eventos processados: {len(events)}")
    print(events.groupby("country_code").size().to_string())
    print(f"Arquivo salvo em: {PROCESSED_PATH}")
    print(f"Resumo salvo em: {SUMMARY_PATH}")
