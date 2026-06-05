from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "bcb_sgs_indicators.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "bcb_sgs_analysis_ready.csv"


def prepare_bcb_sgs(input_path: Path = INPUT_PATH, output_path: Path = OUTPUT_PATH) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["series_code"] = pd.to_numeric(df["series_code"], errors="raise").astype("int64")

    df = df[
        [
            "date",
            "series_slug",
            "series_code",
            "series_name",
            "value",
        ]
    ].sort_values(["series_slug", "date"])

    if df["value"].isna().any():
        missing_count = int(df["value"].isna().sum())
        raise ValueError(f"Foram encontrados {missing_count} valores ausentes.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, date_format="%Y-%m-%d")
    return df


if __name__ == "__main__":
    result = prepare_bcb_sgs()
    print(f"Linhas preparadas: {len(result)}")
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
