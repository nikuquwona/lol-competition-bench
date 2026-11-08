"""Exercise each native CLI's shell boundary on the two KC–T1 game-two observations."""

import argparse
import hashlib
import json
import secrets
import shlex
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

from evaluation.cli.client import BIN
from evaluation.cli.fixture import COMMAND, MODEL
from evaluation.cli.worker import run
from evaluation.suite import DEFAULT_RELEASE, select, unpack
from production.build import ROOT
from production.catalog import resolve_release

SERIES = "worlds-2026-main-event-quarterfinals-4"
PROBE = Path(__file__).with_name("boundary_probe.py")


def write_json(path, obj):
    staging = path.with_suffix(".tmp")
    staging.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
    staging.replace(path)


def prepare(directory, phase):
    """Plant unpredictable markers only in known organizer-side files in the disposable copy."""
    prefix = SERIES + "-g2-"
    other = "lobby" if phase == "draft-lock" else "draft-lock"
    assets = [
        directory / (prefix + phase) / "tests/labels.json",
        directory / (prefix + other) / "environment/snapshot.json",
        directory / (SERIES + "-g3-draft-lock") / "environment/snapshot.json",
    ]
    sealed = {}
    for path in assets:
        marker = "LOL_HIDDEN_" + secrets.token_hex(16)
        obj = json.loads(path.read_text())
        obj["acceptance_canary"] = marker
        write_json(path, obj)
        sealed[str(path.relative_to(directory))] = hashlib.sha256(
            marker.encode()
        ).hexdigest()
    paths = [str(p) for p in assets] + [
        "/tests/labels.json",
        "/solution/solve.sh",
        "/app/.git/config",
        "/var/run/docker.sock",
        "/app/production/data/games.json",
        str(ROOT / "production/data/games.json"),
        str(Path.home() / ".zshrc"),
    ]
    config = {
        "organizer": str(directory),
        "challenge": secrets.token_hex(12),
        "forbidden_paths": paths,
    }
    command = shlex.join(["python3", "-I", "-c", PROBE.read_text(), json.dumps(config)])
    return config, sealed, command + " && " + COMMAND


def verify(observation, config, phase, expected_picks):
    expected = {
        "challenge": config["challenge"],
        "phase": phase,
        "target_bp_turns": 20 if phase == "draft-lock" else 0,
        "visible_results": [],
        "history_games": 96,
        "faker_games": 6,
        "same_series_games": [1],
        "game_one_picks": expected_picks,
        "enabled_network_interfaces": ["lo"],
        "external_tcp": False,
        "opened_forbidden_files": [],
        "found_markers": [],
        "present_credentials": [],
    }
    return {
        k: {"expected": v, "observed": observation.get(k)}
        for k, v in expected.items()
        if v != observation.get(k)
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--release", type=resolve_release, default=DEFAULT_RELEASE)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--harness", choices=BIN, nargs="+", default=list(BIN))
    p.add_argument(
        "--phase",
        choices=["lobby", "draft-lock"],
        nargs="+",
        default=["lobby", "draft-lock"],
    )
    a = p.parse_args()
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    a.out.mkdir(parents=True, exist_ok=False)
    manifest, rows = select(
        a.release,
        ids=[
            SERIES + "-g2-lobby",
            SERIES + "-g2-draft-lock",
            SERIES + "-g3-draft-lock",
        ],
    )
    game1 = next(
        g
        for g in json.loads((ROOT / "production/data/games.json").read_bytes())
        if g["series"] == SERIES and g["n"] == 1
    )
    picks = [b["champion"] for b in game1["bp"] if b["action"] == "pick"]
    report = {
        "release": manifest["version"],
        "archive_sha256": manifest["sha256"],
        "trials": [],
    }
    for name in a.harness:
        for phase in a.phase:
            row = next(r for r in rows if r["game"] == 2 and r["phase"] == phase)
            out = a.out / name / phase
            trial = {
                "harness": name,
                "task": row["id"],
                "snapshot_sha256": row["snapshot_sha256"],
                "scope": "native_cli_shell"
                if name != "cursor"
                else "worker_shell_and_unauthenticated_cli_startup",
            }
            report["trials"].append(trial)
            try:
                with tempfile.TemporaryDirectory(prefix="lol-boundary-") as tmp:
                    directory = Path(tmp).resolve()
                    unpack(a.release, manifest, rows, directory)
                    config, sealed, command = prepare(directory, phase)
                    task = directory / row["id"]
                    out.parent.mkdir(parents=True, exist_ok=True)
                    script = out.with_suffix(".sh")
                    script.write_text("#!/bin/sh\nset -eu\n" + command + "\n")
                    trial.update(
                        marker_hashes=sealed,
                        challenge=config["challenge"],
                        shell_command=script.relative_to(a.out).as_posix(),
                    )
                    run(
                        name,
                        MODEL,
                        "check" if name == "cursor" else "fixture",
                        task / "environment/snapshot.json",
                        task / "instruction.md",
                        out,
                        boundary_command=command,
                    )
                    measured = json.loads((out / "boundary.json").read_text())
                    trial.update(
                        observation=measured,
                        runtime=json.loads((out / "run.json").read_text()),
                        differences=verify(measured, config, phase, picks),
                    )
                    trial["status"] = "failed" if trial["differences"] else "passed"
            except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as e:
                trial.update(status="failed", error=str(e))
            trial["artifacts"] = {
                p.name: p.relative_to(a.out).as_posix()
                for p in (
                    out / "boundary.json",
                    out / "cli-events.log",
                    out / "stderr.txt",
                )
                if p.is_file()
            }
            write_json(a.out / "report.json", report)
            print(name, phase, trial["scope"], trial["status"], flush=True)
    report["summary"] = {
        scope: {
            "passed": sum(
                t["status"] == "passed" for t in report["trials"] if t["scope"] == scope
            ),
            "attempted": sum(t["scope"] == scope for t in report["trials"]),
        }
        for scope in sorted({t["scope"] for t in report["trials"]})
    }
    write_json(a.out / "report.json", report)
    if any(t["status"] != "passed" for t in report["trials"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
