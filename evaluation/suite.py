"""Select tasks from one pinned release, run a model/harness pair, and account for every trial."""

import argparse
import hashlib
import json
import os
import re
import uuid
from contextlib import contextmanager
import shutil
import subprocess
import tarfile
import tempfile
from collections import Counter
from pathlib import Path, PurePosixPath

from evaluation.baseline import predict
from evaluation.cli.client import BIN
from production.build import ROOT
from production.score import FIELDS, read_prediction, score

DEFAULT_RELEASE = ROOT / "datasets/replay-v2"
SAMPLE = "worlds-2026-main-event-quarterfinals-4-g2-draft-lock"


def select(release, ids=(), phase=None, patch=None, limit=None, series=None, game=None):
    manifest = json.loads((release / "manifest.json").read_text())
    rows = manifest["tasks"]
    keys = {row["id"] for row in rows}
    if any(not re.fullmatch(r"[a-z0-9][a-z0-9-]+", k) for k in keys):
        raise ValueError("Unsafe task identifier")
    if (
        manifest["format"] != 1
        or len(keys) != len(rows)
        or len(rows) != manifest["count"]
    ):
        raise ValueError("Invalid release index")
    if set(ids) - keys:
        raise ValueError("Unknown task ID")
    selected = [
        r
        for r in rows
        if (not ids or r["id"] in ids)
        and (not phase or phase == r["phase"])
        and (not patch or patch == r["patch"])
        and (not series or series == r["series"])
        and (not game or game == r["game"])
    ]
    if limit is not None:
        if limit < 1:
            raise ValueError("limit must be positive")
        selected = selected[:limit]
    if not selected:
        raise ValueError("Empty task selection")
    return manifest, selected


def unpack(release, manifest, rows, out):
    archive = release / "tasks.tar.gz"
    wanted = {r["id"] for r in rows}
    with archive.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != manifest["sha256"]:
            raise ValueError("Release archive checksum mismatch")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as tar:
            for member in tar:
                parts = PurePosixPath(member.name).parts
                if not member.isfile() or not parts or parts[0] == "/" or ".." in parts:
                    raise ValueError("Unsafe archive entry")
                if parts[0] not in wanted:
                    continue
                path = out.joinpath(*parts)
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("xb") as target, tar.extractfile(member) as src:
                    shutil.copyfileobj(src, target)
                path.chmod(0o755 if path.suffix == ".sh" else 0o644)
    for r in rows:
        task = out / r["id"]
        for rel, key in [
            ("environment/snapshot.json", "snapshot_sha256"),
            ("instruction.md", "prompt_sha256"),
        ]:
            if hashlib.sha256((task / rel).read_bytes()).hexdigest() != r[key]:
                raise ValueError("Task identity mismatch")


def summary(rows):
    good = [r for r in rows if r["status"] == "scored"]
    return dict(
        selected=len(rows),
        scored=len(good),
        statuses=dict(Counter(r["status"] for r in rows)),
        mean_reward=sum(r["reward"] for r in good) / len(rows),
        brier_on_scored={
            k: sum(r["brier"][k] for r in good) / len(good) if good else None
            for k in FIELDS
        },
    )


def report_row(task, prediction):
    labels = json.loads((task / "tests/labels.json").read_text())
    if (
        not isinstance(prediction, dict)
        or set(prediction) != set(FIELDS)
        or not all(type(p) in (float, int) and 0 <= p <= 1 for p in prediction.values())
    ):
        raise ValueError("Invalid prediction")
    return dict(
        status="scored",
        prediction=prediction,
        reward=score(prediction, labels),
        brier={k: (prediction[k] - labels[k]) ** 2 for k in FIELDS},
    )


def write_report(out, doc):
    path = out / "report.tmp"
    path.write_text(json.dumps(doc, indent=2) + "\n")
    path.replace(out / "report.json")


@contextmanager
def suite_image(harness, enabled):
    """Amortize the CLI installation, while trial containers and volumes remain disposable."""
    if not enabled:
        yield {}
        return
    from evaluation.cli.worker import docker, HERE

    tag = "lolbench-suite-" + uuid.uuid4().hex[:12] + ":trial"
    try:
        docker(
            "build",
            "-q",
            "-t",
            tag,
            "--build-arg",
            f"HARNESS={harness}",
            str(HERE),
            timeout=600,
        )
        yield {"BENCH_SUITE_IMAGE": tag}
    finally:
        docker("image", "rm", tag, check=False, capture=True)


