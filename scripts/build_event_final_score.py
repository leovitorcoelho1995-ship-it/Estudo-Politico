from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

EVENTS_PATH = PROCESSED_DIR / "political_events_processed.csv"
IMPACT_PATH = PROCESSED_DIR / "event_economic_impact_normalized.csv"
ROBUSTNESS_PATH = PROCESSED_DIR / "event_economic_impact_robustness.csv"
SIGNIFICANCE_PATH = PROCESSED_DIR / "event_economic_impact_significance.csv"
PERSISTENCE_PATH = PROCESSED_DIR / "event_shock_persistence.csv"
CONTAMINATION_PATH = PROCESSED_DIR / "event_window_contamination.csv"
TRENDS_ALIGNMENT_PATH = PROCESSED_DIR / "trends_event_alignment.csv"

OUTPUT_PATH = PROCESSED_DIR / "event_final_score.csv"
SUMMARY_PATH = PROCESSED_DIR / "event_final_score_summary.csv"
CONFIG_PATH = PROCESSED_DIR / "event_final_score_config.csv"
SCORE_VERSION = "score_v1_1_trends_partial"

WEIGHTS = {
    "impact_score": 0.35,
    "robustness_score": 0.25,
    "significance_score": 0.15,
    "persistence_score": 0.15,
    "trends_score": 0.05,
    "contamination_penalty": -0.05,
}

PERSISTENCE_SCORE = {
    "persistiu": 100,
    "decaiu lentamente": 70,
    "reverteu rapido": 40,
    "sem choque relevante": 0,
    "insuficiente": 0,
}

CONTAMINATION_PENALTY = {
    "alta": 100,
    "moderada": 50,
    "baixa": 0,
}


def clip_0_100(value: float | int | None) -> float:
    if value is None or pd.isna(value):
        return 0.0
    return float(max(0.0, min(100.0, value)))


def score_significance(p_value_fdr: float | None) -> float:
    if p_value_fdr is None or pd.isna(p_value_fdr) or p_value_fdr <= 0:
        return 0.0 if p_value_fdr is None or pd.isna(p_value_fdr) else 100.0
    if p_value_fdr >= 0.10:
        return 0.0
    if p_value_fdr <= 0.001:
        return 100.0
    return clip_0_100((0.10 - p_value_fdr) / 0.099 * 100)


def score_tier(value: float) -> str:
    if value >= 80:
        return "muito alto"
    if value >= 65:
        return "alto"
    if value >= 45:
        return "medio"
    return "baixo"


def score_caveat(row: pd.Series) -> str:
    notes: list[str] = []
    if row.get("contamination_level_90d") == "alta":
        notes.append("cluster de eventos proximos")
    elif row.get("contamination_level_90d") == "moderada":
        notes.append("janela com contaminacao moderada")
    if not bool(row.get("has_trends_data")):
        notes.append("sem Trends coletado")
    if row.get("date_precision") in {"month", "year", "year_range"}:
        notes.append(f"data com precisao {row.get('date_precision')}")
    return "; ".join(notes) if notes else "sem alerta principal"


