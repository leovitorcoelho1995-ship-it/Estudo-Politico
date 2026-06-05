# -*- coding: utf-8 -*-
from __future__ import annotations

import html
import textwrap
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
TRENDS_NORMALIZED_PATH = PROCESSED_DIR / "trends_normalized.csv"
TRENDS_ALIGNMENT_PATH = PROCESSED_DIR / "trends_event_alignment.csv"
ROBUSTNESS_PATH = PROCESSED_DIR / "event_economic_impact_robustness.csv"
SIGNIFICANCE_PATH = PROCESSED_DIR / "event_economic_impact_significance.csv"
CONTAMINATION_PATH = PROCESSED_DIR / "event_window_contamination.csv"
PERSISTENCE_PATH = PROCESSED_DIR / "event_shock_persistence.csv"
EVENT_STUDY_PATH = PROCESSED_DIR / "event_study_series.csv"
EVENT_STUDY_AGG_PATH = PROCESSED_DIR / "event_study_category_aggregates.csv"
FINAL_SCORE_PATH = PROCESSED_DIR / "event_final_score.csv"

REQUIRED_DATA_FILES = [
    "political_events_processed.csv",
    "economic_indicators_normalized.csv",
    "event_economic_impact_normalized.csv",
    "ranking_short_term_impacts.csv",
    "ranking_annual_impacts.csv",
    "ranking_annual_context_by_country_year.csv",
]

COUNTRY_LABELS = {
    "BRA": "Brasil",
    "USA": "Estados Unidos",
    "ARG": "Argentina",
}

WORLD_BANK_MAX_YEAR = 2024

COUNTRY_COLORS = {
    "BRA": "#0d7a5f",
    "USA": "#3867b7",
    "ARG": "#7b61a8",
}

COR_PRINCIPAL = "#0d7a5f"
COR_SECUNDARIA = "#4ade80"
COR_ACCENT = "#c0392b"
COR_MUTED = "#7a7570"
COR_INK = "#0c0c0d"
COR_PAPER = "#f5f2ed"
COR_CREAM = "#ede9e2"
COR_BORDER = "#d9d4cc"

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Syne, system-ui, sans-serif", color=COR_INK, size=13),
)

TICK_FONT = dict(family="DM Mono, monospace", size=12, color=COR_MUTED)
LABEL_FONT = dict(family="DM Mono, monospace", size=13, color=COR_MUTED)

INDICATOR_LABELS = {
    "cambio": "Dolar comercial",
    "dolar_blue": "Dolar blue",
    "dolar_oficial": "Dolar oficial",
    "gasolina": "Gasolina",
    "ipca": "Inflacao ao consumidor",
    "selic": "Juros basicos",
    "central_government_debt_pct_gdp": "Divida publica",
    "gdp_growth_annual_pct": "Crescimento do PIB",
    "gdp_per_capita_current_usd": "PIB por pessoa",
    "inflation_annual_pct": "Inflacao anual",
    "unemployment_pct": "Desemprego",
    "cpi": "Inflacao ao consumidor",
    "fed_funds": "Juros basicos",
    "unemployment": "Desemprego",
    "real_gdp": "PIB real",
}

CATEGORY_LABELS = {
    "politics": "Politica",
    "economy": "Economia",
    "external_shock": "Choque externo",
    "society": "Sociedade",
}

SUBCATEGORY_LABELS = {
    "institutional": "Institucional",
    "fiscal": "Politica fiscal",
    "labor_market": "Trabalho e emprego",
    "election_justice": "Eleicao e Justica",
    "election_crisis": "Eleicao e crise",
    "election": "Eleicao",
    "health_crisis": "Crise sanitaria",
    "political_crisis": "Crise politica",
    "energy_inflation": "Combustiveis e inflacao",
    "energy_fiscal": "Combustiveis e impostos",
    "institutional_crisis": "Crise institucional",
    "energy": "Energia e combustiveis",
    "macroeconomy": "Cenario macroeconomico",
    "trade": "Comercio exterior",
    "monetary_policy": "Juros e Banco Central",
    "fiscal_energy": "Fiscal e energia",
    "economic_policy": "Politica economica",
    "debt_exchange_rate": "Divida e cambio",
    "exchange_rate_inflation": "Cambio e inflacao",
    "debt": "Divida",
    "fiscal_social": "Fiscal e social",
    "social_reaction": "Reacao social",
}

FREQUENCY_LABELS = {
    "daily": "diaria",
    "weekly": "semanal",
    "monthly": "mensal",
    "quarterly": "trimestral",
    "annual": "anual",
}

DATE_PRECISION_LABELS = {
    "day": "Data exata",
    "month": "Mes aproximado",
    "year": "Ano",
    "year_range": "Periodo",
}


