from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"

EVENTS_PATH = PROCESSED_DIR / "political_events_processed.csv"
INDICATORS_PATH = PROCESSED_DIR / "economic_indicators_normalized.csv"
SHORT_IMPACT_PATH = PROCESSED_DIR / "event_economic_impact_normalized.csv"
ANNUAL_IMPACT_PATH = PROCESSED_DIR / "annual_event_impact.csv"

INDICATOR_COVERAGE_PATH = PROCESSED_DIR / "audit_indicator_coverage.csv"
EVENT_COVERAGE_PATH = PROCESSED_DIR / "audit_event_coverage.csv"
GAP_SUMMARY_PATH = PROCESSED_DIR / "audit_gap_summary.csv"
MARKDOWN_REPORT_PATH = REPORTS_DIR / "project_audit.md"


def build_indicator_coverage(indicators: pd.DataFrame) -> pd.DataFrame:
    indicators["date"] = pd.to_datetime(indicators["date"])
    coverage = (
        indicators.groupby(
            ["country_code", "country_name", "source", "frequency", "indicator_group", "indicator_slug"],
            as_index=False,
        )
        .agg(
            rows=("value", "size"),
            start_date=("date", "min"),
            end_date=("date", "max"),
            missing_values=("value", lambda values: values.isna().sum()),
        )
        .sort_values(["country_code", "source", "frequency", "indicator_group", "indicator_slug"])
    )
    return coverage


def build_event_coverage(
    events: pd.DataFrame,
    short_impact: pd.DataFrame,
    annual_impact: pd.DataFrame,
) -> pd.DataFrame:
    short_event_ids = set(short_impact["event_id"])
    annual_event_ids = set(annual_impact["event_id"])

    coverage = events.copy()
    coverage["has_short_term_impact"] = coverage["event_id"].isin(short_event_ids)
    coverage["has_annual_impact"] = coverage["event_id"].isin(annual_event_ids)
    coverage["coverage_status"] = "annual_only"
    coverage.loc[coverage["has_short_term_impact"], "coverage_status"] = "short_and_annual"
    coverage.loc[
        ~coverage["has_short_term_impact"] & ~coverage["has_annual_impact"],
        "coverage_status",
    ] = "not_covered"

    return coverage[
        [
            "event_id",
            "country_code",
            "country_name",
            "event_name",
            "date_precision",
            "event_category",
            "event_subcategory",
            "has_short_term_impact",
            "has_annual_impact",
            "coverage_status",
        ]
    ].sort_values(["country_code", "coverage_status", "event_name"])


def build_gap_summary(indicators: pd.DataFrame, event_coverage: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    countries = sorted(event_coverage["country_code"].unique())
    for country in countries:
        country_indicators = indicators[indicators["country_code"] == country]
        country_events = event_coverage[event_coverage["country_code"] == country]
        frequent_indicators = country_indicators[
            country_indicators["frequency"].isin(["daily", "weekly", "monthly", "quarterly"])
        ]["indicator_slug"].nunique()

        short_events = int(country_events["has_short_term_impact"].sum())
        total_events = len(country_events)
        annual_events = int(country_events["has_annual_impact"].sum())

        if frequent_indicators == 0:
            priority_gap = "sem indicadores frequentes"
        elif short_events < total_events:
            priority_gap = "eventos longos ou sem janela curta"
        else:
            priority_gap = "cobertura curta adequada"

        rows.append(
            {
                "country_code": country,
                "total_events": total_events,
                "short_term_events": short_events,
                "annual_events": annual_events,
                "frequent_indicators": frequent_indicators,
                "annual_indicators": country_indicators[country_indicators["frequency"] == "annual"][
                    "indicator_slug"
                ].nunique(),
                "priority_gap": priority_gap,
            }
        )

    rows.extend(
        [
            {
                "country_code": "PROJECT",
                "total_events": int(len(event_coverage)),
                "short_term_events": int(event_coverage["has_short_term_impact"].sum()),
                "annual_events": int(event_coverage["has_annual_impact"].sum()),
                "frequent_indicators": int(
                    indicators[indicators["frequency"].isin(["daily", "weekly", "monthly", "quarterly"])][
                        ["country_code", "indicator_slug"]
                    ].drop_duplicates().shape[0]
                ),
                "annual_indicators": int(
                    indicators[indicators["frequency"] == "annual"][["country_code", "indicator_slug"]]
                    .drop_duplicates()
                    .shape[0]
                ),
                "priority_gap": "Google Trends parcial; fontes verificadas no top 15 e contextuais no restante",
            }
        ]
    )

    return pd.DataFrame(rows)


def write_markdown_report(
    indicator_coverage: pd.DataFrame,
    event_coverage: pd.DataFrame,
    gap_summary: pd.DataFrame,
) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    def markdown_table(frame: pd.DataFrame) -> str:
        text_frame = frame.fillna("").astype(str)
        header = "| " + " | ".join(text_frame.columns) + " |"
        separator = "| " + " | ".join(["---"] * len(text_frame.columns)) + " |"
        rows = [
            "| " + " | ".join(row) + " |"
            for row in text_frame.to_numpy().tolist()
        ]
        return "\n".join([header, separator, *rows])

    uncovered_short = event_coverage[~event_coverage["has_short_term_impact"]]
    indicator_frequency_summary = (
        indicator_coverage.groupby(["country_code", "frequency"], as_index=False)
        .agg(indicators=("indicator_slug", "nunique"), rows=("rows", "sum"))
    )
    lines = [
        "# Auditoria do projeto",
        "",
        "## Resumo de lacunas",
        "",
        markdown_table(gap_summary),
        "",
        "## Eventos sem cobertura de curto prazo",
        "",
        markdown_table(
            uncovered_short[
                ["country_code", "event_name", "date_precision", "coverage_status"]
            ]
        ),
        "",
        "## Cobertura de indicadores por pais e frequencia",
        "",
        markdown_table(indicator_frequency_summary),
        "",
    ]

    MARKDOWN_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def build_audit() -> None:
    events = pd.read_csv(EVENTS_PATH)
    indicators = pd.read_csv(INDICATORS_PATH)
    short_impact = pd.read_csv(SHORT_IMPACT_PATH)
    annual_impact = pd.read_csv(ANNUAL_IMPACT_PATH)

    indicator_coverage = build_indicator_coverage(indicators)
    event_coverage = build_event_coverage(events, short_impact, annual_impact)
    gap_summary = build_gap_summary(indicators, event_coverage)

    indicator_coverage.to_csv(INDICATOR_COVERAGE_PATH, index=False, date_format="%Y-%m-%d")
    event_coverage.to_csv(EVENT_COVERAGE_PATH, index=False)
    gap_summary.to_csv(GAP_SUMMARY_PATH, index=False)
    write_markdown_report(indicator_coverage, event_coverage, gap_summary)

    print(f"Indicadores auditados: {len(indicator_coverage)} linhas")
    print(f"Eventos auditados: {len(event_coverage)} linhas")
    print(f"Resumo salvo em: {GAP_SUMMARY_PATH}")
    print(f"Relatorio salvo em: {MARKDOWN_REPORT_PATH}")


if __name__ == "__main__":
    build_audit()
