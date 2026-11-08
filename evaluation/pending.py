"""Run a frozen, unlabeled Harbor task and seal the submitted probabilities."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess

from production.build import ROOT
from production.intake import slug, submit, trusted_case
from production.score import read_prediction
from evaluation.cli.client import BIN


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", type=Path)
    parser.add_argument("--entrant", required=True)
    parser.add_argument("--harness", choices=BIN, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    trusted_case(args.case)
    entrant = slug(args.entrant)
    if (args.case / "result.json").exists() or (
        args.case / "receipts" / (entrant + ".json")
    ).exists():
        raise ValueError("Case has settled or entrant has already submitted")
    mode = "vendor" if args.harness == "cursor" else "live"
    credential = "CURSOR_API_KEY" if mode == "vendor" else "DEEPSEEK_API_KEY"
    if not shutil.which("harbor") or not os.environ.get(credential):
        raise ValueError(f"Requires Harbor 0.25.0, Docker and {credential}")
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    env = {
        **os.environ,
        "PYTHONPATH": str(ROOT),
        "BENCH_CLI": args.harness,
        "BENCH_MODE": mode,
        "BENCH_MODEL": args.model,
    }
    subprocess.run(
        [
            "harbor",
            "run",
            "-p",
            str((args.case / "task").resolve()),
            "-a",
            "evaluation.cli.agent:CompetitionCLI",
            "--disable-verification",
            "--agent-timeout-multiplier",
            "2",
            "--jobs-dir",
            str(out),
        ],
        cwd=ROOT,
        env=env,
        check=True,
    )
    forecasts = list(out.rglob("artifacts/app/prediction.json"))
    if len(forecasts) != 1:
        raise ValueError("Run did not produce exactly one forecast")
    submit(args.case, entrant, read_prediction(forecasts[0]))
    print(args.case / "receipts" / (entrant + ".json"))
