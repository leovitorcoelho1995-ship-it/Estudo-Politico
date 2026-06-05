from __future__ import annotations

import argparse
import time
from pathlib import Path

import pandas as pd
from pytrends.request import TrendReq


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
RAW_DIR = PROJECT_ROOT / "data" / "raw"

EVENTS_PATH = PROCESSED_DIR / "political_events_processed.csv"
RAW_OUTPUT_DIR = RAW_DIR / "trends"
RELATED_OUTPUT_PATH = RAW_OUTPUT_DIR / "trends_related_queries.csv"

GEO_MAP = {
    "BRA": "BR",
    "USA": "US",
    "ARG": "AR",
}

SEED_TERMS = {
    "BRA_2016_08_31": ["impeachment dilma", "dilma impeachment", "temer"],
    "BRA_2016_10_19": ["copom selic", "corte selic", "taxa selic"],
    "BRA_2016_12_15": ["teto de gastos", "pec do teto", "gastos publicos"],
    "BRA_2017_05_17": ["joesley day", "temer joesley", "jbs temer"],
    "BRA_2017_07_13": ["reforma trabalhista", "terceirizacao", "clt reforma"],
    "BRA_2018_04_07": ["lula preso", "prisao lula", "lava jato"],
    "BRA_2018_05_21": ["greve caminhoneiros", "caminhoneiros", "diesel greve"],
    "BRA_2018_05_27": ["subvencao diesel", "diesel caminhoneiros", "preco diesel"],
    "BRA_2018_09_06": ["facada bolsonaro", "bolsonaro facada", "juiz de fora"],
    "BRA_2018_10_28": ["bolsonaro", "eleicao 2018", "paulo guedes"],
    "BRA_2020_03_11": ["coronavirus brasil", "pandemia brasil", "covid brasil"],
    "BRA_2020_04_02": ["auxilio emergencial", "coronavirus auxilio", "caixa auxilio"],
    "BRA_2021_02_19": ["petrobras", "castello branco petrobras", "preco combustivel"],
    "BRA_2021_03_17": ["alta selic", "copom selic", "taxa selic"],
    "BRA_2021_04_27": ["cpi covid", "vacina covid", "pandemia brasil"],
    "BRA_2021_12_02": ["pec precatorios", "precatorios", "auxilio brasil"],
    "BRA_2021_2022": ["preco combustivel", "preco gasolina", "gasolina brasil"],
    "BRA_2022_02_24": ["guerra ucrania", "preco gasolina", "petroleo"],
    "BRA_2022_06_23": ["icms gasolina", "preco gasolina", "combustivel"],
    "BRA_2022_07_14": ["pec beneficios", "auxilio brasil", "pec kamikaze"],
    "BRA_2022_10_30": ["lula", "bolsonaro", "eleicao 2022"],
    "BRA_2022_12_09": ["fernando haddad fazenda", "haddad ministro", "ministro da fazenda"],
    "BRA_2022_12_21": ["pec transicao", "orcamento", "bolsa familia"],
    "BRA_2023_01_08": ["8 de janeiro", "invasao brasilia", "atos antidemocraticos"],
    "BRA_2023_03_30": ["arcabouco fiscal", "novo arcabouco fiscal", "haddad"],
    "BRA_2023_05_16": ["preco combustivel", "petrobras combustivel", "politica de precos petrobras"],
    "BRA_2023_08_02": ["corte selic", "copom selic", "taxa selic"],
    "BRA_2023_08_31": ["arcabouco fiscal", "novo arcabouco fiscal", "regra fiscal"],
    "BRA_2023_12_20": ["reforma tributaria", "tributaria", "imposto"],
    "BRA_2024_09_18": ["alta selic", "copom selic", "taxa selic"],
    "BRA_2024_10": ["eleicoes municipais", "prefeito", "eleicao municipal"],
    "USA_2016_11_08": ["trump election", "donald trump", "hillary clinton"],
    "USA_2016_12_14": ["fed rate hike", "interest rates", "federal reserve"],
    "USA_2017_03_15": ["fed rate hike", "interest rates", "federal reserve"],
    "USA_2020_03": ["covid stimulus", "covid unemployment", "pandemic usa"],
    "USA_2017_12_22": ["tax cuts jobs act", "trump tax cuts", "tax reform"],
    "USA_2018_03": ["china tariffs", "trade war", "trump tariffs"],
    "USA_2018_07_06": ["china tariffs", "trade war", "trump tariffs"],
    "USA_2018_12_19": ["fed rate hike", "stock market", "interest rates"],
    "USA_2019_07_31": ["fed rate cut", "interest rates", "federal reserve"],
    "USA_2020_03_03": ["fed emergency rate cut", "interest rates", "federal reserve"],
    "USA_2020_03_15": ["fed zero rates", "quantitative easing", "federal reserve"],
    "USA_2020_03_27": ["cares act", "stimulus check", "covid stimulus"],
    "USA_2020_11_03": ["biden election", "trump biden", "election 2020"],
    "USA_2020_12_27": ["stimulus check", "covid relief bill", "second stimulus"],
    "USA_2021_01_06": ["capitol riot", "january 6", "capitol attack"],
    "USA_2021_03_11": ["stimulus check", "american rescue plan", "biden stimulus"],
    "USA_2021_11_15": ["infrastructure bill", "biden infrastructure", "infrastructure act"],
    "USA_2021_2022": ["inflation", "gas prices", "fed rates"],
    "USA_2022_03": ["fed rates", "interest rates", "inflation"],
    "USA_2022_03_16": ["fed rate hike", "interest rates", "inflation"],
    "USA_2022_06_15": ["fed 75 basis points", "fed rate hike", "interest rates"],
    "USA_2022_08_16": ["inflation reduction act", "climate bill", "biden inflation act"],
    "USA_2023_03_10": ["silicon valley bank", "svb collapse", "bank failure"],
    "USA_2023_05_01": ["first republic bank", "jpmorgan first republic", "bank failure"],
    "USA_2023_06_03": ["debt ceiling", "debt ceiling deal", "us debt limit"],
    "USA_2023_07_26": ["fed rate hike", "interest rates", "federal reserve"],
    "USA_2024_09_18": ["fed rate cut", "interest rates", "federal reserve"],
    "USA_2024_11": ["presidential election", "trump biden", "election 2024"],
    "ARG_2018_06": ["fmi argentina", "dolar argentina", "crisis argentina"],
    "ARG_2018_08_30": ["dolar argentina", "crisis cambiaria", "tasas argentina"],
    "ARG_2019_08_11": ["paso argentina", "macri fernandez", "elecciones argentina"],
    "ARG_2019_09_01": ["cepo cambiario", "dolar argentina", "control de cambios"],
    "ARG_2019_10_27": ["alberto fernandez", "elecciones argentina", "macri fernandez"],
    "ARG_2020_03": ["coronavirus argentina", "cuarentena argentina", "pandemia argentina"],
    "ARG_2020_05_22": ["default argentina", "deuda argentina", "bonos argentina"],
    "ARG_2020_08_04": ["deuda argentina", "reestructuracion deuda", "bonistas argentina"],
    "ARG_2022_03": ["fmi argentina", "deuda argentina", "acuerdo fmi"],
    "ARG_2022_07_02": ["martin guzman", "renuncia guzman", "ministro economia argentina"],
    "ARG_2022_08_03": ["sergio massa", "ministro economia", "dolar argentina"],
    "ARG_2023_08": ["milei", "dolarizacion", "primarias argentina"],
    "ARG_2023_08_14": ["devaluacion argentina", "dolar argentina", "paso milei"],
    "ARG_2023_11_19": ["milei presidente", "javier milei", "dolarizacion argentina"],
    "ARG_2023_12": ["devaluacion argentina", "dolar argentina", "caputo"],
    "ARG_2023_12_12": ["caputo", "devaluacion argentina", "dolar argentina"],
    "ARG_2023_12_20": ["dnu milei", "milei decreto", "desregulacion"],
    "ARG_2024_01_24": ["paro general", "cgt", "milei protestas"],
    "ARG_2024_04_30": ["ley bases", "milei ley bases", "reformas milei"],
    "ARG_2024_06_12": ["ley bases senado", "ley bases", "milei"],
}


