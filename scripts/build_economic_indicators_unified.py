from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

BCB_PATH = PROCESSED_DIR / "bcb_sgs_analysis_ready.csv"
FRED_PATH = PROCESSED_DIR / "fred_indicators_usa.csv"
WORLD_BANK_PATH = PROCESSED_DIR / "world_bank_indicators.csv"
BLUELYTICS_PATH = PROCESSED_DIR / "bluelytics_indicators_argentina.csv"
OUTPUT_PATH = PROCESSED_DIR / "economic_indicators_unified.csv"
SUMMARY_PATH = PROCESSED_DIR / "economic_indicators_unified_summary.csv"


BCB_METADATA = {
    "cambio": {
        "country_code": "BRA",
        "country_name": "Brazil",
        "frequency": "daily",
        "indicator_group": "exchange_rate",
        "unit": "BRL per USD",
    },
    "gasolina": {
        "country_code": "BRA",
        "country_name": "Brazil",
        "frequency": "monthly",
        "indicator_group": "gasoline",
        "unit": "index_or_price",
    },
    "ipca": {
        "country_code": "BRA",
        "country_name": "Brazil",
        "frequency": "monthly",
        "indicator_group": "inflation",
        "unit": "monthly_pct",
    },
    "selic": {
        "country_code": "BRA",
        "country_name": "Brazil",
        "frequency": "daily",
        "indicator_group": "interest_rate",
        "unit": "daily_rate",
    },
}


FRED_METADATA = {
    "cpi": {
        "frequency": "monthly",
        "indicator_group": "inflation",
        "unit": "index",
    },
    "fed_funds": {
        "frequency": "monthly",
        "indicator_group": "interest_rate",
        "unit": "annual_pct",
    },
    "gasoline": {
        "frequency": "weekly",
        "indicator_group": "gasoline",
        "unit": "USD per gallon",
    },
    "real_gdp": {
        "frequency": "quarterly",
        "indicator_group": "gdp",
        "unit": "billions chained 2017 USD",
    },
    "unemployment": {
        "frequency": "monthly",
        "indicator_group": "unemployment",
        "unit": "annual_pct",
    },
}


BLUELYTICS_METADATA = {
    "dolar_blue": {
        "country_code": "ARG",
        "country_name": "Argentina",
        "frequency": "daily",
        "indicator_group": "exchange_rate",
        "unit": "ARS per USD",
    },
    "dolar_oficial": {
        "country_code": "ARG",
        "country_name": "Argentina",
        "frequency": "daily",
        "indicator_group": "exchange_rate",
        "unit": "ARS per USD",
    },
}


WORLD_BANK_METADATA = {
    "central_government_debt_pct_gdp": {
        "frequency": "annual",
        "indicator_group": "debt",
        "unit": "pct_gdp",
    },
    "gdp_growth_annual_pct": {
        "frequency": "annual",
        "indicator_group": "gdp",
        "unit": "annual_pct",
    },
    "gdp_per_capita_current_usd": {
        "frequency": "annual",
        "indicator_group": "gdp",
        "unit": "current_usd",
    },
    "inflation_annual_pct": {
        "frequency": "annual",
        "indicator_group": "inflation",
        "unit": "annual_pct",
    },
    "unemployment_pct": {
        "frequency": "annual",
        "indicator_group": "unemployment",
        "unit": "annual_pct",
    },
}


OUTPUT_COLUMNS = [
    "country_code",
    "country_name",
    "date",
    "year",
    "frequency",
    "indicator_group",
    "indicator_slug",
    "indicator_code",
    "indicator_name",
    "value",
    "unit",
    "source",
]


def normalize_bcb() -> pd.DataFrame:
    df = pd.read_csv(BCB_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    for column in ["country_code", "country_name", "frequency", "indicator_group", "unit"]:
        df[column] = df["series_slug"].map(
            {slug: metadata[column] for slug, metadata in BCB_METADATA.items()}
        )

    df = df.rename(
        columns={
            "series_slug": "indicator_slug",
            "series_code": "indicator_code",
            "series_name": "indicator_name",
        }
    )
    df["source"] = "Banco Central do Brasil SGS"
    df["year"] = df["date"].dt.year

    return df[OUTPUT_COLUMNS]


def normalize_fred() -> pd.DataFrame:
    df = pd.read_csv(FRED_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    for column in ["frequency", "indicator_group", "unit"]:
        df[column] = df["series_slug"].map(
            {slug: metadata[column] for slug, metadata in FRED_METADATA.items()}
        )

    df = df.rename(
        columns={
            "series_slug": "indicator_slug",
            "series_code": "indicator_code",
            "series_name": "indicator_name",
        }
    )
    df["year"] = df["date"].dt.year

    return df[OUTPUT_COLUMNS]


def normalize_bluelytics() -> pd.DataFrame:
    df = pd.read_csv(BLUELYTICS_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    for column in ["country_code", "country_name", "frequency", "indicator_group", "unit"]:
        df[column] = df["series_slug"].map(
            {slug: metadata[column] for slug, metadata in BLUELYTICS_METADATA.items()}
        )

    df = df.rename(
        columns={
            "series_slug": "indicator_slug",
            "series_code": "indicator_code",
            "series_name": "indicator_name",
        }
    )
    df["year"] = df["date"].dt.year

    return df[OUTPUT_COLUMNS]


def normalize_world_bank() -> pd.DataFrame:
    df = pd.read_csv(WORLD_BANK_PATH)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"]).copy()
    df["year"] = pd.to_numeric(df["year"], errors="raise").astype("int64")
    df["date"] = pd.to_datetime(df["year"].astype(str) + "-01-01")

    for column in ["frequency", "indicator_group", "unit"]:
        df[column] = df["indicator_slug"].map(
            {slug: metadata[column] for slug, metadata in WORLD_BANK_METADATA.items()}
        )

    df = df.rename(
        columns={
            "indicator_code": "indicator_code",
            "indicator_name": "indicator_name",
        }
    )

    return df[OUTPUT_COLUMNS]


def build_unified() -> pd.DataFrame:
    frames = [normalize_bcb(), normalize_fred(), normalize_world_bank()]
    if BLUELYTICS_PATH.exists():
        frames.append(normalize_bluelytics())

    unified = pd.concat(frames, ignore_index=True)
    unified = unified.dropna(subset=["value", "country_code", "indicator_group"])
    unified = unified.sort_values(["country_code", "indicator_group", "indicator_slug", "date"])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    unified.to_csv(OUTPUT_PATH, index=False, date_format="%Y-%m-%d")

    summary = (
        unified.groupby(
            ["country_code", "source", "indicator_group", "indicator_slug", "frequency"],
            as_index=False,
        )
        .agg(
            rows=("value", "size"),
            start_date=("date", "min"),
            end_date=("date", "max"),
            min_value=("value", "min"),
            max_value=("value", "max"),
        )
        .sort_values(["country_code", "source", "indicator_group", "indicator_slug"])
    )
    summary.to_csv(SUMMARY_PATH, index=False, date_format="%Y-%m-%d")

    return unified


if __name__ == "__main__":
    result = build_unified()
    print(f"Linhas unificadas: {len(result)}")
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
    print(f"Resumo salvo em: {SUMMARY_PATH}")
