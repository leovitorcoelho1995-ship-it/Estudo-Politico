from __future__ import annotations

from pathlib import Path

import pandas as pd

from collect_trends import SEED_TERMS, fallback_terms


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

EVENTS_PATH = PROCESSED_DIR / "political_events_processed.csv"
TRENDS_PATH = PROCESSED_DIR / "trends_normalized.csv"
OUTPUT_PATH = PROCESSED_DIR / "trends_coverage.csv"
SUMMARY_PATH = PROCESSED_DIR / "trends_coverage_summary.csv"


def build_trends_coverage() -> pd.DataFrame:
    events = pd.read_csv(EVENTS_PATH)
    trends = pd.read_csv(TRENDS_PATH) if TRENDS_PATH.exists() else pd.DataFrame()

    if trends.empty:
        covered_ids: set[str] = set()
        terms_by_event = pd.DataFrame(columns=["event_id", "collected_terms"])
    else:
        covered_ids = set(trends["event_id"].dropna().astype(str))
        terms_by_event = (
            trends.groupby("event_id", as_index=False)
            .agg(collected_terms=("term", lambda values: "; ".join(sorted(set(values.dropna().astype(str))))))
        )

    coverage = events[
        [
            "event_id",
            "country_code",
            "country_name",
            "event_name",
            "date_precision",
            "event_category",
            "event_subcategory",
        ]
    ].copy()
    coverage["has_trends_data"] = coverage["event_id"].isin(covered_ids)
    coverage["has_seed_terms"] = coverage["event_id"].isin(SEED_TERMS)
    coverage["seed_terms"] = coverage.apply(
        lambda row: "; ".join(SEED_TERMS.get(row["event_id"], fallback_terms(row["event_name"], row["country_code"]))),
        axis=1,
    )
    coverage = coverage.merge(terms_by_event, on="event_id", how="left")
    coverage["trends_status"] = "missing_collection"
    coverage.loc[coverage["has_trends_data"], "trends_status"] = "collected"
    coverage.loc[
        ~coverage["has_seed_terms"] & ~coverage["has_trends_data"],
        "trends_status",
    ] = "missing_seed_terms"

    coverage.to_csv(OUTPUT_PATH, index=False)
    summary = (
        coverage.groupby(["country_code", "trends_status"], as_index=False)
        .agg(events=("event_id", "size"))
        .sort_values(["country_code", "trends_status"])
    )
    summary.to_csv(SUMMARY_PATH, index=False)
    return coverage


if __name__ == "__main__":
    result = build_trends_coverage()
    print(f"Eventos auditados em Trends: {len(result)}")
    print(result.groupby(["country_code", "trends_status"]).size().to_string())
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
