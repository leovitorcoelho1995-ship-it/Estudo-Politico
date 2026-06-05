from __future__ import annotations

import csv
import json
from http.client import RemoteDisconnected
from datetime import date
from datetime import datetime
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

BCB_SERIES = {
    "ipca": {"code": 433, "name": "IPCA"},
    "selic": {"code": 11, "name": "Selic"},
    "cambio": {"code": 1, "name": "Taxa de cambio"},
    "gasolina": {"code": 24369, "name": "Gasolina"},
}


def parse_brazilian_date(value: str) -> date:
    return datetime.strptime(value, "%d/%m/%Y").date()


def format_brazilian_date(value: date) -> str:
    return value.strftime("%d/%m/%Y")


def iter_year_chunks(start_date: str, end_date: str):
    start = parse_brazilian_date(start_date)
    end = parse_brazilian_date(end_date)
    current = start

    while current <= end:
        chunk_end = min(date(current.year, 12, 31), end)
        yield format_brazilian_date(current), format_brazilian_date(chunk_end)
        current = date(current.year + 1, 1, 1)


def fetch_sgs_series_chunk(
    code: int,
    start_date: str,
    end_date: str,
    max_attempts: int = 4,
) -> list[dict[str, str]]:
    params = urlencode(
        {
            "formato": "json",
            "dataInicial": start_date,
            "dataFinal": end_date,
        }
    )
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados?{params}"
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "radar-politico-economico/0.1",
        },
    )

    for attempt in range(1, max_attempts + 1):
        try:
            with urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, RemoteDisconnected, URLError) as error:
            if attempt == max_attempts:
                raise

            wait_seconds = attempt * 3
            print(
                f"  Tentativa {attempt} falhou para SGS {code} "
                f"({start_date} a {end_date}): {error}. "
                f"Nova tentativa em {wait_seconds}s..."
            )
            sleep(wait_seconds)

    return []


def fetch_sgs_series(code: int, start_date: str, end_date: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    for chunk_start, chunk_end in iter_year_chunks(start_date, end_date):
        rows.extend(fetch_sgs_series_chunk(code, chunk_start, chunk_end))
        sleep(1)

    return rows


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def collect_all(start_date: str = "01/01/2016", end_date: str | None = None) -> None:
    if end_date is None:
        today = date.today()
        end_date = today.strftime("%d/%m/%Y")

    combined_rows: list[dict[str, str]] = []

    for slug, metadata in BCB_SERIES.items():
        code = metadata["code"]
        name = metadata["name"]
        print(f"Baixando {name} (SGS {code})...")

        rows = fetch_sgs_series(code, start_date, end_date)
        raw_rows = [
            {
                "date": row["data"],
                "value": row["valor"].replace(",", "."),
                "series_code": str(code),
                "series_slug": slug,
                "series_name": name,
            }
            for row in rows
        ]

        raw_path = RAW_DIR / f"bcb_sgs_{slug}.csv"
        write_csv(
            raw_path,
            raw_rows,
            ["date", "value", "series_code", "series_slug", "series_name"],
        )
        combined_rows.extend(raw_rows)

    processed_path = PROCESSED_DIR / "bcb_sgs_indicators.csv"
    write_csv(
        processed_path,
        combined_rows,
        ["date", "value", "series_code", "series_slug", "series_name"],
    )

    print(f"Arquivos brutos salvos em: {RAW_DIR}")
    print(f"Arquivo consolidado salvo em: {processed_path}")


if __name__ == "__main__":
    collect_all()
