from __future__ import annotations

from math import erfc, sqrt
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

IMPACT_PATH = PROCESSED_DIR / "event_economic_impact_normalized.csv"
INDICATORS_PATH = PROCESSED_DIR / "economic_indicators_unified.csv"
OUTPUT_PATH = PROCESSED_DIR / "event_economic_impact_significance.csv"
SUMMARY_PATH = PROCESSED_DIR / "event_economic_impact_significance_summary.csv"

MIN_OBSERVATIONS_PER_SIDE = 3


def two_sided_normal_p_value(z_value: float | None) -> float | None:
    if z_value is None or pd.isna(z_value):
        return None
    return erfc(abs(float(z_value)) / sqrt(2))


def benjamini_hochberg(p_values: pd.Series) -> pd.Series:
    result = pd.Series(pd.NA, index=p_values.index, dtype="Float64")
    valid = pd.to_numeric(p_values, errors="coerce").dropna().sort_values()
    n_tests = len(valid)
    if n_tests == 0:
        return result

    adjusted = valid * n_tests / pd.Series(range(1, n_tests + 1), index=valid.index)
    adjusted = adjusted.iloc[::-1].cummin().iloc[::-1].clip(upper=1)
    result.loc[adjusted.index] = adjusted
    return result


def significance_label(p_value_fdr: float | None) -> str:
    if p_value_fdr is None or pd.isna(p_value_fdr):
        return "insuficiente"
    if p_value_fdr < 0.01:
        return "forte"
    if p_value_fdr < 0.05:
        return "moderada"
    if p_value_fdr < 0.10:
        return "fraca"
    return "nao significativa"


def summarize_test(row: pd.Series, indicators: pd.DataFrame) -> dict[str, object]:
    series = indicators[
        (indicators["country_code"] == row["country_code"])
        & (indicators["indicator_slug"] == row["indicator_slug"])
        & (indicators["source"] == row["indicator_source"])
    ].copy()

    before = series[
        (series["date"] >= row["before_start"]) & (series["date"] <= row["before_end"])
    ]["value"].dropna()
    after = series[
        (series["date"] >= row["after_start"]) & (series["date"] <= row["after_end"])
    ]["value"].dropna()

    before_n = len(before)
    after_n = len(after)
    result = row.to_dict()
    result.update(
        {
            "test_name": "welch_approx_normal",
            "test_note": "Welch aproximado com p-value normal; usar SciPy para t-distribution exata em versao academica.",
            "before_test_observations": before_n,
            "after_test_observations": after_n,
            "before_std": before.std(ddof=1) if before_n > 1 else pd.NA,
            "after_std": after.std(ddof=1) if after_n > 1 else pd.NA,
            "mean_difference": pd.NA,
            "standard_error": pd.NA,
            "test_statistic": pd.NA,
            "p_value": pd.NA,
            "ci95_low": pd.NA,
            "ci95_high": pd.NA,
        }
    )

    if before_n < MIN_OBSERVATIONS_PER_SIDE or after_n < MIN_OBSERVATIONS_PER_SIDE:
        return result

    before_mean = before.mean()
    after_mean = after.mean()
    before_var = before.var(ddof=1)
    after_var = after.var(ddof=1)
    standard_error = sqrt((before_var / before_n) + (after_var / after_n))
    mean_difference = after_mean - before_mean

    if standard_error == 0 or pd.isna(standard_error):
        return result

    test_statistic = mean_difference / standard_error
    p_value = two_sided_normal_p_value(test_statistic)
    ci_margin = 1.96 * standard_error

    result.update(
        {
            "mean_difference": mean_difference,
            "standard_error": standard_error,
            "test_statistic": test_statistic,
            "p_value": p_value,
            "ci95_low": mean_difference - ci_margin,
            "ci95_high": mean_difference + ci_margin,
        }
    )
    return result


def build_event_statistical_tests() -> pd.DataFrame:
    impact = pd.read_csv(IMPACT_PATH)
    indicators = pd.read_csv(INDICATORS_PATH)

    for column in ["event_anchor_date", "before_start", "before_end", "after_start", "after_end"]:
        impact[column] = pd.to_datetime(impact[column], errors="coerce")
    indicators["date"] = pd.to_datetime(indicators["date"], errors="coerce")
    indicators["value"] = pd.to_numeric(indicators["value"], errors="coerce")
    indicators = indicators.dropna(subset=["date", "value"]).copy()

    rows = [summarize_test(row, indicators) for _, row in impact.iterrows()]
    result = pd.DataFrame(rows)
    if result.empty:
        raise ValueError("Nenhum teste estatistico foi gerado.")

    result["p_value"] = pd.to_numeric(result["p_value"], errors="coerce")
    result["fdr_family"] = (
        result["country_code"].astype(str)
        + "|"
        + result["indicator_slug"].astype(str)
        + "|"
        + result["window_days"].astype(str)
    )
    result["p_value_fdr"] = (
        result.groupby("fdr_family", group_keys=False)["p_value"].apply(benjamini_hochberg)
    )
    result["significance_label"] = result["p_value_fdr"].map(significance_label)
    result["is_significant_05"] = result["p_value_fdr"] < 0.05

    result = result.sort_values(
        ["country_code", "event_anchor_date", "event_id", "indicator_slug", "window_days"]
    )
    result.to_csv(OUTPUT_PATH, index=False)

    summary = (
        result.groupby(["country_code", "window_days", "significance_label"], as_index=False)
        .agg(
            rows=("event_id", "size"),
            events=("event_id", "nunique"),
            median_p_value_fdr=("p_value_fdr", "median"),
            significant_05=("is_significant_05", "sum"),
        )
        .sort_values(["country_code", "window_days", "significance_label"])
    )
    summary.to_csv(SUMMARY_PATH, index=False)

    return result


if __name__ == "__main__":
    output = build_event_statistical_tests()
    print(f"Linhas com testes estatisticos: {len(output)}")
    print(output.groupby("significance_label").size().to_string())
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
    print(f"Resumo salvo em: {SUMMARY_PATH}")
