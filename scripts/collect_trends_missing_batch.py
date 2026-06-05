from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from collect_trends import collect_trends


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
TRENDS_COVERAGE_PATH = PROCESSED_DIR / "trends_coverage.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Coleta um lote pequeno de eventos pendentes no Google Trends.")
    parser.add_argument("--country-code", choices=["ARG", "BRA", "USA"], help="Filtra pais.")
    parser.add_argument("--batch-size", type=int, default=5, help="Numero maximo de eventos no lote.")
    parser.add_argument("--sleep-seconds", type=float, default=20.0, help="Pausa entre eventos.")
    parser.add_argument("--padding-days", type=int, default=180)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    coverage = pd.read_csv(TRENDS_COVERAGE_PATH)
    pending = coverage[coverage["trends_status"] == "missing_collection"].copy()
    if args.country_code:
        pending = pending[pending["country_code"] == args.country_code].copy()

    event_ids = pending["event_id"].head(args.batch_size).tolist()
    if not event_ids:
        print("Nenhum evento pendente encontrado para os filtros informados.")
        return

    print("Eventos selecionados:")
    for event_id in event_ids:
        print(f"- {event_id}")

    collect_trends(
        event_ids=event_ids,
        padding_days=args.padding_days,
        sleep_seconds=args.sleep_seconds,
        skip_existing=True,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