st.set_page_config(
    page_title="Atenção Política & Impacto Econômico",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&display=swap');
    :root {
        --paper: #f5f2ed;
        --cream: #ede9e2;
        --ink: #0c0c0d;
        --muted: #7a7570;
        --line: #d9d4cc;
        --green: #0d7a5f;
        --green-soft: rgba(13,122,95,.1);
        --red: #c0392b;
        --code: #fbfaf7;
        --mono: 'DM Mono', monospace;
        --serif: 'DM Serif Display', Georgia, serif;
        --sans: 'Syne', system-ui, sans-serif;
    }
    html, body, [class*="css"] {
        font-family: var(--sans) !important;
        color: var(--ink) !important;
        font-weight: 500;
    }
    .stApp {
        background: var(--paper);
        color: var(--ink);
    }
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 95% !important;
    }
    section[data-testid="stSidebar"] {
        background: #ede9e2;
        border-right: 1px solid var(--line);
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    section[data-testid="stSidebar"] h3 {
        font-family: var(--mono) !important;
        color: var(--muted) !important;
        font-size: .72rem !important;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: .45rem !important;
    }
    .sidebar-brand {
        border-bottom: 1px solid var(--line);
        margin-bottom: 1.1rem;
        padding-bottom: 1rem;
    }
    .sidebar-title {
        font-family: var(--serif);
        color: var(--ink);
        font-size: 1.45rem;
        line-height: 1.05;
    }
    .sidebar-subtitle {
        color: var(--muted);
        font-family: var(--mono);
        font-size: .68rem;
        margin-top: .45rem;
        text-transform: uppercase;
        letter-spacing: .06em;
    }
    .sidebar-note {
        color: #5f5a55;
        font-size: .82rem;
        line-height: 1.55;
        margin: .8rem 0 1rem 0;
    }
    h1, h2, h3 {
        letter-spacing: 0;
    }
    h1 {
        font-family: var(--serif) !important;
        font-size: clamp(2.7rem, 6vw, 4.8rem) !important;
        line-height: 1.05 !important;
        font-weight: 400 !important;
        margin-bottom: .65rem !important;
    }
    h2 {
        font-family: var(--serif) !important;
        font-size: clamp(1.75rem, 3vw, 2.35rem) !important;
        font-weight: 400 !important;
        border-top: 1px solid var(--line);
        padding-top: 1.2rem;
        margin-top: 2.1rem;
    }
    h3 {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }
    p, li, .stMarkdown {
        line-height: 1.7;
    }
    .hero-block {
        padding: 2.5rem 0 1.7rem 0;
        border-bottom: 1px solid var(--line);
        margin-bottom: 1.7rem;
    }
    .hero-eyebrow {
        font-family: var(--mono);
        font-size: .78rem;
        color: var(--muted);
        letter-spacing: .1em;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: .6rem;
        margin-bottom: 1rem;
    }
    .hero-eyebrow::before {
        content: '';
        display: inline-block;
        width: 24px;
        height: 1px;
        background: var(--green);
    }
    .hero-title {
        font-family: var(--serif);
        font-size: clamp(2.7rem, 6vw, 4.8rem);
        line-height: 1.05;
        color: var(--ink);
    }
    .hero-title em {
        color: var(--green);
        font-style: italic;
    }
    .hero-lead {
        color: #5f5a55;
        font-size: 1.12rem;
        max-width: 820px;
        line-height: 1.85;
        margin-top: .65rem;
    }
    .subtitle {
        color: var(--muted);
        font-size: 0.9rem;
        margin-bottom: 0.7rem;
    }
    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
        margin: 0.35rem 0 1rem 0;
    }
    .pill {
        border: 1px solid var(--line);
        border-radius: 4px;
        padding: 0.12rem 0.45rem;
        color: #4c4942;
        background: #ede8df;
        font-size: 0.72rem;
        font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
    }
    .top-filter-intro {
        border-top: 1px solid var(--line);
        padding-top: .95rem;
        margin: 1.15rem 0 .55rem 0;
    }
    .top-filter-kicker {
        font-family: var(--mono);
        color: var(--muted);
        font-size: .68rem;
        text-transform: uppercase;
        letter-spacing: .08em;
        margin-bottom: .2rem;
    }
    .top-filter-title {
        color: var(--ink);
        font-family: var(--serif);
        font-size: 1.35rem;
        line-height: 1.1;
    }
    .top-filter-copy {
        color: #5f5a55;
        font-size: .86rem;
        line-height: 1.55;
        max-width: 720px;
        margin-top: .35rem;
    }
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: .75rem;
        margin: 1.2rem 0 1.5rem 0;
    }
    .kpi-card {
        background: var(--cream);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1rem 1.15rem;
    }
    .kpi-val {
        font-family: var(--serif);
        font-size: 2.25rem;
        line-height: 1;
        color: var(--ink);
    }
    .kpi-label {
        font-family: var(--mono);
        font-size: .72rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: .07em;
        margin-top: .3rem;
    }
    .section-header {
        display: flex;
        align-items: baseline;
        gap: .75rem;
        margin: 2.3rem 0 1rem 0;
        padding-bottom: .75rem;
        border-bottom: 1px solid var(--line);
    }
    .section-num {
        font-family: var(--mono);
        font-size: .78rem;
        color: var(--muted);
        letter-spacing: .08em;
    }
    .section-title {
        font-family: var(--serif);
        font-size: clamp(1.7rem, 3vw, 2.3rem);
        color: var(--ink);
    }
    .section-title em {
        color: var(--green);
        font-style: italic;
    }
    .metric-note {
        color: var(--muted);
        font-size: 0.78rem;
    }
    .story-callout {
        border-left: 3px solid var(--green);
        border-radius: 0 6px 6px 0;
        padding: 1rem 1.2rem;
        margin: 1rem 0 1.2rem 0;
        color: #3b3933;
        background: var(--cream);
        font-size: 1.03rem;
        line-height: 1.75;
    }
    .insight-list {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: .75rem;
        margin: 1rem 0 1.4rem 0;
    }
    .insight-item {
        background: var(--cream);
        border: 1px solid var(--line);
        border-radius: 6px;
        padding: .9rem 1rem;
        color: var(--ink);
        line-height: 1.6;
    }
    .insight-kicker {
        font-family: var(--mono);
        font-size: .68rem;
        color: var(--green);
        text-transform: uppercase;
        letter-spacing: .07em;
        margin-bottom: .35rem;
    }
    .insight-text {
        font-size: .96rem;
    }
    .movement-panel {
        background: var(--cream);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1rem;
        min-height: 520px;
    }
    .movement-panel h3 {
        margin: .25rem 0 .2rem 0 !important;
        font-family: var(--serif) !important;
        font-size: 1.35rem !important;
        line-height: 1.18 !important;
        font-weight: 400 !important;
    }
    .movement-kicker,
    .movement-meta,
    .movement-direction {
        font-family: var(--mono);
        color: var(--muted);
        font-size: .68rem;
        text-transform: uppercase;
        letter-spacing: .06em;
    }
    .movement-rule {
        border-top: 1px solid var(--line);
        margin: .9rem 0;
    }
    .movement-card {
        background: #f8f5ef;
        border: 1px solid var(--line);
        border-left-width: 4px;
        border-radius: 6px;
        padding: .8rem;
        margin-top: .7rem;
    }
    .movement-card.up { border-left-color: var(--green); }
    .movement-card.down { border-left-color: var(--red); }
    .movement-card-top {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: .6rem;
        color: var(--ink);
        font-size: .88rem;
        line-height: 1.35;
    }
    .movement-card-top span {
        font-weight: 700;
    }
    .movement-card-top strong {
        flex: 0 0 auto;
        font-family: var(--mono);
        font-size: .76rem;
    }
    .movement-card.up strong { color: var(--green); }
    .movement-card.down strong { color: var(--red); }
    .movement-direction {
        margin-top: .28rem;
        text-transform: none;
        letter-spacing: 0;
    }
    .movement-bar {
        height: 6px;
        margin-top: .55rem;
        border-radius: 999px;
        background: var(--line);
        overflow: hidden;
    }
    .movement-bar div {
        height: 100%;
        border-radius: 999px;
        background: var(--green);
    }
    .movement-card.down .movement-bar div {
        background: var(--red);
    }
    .movement-empty {
        color: var(--muted);
        font-size: .88rem;
        line-height: 1.65;
        margin: .7rem 0 0 0;
    }
    .trend-summary-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: .75rem;
        margin: .85rem 0 1rem 0;
    }
    .trend-summary-card {
        border: 1px solid var(--line);
        border-radius: 6px;
        background: #f8f5ef;
        padding: .85rem .95rem;
    }
    .trend-summary-kicker {
        font-family: var(--mono);
        color: var(--muted);
        font-size: .66rem;
        text-transform: uppercase;
        letter-spacing: .07em;
        margin-bottom: .35rem;
    }
    .trend-summary-value {
        color: var(--ink);
        font-size: 1rem;
        font-weight: 700;
        line-height: 1.35;
    }
    .trend-summary-meta {
        color: #5f5a55;
        font-size: .78rem;
        line-height: 1.45;
        margin-top: .25rem;
    }
    div[data-testid="stMetric"] {
        background: transparent;
        border-top: 1px solid var(--line);
        padding-top: 0.4rem;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line);
    }
    pre {
        border: 1px solid var(--line) !important;
        background: var(--code) !important;
    }
    div[data-testid="stRadio"] label,
    div[data-testid="stMultiSelect"] label,
    div[data-testid="stSegmentedControl"] label {
        font-family: var(--mono);
        color: var(--muted);
        font-size: .78rem;
        text-transform: uppercase;
        letter-spacing: .06em;
    }
    div[role="radiogroup"] {
        gap: .45rem;
    }
    div[role="radiogroup"] label {
        background: var(--cream);
        border: 1px solid var(--line);
        border-radius: 6px;
        padding: .38rem .7rem;
        min-height: 2.1rem;
    }
    div[role="radiogroup"] label:has(input:checked) {
        background: var(--ink);
        border-color: var(--ink);
        color: var(--paper) !important;
    }
    div[role="radiogroup"] label:has(input:checked) p {
        color: var(--paper) !important;
    }
    .stDataFrame [role="gridcell"], .stDataFrame [role="columnheader"],
    .stDataFrame [role="gridcell"] div, .stDataFrame [role="columnheader"] div,
    .stDataFrame .gdg-cell, .stDataFrame .gdg-cell span {
        font-size: 15px !important;
        line-height: 1.5 !important;
    }
    .stDataFrame [role="columnheader"], .stDataFrame [role="columnheader"] div {
        color: #5f5a55 !important;
        font-weight: 700 !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    @media (max-width: 900px) {
        .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .insight-list { grid-template-columns: 1fr; }
        .trend-summary-grid { grid-template-columns: 1fr; }
        .stPlotlyChart {
            overflow-x: auto;
        }
        .stPlotlyChart > div {
            min-width: 680px;
        }
        div[data-testid="stDataFrame"] {
            overflow-x: auto;
        }
    }
    @media (max-width: 620px) {
        .block-container {
            padding-top: 1rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            max-width: 100% !important;
        }
        .kpi-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: .6rem !important;
        }
        h1 {
            font-size: 2.1rem !important;
        }
        h2 {
            font-size: 1.5rem !important;
        }
        .hero-title {
            font-size: 2.2rem !important;
            line-height: 1.02 !important;
        }
        .hero-lead {
            font-size: 0.92rem !important;
            line-height: 1.5 !important;
        }
        .hero-eyebrow {
            font-size: .64rem !important;
            line-height: 1.35 !important;
        }
        .pill-row {
            gap: .35rem !important;
        }
        .pill {
            font-size: .62rem !important;
            padding: .25rem .45rem !important;
        }
        .kpi-card {
            padding: 0.75rem 0.8rem !important;
        }
        .kpi-val {
            font-size: 1.55rem !important;
        }
        .kpi-label {
            font-size: .62rem !important;
        }
        .section-header {
            grid-template-columns: 2.1rem 1fr !important;
            gap: .6rem !important;
            margin-top: 1.35rem !important;
        }
        .section-num {
            font-size: .72rem !important;
        }
        .section-title {
            font-size: 1.45rem !important;
            line-height: 1.08 !important;
        }
        .story-callout,
        .metric-note {
            font-size: .86rem !important;
            line-height: 1.55 !important;
        }
        .insight-item {
            padding: .85rem !important;
        }
        div[data-testid="stHorizontalBlock"] {
            gap: .65rem !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            padding: .65rem !important;
        }
        div[role="radiogroup"] {
            gap: .35rem !important;
        }
        div[role="radiogroup"] label {
            min-height: 2.25rem !important;
            padding: .32rem .48rem !important;
        }
        div[role="radiogroup"] label p {
            font-size: .78rem !important;
            white-space: normal !important;
        }
        div[data-baseweb="tab-list"] {
            gap: .2rem !important;
            overflow-x: auto !important;
            flex-wrap: nowrap !important;
        }
        button[data-baseweb="tab"] {
            min-width: max-content !important;
            padding: .35rem .55rem !important;
        }
        button[data-baseweb="tab"] p {
            font-size: .78rem !important;
        }
        .stDataFrame [role="gridcell"], .stDataFrame [role="columnheader"],
        .stDataFrame [role="gridcell"] div, .stDataFrame [role="columnheader"] div,
        .stDataFrame .gdg-cell, .stDataFrame .gdg-cell span {
            font-size: 13px !important;
            line-height: 1.35 !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def data_signature() -> tuple[tuple[str, float | None], ...]:
    paths = [
        *(PROCESSED_DIR / file_name for file_name in REQUIRED_DATA_FILES),
        ROBUSTNESS_PATH,
        SIGNIFICANCE_PATH,
        CONTAMINATION_PATH,
        PERSISTENCE_PATH,
        EVENT_STUDY_PATH,
        EVENT_STUDY_AGG_PATH,
        FINAL_SCORE_PATH,
        TRENDS_NORMALIZED_PATH,
        TRENDS_ALIGNMENT_PATH,
    ]
    return tuple((path.name, path.stat().st_mtime if path.exists() else None) for path in paths)


def require_data_files() -> None:
    missing = [file_name for file_name in REQUIRED_DATA_FILES if not (PROCESSED_DIR / file_name).exists()]
    if not missing:
        return

    st.error("Base processada nao encontrada no deploy.")
    st.markdown(
        "O app precisa dos CSVs em `data/processed/`. Rode o pipeline localmente, versiona esses arquivos e faca novo deploy."
    )
    st.code("\n".join(f"data/processed/{file_name}" for file_name in missing), language="text")
    st.stop()


@st.cache_data(show_spinner=False)
def load_data(signature: tuple[tuple[str, float | None], ...] | None = None) -> dict[str, pd.DataFrame]:
    require_data_files()
    events = pd.read_csv(PROCESSED_DIR / "political_events_processed.csv")
    indicators = pd.read_csv(PROCESSED_DIR / "economic_indicators_normalized.csv")
    event_impact = pd.read_csv(PROCESSED_DIR / "event_economic_impact_normalized.csv")
    short_rank = pd.read_csv(PROCESSED_DIR / "ranking_short_term_impacts.csv")
    annual_rank = pd.read_csv(PROCESSED_DIR / "ranking_annual_impacts.csv")
    annual_context = pd.read_csv(PROCESSED_DIR / "ranking_annual_context_by_country_year.csv")
    robustness = pd.read_csv(ROBUSTNESS_PATH) if ROBUSTNESS_PATH.exists() else pd.DataFrame()
    significance = pd.read_csv(SIGNIFICANCE_PATH) if SIGNIFICANCE_PATH.exists() else pd.DataFrame()
    contamination = pd.read_csv(CONTAMINATION_PATH) if CONTAMINATION_PATH.exists() else pd.DataFrame()
    persistence = pd.read_csv(PERSISTENCE_PATH) if PERSISTENCE_PATH.exists() else pd.DataFrame()
    event_study = pd.read_csv(EVENT_STUDY_PATH) if EVENT_STUDY_PATH.exists() else pd.DataFrame()
    event_study_agg = pd.read_csv(EVENT_STUDY_AGG_PATH) if EVENT_STUDY_AGG_PATH.exists() else pd.DataFrame()
    final_score = pd.read_csv(FINAL_SCORE_PATH) if FINAL_SCORE_PATH.exists() else pd.DataFrame()
    trends = pd.read_csv(TRENDS_NORMALIZED_PATH) if TRENDS_NORMALIZED_PATH.exists() else pd.DataFrame()
    trends_alignment = (
        pd.read_csv(TRENDS_ALIGNMENT_PATH) if TRENDS_ALIGNMENT_PATH.exists() else pd.DataFrame()
    )

    for frame, columns in [
        (events, ["start_date", "end_date"]),
        (indicators, ["date"]),
        (event_impact, ["event_anchor_date", "before_start", "before_end", "after_start", "after_end"]),
        (short_rank, ["event_anchor_date"]),
        (robustness, ["event_anchor_date", "before_start", "before_end", "after_start", "after_end"]),
        (significance, ["event_anchor_date", "before_start", "before_end", "after_start", "after_end"]),
        (contamination, ["event_anchor_date"]),
        (persistence, ["event_anchor_date", "peak_date_after"]),
        (event_study, ["event_anchor_date", "date"]),
        (event_study_agg, []),
        (final_score, ["start_date", "end_date"]),
        (trends, ["date", "event_start_date", "event_end_date"]),
        (trends_alignment, ["event_start_date", "event_end_date", "peak_date"]),
    ]:
        for column in columns:
            if column in frame.columns:
                frame[column] = pd.to_datetime(frame[column])

    for frame in [events, event_impact, short_rank, annual_rank, annual_context, robustness, significance, contamination, persistence, event_study, event_study_agg, final_score]:
        if "date_precision" in frame.columns:
            frame["date_precision_label"] = frame["date_precision"].map(DATE_PRECISION_LABELS).fillna(
                frame["date_precision"]
            )
        if "event_date_precision" in frame.columns:
            frame["event_date_precision_label"] = frame["event_date_precision"].map(
                DATE_PRECISION_LABELS
            ).fillna(frame["event_date_precision"])
        if "event_category" in frame.columns:
            frame["event_category_label"] = frame["event_category"].map(CATEGORY_LABELS).fillna(
                frame["event_category"]
            )
        if "event_subcategory" in frame.columns:
            frame["event_subcategory_label"] = frame["event_subcategory"].map(SUBCATEGORY_LABELS).fillna(
                frame["event_subcategory"]
            )
        if "indicator_slug" in frame.columns:
            frame["indicator_label"] = frame["indicator_slug"].map(INDICATOR_LABELS).fillna(
                frame["indicator_slug"]
            )

    indicators["indicator_label"] = indicators["indicator_slug"].map(INDICATOR_LABELS).fillna(
        indicators["indicator_slug"]
    )
    indicators["frequency_label"] = indicators["frequency"].map(FREQUENCY_LABELS).fillna(
        indicators["frequency"]
    )

    return {
        "events": events,
        "indicators": indicators,
        "event_impact": event_impact,
        "short_rank": short_rank,
        "annual_rank": annual_rank,
        "annual_context": annual_context,
        "robustness": robustness,
        "significance": significance,
        "contamination": contamination,
        "persistence": persistence,
        "event_study": event_study,
        "event_study_agg": event_study_agg,
        "final_score": final_score,
        "trends": trends,
        "trends_alignment": trends_alignment,
    }


def technical_expander(title: str, explanation: str, code: str, enabled: bool) -> None:
    if not enabled:
        return
    with st.expander(title, expanded=False):
        st.write(explanation)
        st.code(code.strip(), language="python")


def learning_expander(title: str, what: str, why: str, replicate: str, code: str, enabled: bool) -> None:
    if not enabled:
        return
    with st.expander(f"{title}", expanded=True):
        st.markdown("**O que esta acontecendo aqui:**")
        st.write(what)
        st.markdown("**Por que essa decisao foi tomada:**")
        st.write(why)
        st.markdown("**Como replicar do zero:**")
        st.write(replicate)
        st.markdown("**Codigo Pandas / Plotly:**")
        st.code(code.strip(), language="python")


def plain_note(text: str) -> None:
    st.markdown(f'<div class="metric-note">{html.escape(text)}</div>', unsafe_allow_html=True)


def story_callout(text: str) -> None:
    st.markdown(f'<div class="story-callout">{html.escape(text)}</div>', unsafe_allow_html=True)


def coverage_note(scope: str = "geral") -> None:
    if scope == "annual":
        text = (
            f"Dados anuais do World Bank estao limitados a {WORLD_BANK_MAX_YEAR}, "
            "porque a publicacao internacional costuma ter defasagem de 1 a 2 anos."
        )
    else:
        text = (
            f"Cobertura: series frequentes de BCB, FRED e Bluelytics chegam ate 2026; "
            f"series anuais do World Bank entram ate {WORLD_BANK_MAX_YEAR} por defasagem de publicacao."
        )
    plain_note(text)


def detail_mode_note(technical_mode: bool, learning_mode: bool) -> None:
    if technical_mode:
        plain_note("Modo tecnico ativo: os paineis de detalhes tecnicos aparecem abaixo dos graficos.")
    elif learning_mode:
        plain_note("Meu aprendizado ativo: os blocos pedagogicos aparecem abertos ao longo da analise.")
    else:
        plain_note("Leitura simples ativa: a pagina prioriza narrativa e graficos, escondendo formulas e passos tecnicos.")


def insight_cards(items: list[tuple[str, str]]) -> None:
    cards = "".join(
        (
            '<div class="insight-item">'
            f'<div class="insight-kicker">{html.escape(title)}</div>'
            f'<div class="insight-text">{html.escape(body)}</div>'
            "</div>"
        )
        for title, body in items
    )
    st.markdown(f'<div class="insight-list">{cards}</div>', unsafe_allow_html=True)


def section_header(number: str, title: str, emphasis: str | None = None) -> None:
    if emphasis:
        title_html = title.replace(emphasis, f"<em>{emphasis}</em>", 1)
    else:
        title_html = title
    st.markdown(
        f"""
        <div class="section-header">
          <span class="section-num">{number}</span>
          <div class="section-title">{title_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_chart(fig, height: int, left_margin: int = 40):
    fig.update_layout(
        **CHART_LAYOUT,
        height=height,
        margin=dict(l=left_margin, r=30, t=25, b=40),
        legend_title_text="",
        hoverlabel=dict(
            bgcolor=COR_CREAM,
            bordercolor=COR_BORDER,
            font=dict(family="Syne, system-ui, sans-serif", color=COR_INK),
        ),
    )
    fig.update_xaxes(
        gridcolor=COR_BORDER,
        zerolinecolor=COR_BORDER,
        tickfont=TICK_FONT,
        title_font=LABEL_FONT,
    )
    fig.update_yaxes(
        gridcolor=COR_BORDER,
        zerolinecolor=COR_BORDER,
        tickfont=TICK_FONT,
        title_font=LABEL_FONT,
        automargin=True,
    )
    return fig


def add_event_overlays(fig, events: pd.DataFrame, selected_event: pd.Series, show_all_events: bool) -> None:
    selected_event_id = selected_event.get("event_id", selected_event.name)
    if show_all_events:
        for _, event in events.iterrows():
            start = event["start_date"]
            end = event["end_date"]
            if pd.isna(start) or pd.isna(end):
                continue
            if event["event_id"] == selected_event_id:
                continue
            date_label = start.strftime("%d/%m/%Y")
            if start != end:
                date_label = f"{start:%d/%m/%Y} a {end:%d/%m/%Y}"
            fig.add_shape(
                type="line",
                x0=start,
                x1=start,
                y0=0,
                y1=1,
                xref="x",
                yref="paper",
                line=dict(color="rgba(122,117,112,.32)", width=1, dash="dot"),
                layer="below",
            )
            fig.add_annotation(
                x=start,
                y=0.99,
                xref="x",
                yref="paper",
                text="evento",
                hovertext=f"{event['event_name']}<br>{date_label}",
                showarrow=False,
                captureevents=True,
                textangle=-90,
                font=dict(family="DM Mono, monospace", size=9, color="rgba(95,90,85,.72)"),
                bgcolor="rgba(245,242,237,.75)",
                bordercolor="rgba(122,117,112,.35)",
                borderwidth=1,
                borderpad=1,
            )

    start = selected_event["start_date"]
    end = selected_event["end_date"]
    if start == end:
        fig.add_shape(
            type="line",
            x0=start,
            x1=start,
            y0=0,
            y1=1,
            xref="x",
            yref="paper",
            line=dict(color=COR_ACCENT, width=2.2, dash="dot"),
        )
        annotation_x = start
    else:
        fig.add_shape(
            type="rect",
            x0=start,
            x1=end,
            y0=0,
            y1=1,
            xref="x",
            yref="paper",
            fillcolor="rgba(192,57,43,.12)",
            line=dict(color=COR_ACCENT, width=1.3, dash="dot"),
            layer="below",
        )
        annotation_x = start + (end - start) / 2

    fig.add_annotation(
        x=annotation_x,
        y=1.03,
        xref="x",
        yref="paper",
        text=selected_event["event_name"],
        showarrow=False,
        font=dict(family="DM Mono, monospace", size=11, color=COR_ACCENT),
        bgcolor=COR_PAPER,
        bordercolor=COR_ACCENT,
        borderwidth=1,
        borderpad=4,
    )


def nearby_event_hover_labels(dates: pd.Series, events: pd.DataFrame, selected_event_id: str, window_days: int = 21) -> pd.Series:
    event_rows = events[["event_id", "start_date", "end_date", "event_name"]].dropna(subset=["start_date"]).copy()
    if event_rows.empty:
        return pd.Series(["Sem evento proximo"] * len(dates), index=dates.index)

    labels = []
    for date in dates:
        if pd.isna(date):
            labels.append("Sem evento proximo")
            continue

        distances = []
        for _, event in event_rows.iterrows():
            start = event["start_date"]
            end = event["end_date"] if pd.notna(event["end_date"]) else start
            if start <= date <= end:
                distance = 0
            else:
                distance = min(abs((date - start).days), abs((date - end).days))
            if distance <= window_days:
                prefix = "Selecionado: " if event["event_id"] == selected_event_id else ""
                distances.append((distance, f"{prefix}{event['event_name']} ({distance}d)"))

        if distances:
            labels.append("<br>".join(item for _, item in sorted(distances)[:3]))
        else:
            labels.append("Sem evento proximo")

    return pd.Series(labels, index=dates.index)


def render_event_movement_cards(selected_event: pd.Series, impacts: pd.DataFrame) -> None:
    event_name = html.escape(str(selected_event["event_name"]))
    event_date = selected_event["start_date"].strftime("%d/%m/%Y") if pd.notna(selected_event["start_date"]) else "N/A"
    event_precision = html.escape(str(selected_event.get("date_precision_label", "")))

    if not impacts.empty:
        top_impacts = (
            impacts.sort_values("abs_standardized_change", ascending=False)
            .drop_duplicates("indicator_label")
            .head(4)
        )
    else:
        top_impacts = pd.DataFrame()

    card_html = f"""
<div class="movement-panel">
    <div class="movement-kicker">evento em foco</div>
    <h3>{event_name}</h3>
    <div class="movement-meta">{event_date} · {event_precision}</div>
    <div class="movement-rule"></div>
    <div class="movement-kicker">maiores movimentos</div>
"""

    if top_impacts.empty:
        card_html += """
    <p class="movement-empty">
        Sem dados de curto prazo para este evento. A leitura fica melhor no painel anual quando a data e ampla.
    </p>
"""
    else:
        for _, row in top_impacts.iterrows():
            value = row["standardized_change"]
            abs_value = row["abs_standardized_change"]
            is_up = value >= 0
            direction = "subiu" if is_up else "caiu"
            arrow = "&uarr;" if is_up else "&darr;"
            tone = "up" if is_up else "down"
            width = min(100, max(8, int((abs_value / 3.0) * 100)))
            indicator = html.escape(str(row["indicator_label"]))
            window = int(row["window_days"])
            card_html += f"""
    <div class="movement-card {tone}">
        <div class="movement-card-top">
            <span>{indicator}</span>
            <strong>{arrow} {format_number(abs_value)} sigma</strong>
        </div>
        <div class="movement-direction">{direction} na janela de {window} dias</div>
        <div class="movement-bar"><div style="width:{width}%"></div></div>
    </div>
"""

    card_html += "</div>"
    st.html(textwrap.dedent(card_html).strip())


def render_trends_section(
    selected_event: pd.Series,
    selected_event_id: str,
    country_trends: pd.DataFrame,
    country_trends_alignment: pd.DataFrame,
    selected_indicators: list[str],
    country_indicators: pd.DataFrame,
    technical_mode: bool,
) -> None:
    section_header("03b", "Atencao publica ao redor do evento", "Atencao")
    plain_note(
        "O Google Trends mede interesse relativo de busca. Aqui ele aparece em Z-score para comparar picos de atencao publica com movimentos economicos."
    )

    if country_trends.empty:
        st.info(
            "Camada de Trends pronta no app, mas ainda sem coleta real. Rode: "
            "`python scripts/collect_trends.py --event-id EVENT_ID`, depois "
            "`python scripts/build_trends_layer.py` e `python scripts/build_trends_event_alignment.py`."
        )
        return

    event_trends = country_trends[country_trends["event_id"] == selected_event_id].copy()
    if event_trends.empty:
        st.info(
            f"Ainda nao ha dados de Google Trends para este evento ({selected_event_id}). "
            "Use o coletor com esse event_id para preencher a camada."
        )
        return

    alignment = country_trends_alignment[
        country_trends_alignment["event_id"] == selected_event_id
    ].copy()
    if not alignment.empty:
        top_peak = alignment.sort_values("peak_z_score", ascending=False).iloc[0]
        peak_date = top_peak["peak_date"].strftime("%d/%m/%Y") if pd.notna(top_peak["peak_date"]) else "-"
        days = int(top_peak["days_from_event"])
        if days == 0:
            distance = "no dia do evento"
        elif days < 0:
            distance = f"{abs(days)} dias antes"
        else:
            distance = f"{days} dias depois"
        summary_html = f"""
        <div class="trend-summary-grid">
          <div class="trend-summary-card">
            <div class="trend-summary-kicker">termo com maior pico</div>
            <div class="trend-summary-value">{html.escape(str(top_peak["term"]))}</div>
            <div class="trend-summary-meta">Interesse maximo: {format_number(top_peak["peak_interest"], 0)} / 100</div>
          </div>
          <div class="trend-summary-card">
            <div class="trend-summary-kicker">quando o publico buscou</div>
            <div class="trend-summary-value">{html.escape(str(top_peak["timing"]))}</div>
            <div class="trend-summary-meta">{peak_date} · {distance}</div>
          </div>
          <div class="trend-summary-card">
            <div class="trend-summary-kicker">intensidade do pico</div>
            <div class="trend-summary-value">{format_number(top_peak["peak_z_score"])} sigma</div>
            <div class="trend-summary-meta">Z-score do termo dentro da janela coletada</div>
          </div>
        </div>
        """
        st.html(textwrap.dedent(summary_html).strip())

    term_order = (
        alignment.sort_values("peak_z_score", ascending=False)["term"].dropna().drop_duplicates().tolist()
        if not alignment.empty
        else []
    )
    term_options = term_order or sorted(event_trends["term"].dropna().unique())
    selected_term = st.segmented_control(
        "termo de busca",
        term_options,
        default=term_options[0],
        key=f"trend_term_{selected_event_id}",
        width="stretch",
    )

    trend_line = event_trends[event_trends["term"] == selected_term].copy()
    trend_plot = trend_line[["date", "z_score"]].copy()
    trend_plot["serie"] = f"Busca: {selected_term}"

    indicator_label = selected_indicators[0] if selected_indicators else None
    if indicator_label:
        start = trend_line["date"].min()
        end = trend_line["date"].max()
        indicator_plot = country_indicators[
            (country_indicators["indicator_label"] == indicator_label)
            & (country_indicators["date"] >= start)
            & (country_indicators["date"] <= end)
        ][["date", "z_score"]].copy()
        indicator_plot["serie"] = f"Indicador: {indicator_label}"
    else:
        indicator_plot = pd.DataFrame(columns=["date", "z_score", "serie"])

    combined = pd.concat([trend_plot, indicator_plot], ignore_index=True)
    fig_trends = px.line(
        combined,
        x="date",
        y="z_score",
        color="serie",
        custom_data=["serie"],
        labels={"z_score": "distancia do padrao", "date": "data", "serie": ""},
        color_discrete_sequence=[COR_ACCENT, COR_PRINCIPAL],
    )
    fig_trends.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Data: %{x|%d/%m/%Y}<br>"
            "Z-score: %{y:.2f}"
            "<extra></extra>"
        )
    )
    add_event_overlays(fig_trends, pd.DataFrame([selected_event]), selected_event, show_all_events=False)
    style_chart(fig_trends, height=420, left_margin=55)
    st.plotly_chart(fig_trends, use_container_width=True)

    if not alignment.empty:
        table = alignment[
            ["term", "peak_date", "peak_interest", "peak_z_score", "days_from_event", "timing"]
        ].copy()
        table["peak_date"] = table["peak_date"].dt.strftime("%d/%m/%Y")
        table["peak_z_score"] = table["peak_z_score"].map(lambda value: format_number(value))
        table = table.rename(
            columns={
                "term": "termo",
                "peak_date": "pico",
                "peak_interest": "interesse",
                "peak_z_score": "z-score pico",
                "days_from_event": "dias do evento",
                "timing": "momento",
            }
        )
        st.dataframe(table, use_container_width=True, hide_index=True, height=180)

    technical_expander(
        "detalhes tecnicos da camada Trends",
        "Dados usados: trends_normalized.csv e trends_event_alignment.csv. O interesse do Google Trends e relativo (0 a 100) dentro do timeframe coletado; o app converte cada termo em Z-score antes de comparar com indicadores economicos.",
        """
python scripts/collect_trends.py --event-id BRA_2022_06
python scripts/build_trends_layer.py
python scripts/build_trends_event_alignment.py
        """,
        technical_mode,
    )


def format_number(value: float | int | None, digits: int = 2) -> str:
    if value is None or pd.isna(value):
        return "-"
    return f"{value:.{digits}f}".replace(".", ",")


def best_event_robustness(event_id: str, robustness: pd.DataFrame) -> str:
    if robustness.empty or "event_id" not in robustness.columns:
        return "sem dados"

    event_rows = robustness[robustness["event_id"] == event_id].copy()
    if event_rows.empty:
        return "sem dados"

    if "historical_percentile" in event_rows.columns:
        event_rows["historical_percentile"] = pd.to_numeric(
            event_rows["historical_percentile"], errors="coerce"
        )
        event_rows = event_rows.sort_values("historical_percentile", ascending=False)

    label = str(event_rows.iloc[0].get("rarity_label", "sem dados"))
    percentile = event_rows.iloc[0].get("historical_percentile", pd.NA)
    if pd.isna(percentile):
        return label
    return f"{label} ({format_number(percentile, 0)}%)"


def best_event_contamination(event_id: str, contamination: pd.DataFrame, window_days: int = 90) -> str:
    if contamination.empty or "event_id" not in contamination.columns:
        return "sem dados"

    event_rows = contamination[
        (contamination["event_id"] == event_id)
        & (contamination["window_days"] == window_days)
    ].copy()
    if event_rows.empty:
        return "sem dados"

    row = event_rows.iloc[0]
    level = str(row.get("contamination_level", "sem dados"))
    count = row.get("nearby_event_count", pd.NA)
    if pd.isna(count):
        return level
    return f"{level} ({int(count)})"


def event_table(
    events: pd.DataFrame,
    short_rank: pd.DataFrame,
    robustness: pd.DataFrame,
    contamination: pd.DataFrame,
) -> pd.DataFrame:
    table = events[
        [
            "event_id",
            "start_date",
            "end_date",
            "event_name",
            "event_category_label",
            "event_subcategory_label",
            "date_precision_label",
        ]
    ].copy()

    def get_impact(event):
        if "event_id" in short_rank.columns:
            row = short_rank[short_rank["event_id"] == event["event_id"]]
        else:
            row = short_rank[short_rank["event_name"] == event["event_name"]]
        if row.empty:
            return "sem dados"
        val = row["abs_standardized_change"].max()
        if val > 1.5:
            return "alto"
        elif val > 0.5:
            return "medio"
        return "baixo"

    table["impacto"] = table.apply(get_impact, axis=1)
    table["robustez"] = table["event_id"].map(lambda event_id: best_event_robustness(event_id, robustness))
    table["contaminacao"] = table["event_id"].map(
        lambda event_id: best_event_contamination(event_id, contamination)
    )

    table["start_date"] = table["start_date"].dt.strftime("%d/%m/%Y")
    table["end_date"] = table["end_date"].dt.strftime("%d/%m/%Y")
    table = table.drop(columns=["event_id"])
    
    table = table.rename(
        columns={
            "start_date": "inicio",
            "end_date": "fim",
            "event_name": "evento",
            "event_category_label": "tema",
            "event_subcategory_label": "assunto",
            "date_precision_label": "tipo de data",
        }
    )
    cols = ["inicio", "fim", "evento", "impacto", "robustez", "contaminacao", "tema", "assunto", "tipo de data"]
    return table[cols]


def annual_table(df: pd.DataFrame) -> pd.DataFrame:
    table = df[
        [
            "event_name",
            "event_year",
            "indicator_label",
            "change_from_previous_year",
            "z_change_from_previous_year",
        ]
    ].copy()
    table["change_from_previous_year"] = table["change_from_previous_year"].map(
        lambda value: format_number(value)
    )
    table["z_change_from_previous_year"] = table["z_change_from_previous_year"].map(
        lambda value: format_number(value)
    )
    return table.rename(
        columns={
            "event_name": "evento",
            "event_year": "ano",
            "indicator_label": "indicador",
            "change_from_previous_year": "mudanca vs. ano anterior",
            "z_change_from_previous_year": "intensidade padronizada",
        }
    )


def country_story(country: str, short_rank: pd.DataFrame, annual_rank: pd.DataFrame) -> str:
    country_name = COUNTRY_LABELS[country]
    if not short_rank.empty:
        top = short_rank.iloc[0]
        return (
            f"Em {country_name}, o movimento de curto prazo mais forte nesta base aparece em "
            f"'{top['event_name']}', envolvendo {top['indicator_label'].lower()}. "
            f"A intensidade foi de {format_number(top['abs_standardized_change'])} desvios-padrao, "
            "ou seja, um movimento bem acima do comportamento normal da serie."
        )
    if not annual_rank.empty:
        top = annual_rank.iloc[0]
        return (
            f"Em {country_name}, a leitura disponivel por enquanto e anual. O contexto macro mais forte "
            f"aparece em {int(top['event_year'])}, associado a {top['indicator_label'].lower()}."
        )
    return f"Ainda nao ha informacoes suficientes para destacar um movimento em {country_name}."


def country_insights(country: str, short_rank: pd.DataFrame, annual_rank: pd.DataFrame) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    if not short_rank.empty:
        top = short_rank.iloc[0]
        items.append(
            (
                "Curto prazo",
                f"{top['event_name']} aparece como maior movimento em {top['indicator_label'].lower()} na janela de {int(top['window_days'])} dias.",
            )
        )
        repeated = short_rank.head(20)["indicator_label"].mode()
        if not repeated.empty:
            items.append(
                (
                    "Indicador recorrente",
                    f"{repeated.iloc[0]} aparece com frequencia entre os maiores movimentos do pais.",
                )
            )
    if not annual_rank.empty:
        annual = annual_rank.iloc[0]
        items.append(
            (
                "Contexto anual",
                f"No recorte anual, {annual['indicator_label'].lower()} se destaca em {int(annual['event_year'])}.",
            )
        )
    if len(items) < 3:
        items.append(
            (
                "Leitura cuidadosa",
                "Os resultados indicam associacao temporal e intensidade relativa; nao devem ser lidos como causalidade direta.",
            )
        )
    return items[:3]


def header() -> None:
    st.markdown(
        f"""
        <div class="hero-block">
          <div class="hero-eyebrow">Análise política e economia · 2016-2026</div>
          <div class="hero-eyebrow" style="margin-top:.3rem; opacity:.7; text-transform:none; letter-spacing:normal;">
            diário/mensal até jun/2026 · anual até {WORLD_BANK_MAX_YEAR}
          </div>
          <div class="hero-title">Aten&ccedil;&atilde;o Pol&iacute;tica<br><em>& Impacto Econ&ocirc;mico</em></div>
          <div class="hero-lead">
            Uma leitura guiada sobre eventos políticos e mudanças econômicas no Brasil, nos EUA e na Argentina.
            A visão simples conta a história; o modo técnico abre as fórmulas, fontes e decisões metodológicas.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="pill-row">
            <span class="pill">python</span>
            <span class="pill">pandas</span>
            <span class="pill">plotly</span>
            <span class="pill">streamlit</span>
            <span class="pill">bcb-sgs</span>
            <span class="pill">fred</span>
            <span class="pill">world-bank</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_row(data: dict[str, pd.DataFrame], learning_mode: bool = False) -> None:
    events = data["events"]
    indicators = data["indicators"]
    short_rank = data["short_rank"]
    annual_context = data["annual_context"]

    st.markdown(
        f"""
        <div class="kpi-grid">
          <div class="kpi-card"><div class="kpi-val">{len(events)}</div><div class="kpi-label">Eventos analisados</div></div>
          <div class="kpi-card"><div class="kpi-val">{indicators["country_code"].nunique()}</div><div class="kpi-label">Paises</div></div>
          <div class="kpi-card"><div class="kpi-val">{len(indicators):,}</div><div class="kpi-label">Registros economicos</div></div>
          <div class="kpi-card"><div class="kpi-val">{len(short_rank) + len(annual_context):,}</div><div class="kpi-label">Comparacoes</div></div>
        </div>
        """.replace(",", "."),
        unsafe_allow_html=True,
    )
    plain_note(
        "Na leitura normal, os graficos mostram intensidade relativa: quanto algo saiu do padrao daquele proprio pais."
    )
    coverage_note()

    learning_expander(
        "Aprendizado: Cartões de Resumo (KPIs)",
        "Exibe métricas agregadas do banco de dados unificado do projeto: número total de eventos, países catalogados, registros econômicos processados e comparações estatísticas calculadas.",
        "Antes de analisar dados granulares de séries temporais, é fundamental que o analista conheça a escala e a volumetria da base de dados com a qual está trabalhando. Os KPIs servem como o 'cartão de visitas' do pipeline de dados.",
        "1. Carregue os dataframes agregados do pipeline.\n2. Utilize len() para obter o total de linhas dos conjuntos de dados de eventos e registros.\n3. Utilize .nunique() no Pandas sobre a coluna country_code para contar os países cobertos.",
        """
total_events = len(events)
total_countries = indicators["country_code"].nunique()
total_records = len(indicators)
        """,
        learning_mode
    )


def country_view(data: dict[str, pd.DataFrame], country: str, technical_mode: bool, learning_mode: bool = False) -> None:
    events = data["events"]
    indicators = data["indicators"]
    event_impact = data["event_impact"]
    short_rank = data["short_rank"]
    annual_rank = data["annual_rank"]
    robustness = data["robustness"]
    significance = data["significance"]
    contamination = data["contamination"]
    persistence = data["persistence"]
    event_study = data["event_study"]
    event_study_agg = data["event_study_agg"]
    final_score = data["final_score"]
    trends = data["trends"]
    trends_alignment = data["trends_alignment"]

    country_events = events[events["country_code"] == country].copy()
    country_indicators = indicators[indicators["country_code"] == country].copy()
    country_event_impact = event_impact[event_impact["country_code"] == country].copy()
    country_short = short_rank[short_rank["country_code"] == country].copy()
    country_annual = annual_rank[annual_rank["country_code"] == country].copy()
    country_robustness = (
        robustness[robustness["country_code"] == country].copy()
        if "country_code" in robustness.columns
        else pd.DataFrame()
    )
    country_significance = (
        significance[significance["country_code"] == country].copy()
        if "country_code" in significance.columns
        else pd.DataFrame()
    )
    country_contamination = (
        contamination[contamination["country_code"] == country].copy()
        if "country_code" in contamination.columns
        else pd.DataFrame()
    )
    country_persistence = (
        persistence[persistence["country_code"] == country].copy()
        if "country_code" in persistence.columns
        else pd.DataFrame()
    )
    country_event_study = (
        event_study[event_study["country_code"] == country].copy()
        if "country_code" in event_study.columns
        else pd.DataFrame()
    )
    country_event_study_agg = (
        event_study_agg[event_study_agg["country_code"] == country].copy()
        if "country_code" in event_study_agg.columns
        else pd.DataFrame()
    )
    country_final_score = (
        final_score[final_score["country_code"] == country].copy()
        if "country_code" in final_score.columns
        else pd.DataFrame()
    )
    country_trends = trends[trends["country_code"] == country].copy() if "country_code" in trends.columns else pd.DataFrame()
    country_trends_alignment = (
        trends_alignment[trends_alignment["country_code"] == country].copy()
        if "country_code" in trends_alignment.columns
        else pd.DataFrame()
    )

    section_header("01", f"{COUNTRY_LABELS[country]} · leitura por pais", COUNTRY_LABELS[country])
    st.write(
        "Esta visao ajuda a responder: quais eventos foram mapeados, quais indicadores economicos se mexeram "
        "e se esses movimentos foram comuns ou fora do padrao historico do proprio pais."
    )
    story_callout(country_story(country, country_short, country_annual))
    insight_cards(country_insights(country, country_short, country_annual))

    section_header("02", "Linha do tempo de eventos", "eventos")
    plain_note("Clique em uma linha da tabela para selecionar e focar o evento nos gráficos abaixo.")
    
    selected = st.dataframe(
        event_table(country_events, short_rank, country_robustness, country_contamination),
        use_container_width=True,
        hide_index=True,
        height=360,
        on_select="rerun",
        selection_mode="single-row",
    )
    
    if selected and "selection" in selected and selected["selection"]["rows"]:
        row_idx = selected["selection"]["rows"][0]
        selected_event_id = country_events.iloc[row_idx]["event_id"]
    else:
        selected_event_id = country_events.iloc[0]["event_id"]
        
    event_lookup = country_events.set_index("event_id")
    selected_event = event_lookup.loc[selected_event_id]
    selected_event_impacts = country_event_impact[
        country_event_impact["event_id"] == selected_event_id
    ].copy()
    selected_event_robustness = (
        country_robustness[country_robustness["event_id"] == selected_event_id].copy()
        if "event_id" in country_robustness.columns
        else pd.DataFrame()
    )
    selected_event_significance = (
        country_significance[country_significance["event_id"] == selected_event_id].copy()
        if "event_id" in country_significance.columns
        else pd.DataFrame()
    )
    selected_event_contamination = (
        country_contamination[country_contamination["event_id"] == selected_event_id].copy()
        if "event_id" in country_contamination.columns
        else pd.DataFrame()
    )
    selected_event_persistence = (
        country_persistence[country_persistence["event_id"] == selected_event_id].copy()
        if "event_id" in country_persistence.columns
        else pd.DataFrame()
    )
    selected_event_study = (
        country_event_study[country_event_study["event_id"] == selected_event_id].copy()
        if "event_id" in country_event_study.columns
        else pd.DataFrame()
    )
    
    scroll_js = f"""
    <script>
        try {{
            window.parent.document.getElementById("grafico-indicadores").scrollIntoView({{behavior: "smooth"}});
        }} catch (e) {{
            console.error("Scroll blocked:", e);
        }}
    </script>
    """
    if "last_selected_event_id" not in st.session_state:
        st.session_state["last_selected_event_id"] = selected_event_id
        should_scroll = False
    elif st.session_state["last_selected_event_id"] != selected_event_id:
        st.session_state["last_selected_event_id"] = selected_event_id
        should_scroll = True
    else:
        should_scroll = False

    if should_scroll:
        st.components.v1.html(scroll_js, height=0, width=0)

    st.markdown('<div id="grafico-indicadores"></div>', unsafe_allow_html=True)
    
    event_date_str = selected_event["start_date"].strftime("%m/%Y") if pd.notna(selected_event["start_date"]) else ""
    event_category_str = selected_event["event_category_label"] if "event_category_label" in selected_event else selected_event["event_category"]
    
    st.info(
        f"**Você selecionou:** \"{selected_event['event_name']}\" · {event_date_str} · {event_category_str}  \n"
        "A linha vermelha no gráfico marca quando esse evento aconteceu."
    )
    
    st.segmented_control(
        "Mapa da leitura",
        ["Evento", "Padroes", "Score", "Rankings", "Anual"],
        default="Evento",
        key=f"country_reading_map_{country}",
        width="stretch",
        disabled=True,
    )
    plain_note(
        "A sequencia abaixo organiza a leitura em evento selecionado, padroes agregados, score sintetico, rankings e contexto anual."
    )

    event_tab, patterns_tab, score_tab, rankings_tab, annual_tab = st.tabs(["Evento", "Padroes", "Score", "Rankings", "Anual"])

    with event_tab:
        section_header("03", "Comportamento dos indicadores", "indicadores")
        plain_note(
            "Linha acima de zero indica valor acima do padrao historico do pais; abaixo de zero indica valor abaixo do padrao."
        )
        available = sorted(country_indicators["indicator_label"].unique())
        impact_defaults = (
            selected_event_impacts.sort_values("abs_standardized_change", ascending=False)["indicator_label"]
            .dropna()
            .drop_duplicates()
            .head(4)
            .tolist()
        )
        default = impact_defaults or available[: min(4, len(available))]
    
        col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1.7, 1, 1])
        with col_ctrl1:
            selected = st.multiselect("indicadores", available, default=default)
        with col_ctrl2:
            chart_window = st.selectbox(
                "janela",
                ["evento +/- 2 anos", "serie completa"],
                key=f"indicator_window_{country}_{selected_event_id}",
            )
        with col_ctrl3:
            show_all_events = st.toggle(
                "marcar acontecimentos no grafico",
                value=False,
                key=f"show_all_events_{country}",
            )
        
        plot_df = country_indicators[country_indicators["indicator_label"].isin(selected)].copy()
        if chart_window == "evento +/- 2 anos" and pd.notna(selected_event["start_date"]):
            window_start = selected_event["start_date"] - pd.Timedelta(days=730)
            window_end = selected_event["start_date"] + pd.Timedelta(days=730)
            plot_df = plot_df[(plot_df["date"] >= window_start) & (plot_df["date"] <= window_end)].copy()

        if plot_df.empty:
            st.warning("Nao ha dados economicos disponiveis para os indicadores e a janela selecionados.")
            render_event_movement_cards(selected_event, selected_event_impacts)
        else:
            plot_df["nearby_events"] = nearby_event_hover_labels(
                plot_df["date"], country_events, selected_event_id, window_days=21
            )

            fig = px.line(
                plot_df,
                x="date",
                y="z_score",
                color="indicator_label",
                custom_data=["indicator_label", "value", "unit", "source", "frequency_label", "nearby_events"],
                labels={"z_score": "distancia do padrao historico", "date": "data", "indicator_label": "indicador"},
                color_discrete_sequence=px.colors.qualitative.Safe,
            )
            fig.update_traces(
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Data: %{x|%d/%m/%Y}<br>"
                    "Distancia do padrao: %{y:.2f}<br>"
                    "Valor original: %{customdata[1]:.2f} %{customdata[2]}<br>"
                    "Frequencia: %{customdata[4]}<br>"
                    "Fonte: %{customdata[3]}<br><br>"
                    "<b>Eventos proximos (+/-21d)</b><br>%{customdata[5]}"
                    "<extra></extra>"
                )
            )
            add_event_overlays(fig, country_events, selected_event, show_all_events)
            style_chart(fig, height=560, left_margin=55)
        
            chart_col, card_col = st.columns([2.3, 1])
            with chart_col:
                st.plotly_chart(fig, use_container_width=True)
            with card_col:
                render_event_movement_cards(selected_event, selected_event_impacts)

        render_trends_section(
            selected_event,
            selected_event_id,
            country_trends,
            country_trends_alignment,
            selected,
            country_indicators,
            technical_mode,
        )

        technical_expander(
            "detalhes tecnicos desta serie",
            "Dados usados: economic_indicators_normalized.csv. A coluna principal do grafico e z_score. Ela padroniza cada serie dentro do proprio pais, indicador e fonte. Isso evita comparar nivel bruto de economias diferentes.",
            """
    df = pd.read_csv("data/processed/economic_indicators_normalized.csv")
    df = df[df["country_code"] == country]
    df["z_score"] = (df["value"] - media_da_serie) / desvio_padrao_da_serie
    fig = px.line(df, x="date", y="z_score", color="indicator_slug")
            """,
            technical_mode,
        )

        learning_expander(
            "Aprendizado: Normalização por Z-Score",
            "O gráfico exibe a variação do indicador em relação à sua própria média histórica, expressa em desvios-padrão (Z-score). Isso reposiciona todas as séries temporais em torno de uma linha zero (média).",
            "Se colocarmos a taxa de inflação do Brasil (normalmente mais alta) e a dos EUA (normalmente mais baixa) no mesmo gráfico de valores brutos, a inflação americana parecerá insignificante. O Z-score normaliza cada país em relação a si mesmo, permitindo comparar a magnitude do choque.",
            "1. Calcule a média e o desvio padrão histórico para cada país e indicador.\n2. Subtraia a média histórica de cada registro de valor e divida pelo desvio padrão histórico.",
            """
    # Cálculo do Z-score por grupo no Pandas
    df["z_score"] = df.groupby(["country_code", "indicator_slug"])["value"].transform(
        lambda x: (x - x.mean()) / x.std()
    )
            """,
            learning_mode,
        )

        learning_expander(
            "Aprendizado: Marcação de Eventos no Plotly",
            "Desenha marcas verticais (para datas exatas) ou retângulos vermelhos translúcidos (para períodos prolongados) nos momentos exatos em que os eventos políticos ocorreram.",
            "Adicionar marcas visuais das datas dos eventos por cima dos gráficos econômicos permite ao usuário fazer uma correlação visual rápida se o indicador já vinha subindo/caindo antes do evento ou se inverteu a tendência logo após o choque.",
            "1. Obtenha a data de início e fim do evento selecionado.\n2. Se início e fim forem iguais, utilize fig.add_shape() com type='line' na data do evento.\n3. Se o evento cobrir um período, utilize type='rect' cobrindo o intervalo entre início e fim.",
            """
    # Adicionar linha vertical no Plotly
    fig.add_shape(
        type="line", x0=start_date, x1=start_date,
        y0=0, y1=1, xref="x", yref="paper",
        line=dict(color="red", width=2, dash="dot")
    )
            """,
            learning_mode,
        )
        if technical_mode:
            with st.expander("cobertura tecnica dos indicadores deste pais", expanded=False):
                coverage = (
                    country_indicators.groupby(
                        ["indicator_label", "frequency_label", "source", "unit"], as_index=False
                    )
                    .agg(
                        registros=("value", "size"),
                        inicio=("date", "min"),
                        fim=("date", "max"),
                        media=("value", "mean"),
                        desvio_padrao=("value", "std"),
                    )
                    .sort_values(["indicator_label", "source"])
                )
                coverage["inicio"] = coverage["inicio"].dt.strftime("%d/%m/%Y")
                coverage["fim"] = coverage["fim"].dt.strftime("%d/%m/%Y")
                coverage["media"] = coverage["media"].map(lambda value: format_number(value))
                coverage["desvio_padrao"] = coverage["desvio_padrao"].map(lambda value: format_number(value))
                st.dataframe(coverage, use_container_width=True, hide_index=True)

        section_header("04", "Movimentacao ligada ao evento destacado", "evento")
        plain_note(
            "Aqui a leitura sai do grafico geral e foca no evento selecionado: quais indicadores tiveram maior diferenca entre antes e depois."
        )
        if selected_event_impacts.empty:
            st.info(
                "Este evento ainda nao tem calculo de curto prazo. Isso acontece quando o pais so tem dados anuais ou quando a data e um periodo longo."
            )
        else:
            top_event = selected_event_impacts.sort_values("abs_standardized_change", ascending=False).head(12)
            if not selected_event_contamination.empty:
                contamination_90 = selected_event_contamination[
                    selected_event_contamination["window_days"] == 90
                ]
                if not contamination_90.empty and bool(contamination_90.iloc[0].get("is_contaminated_window")):
                    row = contamination_90.iloc[0]
                    st.warning(
                        "Janela contaminada: ha "
                        f"{int(row['nearby_event_count'])} evento(s) do mesmo pais em ate 90 dias. "
                        "A leitura antes/depois deve ser tratada como associacao temporal, nao atribuicao causal isolada."
                    )
            if not selected_event_robustness.empty:
                robustness_cols = [
                    "event_id",
                    "indicator_slug",
                    "window_days",
                    "historical_percentile",
                    "rarity_label",
                ]
                available_cols = [col for col in robustness_cols if col in selected_event_robustness.columns]
                top_event = top_event.merge(
                    selected_event_robustness[available_cols],
                    on=["event_id", "indicator_slug", "window_days"],
                    how="left",
                )
            if not selected_event_significance.empty:
                significance_cols = [
                    "event_id",
                    "indicator_slug",
                    "window_days",
                    "p_value_fdr",
                    "significance_label",
                ]
                available_cols = [col for col in significance_cols if col in selected_event_significance.columns]
                top_event = top_event.merge(
                    selected_event_significance[available_cols],
                    on=["event_id", "indicator_slug", "window_days"],
                    how="left",
                )
            if not selected_event_persistence.empty:
                persistence_cols = [
                    "event_id",
                    "indicator_slug",
                    "window_days",
                    "peak_abs_z_after",
                    "days_to_peak",
                    "days_until_normal_range",
                    "persistence_label",
                ]
                available_cols = [col for col in persistence_cols if col in selected_event_persistence.columns]
                top_event = top_event.merge(
                    selected_event_persistence[available_cols],
                    on=["event_id", "indicator_slug", "window_days"],
                    how="left",
                )
            fig_event = px.bar(
                top_event.sort_values("abs_standardized_change"),
                x="abs_standardized_change",
                y="indicator_label",
                color="window_days",
                orientation="h",
                custom_data=[
                    "event_name",
                    "indicator_label",
                    "window_days",
                    "before_mean",
                    "after_mean",
                    "absolute_change",
                    "standardized_change",
                    "indicator_frequency",
                ],
                labels={
                    "abs_standardized_change": "intensidade do movimento",
                    "indicator_label": "",
                    "window_days": "janela",
                },
                color_continuous_scale=[[0, COR_CREAM], [0.55, COR_SECUNDARIA], [1, COR_PRINCIPAL]],
            )
            fig_event.update_traces(
                hovertemplate=(
                    "<b>%{customdata[1]}</b><br>"
                    "Evento: %{customdata[0]}<br>"
                    "Janela: %{customdata[2]} dias<br>"
                    "Media antes: %{customdata[3]:.2f}<br>"
                    "Media depois: %{customdata[4]:.2f}<br>"
                    "Mudanca: %{customdata[5]:.2f}<br>"
                    "Intensidade: %{customdata[6]:.2f} desvios-padrao<br>"
                    "Frequencia: %{customdata[7]}"
                    "<extra></extra>"
                )
            )
            fig_event.update_coloraxes(colorbar=dict(title="dias", tickfont=TICK_FONT))
            style_chart(fig_event, height=460, left_margin=190)
            st.plotly_chart(fig_event, use_container_width=True)

            if not selected_event_study.empty:
                study_options = (
                    top_event.sort_values("abs_standardized_change", ascending=False)["indicator_label"]
                    .dropna()
                    .drop_duplicates()
                    .tolist()
                )
                selected_study_indicator = st.selectbox(
                    "Indicador no estudo de evento",
                    study_options,
                    index=0,
                    key=f"event_study_indicator_{selected_event_id}",
                )
                study_plot = selected_event_study[
                    selected_event_study["indicator_label"] == selected_study_indicator
                ].sort_values("relative_day")
                if not study_plot.empty:
                    fig_study = px.line(
                        study_plot,
                        x="relative_day",
                        y="z_score",
                        color="indicator_label",
                        custom_data=["date", "indicator_label", "z_score", "value", "unit"],
                        labels={
                            "relative_day": "dias em relacao ao evento",
                            "z_score": "desvio do padrao historico",
                            "indicator_label": "",
                        },
                    )
                    fig_study.add_vline(x=0, line_color=COR_ACCENT, line_width=2)
                    fig_study.add_hrect(y0=-1, y1=1, fillcolor="#ffffff", opacity=0.35, line_width=0)
                    fig_study.update_traces(
                        hovertemplate=(
                            "<b>%{customdata[1]}</b><br>"
                            "Data: %{customdata[0]|%d/%m/%Y}<br>"
                            "Dia relativo: %{x}<br>"
                            "Z-score: %{customdata[2]:.2f}<br>"
                            "Valor: %{customdata[3]:.2f} %{customdata[4]}"
                            "<extra></extra>"
                        )
                    )
                    style_chart(fig_study, height=380, left_margin=60)
                    st.plotly_chart(fig_study, use_container_width=True)

            event_table_impact = top_event[
                [col for col in [
                    "indicator_label",
                    "window_days",
                    "before_mean",
                    "after_mean",
                    "absolute_change",
                    "standardized_change",
                    "historical_percentile",
                    "rarity_label",
                    "p_value_fdr",
                    "significance_label",
                    "peak_abs_z_after",
                    "days_to_peak",
                    "days_until_normal_range",
                    "persistence_label",
                ] if col in top_event.columns]
            ].copy()
            for column in ["before_mean", "after_mean", "absolute_change", "standardized_change"]:
                event_table_impact[column] = event_table_impact[column].map(lambda value: format_number(value))
            if "historical_percentile" in event_table_impact.columns:
                event_table_impact["historical_percentile"] = event_table_impact[
                    "historical_percentile"
                ].map(lambda value: format_number(value, 0))
            if "p_value_fdr" in event_table_impact.columns:
                event_table_impact["p_value_fdr"] = event_table_impact["p_value_fdr"].map(
                    lambda value: format_number(value, 3)
                )
            if "peak_abs_z_after" in event_table_impact.columns:
                event_table_impact["peak_abs_z_after"] = event_table_impact["peak_abs_z_after"].map(
                    lambda value: format_number(value)
                )
            for column in ["days_to_peak", "days_until_normal_range"]:
                if column in event_table_impact.columns:
                    event_table_impact[column] = event_table_impact[column].map(
                        lambda value: "-" if pd.isna(value) else str(int(value))
                    )
            event_table_impact = event_table_impact.rename(
                columns={
                    "indicator_label": "indicador",
                    "window_days": "janela dias",
                    "before_mean": "media antes",
                    "after_mean": "media depois",
                    "absolute_change": "mudanca",
                    "standardized_change": "intensidade padronizada",
                    "historical_percentile": "percentil historico",
                    "rarity_label": "robustez",
                    "p_value_fdr": "p-value FDR",
                    "significance_label": "significancia",
                    "peak_abs_z_after": "pico |z| pos",
                    "days_to_peak": "dias ate pico",
                    "days_until_normal_range": "dias ate normalizar",
                    "persistence_label": "persistencia",
                }
            )
            st.dataframe(event_table_impact, use_container_width=True, hide_index=True, height=300)

        technical_expander(
            "como o evento foi ligado ao grafico",
            "O evento selecionado vem de political_events_processed.csv. A linha ou faixa vermelha usa start_date e end_date. O grafico de movimentacao usa event_economic_impact_normalized.csv, calculado por janelas antes/depois.",
            """
    selected_event = events.loc[event_id]
    fig.add_shape(type="line", x0=selected_event.start_date, x1=selected_event.start_date)

    impact = event_economic_impact_normalized[
        event_economic_impact_normalized["event_id"] == selected_event_id
    ]
    ranking = impact.sort_values("abs_standardized_change", ascending=False)
            """,
            technical_mode,
        )

        learning_expander(
            "Aprendizado: Variação de Médias Antes/Depois",
            "Calcula e compara a média do indicador em um intervalo pré-evento (antes) e pós-evento (depois) para medir o impacto imediato daquele evento.",
            "Eventos pontuais provocam reações nos mercados que muitas vezes se dissipam com o tempo. Comparar as médias pré e pós-evento em janelas curtas (ex. 30 ou 90 dias) ajuda a filtrar o ruído macroeconômico geral e focar no choque pontual.",
            "1. Defina uma janela de dias (ex: 30 dias).\n2. Filtre os registros do indicador no período [data_evento - janela, data_evento - 1] e calcule a média.\n3. Filtre no período [data_evento + 1, data_evento + janela] e calcule a média pós-evento.\n4. Calcule a diferença das médias e normalize pelo desvio padrão histórico.",
            """
    # Cálculo de impacto de curto prazo no Pandas
    before_mean = df[(df["date"] >= event_date - pd.Timedelta(days=window)) & (df["date"] < event_date)]["value"].mean()
    after_mean = df[(df["date"] > event_date) & (df["date"] <= event_date + pd.Timedelta(days=window))]["value"].mean()
    standardized_change = (after_mean - before_mean) / historical_std
            """,
            learning_mode,
        )

    with patterns_tab:
        section_header("05", "Curva media por categoria", "categorias")
        plain_note(
            "Com mais eventos, a leitura passa do caso individual para o padrao medio de cada tipo de evento."
        )
        if country_event_study_agg.empty:
            st.info("Ainda nao ha curvas agregadas de event study para este pais.")
        else:
            category_options = sorted(country_event_study_agg["event_category_label"].dropna().unique())
            default_categories = category_options[: min(3, len(category_options))]
            selected_categories = st.multiselect(
                "Categorias",
                category_options,
                default=default_categories,
                key=f"event_study_categories_{country}",
            )
            agg_plot = country_event_study_agg[
                country_event_study_agg["event_category_label"].isin(selected_categories)
            ].copy()
            if agg_plot.empty:
                st.info("Selecione pelo menos uma categoria para comparar.")
            else:
                fig_agg = px.line(
                    agg_plot,
                    x="relative_day",
                    y="mean_z_score",
                    color="event_category_label",
                    custom_data=[
                        "event_category_label",
                        "mean_z_score",
                        "p25_z_score",
                        "p75_z_score",
                        "events",
                        "observations",
                    ],
                    labels={
                        "relative_day": "dias em relacao ao evento",
                        "mean_z_score": "z-score medio",
                        "event_category_label": "",
                    },
                )
                fig_agg.add_vline(x=0, line_color=COR_ACCENT, line_width=2)
                fig_agg.add_hrect(y0=-1, y1=1, fillcolor="#ffffff", opacity=0.3, line_width=0)
                fig_agg.update_traces(
                    hovertemplate=(
                        "<b>%{customdata[0]}</b><br>"
                        "Dia relativo: %{x}<br>"
                        "Media: %{customdata[1]:.2f}<br>"
                        "P25-P75: %{customdata[2]:.2f} a %{customdata[3]:.2f}<br>"
                        "Eventos: %{customdata[4]}<br>"
                        "Observacoes: %{customdata[5]}"
                        "<extra></extra>"
                    )
                )
                style_chart(fig_agg, height=430, left_margin=60)
                st.plotly_chart(fig_agg, use_container_width=True)

                agg_table = (
                    agg_plot.groupby("event_category_label", as_index=False)
                    .agg(
                        eventos=("events", "max"),
                        pico_medio_abs=("mean_z_score", lambda values: values.abs().max()),
                        mediana_observacoes=("observations", "median"),
                    )
                    .sort_values("pico_medio_abs", ascending=False)
                )
                agg_table["pico_medio_abs"] = agg_table["pico_medio_abs"].map(lambda value: format_number(value))
                agg_table["mediana_observacoes"] = agg_table["mediana_observacoes"].map(
                    lambda value: format_number(value, 0)
                )
                st.dataframe(agg_table, use_container_width=True, hide_index=True)

    with score_tab:
        section_header("06", "Score final dos eventos", "score")
        plain_note(
            "Score sintetico combina impacto, robustez, significancia, persistencia, atencao publica e penaliza janelas contaminadas."
        )
        if country_final_score.empty:
            st.info("Ainda nao ha score final calculado para este pais.")
        else:
            score_cols = [
                "score_rank_country",
                "event_name",
                "event_category_label",
                "score_tier",
                "final_score",
                "impact_score",
                "robustness_score",
                "significance_score",
                "persistence_score",
                "trends_score",
                "contamination_penalty",
                "score_caveat",
                "score_note",
            ]
            top_score = country_final_score.sort_values("final_score", ascending=False).head(15).copy()
            fig_score = px.bar(
                top_score.sort_values("final_score"),
                x="final_score",
                y="event_name",
                color="event_category_label",
                orientation="h",
                custom_data=[
                    "event_name",
                    "final_score",
                    "score_tier",
                    "impact_score",
                    "robustness_score",
                    "significance_score",
                    "persistence_score",
                    "trends_score",
                    "contamination_penalty",
                    "score_caveat",
                ],
                labels={"final_score": "score final", "event_name": "", "event_category_label": ""},
            )
            fig_score.update_traces(
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Score: %{customdata[1]:.1f}<br>"
                    "Faixa: %{customdata[2]}<br>"
                    "Impacto: %{customdata[3]:.0f}<br>"
                    "Robustez: %{customdata[4]:.0f}<br>"
                    "Significancia: %{customdata[5]:.0f}<br>"
                    "Persistencia: %{customdata[6]:.0f}<br>"
                    "Trends: %{customdata[7]:.0f}<br>"
                    "Penalidade contaminacao: %{customdata[8]:.0f}<br>"
                    "Alerta: %{customdata[9]}"
                    "<extra></extra>"
                )
            )
            style_chart(fig_score, height=520, left_margin=240)
            st.plotly_chart(fig_score, use_container_width=True)

            score_table = top_score[[col for col in score_cols if col in top_score.columns]].copy()
            for column in [
                "final_score",
                "impact_score",
                "robustness_score",
                "significance_score",
                "persistence_score",
                "trends_score",
                "contamination_penalty",
            ]:
                if column in score_table.columns:
                    score_table[column] = score_table[column].map(lambda value: format_number(value, 1))
            score_table = score_table.rename(
                columns={
                    "score_rank_country": "rank",
                    "event_name": "evento",
                    "event_category_label": "categoria",
                    "score_tier": "faixa",
                    "final_score": "score",
                    "impact_score": "impacto",
                    "robustness_score": "robustez",
                    "significance_score": "significancia",
                    "persistence_score": "persistencia",
                    "trends_score": "trends",
                    "contamination_penalty": "penalidade",
                    "score_caveat": "alerta",
                    "score_note": "decomposicao",
                }
            )
            st.dataframe(score_table, use_container_width=True, hide_index=True, height=330)

    with rankings_tab:
        section_header("07", "Maiores movimentos ao redor dos eventos", "movimentos")
        plain_note(
            "Este ranking mostra onde houve maior mudanca antes/depois do evento, ajustada pela volatilidade normal do indicador."
        )
        if country_short.empty:
            st.info("Ainda nao ha dados frequentes suficientes para este pais. Por enquanto, use a leitura anual comparativa.")
        else:
            top_short = country_short.head(12)
            fig = px.bar(
                top_short.sort_values("abs_standardized_change"),
                x="abs_standardized_change",
                y="event_name",
                color="indicator_label",
                orientation="h",
                custom_data=[
                    "event_name",
                    "indicator_label",
                    "window_days",
                    "absolute_change",
                    "standardized_change",
                    "event_category_label",
                ],
                labels={"abs_standardized_change": "intensidade do movimento", "event_name": ""},
            )
            fig.update_traces(
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Indicador: %{customdata[1]}<br>"
                    "Tema: %{customdata[5]}<br>"
                    "Janela: %{customdata[2]} dias<br>"
                    "Mudanca: %{customdata[3]:.2f}<br>"
                    "Intensidade: %{customdata[4]:.2f} desvios-padrao"
                    "<extra></extra>"
                )
            )
            style_chart(fig, height=560, left_margin=260)
            st.plotly_chart(fig, use_container_width=True)

        technical_expander(
            "detalhes tecnicos do ranking de curto prazo",
            "Dados usados: event_economic_impact_normalized.csv. Para cada evento, o app compara a media antes e depois em janelas de 30, 90, 180 e 365 dias. A metrica principal e standardized_change.",
            """
    media_antes = media(indicador entre evento - janela e evento - 1 dia)
    media_depois = media(indicador entre evento + 1 dia e evento + janela)
    mudanca_absoluta = media_depois - media_antes
    standardized_change = mudanca_absoluta / desvio_padrao_historico_do_indicador
            """,
            technical_mode,
        )

        learning_expander(
            "Aprendizado: Ranking de Choques Econômicos",
            "Ordena os eventos com base no tamanho absoluto da variação do Z-score nas janelas de impacto. O maior valor absoluto encabeça a lista.",
            "Ao usar o desvio padrão como unidade comum de choque (magnitude de desvios-padrão), conseguimos ranquear de forma justa qual evento político esteve associado à maior perturbação relativa em indicadores com unidades completamente distintas (câmbio vs. inflação vs. desemprego).",
            "1. Junte todas as variações padronizadas de curto prazo calculadas para todos os eventos.\n2. Calcule o valor absoluto do desvio padrão de cada variação.\n3. Ordene o dataframe em ordem decrescente por essa métrica e selecione as primeiras linhas.",
            """
    # Ranquear maiores movimentos absolutos
    ranking = impacts.sort_values("abs_standardized_change", ascending=False)
    top_impacts = ranking.head(12)
            """,
            learning_mode,
        )

    with annual_tab:
        section_header("08", "Contexto macro anual", "anual")
        coverage_note("annual")
        country_annual = country_annual[country_annual["event_year"] <= WORLD_BANK_MAX_YEAR].copy()
        top_annual = country_annual.head(12)
        st.dataframe(
            annual_table(top_annual),
            use_container_width=True,
            hide_index=True,
            height=360,
        )