def fallback_terms(event_name: str, country_code: str) -> list[str]:
    suffix = {
        "BRA": "brasil",
        "USA": "usa",
        "ARG": "argentina",
    }.get(country_code, "")
    base = event_name.lower()
    return [base, f"{base} {suffix}".strip()]


def event_timeframe(start_date: pd.Timestamp, end_date: pd.Timestamp, padding_days: int) -> str:
    start = start_date - pd.Timedelta(days=padding_days)
    end = end_date + pd.Timedelta(days=padding_days)
    return f"{start:%Y-%m-%d} {end:%Y-%m-%d}"


def collect_for_event(
    pytrends: TrendReq,
    event: pd.Series,
    terms: list[str],
    padding_days: int,
) -> tuple[pd.DataFrame, list[dict]]:
    geo = GEO_MAP[event["country_code"]]
    timeframe = event_timeframe(event["start_date"], event["end_date"], padding_days)
    terms = terms[:5]

    pytrends.build_payload(terms, geo=geo, timeframe=timeframe)
    interest = pytrends.interest_over_time()
    related = pytrends.related_queries()

    if interest.empty:
        return pd.DataFrame(), []

    interest = interest.reset_index()
    is_partial = interest["isPartial"] if "isPartial" in interest.columns else False
    rows = []
    for term in terms:
        if term not in interest.columns:
            continue
        term_rows = pd.DataFrame(
            {
                "event_id": event["event_id"],
                "country_code": event["country_code"],
                "country_name": event["country_name"],
                "event_name": event["event_name"],
                "event_start_date": event["start_date"],
                "event_end_date": event["end_date"],
                "geo": geo,
                "timeframe": timeframe,
                "date": interest["date"],
                "term": term,
                "interest": interest[term],
                "is_partial": is_partial,
            }
        )
        rows.append(term_rows)

    related_rows = []
    for term, payload in related.items():
        for kind in ["top", "rising"]:
            frame = payload.get(kind)
            if frame is None or frame.empty:
                continue
            for _, row in frame.iterrows():
                related_rows.append(
                    {
                        "event_id": event["event_id"],
                        "country_code": event["country_code"],
                        "event_name": event["event_name"],
                        "seed_term": term,
                        "query_type": kind,
                        "query": row.get("query"),
                        "value": row.get("value"),
                    }
                )

    if not rows:
        return pd.DataFrame(), related_rows
    return pd.concat(rows, ignore_index=True), related_rows


