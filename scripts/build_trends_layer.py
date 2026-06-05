from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_TRENDS_DIR = PROJECT_ROOT / "data" / "raw" / "trends"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_PATH = PROCESSED_DIR / "trends_normalized.csv"
SUMMARY_PATH = PROCESSED_DIR / "trends_normalized_summary.csv"

OUTPUT_COLUMNS = [
    "event_id",
    "country_code",
    "country_name",
    "event_name",
    "event_start_date",
    "event_end_date",
    "geo",
    "timeframe",
    "date",
    "term",
    "interest",
    "is_partial",
    "series_mean",
    "series_std",
    "z_score",
]


def empty_output() -> pd.DataFrame:
    df = pd.DataFrame(columns=OUTPUT_COLUMNS)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    pd.DataFrame(
        columns=[
            "event_id",
            "country_code",
            "event_name",
            "term",
            "rows",
            "start_date",
            "end_date",
            "mean_interest",
            "max_interest",
            "max_z_score",
        ]
    ).to_csv(SUMMARY_PATH, index=False)
    return df


def normalize_group(group: pd.DataFrame) -> pd.DataFrame:
    group = group.sort_values("date").copy()
    mean_value = group["interest"].mean()
    std_value = group["interest"].std(ddof=0)
    group["series_mean"] = mean_value
    group["series_std"] = std_value
    group["z_score"] = (group["interest"] - mean_value) / std_value if std_value != 0 else pd.NA
    return group


def build_trends_layer() -> pd.DataFrame:
    files = sorted(RAW_TRENDS_DIR.glob("trends_*.csv"))
    files = [path for path in files if path.name != "trends_related_queries.csv"]
    if not files:
        print(f"Nenhum arquivo bruto encontrado em: {RAW_TRENDS_DIR}")
        return empty_output()

    frames = [pd.read_csv(path) for path in files]
    df = pd.concat(frames, ignore_index=True)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["event_start_date"] = pd.to_datetime(df["event_start_date"], errors="coerce")
    df["event_end_date"] = pd.to_datetime(df["event_end_date"], errors="coerce")
    df["interest"] = pd.to_numeric(df["interest"], errors="coerce")
    df = df.dropna(subset=["date", "interest", "term", "event_id"]).copy()

    normalized = pd.concat(
        [normalize_group(group) for _, group in df.groupby(["event_id", "term"])],
        ignore_index=True,
    )
    normalized = normalized.sort_values(["country_code", "event_id", "term", "date"])
    normalized = normalized[OUTPUT_COLUMNS]

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    normalized.to_csv(OUTPUT_PATH, index=False, date_format="%Y-%m-%d")

    summary = (
        normalized.groupby(["event_id", "country_code", "event_name", "term"], as_index=False)
        .agg(
            rows=("interest", "size"),
            start_date=("date", "min"),
            end_date=("date", "max"),
            mean_interest=("interest", "mean"),
            max_interest=("interest", "max"),
            max_z_score=("z_score", "max"),
        )
        .sort_values(["country_code", "event_id", "term"])
    )
    summary.to_csv(SUMMARY_PATH, index=False, date_format="%Y-%m-%d")
    return normalized


if __name__ == "__main__":
    result = build_trends_layer()
    print(f"Linhas Trends normalizadas: {len(result)}")
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