def comparison_view(data: dict[str, pd.DataFrame], technical_mode: bool, learning_mode: bool = False) -> None:
    annual_context = data["annual_context"].copy()
    indicators = data["indicators"].copy()
    event_study_agg = data["event_study_agg"].copy()

    section_header("01", "Relacao entre paises", "paises")
    st.write(
        "Aqui a comparacao e feita por intensidade relativa. Em vez de perguntar qual pais tem o maior numero bruto, "
        "a pergunta e: em qual pais o indicador saiu mais do seu proprio padrao historico"
    )
    annual_context = annual_context[annual_context["event_year"] <= WORLD_BANK_MAX_YEAR].copy()
    if not annual_context.empty:
        top_context = annual_context.iloc[0]
        story_callout(
            f"O maior destaque anual nesta base aparece em {COUNTRY_LABELS[top_context['country_code']]} "
            f"no ano de {int(top_context['event_year'])}, em {top_context['indicator_label'].lower()}."
        )
        top_country = annual_context.head(25)["country_code"].mode().iloc[0]
        top_indicator = annual_context.head(25)["indicator_label"].mode().iloc[0]
        insight_cards(
            [
                (
                    "Maior destaque",
                    f"{COUNTRY_LABELS[top_context['country_code']]} concentra o maior choque anual observado no ranking.",
                ),
                (
                    "Pais recorrente",
                    f"{COUNTRY_LABELS[top_country]} aparece mais vezes entre os 25 maiores contextos macro.",
                ),
                (
                    "Indicador sensivel",
                    f"{top_indicator} e o indicador mais recorrente entre os maiores movimentos anuais.",
                ),
            ]
        )

    top = annual_context.head(25).copy()
    top["label"] = (
        top["country_code"]
        + " · "
        + top["event_year"].astype(str)
        + " · "
        + top["indicator_label"]
    )

    fig = px.bar(
        top.sort_values("abs_z_change_from_previous_year"),
        x="abs_z_change_from_previous_year",
        y="label",
        color="country_code",
        orientation="h",
        custom_data=[
            "country_name",
            "event_year",
            "indicator_label",
            "event_name",
            "z_change_from_previous_year",
            "change_from_previous_year",
        ],
        color_discrete_map=COUNTRY_COLORS,
        labels={"abs_z_change_from_previous_year": "intensidade da mudanca anual", "label": ""},
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]} · %{customdata[1]}</b><br>"
            "Indicador: %{customdata[2]}<br>"
            "Evento de referencia: %{customdata[3]}<br>"
            "Mudanca anual: %{customdata[5]:.2f}<br>"
            "Intensidade: %{customdata[4]:.2f} desvios-padrao"
            "<extra></extra>"
        )
    )
    style_chart(fig, height=820, left_margin=320)
    st.plotly_chart(fig, use_container_width=True)

    section_header("02", "Curto prazo entre paises", "curto prazo")
    st.write(
        "Aqui a comparacao usa curvas medias de event study. A pergunta e: para uma mesma categoria, "
        "qual pais costuma sair mais do seu proprio padrao nos dias ao redor dos eventos?"
    )
    if event_study_agg.empty:
        st.info("Ainda nao ha curvas agregadas de curto prazo para comparar os paises.")
    else:
        category_options = sorted(event_study_agg["event_category_label"].dropna().unique())
        selected_category = st.selectbox(
            "categoria de evento",
            category_options,
            index=category_options.index("Economia") if "Economia" in category_options else 0,
            key="comparison_event_category",
        )
        comparison_plot = event_study_agg[
            event_study_agg["event_category_label"] == selected_category
        ].copy()
        if comparison_plot.empty:
            st.info("Sem dados para esta categoria.")
        else:
            fig_short = px.line(
                comparison_plot,
                x="relative_day",
                y="mean_z_score",
                color="country_code",
                custom_data=[
                    "country_name",
                    "event_category_label",
                    "mean_z_score",
                    "p25_z_score",
                    "p75_z_score",
                    "events",
                    "observations",
                ],
                color_discrete_map=COUNTRY_COLORS,
                labels={
                    "relative_day": "dias em relacao ao evento",
                    "mean_z_score": "z-score medio",
                    "country_code": "pais",
                },
            )
            fig_short.add_vline(x=0, line_color=COR_ACCENT, line_width=2)
            fig_short.add_hrect(y0=-1, y1=1, fillcolor="#ffffff", opacity=0.3, line_width=0)
            fig_short.update_traces(
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Categoria: %{customdata[1]}<br>"
                    "Dia relativo: %{x}<br>"
                    "Media: %{customdata[2]:.2f}<br>"
                    "P25-P75: %{customdata[3]:.2f} a %{customdata[4]:.2f}<br>"
                    "Eventos: %{customdata[5]}<br>"
                    "Observacoes: %{customdata[6]}"
                    "<extra></extra>"
                )
            )
            style_chart(fig_short, height=520, left_margin=60)
            st.plotly_chart(fig_short, use_container_width=True)

            short_summary = (
                comparison_plot.groupby(["country_code", "country_name"], as_index=False)
                .agg(
                    eventos=("events", "max"),
                    pico_medio_abs=("mean_z_score", lambda values: values.abs().max()),
                    mediana_eventos_no_dia=("events", "median"),
                    mediana_observacoes=("observations", "median"),
                )
                .sort_values("pico_medio_abs", ascending=False)
            )
            short_summary["pico_medio_abs"] = short_summary["pico_medio_abs"].map(lambda value: format_number(value))
            short_summary["mediana_eventos_no_dia"] = short_summary["mediana_eventos_no_dia"].map(
                lambda value: format_number(value, 0)
            )
            short_summary["mediana_observacoes"] = short_summary["mediana_observacoes"].map(
                lambda value: format_number(value, 0)
            )
            short_summary = short_summary.rename(
                columns={
                    "country_code": "pais",
                    "country_name": "nome",
                    "eventos": "eventos max",
                    "pico_medio_abs": "pico medio |z|",
                    "mediana_eventos_no_dia": "mediana eventos/dia",
                    "mediana_observacoes": "mediana obs/dia",
                }
            )
            st.dataframe(short_summary, use_container_width=True, hide_index=True)

    section_header("03", "Trajetorias anuais comparaveis", "anuais")
    coverage_note("annual")
    choices = ["inflation_annual_pct", "unemployment_pct", "gdp_growth_annual_pct"]
    selected = st.radio(
        "indicador anual",
        choices,
        format_func=lambda slug: INDICATOR_LABELS.get(slug, slug),
        horizontal=True,
    )
    plot_df = indicators[
        (indicators["source"] == "World Bank API")
        & (indicators["indicator_slug"] == selected)
        & (indicators["date"].dt.year <= WORLD_BANK_MAX_YEAR)
    ]
    fig = px.line(
        plot_df,
        x="date",
        y="z_score",
        color="country_code",
        markers=True,
        custom_data=["country_name", "indicator_label", "value", "unit"],
        color_discrete_map=COUNTRY_COLORS,
        labels={"z_score": "distancia do padrao historico", "date": "ano", "country_code": "pais"},
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Indicador: %{customdata[1]}<br>"
            "Ano: %{x|%Y}<br>"
            "Distancia do padrao: %{y:.2f}<br>"
            "Valor original: %{customdata[2]:.2f} %{customdata[3]}"
            "<extra></extra>"
        )
    )
    style_chart(fig, height=540, left_margin=55)
    st.plotly_chart(fig, use_container_width=True)

    technical_expander(
        "detalhes tecnicos da comparacao entre paises",
        "Dados usados: ranking_annual_context_by_country_year.csv e economic_indicators_normalized.csv. A comparacao entre paises usa z-score e mudanca de z-score, nao valores brutos. Eventos no mesmo ano podem compartilhar o mesmo contexto macro.",
        """
z_score = (valor - media_historica_do_pais_indicador) / desvio_padrao_historico
choque_anual = z_score_ano_evento - z_score_ano_anterior
ranking = abs(choque_anual)
        """,
        technical_mode,
    )

    learning_expander(
        "Aprendizado: Comparação Internacional Justa",
        "Mede e compara os choques econômicos anuais relativos entre o Brasil, EUA e Argentina, usando o deslocamento do Z-score em relação ao ano anterior.",
        "Em economias hiperinflacionárias (como a Argentina em alguns períodos), as variações brutas são massivas e mascaram variações atípicas em economias mais estáveis (como os EUA). O desvio da variação anual Z-score corrige essa distorção.",
        "1. Calcule a variação do Z-score anual de cada país.\n2. Subtraia o Z-score do ano anterior para obter o choque anual.\n3. Ranqueie os choques em termos absolutos entre todos os países na mesma tabela.",
        """
# Choque do Z-score anual comparativo
annual_context["choque_anual"] = annual_context["z_score"] - annual_context["z_score_prev_year"]
ranking_comparativo = annual_context.sort_values("abs_choque_anual", ascending=False)
        """,
        learning_mode,
    )

    learning_expander(
        "Aprendizado: Trajetórias Anuais no Banco Mundial",
        "Plota o histórico de médio-longo prazo dos indicadores anuais agregados pelo Banco Mundial para os três países simultaneamente, expressos em desvios-padrão (Z-scores).",
        "Os indicadores de alta frequência (diários/mensais) são ótimos para o curto prazo, mas diferem entre países. O Banco Mundial nos fornece séries idênticas e normalizadas globalmente para comparar a evolução estrutural ao longo de anos (2016-2024).",
        "1. Filtre a base de dados unificada pelas séries que possuem origem no Banco Mundial (World Bank API).\n2. Normalize os valores para Z-score anual por país e plote as linhas usando o Plotly Express.",
        """
# Filtrar e plotar trajetórias anuais do Banco Mundial
plot_df = indicators[indicators["source"] == "World Bank API"]
fig = px.line(plot_df, x="date", y="z_score", color="country_code")
        """,
        learning_mode,
    )


