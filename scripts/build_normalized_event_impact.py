from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

IMPACT_PATH = PROCESSED_DIR / "event_economic_impact.csv"
NORMALIZED_INDICATORS_PATH = PROCESSED_DIR / "economic_indicators_normalized_summary.csv"
OUTPUT_PATH = PROCESSED_DIR / "event_economic_impact_normalized.csv"
SUMMARY_PATH = PROCESSED_DIR / "event_economic_impact_normalized_summary.csv"


def build_normalized_impact() -> pd.DataFrame:
    impact = pd.read_csv(IMPACT_PATH)
    indicator_stats = pd.read_csv(NORMALIZED_INDICATORS_PATH)

    stats = indicator_stats[
        [
            "country_code",
            "indicator_slug",
            "source",
            "std_value",
        ]
    ].rename(
        columns={
            "source": "indicator_source",
            "std_value": "historical_std",
        }
    )

    result = impact.merge(
        stats,
        on=["country_code", "indicator_slug", "indicator_source"],
        how="left",
        validate="many_to_one",
    )

    result["standardized_change"] = result["absolute_change"] / result["historical_std"]
    result.loc[result["historical_std"].isna() | (result["historical_std"] == 0), "standardized_change"] = pd.NA
    result["abs_standardized_change"] = result["standardized_change"].abs()

    result = result.sort_values(
        ["country_code", "event_anchor_date", "event_id", "indicator_slug", "window_days"]
    )
    result.to_csv(OUTPUT_PATH, index=False)

    summary = (
        result.groupby(["country_code", "indicator_slug", "window_days"], as_index=False)
        .agg(
            rows=("event_id", "size"),
            max_abs_standardized_change=("abs_standardized_change", "max"),
            median_abs_standardized_change=("abs_standardized_change", "median"),
        )
        .sort_values(["country_code", "indicator_slug", "window_days"])
    )
    summary.to_csv(SUMMARY_PATH, index=False)

    return result


if __name__ == "__main__":
    output = build_normalized_impact()
    print(f"Linhas de impacto normalizadas: {len(output)}")
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
    print(f"Resumo salvo em: {SUMMARY_PATH}")
