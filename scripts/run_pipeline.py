from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable

COLLECTION_STEPS = [
    "collect_bcb_sgs.py",
    "prepare_bcb_sgs.py",
    "summarize_bcb_sgs.py",
    "collect_world_bank.py",
    "collect_fred.py",
    "collect_bluelytics.py",
]

PROCESSING_STEPS = [
    "build_economic_indicators_unified.py",
    "build_normalized_economic_indicators.py",
    "prepare_political_events.py",
    "build_event_sources_template.py",
    "build_event_economic_impact.py",
    "build_normalized_event_impact.py",
    "build_event_statistical_tests.py",
    "build_event_window_contamination.py",
    "build_event_shock_persistence.py",
    "build_event_study_series.py",
    "build_event_study_aggregates.py",
    "build_trends_layer.py",
    "build_trends_event_alignment.py",
    "build_trends_coverage.py",
    "build_event_final_score.py",
    "build_historical_robustness.py",
    "build_annual_event_impact.py",
    "build_rankings.py",
    "build_exploratory_charts.py",
    "build_project_audit.py",
]


def run_step(script_name: str) -> None:
    script_path = PROJECT_ROOT / "scripts" / script_name
    print(f"\n=== {script_name} ===", flush=True)
    subprocess.run([PYTHON, str(script_path)], cwd=PROJECT_ROOT, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Roda o pipeline do Radar Politico-Economico.")
    parser.add_argument(
        "--with-collection",
        action="store_true",
        help="Roda tambem coletas externas BCB/FRED/Bluelytics/World Bank.",
    )
    parser.add_argument(
        "--skip-charts",
        action="store_true",
        help="Pula graficos exploratorios HTML.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    steps = []
    if args.with_collection:
        steps.extend(COLLECTION_STEPS)

    steps.extend(PROCESSING_STEPS)
    if args.skip_charts:
        steps = [step for step in steps if step != "build_exploratory_charts.py"]

    for step in steps:
        run_step(step)

    print("\nPipeline concluido.", flush=True)


if __name__ == "__main__":
    main()