def methodology_view(technical_mode: bool, learning_mode: bool = False) -> None:
    section_header("01", "Metodologia do projeto", "Metodologia")
    st.write(
        "O estudo compara eventos politico-economicos com movimentos de indicadores e atencao publica. "
        "A leitura correta e associacao temporal: o app mostra quando um evento coincide com mudancas raras, "
        "fortes ou persistentes, sem afirmar causalidade direta."
    )
    coverage_note()

    steps = [
        ("1 ? coleta", "Foram reunidos indicadores economicos de fontes publicas para Brasil, EUA e Argentina."),
        ("2 ? padronizacao", "Os dados foram colocados em uma tabela unica, com pais, data, indicador, valor, unidade e fonte."),
        ("3 ? comparacao justa", "Cada indicador foi comparado com a propria historia do pais, e nao com o numero bruto de outro pais."),
        ("4 ? eventos", "Eventos entram quando tiveram cobertura publica forte ou foram decisoes formais de politica economica/institucional."),
        ("5 ? impacto", "O sistema mede antes/depois, robustez historica, significancia, contaminacao, persistencia e event study."),
        ("6 ? sintese", "O score final combina os sinais principais e penaliza janelas contaminadas por eventos proximos."),
    ]
    for title, body in steps:
        st.markdown(f"### {title}")
        st.write(body)

    section_header("02", "Criterios e limites", "limites")
    criteria = pd.DataFrame(
        [
            ["Entrada de evento", "Evento entra se teve cobertura de primeira pagina por varios dias ou se foi decisao formal com efeito esperado em indicador da base."],
            ["Evento curto", "Datas exatas e meses aproximados entram no motor antes/depois, persistencia e event study."],
            ["Evento longo", "year e year_range nao sao tratados como choque pontual; ficam mais adequados ao contexto anual."],
            ["Causalidade", "O resultado e associacao temporal. Eventos proximos, tendencia macro e choques externos podem compartilhar a mesma janela."],
            ["Contaminacao", "Janelas com eventos do mesmo pais em ate 30, 90 ou 180 dias recebem flag e penalidade no score."],
            ["Google Trends", "Trends entra quando ha coleta disponivel. Eventos sem coleta nao quebram o pipeline; recebem score de atencao igual a zero ate nova coleta."],
        ],
        columns=["tema", "regra"],
    )
    st.dataframe(criteria, use_container_width=True, hide_index=True)

    section_header("03", "Score final", "Score")
    score_rules = pd.DataFrame(
        [
            ["impacto economico", "35%", "maior movimento padronizado antes/depois"],
            ["robustez historica", "25%", "percentil do movimento contra janelas historicas semelhantes"],
            ["significancia", "15%", "p-value FDR do melhor teste disponivel"],
            ["persistencia", "15%", "se o choque persistiu, decaiu ou voltou rapido ao normal"],
            ["Google Trends", "5%", "pico de atencao publica normalizado; peso reduzido enquanto a cobertura esta parcial"],
            ["contaminacao", "-5%", "penalidade quando ha eventos proximos na janela"],
        ],
        columns=["componente", "peso", "leitura"],
    )
    st.dataframe(score_rules, use_container_width=True, hide_index=True)

    section_header("04", "Cobertura por pais", "pais")
    coverage_rows = [
        ["Argentina", "25 eventos; 20 curto prazo", "dolar oficial e dolar blue diarios; anual World Bank", "curto prazo ainda e muito cambial"],
        ["Brasil", "34 eventos; 32 curto prazo", "cambio, Selic, IPCA, gasolina; anual World Bank", "boa cobertura macro, mas poucos indicadores financeiros"],
        ["Estados Unidos", "29 eventos; 27 curto prazo", "FRED semanal/mensal/trimestral; anual World Bank", "frequencias mistas reduzem detalhe diario"],
    ]
    st.dataframe(
        pd.DataFrame(coverage_rows, columns=["pais", "eventos", "forca", "limite"]),
        use_container_width=True,
        hide_index=True,
    )

    section_header("05", "Estado do Google Trends", "Trends")
    trends_summary_path = PROCESSED_DIR / "trends_coverage_summary.csv"
    if trends_summary_path.exists():
        trends_summary = pd.read_csv(trends_summary_path)
        trends_summary = trends_summary.rename(
            columns={"country_code": "pais", "trends_status": "status", "events": "eventos"}
        )
        st.dataframe(trends_summary, use_container_width=True, hide_index=True)
    plain_note(
        "A coleta do Google Trends e incremental. Como o Google pode limitar requisicoes, a cobertura deve ser expandida em lotes pequenos."
    )

    if technical_mode:
        section_header("06", "Detalhes tecnicos", "tecnicos")
        st.markdown("### fontes")
        st.dataframe(
            pd.DataFrame(
                [
                    ["BCB SGS", "Brasil", "diaria/mensal", "cambio, Selic, IPCA, gasolina"],
                    ["FRED", "Estados Unidos", "semanal/mensal/trimestral", "gasolina, juros, CPI, desemprego, PIB real"],
                    ["Bluelytics", "Argentina", "diaria", "dolar oficial, dolar blue"],
                    ["World Bank API", "Brasil, EUA, Argentina", "anual", "inflacao, desemprego, PIB, divida"],
                    ["Google Trends", "Brasil, EUA, Argentina", "semanal", "atencao publica por termo/evento"],
                ],
                columns=["fonte", "cobertura", "frequencia", "uso"],
            ),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown("### formulas")
        st.code(
            """
z_score = (valor - media_historica) / desvio_padrao_historico

media_antes = media do indicador antes do evento
media_depois = media do indicador depois do evento
mudanca_absoluta = media_depois - media_antes
choque_padronizado = mudanca_absoluta / desvio_padrao_historico

score_final = (
    0.35 * impacto
    + 0.25 * robustez
    + 0.15 * significancia
    + 0.15 * persistencia
    + 0.05 * trends
    - 0.05 * contaminacao
)

choque_anual = z_score_ano_evento - z_score_ano_anterior
            """,
            language="text",
        )
        st.markdown("### limites metodologicos")
        st.write(
            "O projeto nao afirma causalidade direta. Eventos no mesmo ano ou em janelas proximas podem compartilhar o mesmo contexto macro. "
            "Os testes antes/depois ajudam a medir diferenca estatistica, mas nao substituem desenho causal com controles formais."
        )
        st.markdown("### codigo do fluxo")
        st.code(
            """
python scripts/collect_bcb_sgs.py
python scripts/collect_fred.py
python scripts/collect_bluelytics.py
python scripts/collect_world_bank.py
python scripts/build_economic_indicators_unified.py
python scripts/build_normalized_economic_indicators.py
python scripts/prepare_political_events.py
python scripts/build_event_economic_impact.py
python scripts/build_normalized_event_impact.py
python scripts/build_event_statistical_tests.py
python scripts/build_event_window_contamination.py
python scripts/build_event_shock_persistence.py
python scripts/build_event_study_series.py
python scripts/build_event_study_aggregates.py
python scripts/build_trends_layer.py
python scripts/build_trends_event_alignment.py
python scripts/build_trends_coverage.py
python scripts/build_event_final_score.py
python scripts/build_annual_event_impact.py
python scripts/build_rankings.py
            """,
            language="powershell",
        )

    learning_expander(
        "Aprendizado: por que nao falar em causalidade direta",
        "O app alinha datas de eventos com series economicas e mede o que mudou ao redor dessas datas.",
        "Mesmo quando a mudanca e grande, rara e significativa, outros fatos podem ter ocorrido na mesma janela. Por isso a conclusao honesta e associacao temporal robusta, nao causalidade definitiva.",
        "1. Marque o evento.\n2. Compare antes/depois.\n3. Verifique raridade historica.\n4. Veja contaminacao por eventos proximos.\n5. Interprete como evidencia exploratoria.",
        """
impacto = media_depois - media_antes
robusto = percentil_historico >= 95
causalidade = requer_controles_adicionais
        """,
        learning_mode,
    )


def top_filter_controls() -> tuple[str, str | None, bool, bool]:
    st.markdown(
        """
        <div class="top-filter-intro">
          <div class="top-filter-kicker">filtros principais</div>
          <div class="top-filter-title">Escolha o recorte da análise</div>
          <div class="top-filter-copy">
            Primeiro defina o tipo de leitura; quando a análise for por país, escolha o território.
            O nível de detalhe controla se a página fica narrativa, técnica ou pedagógica.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    view_labels = {
        "pais por pais": "País por país",
        "comparar paises": "Comparar países",
        "metodologia": "Metodologia",
    }
    detail_labels = {
        "leitura simples": "Simples",
        "modo tecnico": "Técnico",
        "meu aprendizado": "Meu aprendizado",
    }

    with st.container(border=True):
        view_col, country_col, detail_col = st.columns([1.35, 1.15, 1.25], vertical_alignment="top")
        with view_col:
            view_mode = st.segmented_control(
                "Ver análise",
                list(view_labels),
                default="pais por pais",
                format_func=lambda value: view_labels[value],
                key="top_view_mode",
                width="stretch",
            )
        with country_col:
            if view_mode == "pais por pais":
                country = st.segmented_control(
                    "País",
                    ["BRA", "USA", "ARG"],
                    default="BRA",
                    format_func=lambda code: COUNTRY_LABELS[code],
                    key="top_country",
                    width="stretch",
                )
            else:
                country = None
                st.markdown("##### País")
                st.caption("Este recorte usa todos os países.")
        with detail_col:
            explanation_mode = st.segmented_control(
                "Detalhe",
                list(detail_labels),
                default="leitura simples",
                format_func=lambda value: detail_labels[value],
                key="top_detail_mode",
                width="stretch",
            )

    technical_mode = explanation_mode == "modo tecnico"
    learning_mode = explanation_mode == "meu aprendizado"
    return view_mode, country, technical_mode, learning_mode


def main() -> None:
    data = load_data(data_signature())
    header()
    view_mode, country, technical_mode, learning_mode = top_filter_controls()

    metric_row(data, learning_mode)
    detail_mode_note(technical_mode, learning_mode)

    if view_mode == "pais por pais" and country:
        country_view(data, country, technical_mode, learning_mode)
    elif view_mode == "comparar paises":
        comparison_view(data, technical_mode, learning_mode)
    else:
        methodology_view(technical_mode, learning_mode)


if __name__ == "__main__":
    main()
