"""Run a frozen, unlabeled Harbor task and seal the submitted probabilities."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

from production.build import ROOT
from production.intake import require_open, submit
from production.schema import slug
from production.store import trusted_case
from production.score import read_prediction
from evaluation.cli.client import BIN
from evaluation.cli.gateway import credential_name, free_model


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", type=Path)
    parser.add_argument("--entrant", required=True)
    parser.add_argument("--harness", choices=BIN, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--mode", choices=("live", "vendor", "openrouter-free"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    trusted_case(args.case)
    require_open(args.case)
    entrant = slug(args.entrant)
    if (args.case / "receipts" / (entrant + ".json")).exists():
        raise ValueError("Entrant has already submitted")
    mode = args.mode or ("vendor" if args.harness == "cursor" else "live")
    if (args.harness == "cursor") != (mode == "vendor"):
        raise ValueError("Cursor requires vendor mode")
    if mode == "openrouter-free" and not free_model(args.model):
        raise ValueError("Provide a pinned OpenRouter model ending in :free")
    credential = credential_name(mode)
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
    (runtime,) = out.rglob("cli-run.json")
    completed = json.loads(runtime.read_text())
    if (completed["cli"], completed["requested_model"], completed["mode"]) != (
        args.harness,
        args.model,
        mode,
    ):
        raise ValueError("Unexpected harness, model or run mode in receipt")
    forecasts = list(out.rglob("artifacts/app/prediction.json"))
    if len(forecasts) != 1:
        raise ValueError("Run did not produce exactly one forecast")
    submit(args.case, entrant, read_prediction(forecasts[0]))
    print(args.case / "receipts" / (entrant + ".json"))