def collect_trends(
    event_ids: list[str] | None = None,
    limit: int | None = None,
    padding_days: int = 180,
    sleep_seconds: float = 8.0,
    skip_existing: bool = True,
    dry_run: bool = False,
) -> None:
    events = pd.read_csv(EVENTS_PATH)
    events["start_date"] = pd.to_datetime(events["start_date"])
    events["end_date"] = pd.to_datetime(events["end_date"])
    events = events[events["country_code"].isin(GEO_MAP)].copy()

    if event_ids:
        events = events[events["event_id"].isin(event_ids)].copy()
    if limit is not None:
        events = events.head(limit).copy()

    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pytrends = TrendReq(hl="pt-BR", tz=-180)
    all_related_rows = []

    for _, event in events.iterrows():
        event_id = event["event_id"]
        output_path = RAW_OUTPUT_DIR / f"trends_{event_id}.csv"
        terms = SEED_TERMS.get(event_id, fallback_terms(event["event_name"], event["country_code"]))
        print(f"{event_id}: {terms}")

        if dry_run:
            continue
        if skip_existing and output_path.exists():
            print(f"  pulando, ja existe: {output_path}")
            continue

        try:
            interest, related_rows = collect_for_event(pytrends, event, terms, padding_days)
        except Exception as exc:
            print(f"  falha na coleta: {exc}")
            continue

        if interest.empty:
            print("  sem dados retornados")
            continue

        interest.to_csv(output_path, index=False, date_format="%Y-%m-%d")
        all_related_rows.extend(related_rows)
        print(f"  salvo: {output_path} ({len(interest)} linhas)")
        time.sleep(sleep_seconds)

    if all_related_rows:
        related_df = pd.DataFrame(all_related_rows)
        if RELATED_OUTPUT_PATH.exists():
            existing = pd.read_csv(RELATED_OUTPUT_PATH)
            related_df = pd.concat([existing, related_df], ignore_index=True)
            related_df = related_df.drop_duplicates()
        related_df.to_csv(RELATED_OUTPUT_PATH, index=False)
        print(f"Consultas relacionadas salvas em: {RELATED_OUTPUT_PATH}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Coleta Google Trends por evento politico.")
    parser.add_argument("--event-id", action="append", help="Coletar apenas um event_id; pode repetir.")
    parser.add_argument("--limit", type=int, help="Limitar numero de eventos.")
    parser.add_argument("--padding-days", type=int, default=180)
    parser.add_argument("--sleep-seconds", type=float, default=8.0)
    parser.add_argument("--no-skip-existing", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    collect_trends(
        event_ids=args.event_id,
        limit=args.limit,
        padding_days=args.padding_days,
        sleep_seconds=args.sleep_seconds,
        skip_existing=not args.no_skip_existing,
        dry_run=args.dry_run,
    )
