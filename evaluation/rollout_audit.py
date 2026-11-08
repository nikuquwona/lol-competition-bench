"""Audit published native five-game trials against their frozen Harbor inputs, without executing agent commands."""

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
import tempfile

from evaluation.forecast_io import Evidence, PRED, SNAP, forecast, shell_evidence
from evaluation.selections import suite_ids
from evaluation.suite import DEFAULT_RELEASE, report_row, select, summary, unpack
from production.build import ROOT
from production.score import read_prediction
from production.store import digest, read

# Indicators flag a transcript for human inspection. Absence is not a syscall-level proof.
REVIEW_ACCESS = re.compile(
    r"(?:https?://|(?:^|[;&|\s])(?:curl|wget|ssh|git|pip|npm)\s|"
    r"\b(?:socket|requests|urllib|environ|getenv|subprocess)\b|"
    r"(?:^|[ /'\"(])(?:\.\./|\.git/|\.zshrc\b|labels\.json\b|/tests/|/solution/))"
)
CANARY = re.compile(r"LOL_HIDDEN_[0-9a-fA-F]{32}")
PROBE = "snapshot accessible; labels, personal shell config, public IP and second loopback listener denied"
SOURCE_DIR = ROOT / "evaluation/examples"
DEFAULT_REPORTS = (
    "featured-five-deepseek",
    "featured-five-claude-deepseek",
    "featured-five-openrouter",
)


@dataclass
class Call:
    start: int
    tool: str
    args: object
    end: int | None = None
    output: str = ""
    ok: bool | None = None


def native_calls(path, harness):
    """Keep starts even when a tool never returns; result correlations use native IDs."""
    calls, pending, unpaired = [], {}, []

    def start(identifier, call):
        if not identifier or identifier in pending:
            unpaired.append(call.start)
            if identifier in pending:
                unpaired.append(pending[identifier].start)
        pending[identifier] = call
        calls.append(call)

    with path.open() as stream:
        for line, raw in enumerate(stream, 1):
            event = json.loads(raw)
            if harness == "codex":
                item = event.get("item", {})
                if item.get("type") != "command_execution":
                    continue
                key = item.get("id")
                if event["type"] == "item.started":
                    start(key, Call(line, "Bash", item.get("command", "")))
                elif event["type"] == "item.completed":
                    call = pending.pop(key, None)
                    if call is None or call.args != item.get("command"):
                        unpaired.append(line)
                        if call:
                            unpaired.append(call.start)
                        call = Call(line, "Bash", item.get("command", ""))
                        calls.append(call)
                    call.end, call.output = line, item.get("aggregated_output", "")
                    call.ok = (
                        type(item.get("exit_code")) is int and item["exit_code"] == 0
                    )
                continue
            if harness != "claude":
                raise ValueError("Native audit supports Codex and Claude Code")
            if event.get("type") not in ("user", "assistant"):
                continue
            for block in (event.get("message") or {}).get("content", []):
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    start(block.get("id"), Call(line, block["name"], block["input"]))
                elif block.get("type") == "tool_result":
                    call = pending.pop(block.get("tool_use_id"), None)
                    if call is None:
                        unpaired.append(line)
                        call = Call(line, "unmatched result", {})
                        calls.append(call)
                    value = block.get("content", "")
                    call.end = line
                    call.output = value if isinstance(value, str) else json.dumps(value)
                    call.ok = not block.get("is_error", False)
    unpaired.extend(call.start for call in pending.values())
    return sorted(calls, key=lambda c: c.end or c.start), sorted(set(unpaired))


def inspect_calls(path, harness):
    calls, pending = native_calls(path, harness)
    opened, flags, unknown = [], [], []
    checkpoint = first_write = None
    shell_count = 0
    for call in calls:
        line = call.end or call.start
        args = call.args
        if CANARY.search(json.dumps(args, ensure_ascii=False)):
            flags.append(
                {"line": call.start, "indicator": "hidden marker in tool arguments"}
            )
        if CANARY.search(call.output):
            flags.append({"line": line, "indicator": "hidden marker in tool result"})
        if call.tool == "Bash":
            shell_count += 1
            command = args.get("command", "") if isinstance(args, dict) else args
            if match := REVIEW_ACCESS.search(command):
                flags.append({"line": call.start, "indicator": match[0]})
            event = shell_evidence(command, call.output)
        elif call.tool in ("Read", "Write"):
            path = args.get("file_path", "")
            is_input = bool(re.fullmatch(SNAP, path))
            is_prediction = bool(re.fullmatch(PRED, path))
            writing = call.tool == "Write"
            if not is_prediction and (not is_input or writing):
                flags.append(
                    {"line": call.start, "indicator": "unexpected native file target"}
                )
            event = Evidence(
                snapshot=is_input and not writing,
                read_only=not writing,
                writes=is_prediction and writing,
                kind=("native_write" if writing else "readback")
                if is_prediction
                else None,
                values=forecast(args.get("content", "") if writing else call.output)
                if is_prediction
                else None,
            )
        else:
            flags.append(
                {"line": call.start, "indicator": "unexpected tool " + call.tool}
            )
            event = Evidence(known=False)
        if not event.read_only or (call.ok and event.kind == "readback"):
            checkpoint = None
        if not event.known:
            unknown.append(line)
        if call.ok is not True:
            continue
        if event.snapshot:
            opened.append(line)
        if event.writes and first_write is None:
            first_write = shell_count
        if event.values is not None:
            checkpoint = {
                "line": line,
                "values": event.values,
                "kind": event.kind
                or ("native_write" if call.tool == "Write" else "readback"),
            }
    return {
        "tools": len(calls),
        "shell_calls": shell_count,
        "failed_tools": sum(c.ok is False for c in calls),
        "first_snapshot_line": next(iter(opened), None),
        "first_write_shell_count": first_write,
        "last_checkpoint": checkpoint,
        "access_flags": flags,
        "unpaired_calls": pending,
        "unknown_lines": unknown,
    }


