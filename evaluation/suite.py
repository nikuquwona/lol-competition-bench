"""Select tasks from one pinned release, run a model/harness pair, and account for every trial."""

import argparse
from production.catalog import resolve_release
import fcntl
import math
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

from evaluation.traces import attach, overview
from evaluation.selections import CURRENT_SUITE, suite_ids, suite_names
from evaluation.baseline import predict
from evaluation.cli.client import BIN
from evaluation.cli.gateway import credential_name, free_model
from evaluation.cli.macos_pair import SandboxUnavailable
from production.build import ROOT
from production.coverage import history_card
from production.score import FIELDS, read_prediction, score

DEFAULT_RELEASE = resolve_release("worlds-lpl-2026")
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


def paired_summary(tasks, trials):
    """Compare phases within the same game, keeping unscored pairs in the counts."""
    results = {r["task"]: r for r in trials}
    groups = {}
    for task in tasks:
        phases = groups.setdefault((task["series"], task["game"]), {})
        phases[task["phase"]] = results.get(task["id"], {})
    pairs = []
    planned = 0
    for (series, game), phases in sorted(groups.items()):
        if set(phases) != {"lobby", "draft-lock"}:
            continue
        planned += 1
        if any(phase.get("status") != "scored" for phase in phases.values()):
            continue
        delta = {
            k: phases["lobby"]["brier"][k] - phases["draft-lock"]["brier"][k]
            for k in FIELDS
        }
        pairs.append(dict(series=series, game=game, brier_improvement=delta))
    return dict(
        selected_games=len(groups),
        selected_pairs=planned,
        scored_pairs=len(pairs),
        mean_brier_improvement={
            k: sum(p["brier_improvement"][k] for p in pairs) / len(pairs)
            if pairs
            else None
            for k in FIELDS
        },
        pairs=pairs,
    )


