from __future__ import annotations

import csv
from datetime import date
from http.client import RemoteDisconnected
from pathlib import Path
from time import sleep
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

FRED_SERIES = {
    "cpi": {"code": "CPIAUCSL", "name": "Consumer Price Index for All Urban Consumers"},
    "fed_funds": {"code": "FEDFUNDS", "name": "Effective Federal Funds Rate"},
    "unemployment": {"code": "UNRATE", "name": "Unemployment Rate"},
    "gasoline": {"code": "GASREGW", "name": "US Regular All Formulations Gas Price"},
    "real_gdp": {"code": "GDPC1", "name": "Real Gross Domestic Product"},
}


def fetch_fred_csv(series_code: str, max_attempts: int = 4) -> list[dict[str, str]]:
    params = urlencode({"id": series_code})
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?{params}"
    request = Request(url, headers={"User-Agent": "radar-politico-economico/0.1"})

    for attempt in range(1, max_attempts + 1):
        try:
            with urlopen(request, timeout=60) as response:
                text = response.read().decode("utf-8-sig")
            return list(csv.DictReader(text.splitlines()))
        except (HTTPError, RemoteDisconnected, TimeoutError, URLError) as error:
            if attempt == max_attempts:
                raise

            wait_seconds = attempt * 3
            print(
                f"  Tentativa {attempt} falhou para FRED {series_code}: {error}. "
                f"Nova tentativa em {wait_seconds}s..."
            )
            sleep(wait_seconds)

    return []


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def collect_all(start_date: str = "2016-01-01", end_date: str | None = None) -> None:
    if end_date is None:
        end_date = date.today().isoformat()

    combined_rows: list[dict[str, str]] = []

    for slug, metadata in FRED_SERIES.items():
        code = metadata["code"]
        name = metadata["name"]
        print(f"Baixando FRED: {name} ({code})...")

        observations = fetch_fred_csv(code)
        rows = []
        for item in observations:
            obs_date = item.get("observation_date", "")
            value = item.get(code, "")

            if obs_date < start_date or obs_date > end_date:
                continue
            if value in {"", "."}:
                continue

            row = {
                "country_code": "USA",
                "country_name": "United States",
                "date": obs_date,
                "series_slug": slug,
                "series_code": code,
                "series_name": name,
                "value": value,
                "source": "FRED",
            }
            rows.append(row)
            combined_rows.append(row)

        raw_path = RAW_DIR / f"fred_{slug}.csv"
        write_csv(
            raw_path,
            rows,
            [
                "country_code",
                "country_name",
                "date",
                "series_slug",
                "series_code",
                "series_name",
                "value",
                "source",
            ],
        )
        sleep(1)

    processed_path = PROCESSED_DIR / "fred_indicators_usa.csv"
    write_csv(
        processed_path,
        combined_rows,
        [
            "country_code",
            "country_name",
            "date",
            "series_slug",
            "series_code",
            "series_name",
            "value",
            "source",
        ],
    )
    print(f"Arquivo consolidado salvo em: {processed_path}")


if __name__ == "__main__":
    collect_all()