def package_file(folder, relative):
    path = folder / relative
    if (
        path.is_symlink()
        or not path.resolve().is_relative_to(folder.resolve())
        or not path.is_file()
    ):
        raise ValueError("Missing or unsafe artifact")
    return path


def audit_trial(trial, report_dir, references, organizer, report):
    task_id = trial["task"]
    job = report_dir / "jobs" / task_id
    canonical = references / task_id
    if not job.resolve().is_relative_to(report_dir.resolve()):
        raise ValueError("Job directory escapes the report")
    frozen = package_file(report_dir, trial["trajectory"]["files"]["snapshot"])
    snap = read(frozen)
    current = snap["current"]
    origin = trial.get("origin", {}).get("files_sha256", {})
    measured = inspect_calls(package_file(job, "trajectory.jsonl"), report["harness"])
    expected_ids = set()
    cutoff = datetime.fromisoformat(snap["series_time_utc"])
    for (series, game), row in organizer.items():
        if series == current["series"]:
            visible = game < current["n"]
        else:
            published = row.get("replay_published")
            visible = bool(
                published
                and datetime.fromisoformat(row["series_time"])
                < datetime.fromisoformat(published)
                < cutoff
            )
        if visible:
            expected_ids.add((series, game))
    seen = [(h["series"], h["n"]) for h in snap["history"]]
    saved = (job / "prediction.json").exists()
    runtime = read(package_file(job, "run.json"))
    required = {
        "snapshot.json",
        "instruction.md",
        "run.json",
        "stderr.txt",
        "trajectory.jsonl",
    }
    if trial["status"] == "scored":
        required.add("prediction.json")
    phase = "lobby" if task_id.endswith("-lobby") else "draft-lock"
    routes = (
        {"/v1/responses"}
        if report["harness"] == "codex"
        else {"/v1/messages", "/v1/messages?beta=true"}
    )
    checks = {
        "recorded_inputs_match_release": digest(frozen)
        == digest(canonical / "environment/snapshot.json")
        == trial["snapshot_sha256"]
        == origin.get("snapshot.json")
        and package_file(job, "instruction.md").read_text()
        == (canonical / "instruction.md").read_text().replace("/app/", "./")
        and digest(canonical / "instruction.md") == trial["prompt_sha256"],
        "history_respects_cutoff": set(seen) == expected_ids
        and len(seen) == len(expected_ids),
        "phase_fields": trial["phase"] == snap["phase"] == phase
        and (
            ("bp" not in current)
            if trial["phase"] == "lobby"
            else len(current.get("bp", [])) == 20
        )
        and not {"winner", "blue_win", "blue_gd15", "rating"} & current.keys(),
        "raw_artifacts_intact": set(origin) == required
        and all(
            digest(frozen if file == "snapshot.json" else package_file(job, file))
            == sha
            for file, sha in origin.items()
        ),
        "observed_snapshot_read": measured["first_snapshot_line"] is not None,
        "runtime_matches_trial": runtime == trial.get("runtime")
        and bool(
            re.fullmatch(r"codex-cli [0-9.]+", runtime.get("cli", ""))
            if report["harness"] == "codex"
            else re.fullmatch(r"[0-9.]+ \(Claude Code\)", runtime.get("cli", ""))
        )
        and runtime.get("snapshot_sha256") == trial["snapshot_sha256"]
        and runtime.get("phase") == phase,
        "boundary_probe": runtime.get("boundary_probe") == PROBE,
        "upstream_inference": runtime.get("model") == report["model"]
        and runtime.get("mode") == report["mode"]
        and any(
            req.get("status") == 200 and req.get("path") in routes
            for req in runtime["upstream"]
        ),
        "tools_paired": not measured["unpaired_calls"],
    }
    if trial["status"] == "scored":
        prediction = read_prediction(job / "prediction.json")
        grade = report_row(canonical, prediction)
        checks["independent_grade"] = all(trial[k] == v for k, v in grade.items())
        checks["last_recorded_forecast_matches_submission"] = bool(
            measured["last_checkpoint"]
            and measured["last_checkpoint"]["values"] == prediction
        )
    else:
        checks["failure_excluded_from_scored"] = (
            trial["status"] == "failed"
            and trial.get("reward") == 0
            and not saved
            and "prediction" not in trial
        )
    return {"task": task_id, "status": trial["status"], "checks": checks, **measured}