def summarize_report(report, rows):
    report["summary"] = summary(report["trials"])
    report["by_phase"] = {
        phase: summary([r for r in report["trials"] if r["phase"] == phase])
        for phase in sorted({r["phase"] for r in rows})
    }
    buckets = {}
    for trial in report["trials"]:
        bucket = trial.get("coverage", {}).get("coverage_group", "unrecorded")
        buckets.setdefault(bucket, []).append(trial)
    report["by_coverage"] = {
        bucket: summary(group) for bucket, group in buckets.items()
    }
    report["paired"] = paired_summary(rows, report["trials"])


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
    if a.suite:
        if any(
            (
                a.task,
                a.series,
                a.game,
                a.phase,
                a.patch,
                a.limit,
                getattr(a, "all", False),
            )
        ):
            raise ValueError(
                "--suite selects a complete named task set; choose it alone"
            )
        a.task = suite_ids(a.suite, a.release)
    manifest, rows = select(
        a.release, a.task, a.phase, a.patch, a.limit, a.series, a.game
    )
    if a.list:
        print("\n".join(r["id"] for r in rows))
        return
    if a.resume and a.out is None:
        raise ValueError("--resume requires --out")
    if a.out is None:
        a.out = ROOT / ".work/runs" / str(uuid.uuid4())
    mode = a.mode
    if mode != "baseline":
        if not a.harness or not a.model:
            raise ValueError("Provide --harness and --model")
        if a.backend == "macos" and (
            a.harness not in ("codex", "claude")
            or mode not in ("live", "fixture", "openrouter-free")
        ):
            raise ValueError(
                "macos backend supports Codex and Claude Code in live, openrouter-free or fixture mode"
            )
        if a.backend == "harbor" and not shutil.which("harbor"):
            raise ValueError("Install harbor==0.25.0 on the isolated runner")
        if (a.harness == "cursor") != (mode == "vendor"):
            raise ValueError("Cursor requires its separate vendor mode")
        if mode == "openrouter-free" and not free_model(a.model):
            raise ValueError("Provide a pinned OpenRouter model ending in :free")
        secret = credential_name(mode)
        if secret and not os.getenv(secret):
            raise ValueError("Missing runner credential: " + secret)
    a.out = a.out.resolve()
    if not a.resume:
        a.out.mkdir(parents=True, exist_ok=False)
    with (a.out / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        run_selection(a, manifest, rows)


def run_selection(a, manifest, rows):
    mode = a.mode
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
    if a.suite:
        report["suite"] = a.suite
    if "protocol_sha256" in manifest:
        report["protocol_sha256"] = manifest["protocol_sha256"]
        report["task_spec_id"] = manifest["task_spec"]["id"]
    if a.resume:
        saved = json.loads((a.out / "report.json").read_text())
        if any(report[k] != saved.get(k) for k in report if k != "trials"):
            raise ValueError(
                "Resume requires the original release, selection, backend, harness and model"
            )
        report["trials"] = saved["trials"]
        attempted = [r["task"] for r in report["trials"]]
        if attempted != report["planned"][: len(attempted)]:
            raise ValueError("Invalid checkpoint sequence")
        for record in report["trials"]:
            if record["status"] == "started":
                record.update(
                    status="interrupted",
                    reward=0,
                    error="Interrupted after attempt began",
                )
    remaining = rows[len(report["trials"]) :]
    write_report(a.out, report)
    with (
        tempfile.TemporaryDirectory(prefix="lol-suite-") as tmp,
        suite_image(
            a.harness, len(remaining) > 1 and a.backend == "harbor"
        ) as image_env,
    ):
        directory = Path(tmp)
        unpack(a.release, manifest, remaining, directory)
        for r in remaining:
            task = directory / r["id"]
            view = json.loads((task / "environment/snapshot.json").read_text())
            record = {
                "task": r["id"],
                "coverage": history_card(view["current"], view["history"]),
                "phase": r["phase"],
                "patch": r["patch"],
                "prompt_sha256": r["prompt_sha256"],
                "snapshot_sha256": r["snapshot_sha256"],
            }
            record["status"] = "started"
            report["trials"].append(record)
            write_report(a.out, report)
            try:
                if mode == "baseline":
                    pred = predict(view)
                elif a.backend == "macos":
                    from evaluation.cli.macos_pair import run

                    cli_dir = a.out / "jobs" / r["id"]
                    binary = shutil.which(a.harness)
                    if not binary:
                        raise ValueError(f"Missing {a.harness} CLI")
                    run(
                        r["phase"],
                        cli_dir,
                        Path(binary).resolve(),
                        False,
                        False,
                        task=task,
                        harness=a.harness,
                        model=a.model,
                        fixture=mode == "fixture",
                        openrouter_free=mode == "openrouter-free",
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
                    if not math.isclose(
                        float(reward.read_text()),
                        measured["reward"],
                        rel_tol=0,
                        abs_tol=1e-12,
                    ):
                        raise ValueError("Harbor reward mismatch")
                record.update(measured)
            except SandboxUnavailable as exc:
                record.update(status="environment_error", reward=0, error=str(exc))
            except (
                OSError,
                RuntimeError,
                ValueError,
                subprocess.SubprocessError,
            ) as exc:
                record.update(status="failed", reward=0, error=str(exc))
            if mode != "baseline":
                attach(a.out, record, task)
            write_report(a.out, report)
    summarize_report(report, rows)
    write_report(a.out, report)
    overview(a.out, report)
    print(f"Read: {a.out / 'report.md'}")
    print(json.dumps(report["summary"], indent=2))
    print(f"Report: {a.out / 'report.json'}")
    if report["summary"]["scored"] != len(rows):
        raise SystemExit(1)


def main(simple=False):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--release", type=resolve_release, default=DEFAULT_RELEASE)
    p.add_argument("--out", type=Path)
    p.add_argument(
        "--resume",
        action="store_true",
        help="Continue unstarted tasks from the same report",
    )
    p.add_argument("--task", action="append", default=[])
    p.add_argument(
        "--suite",
        choices=suite_names(),
        help="Use a published, release-pinned task set",
    )
    p.add_argument("--series")
    p.add_argument("--game", type=int)
    p.add_argument("--phase", choices=["lobby", "draft-lock"])
    p.add_argument("--patch")
    p.add_argument("--limit", type=int)
    p.add_argument("--list", action="store_true")
    p.add_argument("--all", action="store_true", help="Select the full source release")
    if simple:
        p.set_defaults(mode="baseline", harness=None, model=None, backend="local")
    else:
        p.add_argument(
            "--mode",
            choices=["live", "openrouter-free", "vendor", "fixture"],
            default="live",
        )
        p.add_argument("--backend", choices=["harbor", "macos"], default="harbor")
        p.add_argument("--harness", choices=BIN)
        p.add_argument("--model")
    a = p.parse_args()
    if (
        not simple
        and a.release == DEFAULT_RELEASE
        and not any(
            (a.all, a.task, a.series, a.game, a.phase, a.patch, a.limit, a.suite)
        )
    ):
        a.suite = CURRENT_SUITE
    if (
        simple
        and not a.all
        and not any(
            (a.task, a.series, a.game, a.phase, a.patch, a.limit, a.list, a.suite)
        )
    ):
        a.task = [SAMPLE]
    evaluate(a)