def build_event_final_score() -> pd.DataFrame:
    events = pd.read_csv(EVENTS_PATH)
    impact = pd.read_csv(IMPACT_PATH)
    robustness = pd.read_csv(ROBUSTNESS_PATH)
    significance = pd.read_csv(SIGNIFICANCE_PATH)
    persistence = pd.read_csv(PERSISTENCE_PATH)
    contamination = pd.read_csv(CONTAMINATION_PATH)
    trends = pd.read_csv(TRENDS_ALIGNMENT_PATH) if TRENDS_ALIGNMENT_PATH.exists() else pd.DataFrame()

    impact["abs_standardized_change"] = pd.to_numeric(impact["abs_standardized_change"], errors="coerce")
    robustness["historical_percentile"] = pd.to_numeric(robustness["historical_percentile"], errors="coerce")
    significance["p_value_fdr"] = pd.to_numeric(significance["p_value_fdr"], errors="coerce")
    persistence["peak_abs_z_after"] = pd.to_numeric(persistence["peak_abs_z_after"], errors="coerce")

    event_base = events[
        [
            "event_id",
            "country_code",
            "country_name",
            "start_date",
            "end_date",
            "date_precision",
            "event_name",
            "event_category",
            "event_subcategory",
        ]
    ].copy()

    impact_best = (
        impact.sort_values("abs_standardized_change", ascending=False)
        .drop_duplicates("event_id")
        .rename(
            columns={
                "indicator_slug": "top_impact_indicator",
                "window_days": "top_impact_window_days",
                "abs_standardized_change": "top_abs_standardized_change",
            }
        )[["event_id", "top_impact_indicator", "top_impact_window_days", "top_abs_standardized_change"]]
    )
    impact_best["impact_score"] = impact_best["top_abs_standardized_change"].map(
        lambda value: clip_0_100((value / 3.0) * 100)
    )

    robustness_best = (
        robustness.sort_values("historical_percentile", ascending=False)
        .drop_duplicates("event_id")
        .rename(
            columns={
                "historical_percentile": "top_historical_percentile",
                "rarity_label": "top_rarity_label",
            }
        )[["event_id", "top_historical_percentile", "top_rarity_label"]]
    )
    robustness_best["robustness_score"] = robustness_best["top_historical_percentile"].map(clip_0_100)

    significance_best = (
        significance.sort_values("p_value_fdr", ascending=True)
        .drop_duplicates("event_id")
        .rename(
            columns={
                "p_value_fdr": "best_p_value_fdr",
                "significance_label": "best_significance_label",
            }
        )[["event_id", "best_p_value_fdr", "best_significance_label"]]
    )
    significance_best["significance_score"] = significance_best["best_p_value_fdr"].map(score_significance)

    persistence_best = (
        persistence.sort_values("peak_abs_z_after", ascending=False)
        .drop_duplicates("event_id")
        .rename(
            columns={
                "peak_abs_z_after": "top_peak_abs_z_after",
                "persistence_label": "top_persistence_label",
                "days_to_peak": "top_days_to_peak",
                "days_until_normal_range": "top_days_until_normal_range",
            }
        )[
            [
                "event_id",
                "top_peak_abs_z_after",
                "top_persistence_label",
                "top_days_to_peak",
                "top_days_until_normal_range",
            ]
        ]
    )
    persistence_best["persistence_score"] = persistence_best["top_persistence_label"].map(PERSISTENCE_SCORE).fillna(0)

    contamination_90 = contamination[contamination["window_days"] == 90].copy()
    contamination_90 = contamination_90.rename(
        columns={
            "nearby_event_count": "nearby_events_90d",
            "contamination_level": "contamination_level_90d",
        }
    )[["event_id", "nearby_events_90d", "contamination_level_90d"]]
    contamination_90["contamination_penalty"] = (
        contamination_90["contamination_level_90d"].map(CONTAMINATION_PENALTY).fillna(0)
    )

    if trends.empty:
        trends_best = pd.DataFrame(
            columns=[
                "event_id",
                "top_trends_peak_z",
                "top_trends_term",
                "trends_score",
                "has_trends_data",
                "trends_score_note",
            ]
        )
    else:
        trends["peak_z_score"] = pd.to_numeric(trends["peak_z_score"], errors="coerce")
        trends_best = (
            trends.sort_values("peak_z_score", ascending=False)
            .drop_duplicates("event_id")
            .rename(columns={"peak_z_score": "top_trends_peak_z", "term": "top_trends_term"})[
                ["event_id", "top_trends_peak_z", "top_trends_term"]
            ]
        )
        trends_best["trends_score"] = trends_best["top_trends_peak_z"].map(lambda value: clip_0_100((value / 6.0) * 100))
        trends_best["has_trends_data"] = True
        trends_best["trends_score_note"] = "collected"

    score = event_base
    for frame in [
        impact_best,
        robustness_best,
        significance_best,
        persistence_best,
        contamination_90,
        trends_best,
    ]:
        score = score.merge(frame, on="event_id", how="left")

    for column in ["impact_score", "robustness_score", "significance_score", "persistence_score", "trends_score", "contamination_penalty"]:
        score[column] = pd.to_numeric(score[column], errors="coerce").fillna(0)
    score["has_trends_data"] = score["has_trends_data"].fillna(False).astype(bool)
    score["trends_score_note"] = score["trends_score_note"].fillna(
        "missing_collection_zeroed_low_weight"
    )

    score["final_score"] = sum(score[column] * weight for column, weight in WEIGHTS.items())
    score["final_score"] = score["final_score"].map(clip_0_100)
    score["score_version"] = SCORE_VERSION
    score["score_tier"] = score["final_score"].map(score_tier)
    score["score_caveat"] = score.apply(score_caveat, axis=1)
    score["score_note"] = score.apply(
        lambda row: (
            f"impacto {row['impact_score']:.0f}, robustez {row['robustness_score']:.0f}, "
            f"significancia {row['significance_score']:.0f}, persistencia {row['persistence_score']:.0f}, "
            f"trends {row['trends_score']:.0f}, penalidade {row['contamination_penalty']:.0f}"
        ),
        axis=1,
    )

    score = score.sort_values(
        ["final_score", "start_date", "country_code", "event_id"],
        ascending=[False, True, True, True],
    ).reset_index(drop=True)
    score["score_rank_global"] = score.index + 1
    score["score_rank_country"] = (
        score.groupby("country_code", group_keys=False)
        .apply(lambda frame: pd.Series(range(1, len(frame) + 1), index=frame.index))
        .astype(int)
    )
    score = score.sort_values(["score_rank_global"])
    score.to_csv(OUTPUT_PATH, index=False)

    summary = (
        score.groupby(["country_code", "event_category"], as_index=False)
        .agg(
            events=("event_id", "size"),
            mean_score=("final_score", "mean"),
            median_score=("final_score", "median"),
            max_score=("final_score", "max"),
        )
        .sort_values(["country_code", "max_score"], ascending=[True, False])
    )
    summary.to_csv(SUMMARY_PATH, index=False)

    config = pd.DataFrame(
        [
            {
                "score_version": SCORE_VERSION,
                "component": component,
                "weight": weight,
                "note": (
                    "negative weight means penalty"
                    if weight < 0
                    else "positive contribution"
                ),
            }
            for component, weight in WEIGHTS.items()
        ]
    )
    config.to_csv(CONFIG_PATH, index=False)
    return score


if __name__ == "__main__":
    result = build_event_final_score()
    print(f"Eventos com score: {len(result)}")
    print(result.groupby("country_code")["event_id"].count().to_string())
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
    print(f"Resumo salvo em: {SUMMARY_PATH}")
    print(f"Config salvo em: {CONFIG_PATH}")