def audit(report_dir, references, organizer):
    report = read(report_dir / "report.json")
    manifest = read(DEFAULT_RELEASE / "manifest.json")
    expected = set(suite_ids("featured-five", manifest))
    planned = report.get("planned", [])
    trials = report["trials"]
    unstarted = report.get("unstarted", [])
    expected_partition = Counter(expected)
    partition = Counter(t.get("task") for t in [*trials, *unstarted])
    checks = {
        "fixed_suite_partition": (
            report.get("suite") == "featured-five"
            and report.get("release") == manifest["version"]
            and report.get("archive_sha256") == manifest["sha256"]
            and Counter(planned) == expected_partition
            and partition == expected_partition
            and all(t.get("status") == "not_started" for t in unstarted)
        ),
        "runtime_backend": report.get("backend") == "macos"
        and report.get("harness") in ("codex", "claude")
        and report.get("mode") in ("live", "openrouter-free"),
    }
    results = []
    for trial in trials:
        task = trial.get("task")
        try:
            if task not in expected:
                raise ValueError("Unknown task")
            results.append(
                audit_trial(trial, report_dir, references, organizer, report)
            )
        except (OSError, ValueError, TypeError, KeyError) as err:
            results.append(
                {
                    "task": task,
                    "status": trial.get("status"),
                    "tools": 0,
                    "checks": {"readable_trial": False},
                    "access_flags": [],
                    "error": str(err),
                }
            )
    counts = Counter(t.get("status") for t in trials)
    checks["progress"] = report.get("progress") == {
        "planned": len(expected),
        "attempted": len(trials),
        "scored": counts["scored"],
        "failed": counts["failed"],
        "not_started": len(unstarted),
    }
    metric = "attempted_summary" if unstarted else "summary"
    try:
        checks["summary"] = (
            bool(trials)
            and report.get(metric) == summary(trials)
            and not (unstarted and "summary" in report)
        )
    except (TypeError, ValueError, KeyError, ZeroDivisionError):
        checks["summary"] = False
    for entry in unstarted:
        try:
            task = entry["task"]
            if task not in expected or (report_dir / "jobs" / task).exists():
                raise ValueError("Unexpected unstarted task")
            for key, canonical in (
                ("snapshot", "environment/snapshot.json"),
                ("prompt", "instruction.md"),
            ):
                if digest(package_file(report_dir, entry["files"][key])) != entry[
                    key + "_sha256"
                ] or entry[key + "_sha256"] != digest(references / task / canonical):
                    raise ValueError("Unstarted input mismatch")
        except (OSError, KeyError, ValueError, TypeError):
            checks["unstarted_inputs"] = False
            break
    else:
        checks["unstarted_inputs"] = True
    return {
        "run": report_dir.name,
        "model": report["model"],
        "harness": report["harness"],
        "checks": checks,
        "unstarted": len(unstarted),
        "trials": results,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", type=Path, help="Write machine-readable findings")
    args = p.parse_args()
    organizer = {
        (r["series"], r["n"]): r for r in read(ROOT / "production/data/games.json")
    }
    manifest, rows = select(DEFAULT_RELEASE)
    dirs = [SOURCE_DIR / name for name in DEFAULT_REPORTS]
    ids = set(suite_ids("featured-five", manifest))
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        unpack(DEFAULT_RELEASE, manifest, [r for r in rows if r["id"] in ids], root)
        results = [audit(d, root, organizer) for d in dirs]
    attention = []
    for r in results:
        statuses = Counter(t["status"] for t in r["trials"])
        print(
            r["run"],
            dict(statuses),
            "unstarted",
            r["unstarted"],
            "tool calls",
            sum(t["tools"] for t in r["trials"]),
        )
        if errors := [k for k, v in r["checks"].items() if not v]:
            attention.append((r["run"], "report", errors, []))
        for t in r["trials"]:
            errors = [k for k, v in t["checks"].items() if not v]
            if errors or t["access_flags"]:
                attention.append((r["run"], t["task"], errors, t["access_flags"]))
    if args.json:
        args.json.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    for issue in attention:
        print(*issue)
    if attention:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
