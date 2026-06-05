from __future__ import annotations

import csv
import json
from http.client import RemoteDisconnected
from datetime import date
from pathlib import Path
from time import sleep
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

EVOLUTION_URL = "https://api.bluelytics.com.ar/v2/evolution.json"

BLUELYTICS_SERIES = {
    "Oficial": {
        "series_slug": "dolar_oficial",
        "series_code": "bluelytics_oficial_sell",
        "series_name": "Dolar oficial Argentina",
    },
    "Blue": {
        "series_slug": "dolar_blue",
        "series_code": "bluelytics_blue_sell",
        "series_name": "Dolar blue Argentina",
    },
}


def fetch_evolution(max_attempts: int = 4) -> list[dict[str, object]]:
    request = Request(
        EVOLUTION_URL,
        headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 radar-politico-economico/0.1",
        },
    )

    for attempt in range(1, max_attempts + 1):
        try:
            with urlopen(request, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, RemoteDisconnected, TimeoutError, URLError) as error:
            if attempt == max_attempts:
                raise

            wait_seconds = attempt * 4
            print(
                f"  Tentativa {attempt} falhou para Bluelytics: {error}. "
                f"Nova tentativa em {wait_seconds}s..."
            )
            sleep(wait_seconds)

    return []


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def collect_all(start_date: str = "2016-01-01", end_date: str | None = None) -> None:
    if end_date is None:
        end_date = date.today().isoformat()

    print("Baixando Bluelytics: cambio oficial e dolar blue Argentina...")
    observations = fetch_evolution()

    raw_rows: list[dict[str, object]] = []
    processed_rows: list[dict[str, object]] = []

    for item in observations:
        observation_date = str(item.get("date", ""))
        source_name = str(item.get("source", item.get("source_name", "")))

        if observation_date < start_date or observation_date > end_date:
            continue
        if source_name not in BLUELYTICS_SERIES:
            continue

        value_sell = item.get("value_sell")
        value_buy = item.get("value_buy")
        if value_sell is None:
            continue

        raw_row = {
            "date": observation_date,
            "source_name": source_name,
            "value_sell": value_sell,
            "value_buy": "" if value_buy is None else value_buy,
        }
        raw_rows.append(raw_row)

        metadata = BLUELYTICS_SERIES[source_name]
        processed_rows.append(
            {
                "country_code": "ARG",
                "country_name": "Argentina",
                "date": observation_date,
                "series_slug": metadata["series_slug"],
                "series_code": metadata["series_code"],
                "series_name": metadata["series_name"],
                "value": value_sell,
                "source": "Bluelytics",
            }
        )

    raw_rows = sorted(raw_rows, key=lambda row: (row["source_name"], row["date"]))
    processed_rows = sorted(processed_rows, key=lambda row: (row["series_slug"], row["date"]))

    write_csv(
        RAW_DIR / "bluelytics_evolution.csv",
        raw_rows,
        ["date", "source_name", "value_sell", "value_buy"],
    )
    write_csv(
        PROCESSED_DIR / "bluelytics_indicators_argentina.csv",
        processed_rows,
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

    print(f"Observacoes brutas salvas: {len(raw_rows)}")
    print(f"Linhas processadas salvas: {len(processed_rows)}")
    print(f"Arquivo bruto salvo em: {RAW_DIR / 'bluelytics_evolution.csv'}")
    print(f"Arquivo consolidado salvo em: {PROCESSED_DIR / 'bluelytics_indicators_argentina.csv'}")


if __name__ == "__main__":
    collect_all()
