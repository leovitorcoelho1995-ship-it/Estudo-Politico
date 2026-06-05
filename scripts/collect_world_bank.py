from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

COUNTRIES = {
    "BRA": "Brazil",
    "USA": "United States",
    "ARG": "Argentina",
}

WORLD_BANK_INDICATORS = {
    "inflation_annual_pct": {
        "code": "FP.CPI.TOTL.ZG",
        "name": "Inflation, consumer prices (annual %)",
    },
    "unemployment_pct": {
        "code": "SL.UEM.TOTL.ZS",
        "name": "Unemployment, total (% of total labor force)",
    },
    "gdp_growth_annual_pct": {
        "code": "NY.GDP.MKTP.KD.ZG",
        "name": "GDP growth (annual %)",
    },
    "gdp_per_capita_current_usd": {
        "code": "NY.GDP.PCAP.CD",
        "name": "GDP per capita (current US$)",
    },
    "central_government_debt_pct_gdp": {
        "code": "GC.DOD.TOTL.GD.ZS",
        "name": "Central government debt, total (% of GDP)",
    },
}


def fetch_indicator(indicator_code: str, start_year: int = 2016, end_year: int = 2026) -> list[dict]:
    country_path = ";".join(COUNTRIES)
    params = urlencode(
        {
            "format": "json",
            "mrv": 10,
            "per_page": 1000,
        }
    )
    url = f"https://api.worldbank.org/v2/country/{country_path}/indicator/{indicator_code}?{params}"
    request = Request(url, headers={"User-Agent": "radar-politico-economico/0.1"})

    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    if not isinstance(payload, list) or len(payload) < 2:
        return []

    return payload[1] or []


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def collect_all() -> None:
    combined_rows: list[dict[str, str]] = []

    for slug, metadata in WORLD_BANK_INDICATORS.items():
        code = metadata["code"]
        name = metadata["name"]
        print(f"Baixando World Bank: {name} ({code})...")
        observations = fetch_indicator(code)

        rows = []
        for item in observations:
            country_code = item.get("countryiso3code", "")
            year = item.get("date", "")
            value = item.get("value")

            row = {
                "country_code": country_code,
                "country_name": COUNTRIES.get(country_code, item.get("country", {}).get("value", "")),
                "year": year,
                "indicator_slug": slug,
                "indicator_code": code,
                "indicator_name": name,
                "value": "" if value is None else str(value),
                "source": "World Bank API",
            }
            rows.append(row)
            combined_rows.append(row)

        raw_path = RAW_DIR / f"world_bank_{slug}.csv"
        write_csv(
            raw_path,
            rows,
            [
                "country_code",
                "country_name",
                "year",
                "indicator_slug",
                "indicator_code",
                "indicator_name",
                "value",
                "source",
            ],
        )

    processed_path = PROCESSED_DIR / "world_bank_indicators.csv"
    write_csv(
        processed_path,
        combined_rows,
        [
            "country_code",
            "country_name",
            "year",
            "indicator_slug",
            "indicator_code",
            "indicator_name",
            "value",
            "source",
        ],
    )
    print(f"Arquivo consolidado salvo em: {processed_path}")


if __name__ == "__main__":
    collect_all()
