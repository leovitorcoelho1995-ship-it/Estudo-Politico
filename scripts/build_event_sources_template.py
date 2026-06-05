from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

EVENTS_PATH = PROCESSED_DIR / "political_events_processed.csv"
OUTPUT_PATH = RAW_DIR / "political_event_sources.csv"
AUDIT_PATH = PROCESSED_DIR / "event_sources_audit.csv"
SUMMARY_PATH = PROCESSED_DIR / "event_sources_audit_summary.csv"

SOURCE_COLUMNS = [
    "event_id",
    "country_code",
    "event_name",
    "source_title",
    "source_url",
    "source_type",
    "source_status",
    "notes",
]


def build_template() -> pd.DataFrame:
    events = pd.read_csv(EVENTS_PATH)

    if OUTPUT_PATH.exists():
        sources = pd.read_csv(OUTPUT_PATH)
    else:
        sources = pd.DataFrame(columns=SOURCE_COLUMNS)

    for column in SOURCE_COLUMNS:
        if column not in sources.columns:
            sources[column] = pd.NA

    known_ids = set(sources["event_id"].dropna().astype(str))
    missing = events[~events["event_id"].isin(known_ids)].copy()
    new_rows = pd.DataFrame(
        {
            "event_id": missing["event_id"],
            "country_code": missing["country_code"],
            "event_name": missing["event_name"],
            "source_title": "",
            "source_url": "",
            "source_type": "",
            "source_status": "pending",
            "notes": "add primary or reputable reference source",
        }
    )

    sources = pd.concat([sources[SOURCE_COLUMNS], new_rows], ignore_index=True)
    sources = sources.drop_duplicates(subset=["event_id"], keep="first")
    sources = sources.sort_values(["country_code", "event_id"])
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    sources.to_csv(OUTPUT_PATH, index=False)

    audit = sources.copy()
    audit["has_source_url"] = audit["source_url"].fillna("").astype(str).str.startswith(("http://", "https://"))
    audit["source_status"] = audit["source_status"].fillna("pending")
    audit.to_csv(AUDIT_PATH, index=False)

    summary = (
        audit.groupby(["country_code", "source_status"], as_index=False)
        .agg(events=("event_id", "size"), with_url=("has_source_url", "sum"))
        .sort_values(["country_code", "source_status"])
    )
    summary.to_csv(SUMMARY_PATH, index=False)
    return audit


if __name__ == "__main__":
    result = build_template()
    print(f"Eventos na tabela de fontes: {len(result)}")
    print(result.groupby(["country_code", "source_status"]).size().to_string())
    print(f"Template salvo em: {OUTPUT_PATH}")
    print(f"Auditoria salva em: {AUDIT_PATH}")