def evaluate(a):
    manifest, rows = select(
        a.release, a.task, a.phase, a.patch, a.limit, a.series, a.game
    )
    if a.list:
        print("\n".join(r["id"] for r in rows))
        return
    if a.out is None:
        a.out = ROOT / ".work/runs" / str(uuid.uuid4())
    mode = a.mode
    if mode != "baseline":
        if not a.harness or not a.model:
            raise ValueError("Provide --harness and --model")
        if a.backend == "macos" and (a.harness != "codex" or mode != "live"):
            raise ValueError("macos backend supports live Codex only")
        if a.backend == "harbor" and not shutil.which("harbor"):
            raise ValueError("Install harbor==0.25.0 on the isolated runner")
        if (a.harness == "cursor") != (mode == "vendor"):
            raise ValueError("Cursor requires its separate vendor mode")
        secret = {"live": "DEEPSEEK_API_KEY", "vendor": "CURSOR_API_KEY"}.get(mode)
        if secret and not os.getenv(secret):
            raise ValueError("Missing runner credential: " + secret)
    a.out = a.out.resolve()
    a.out.mkdir(parents=True, exist_ok=False)
    report = dict(
        release=manifest["version"],
        archive_sha256=manifest["sha256"],
        harness=a.harness or "player-baseline",
        model=a.model,
        mode=mode,
        backend=a.backend,
        planned=[r["id"] for r in rows],
        trials=[],
    )
    write_report(a.out, report)
    with (
        tempfile.TemporaryDirectory(prefix="lol-suite-") as tmp,
        suite_image(a.harness, len(rows) > 1 and a.backend == "harbor") as image_env,
    ):
        directory = Path(tmp)
        unpack(a.release, manifest, rows, directory)
        for r in rows:
            task = directory / r["id"]
            record = {
                "task": r["id"],
                "phase": r["phase"],
                "patch": r["patch"],
                "prompt_sha256": r["prompt_sha256"],
                "snapshot_sha256": r["snapshot_sha256"],
            }
            try:
                if mode == "baseline":
                    pred = predict(
                        json.loads((task / "environment/snapshot.json").read_text())
                    )
                elif a.backend == "macos":
                    from evaluation.cli.macos_pair import run

                    cli_dir = a.out / "jobs" / r["id"]
                    binary = shutil.which("codex")
                    if not binary:
                        raise ValueError("Missing Codex CLI")
                    run(
                        r["phase"],
                        cli_dir,
                        Path(binary).resolve(),
                        False,
                        False,
                        task=task,
                        model=a.model,
                    )
                    record["runtime"] = json.loads((cli_dir / "run.json").read_text())
                    pred = read_prediction(cli_dir / "prediction.json")
                else:
                    jobs = a.out / "jobs" / r["id"]
                    env = {
                        **os.environ,
                        **image_env,
                        "BENCH_CLI": a.harness,
                        "BENCH_MODEL": a.model,
                        "BENCH_MODE": mode,
                        "PYTHONPATH": str(ROOT),
                    }
                    subprocess.run(
                        [
                            "harbor",
                            "run",
                            "-p",
                            str(task),
                            "-a",
                            "evaluation.cli.agent:CompetitionCLI",
                            "--agent-timeout-multiplier",
                            "2",
                            "--jobs-dir",
                            str(jobs),
                        ],
                        cwd=ROOT,
                        env=env,
                        check=True,
                    )
                    (runtime,) = jobs.rglob("cli-run.json")
                    record["runtime"] = json.loads(runtime.read_text())
                    (forecast,) = jobs.rglob("artifacts/app/prediction.json")
                    pred = read_prediction(forecast)
                measured = report_row(task, pred)
                if mode != "baseline" and a.backend == "harbor":
                    (reward,) = jobs.rglob("verifier/reward.txt")
                    if abs(float(reward.read_text()) - measured["reward"]) > 1e-12:
                        raise ValueError("Harbor reward mismatch")
                record.update(measured)
            except (
                OSError,
                RuntimeError,
                ValueError,
                subprocess.SubprocessError,
            ) as exc:
                record.update(status="failed", reward=0, error=str(exc))
            report["trials"].append(record)
            write_report(a.out, report)
    report["summary"] = summary(report["trials"])
    report["by_phase"] = {
        phase: summary([r for r in report["trials"] if r["phase"] == phase])
        for phase in sorted({r["phase"] for r in rows})
    }
    write_report(a.out, report)
    print(json.dumps(report["summary"], indent=2))
    print(f"Report: {a.out / 'report.json'}")
    if report["summary"]["scored"] != len(rows):
        raise SystemExit(1)


def main(simple=False):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--release", type=Path, default=DEFAULT_RELEASE)
    p.add_argument("--out", type=Path)
    p.add_argument("--task", action="append", default=[])
    p.add_argument("--series")
    p.add_argument("--game", type=int)
    p.add_argument("--phase", choices=["lobby", "draft-lock"])
    p.add_argument("--patch")
    p.add_argument("--limit", type=int)
    p.add_argument("--list", action="store_true")
    if simple:
        p.set_defaults(mode="baseline", harness=None, model=None, backend="local")
    else:
        p.add_argument("--mode", choices=["live", "vendor", "fixture"], default="live")
        p.add_argument("--backend", choices=["harbor", "macos"], default="harbor")
        p.add_argument("--harness", choices=BIN)
        p.add_argument("--model")
    a = p.parse_args()
    if simple and not any(
        (a.task, a.series, a.game, a.phase, a.patch, a.limit, a.list)
    ):
        a.task = [SAMPLE]
    evaluate(a)
