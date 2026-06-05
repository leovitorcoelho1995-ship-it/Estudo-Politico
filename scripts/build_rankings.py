from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

SHORT_TERM_PATH = PROCESSED_DIR / "event_economic_impact_normalized.csv"
ANNUAL_PATH = PROCESSED_DIR / "annual_event_impact.csv"
CONTAMINATION_PATH = PROCESSED_DIR / "event_window_contamination.csv"

SHORT_TERM_RANKING_PATH = PROCESSED_DIR / "ranking_short_term_impacts.csv"
SHORT_TERM_BY_COUNTRY_PATH = PROCESSED_DIR / "ranking_short_term_impacts_by_country.csv"
ANNUAL_RANKING_PATH = PROCESSED_DIR / "ranking_annual_impacts.csv"
ANNUAL_BY_COUNTRY_PATH = PROCESSED_DIR / "ranking_annual_impacts_by_country.csv"
ANNUAL_CONTEXT_RANKING_PATH = PROCESSED_DIR / "ranking_annual_context_by_country_year.csv"


def build_short_term_rankings(top_n_per_country: int = 20) -> pd.DataFrame:
    df = pd.read_csv(SHORT_TERM_PATH)
    df["abs_standardized_change"] = pd.to_numeric(df["abs_standardized_change"], errors="coerce")
    df = df.dropna(subset=["abs_standardized_change"]).copy()

    if CONTAMINATION_PATH.exists():
        contamination = pd.read_csv(CONTAMINATION_PATH)
        contamination_cols = [
            "event_id",
            "window_days",
            "nearby_event_count",
            "contamination_level",
            "nearby_event_names",
            "is_contaminated_window",
        ]
        df = df.merge(
            contamination[contamination_cols],
            on=["event_id", "window_days"],
            how="left",
        )

    ranking_columns = [
        "country_code",
        "country_name",
        "event_name",
        "event_category",
        "event_subcategory",
        "event_anchor_date",
        "window_days",
        "indicator_group",
        "indicator_slug",
        "indicator_name",
        "indicator_frequency",
        "before_mean",
        "after_mean",
        "absolute_change",
        "percentage_change",
        "historical_std",
        "standardized_change",
        "abs_standardized_change",
    ]
    contamination_ranking_columns = [
        "nearby_event_count",
        "contamination_level",
        "nearby_event_names",
        "is_contaminated_window",
    ]
    ranking_columns.extend(
        [column for column in contamination_ranking_columns if column in df.columns]
    )

    ranking = df[ranking_columns].sort_values("abs_standardized_change", ascending=False)
    ranking.to_csv(SHORT_TERM_RANKING_PATH, index=False)

    by_country = (
        ranking.groupby("country_code", group_keys=False)
        .head(top_n_per_country)
        .reset_index(drop=True)
    )
    by_country.to_csv(SHORT_TERM_BY_COUNTRY_PATH, index=False)

    return ranking


def build_annual_rankings(top_n_per_country: int = 20) -> pd.DataFrame:
    df = pd.read_csv(ANNUAL_PATH)
    df["z_change_from_previous_year"] = pd.to_numeric(
        df["z_change_from_previous_year"], errors="coerce"
    )
    df["abs_z_change_from_previous_year"] = df["z_change_from_previous_year"].abs()
    df = df.dropna(subset=["abs_z_change_from_previous_year"]).copy()

    ranking_columns = [
        "country_code",
        "country_name",
        "event_name",
        "event_category",
        "event_subcategory",
        "event_year",
        "indicator_group",
        "indicator_slug",
        "indicator_name",
        "previous_year_value",
        "event_year_value",
        "next_year_value",
        "change_from_previous_year",
        "change_to_next_year",
        "previous_year_z_score",
        "event_year_z_score",
        "next_year_z_score",
        "z_change_from_previous_year",
        "z_change_to_next_year",
        "abs_z_change_from_previous_year",
    ]

    ranking = df[ranking_columns].sort_values("abs_z_change_from_previous_year", ascending=False)
    ranking.to_csv(ANNUAL_RANKING_PATH, index=False)

    by_country = (
        ranking.groupby("country_code", group_keys=False)
        .head(top_n_per_country)
        .reset_index(drop=True)
    )
    by_country.to_csv(ANNUAL_BY_COUNTRY_PATH, index=False)

    context = (
        ranking.sort_values("abs_z_change_from_previous_year", ascending=False)
        .drop_duplicates(["country_code", "event_year", "indicator_slug"])
        .sort_values("abs_z_change_from_previous_year", ascending=False)
    )
    context.to_csv(ANNUAL_CONTEXT_RANKING_PATH, index=False)

    return ranking


if __name__ == "__main__":
    short_term = build_short_term_rankings()
    annual = build_annual_rankings()

    print(f"Ranking curto prazo: {len(short_term)} linhas")
    print(f"Ranking anual: {len(annual)} linhas")
    print(f"Salvo em: {SHORT_TERM_RANKING_PATH}")
    print(f"Salvo em: {ANNUAL_RANKING_PATH}")
    print(f"Contexto anual salvo em: {ANNUAL_CONTEXT_RANKING_PATH}")
