from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"

SHORT_RANKING_PATH = PROCESSED_DIR / "ranking_short_term_impacts.csv"
ANNUAL_CONTEXT_PATH = PROCESSED_DIR / "ranking_annual_context_by_country_year.csv"
NORMALIZED_INDICATORS_PATH = PROCESSED_DIR / "economic_indicators_normalized.csv"


def write_html(fig, filename: str) -> Path:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / filename
    fig.write_html(path, include_plotlyjs="cdn", full_html=True)
    return path


def build_short_term_ranking_chart() -> Path:
    df = pd.read_csv(SHORT_RANKING_PATH)
    top = df.sort_values("abs_standardized_change", ascending=False).head(25).copy()
    top["label"] = (
        top["country_code"]
        + " | "
        + top["event_name"]
        + " | "
        + top["indicator_slug"]
        + " | "
        + top["window_days"].astype(str)
        + "d"
    )
    top = top.sort_values("abs_standardized_change")

    fig = px.bar(
        top,
        x="abs_standardized_change",
        y="label",
        color="country_code",
        orientation="h",
        hover_data=[
            "event_category",
            "indicator_name",
            "before_mean",
            "after_mean",
            "absolute_change",
            "standardized_change",
        ],
        title="Top 25 impactos economicos de curto prazo",
        labels={
            "abs_standardized_change": "Choque padronizado absoluto",
            "label": "",
            "country_code": "Pais",
        },
    )
    fig.update_layout(height=820, margin=dict(l=260, r=40, t=70, b=50))
    return write_html(fig, "short_term_impact_ranking.html")


def build_annual_context_chart() -> Path:
    df = pd.read_csv(ANNUAL_CONTEXT_PATH)
    top = df.sort_values("abs_z_change_from_previous_year", ascending=False).head(25).copy()
    top["label"] = (
        top["country_code"]
        + " | "
        + top["event_year"].astype(str)
        + " | "
        + top["indicator_slug"]
    )
    top = top.sort_values("abs_z_change_from_previous_year")

    fig = px.bar(
        top,
        x="abs_z_change_from_previous_year",
        y="label",
        color="country_code",
        orientation="h",
        hover_data=[
            "event_name",
            "event_category",
            "previous_year_value",
            "event_year_value",
            "change_from_previous_year",
            "z_change_from_previous_year",
        ],
        title="Top 25 contextos macro anuais mais extremos",
        labels={
            "abs_z_change_from_previous_year": "Mudanca anual padronizada absoluta",
            "label": "",
            "country_code": "Pais",
        },
    )
    fig.update_layout(height=820, margin=dict(l=260, r=40, t=70, b=50))
    return write_html(fig, "annual_context_ranking.html")


def build_normalized_trajectory_chart() -> Path:
    df = pd.read_csv(NORMALIZED_INDICATORS_PATH)
    df["date"] = pd.to_datetime(df["date"])

    selected = df[
        (df["source"] == "World Bank API")
        & (df["indicator_slug"].isin(["inflation_annual_pct", "unemployment_pct", "gdp_growth_annual_pct"]))
    ].copy()

    fig = px.line(
        selected,
        x="date",
        y="z_score",
        color="country_code",
        facet_row="indicator_slug",
        markers=True,
        hover_data=["value", "indicator_name", "unit"],
        title="Trajetorias anuais normalizadas por pais (World Bank)",
        labels={
            "date": "Ano",
            "z_score": "Z-score dentro do proprio pais/indicador",
            "country_code": "Pais",
            "indicator_slug": "Indicador",
        },
    )
    fig.update_yaxes(matches=None)
    fig.update_layout(height=900, margin=dict(l=80, r=40, t=80, b=50))
    return write_html(fig, "world_bank_normalized_trajectories.html")


def build_frequent_series_chart() -> Path:
    df = pd.read_csv(NORMALIZED_INDICATORS_PATH)
    df["date"] = pd.to_datetime(df["date"])

    selected = df[
        (
            (df["country_code"] == "BRA")
            & (df["indicator_slug"].isin(["cambio", "ipca", "selic", "gasolina"]))
        )
        | (
            (df["country_code"] == "USA")
            & (df["indicator_slug"].isin(["cpi", "fed_funds", "unemployment", "gasoline"]))
        )
        | (
            (df["country_code"] == "ARG")
            & (df["indicator_slug"].isin(["dolar_blue", "dolar_oficial"]))
        )
    ].copy()

    fig = px.line(
        selected,
        x="date",
        y="z_score",
        color="indicator_slug",
        facet_col="country_code",
        facet_col_spacing=0.08,
        hover_data=["value", "unit", "source"],
        title="Indicadores frequentes normalizados: Brasil, Estados Unidos e Argentina",
        labels={
            "date": "Data",
            "z_score": "Z-score",
            "indicator_slug": "Indicador",
            "country_code": "Pais",
        },
    )
    fig.update_yaxes(matches=None)
    fig.update_layout(height=650, margin=dict(l=70, r=40, t=80, b=50))
    return write_html(fig, "frequent_indicators_zscore.html")


def build_all() -> list[Path]:
    return [
        build_short_term_ranking_chart(),
        build_annual_context_chart(),
        build_normalized_trajectory_chart(),
        build_frequent_series_chart(),
    ]


if __name__ == "__main__":
    paths = build_all()
    print("Graficos gerados:")
    for path in paths:
        print(path)
