"""Assemble disjoint native macOS CLI runs into a pinned example without replaying inference."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import tempfile

from evaluation.selections import suite_ids, suite_names
from evaluation.cli.public_logs import stage_accounts, strip_accounts
from evaluation.suite import (
    DEFAULT_RELEASE,
    paired_summary,
    report_row,
    select,
    summary,
    summarize_report,
    unpack,
    write_report,
)
from evaluation.traces import attach, overview
from production.score import read_prediction
from production.store import digest, read

JOB_FILES = (
    "instruction.md",
    "prediction.json",
    "run.json",
    "stderr.txt",
    "trajectory.jsonl",
)
CONFIG = ("release", "archive_sha256", "harness", "model", "mode", "backend")


def public_copy(src, dst):
    if src.is_symlink() or not src.is_file():
        raise ValueError(f"Expected a regular source artifact: {src.name}")
    data = src.read_bytes()
    if (
        strip_accounts(data) != data
        or str(Path.home()).encode() in data
        or re.search(rb"\bsk-(?:or-v1-)?[a-zA-Z0-9_-]{18,}", data)
    ):
        raise ValueError(
            f"Source artifact requires operator redaction before publication: {src.name}"
        )
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)


def job_directory(source, task_id):
    job = (source / "jobs" / task_id).resolve()
    if not job.is_relative_to(source.resolve()):
        raise ValueError("Native job directory escapes its source run")
    return job


def native_trial_id(config, task_id, event_digest):
    identity = [*[config[k] for k in CONFIG], task_id, event_digest]
    canonical = json.dumps(identity, ensure_ascii=False, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest()


def file_draft(events):
    """Only claim a draft if a successful native cat printed the complete JSON file."""
    draft = None
    for line in events.read_text().splitlines():
        event = json.loads(line)
        item = event.get("item", {})
        if (
            event.get("type") != "item.completed"
            or item.get("type") != "command_execution"
            or item.get("exit_code") != 0
            or not re.fullmatch(
                r"/bin/(?:ba|z)sh -lc 'cat \[ephemeral\]/app/prediction\.json'",
                item.get("command", ""),
            )
        ):
            continue
        try:
            obj = json.loads(item["aggregated_output"])
        except (KeyError, ValueError):
            continue
        if (
            isinstance(obj, dict)
            and set(obj) == {"p_blue_win", "p_blue_ahead_15"}
            and all(type(v) in (int, float) and 0 <= v <= 1 for v in obj.values())
        ):
            draft = {"native_event": item["id"], "values": obj}
    return draft


def assemble(
    suite,
    release,
    sources,
    out,
    diagnostics=(),
    quota_response=None,
    previous_public=None,
):
    manifest, tasks = select(release, suite_ids(suite, release))
    if out.exists():
        raise FileExistsError(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out.parent) as tmp:
        root = Path(tmp)
        work = root / "example"
        work.mkdir()
        unpack(release, manifest, tasks, root / "tasks")
        source_index = []
        diagnostic_index = []
        trials = {}
        config = None
        planned = {r["id"]: r for r in tasks}
        if quota_response:
            quota = read(quota_response)
            if (
                quota["http_status"] != 429
                or quota["headers"]["X-RateLimit-Remaining"] != "0"
                or "free-models-per-day" not in quota["message"]
            ):
                raise ValueError(
                    "Expected a recorded OpenRouter free daily quota refusal"
                )
            public_copy(quota_response, work / "sources/quota-response.json")
        for index, source in enumerate((*sources, *diagnostics)):
            path = source
            original = path / "report.json"
            doc = read(original)
            settings = {k: doc[k] for k in CONFIG}
            if (
                doc["archive_sha256"] != manifest["sha256"]
                or doc["release"] != manifest["version"]
            ):
                raise ValueError("Source belongs to a different release")
            if doc["backend"] != "macos" or doc["harness"] not in ("codex", "claude"):
                raise ValueError("Expected native macOS Codex or Claude Code artifacts")
            if config is None:
                config = settings
            if settings != config:
                raise ValueError("Run configurations differ")
            if [t["task"] for t in doc["trials"]] != doc["planned"] or not set(
                doc["planned"]
            ) <= planned.keys():
                raise ValueError(
                    "Source does not contain a completed subset of this suite"
                )
            path = stage_accounts(
                path,
                root / "staged" / str(index),
                doc["planned"],
                JOB_FILES,
                previous_public,
            )
            original = path / "report.json"
            doc = read(original)
            report_hash = digest(original)
            proof_path = f"sources/{report_hash}.json"
            public_copy(original, work / proof_path)
            receipt = {
                "sha256": report_hash,
                "file": proof_path,
                "planned": doc["planned"],
            }
            redactions = path / "redactions.json"
            file_receipts = {}
            if redactions.exists():
                file_receipts = read(redactions)
                for rel, proof in file_receipts.items():
                    artifact = (path / rel).resolve()
                    if not artifact.is_relative_to(path.resolve()) or proof.get(
                        "public_sha256"
                    ) != digest(artifact):
                        raise ValueError(
                            "Staged redaction proof does not match its public file"
                        )
                    if not re.fullmatch(
                        "[0-9a-f]{64}", proof.get("original_sha256", "")
                    ):
                        raise ValueError("Invalid original file fingerprint")
                receipt["redactions"] = f"sources/{report_hash}-redactions.json"
                public_copy(redactions, work / receipt["redactions"])
            if source in diagnostics:
                # Only pre-inference authentication failures can be excluded this way.
                for t in doc["trials"]:
                    job = job_directory(path, t["task"])
                    audit = read(job / "run.json")["upstream"]
                    if (
                        t["status"] != "failed"
                        or not audit
                        or any(e["status"] != 401 for e in audit)
                    ):
                        raise ValueError(
                            "Cannot exclude a trial that obtained an upstream response beyond 401"
                        )
                    for name in JOB_FILES:
                        if (job / name).exists():
                            public_copy(
                                job / name,
                                work / "diagnostics" / report_hash / t["task"] / name,
                            )
                diagnostic_index.append(
                    {
                        **receipt,
                        "reason": "OpenRouter 401 before any successful inference",
                    }
                )
                continue
            source_index.append(receipt)
            for t in doc["trials"]:
                i = t["task"]
                if i in trials:
                    raise ValueError(f"Duplicate attempted task: {i}")
                expected = planned[i]
                if any(
                    t[k] != expected[k]
                    for k in ("phase", "patch", "prompt_sha256", "snapshot_sha256")
                ):
                    raise ValueError("Source task identity mismatch")
                task = root / "tasks" / i
                src = job_directory(path, i)
                runtime = read(src / "run.json")
                if (
                    runtime != t.get("runtime", runtime)
                    or runtime["model"] != doc["model"]
                    or runtime["mode"] != doc["mode"]
                    or runtime["snapshot_sha256"] != t["snapshot_sha256"]
                    or (
                        t["status"] == "scored"
                        and not any(e["status"] == 200 for e in runtime["upstream"])
                    )
                ):
                    raise ValueError(
                        "CLI receipt does not attest the requested task and inference"
                    )
                t["runtime"] = runtime
                if t["status"] == "scored":
                    grade = report_row(task, read_prediction(src / "prediction.json"))
                    if any(t[k] != grade[k] for k in grade):
                        raise ValueError(
                            "CLI prediction or grade differs from trusted verifier"
                        )
                elif (
                    t["status"] == "failed"
                    and t.get("reward") == 0
                    and "prediction" not in t
                ):
                    limited = (
                        quota_response
                        and runtime["upstream"]
                        and runtime["upstream"][-1]["status"] == 429
                    )
                    t["failure_class"] = (
                        "provider_daily_quota" if limited else "failed_trial"
                    )
                    if doc["harness"] == "codex" and (
                        draft := file_draft(src / "trajectory.jsonl")
                    ):
                        t["unsettled_draft"] = draft
                else:
                    raise ValueError(
                        f"Source trial has an unsupported terminal state: {i}"
                    )
                for name in JOB_FILES:
                    if name != "prediction.json" or (src / name).exists():
                        public_copy(src / name, work / "jobs" / i / name)
                attach(work, t, task)
                hashes = {
                    k: digest(work / "jobs" / i / k)
                    for k in JOB_FILES
                    if (work / "jobs" / i / k).exists()
                }
                hashes["snapshot.json"] = digest(
                    work / t["trajectory"]["files"]["snapshot"]
                )
                t["origin"] = {
                    "trial_id": native_trial_id(config, i, hashes["trajectory.jsonl"]),
                    "source_report_sha256": report_hash,
                    "source_report": proof_path,
                    "files_sha256": hashes,
                }
                proof = file_receipts.get(f"jobs/{i}/trajectory.jsonl", {})
                if "input_to_account_filter_sha256" in proof:
                    t["origin"]["original_events_sha256"] = proof["original_sha256"]
                if previous := proof.get("prior_public_sha256"):
                    t["origin"]["original_events_sha256"] = proof["original_sha256"]
                    t["origin"]["prior_public_events_sha256"] = previous
                    t["origin"]["prior_public_trial_id"] = native_trial_id(
                        config, i, previous
                    )
                trials[i] = t
        if trials.keys() != planned.keys() and not quota_response:
            raise ValueError("Sources must cover every planned task exactly once")
        report = dict(
            **config,
            suite=suite,
            planned=list(planned),
            trials=[trials[i] for i in planned if i in trials],
        )
        report["provenance"] = {
            "source_runs": source_index,
            "authentication_diagnostics": diagnostic_index,
            "trial_id_fields": [*CONFIG, "task", "trajectory.jsonl SHA-256"],
            "trial_id_encoding": "SHA-256 of a UTF-8 JSON array with compact separators",
        }
        if config["mode"] == "live":
            report["provenance"]["provider_host"] = "api.deepseek.com"
            report["provenance"]["billing"] = (
                "metered; provider invoice amount not recorded"
            )
        if quota_response:
            report["provenance"]["quota_response"] = "sources/quota-response.json"
        report["unstarted"] = []
        for i in planned.keys() - trials.keys():
            view = root / "tasks" / i
            files = {}
            for field, src in (
                ("prompt", view / "instruction.md"),
                ("snapshot", view / "environment/snapshot.json"),
            ):
                dst = work / "inputs" / i / src.name
                public_copy(src, dst)
                files[field] = dst.relative_to(work).as_posix()
            record = planned[i]
            report["unstarted"].append(
                {
                    "task": i,
                    "status": "not_started",
                    "reason": "provider_daily_quota",
                    **{
                        k: record[k]
                        for k in (
                            "phase",
                            "patch",
                            "series",
                            "game",
                            "prompt_sha256",
                            "snapshot_sha256",
                        )
                    },
                    "files": files,
                }
            )
        report["unstarted"].sort(key=lambda x: x["task"])
        report["progress"] = {
            "planned": len(tasks),
            "attempted": len(trials),
            "scored": sum(t["status"] == "scored" for t in trials.values()),
            "failed": sum(t["status"] == "failed" for t in trials.values()),
            "not_started": len(report["unstarted"]),
        }
        if report["unstarted"]:
            report["attempted_summary"] = summary(report["trials"])
            report["paired"] = paired_summary(tasks, report["trials"])
        else:
            summarize_report(report, tasks)
        write_report(work, report)
        overview(work, report)
        work.rename(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", required=True, choices=suite_names())
    parser.add_argument("--release", type=Path, default=DEFAULT_RELEASE)
    parser.add_argument("--source", required=True, type=Path, action="append")
    parser.add_argument(
        "--authentication-diagnostic", type=Path, action="append", default=[]
    )
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument(
        "--previous-public",
        type=Path,
        help="Optional earlier published projection for a redaction migration",
    )
    parser.add_argument(
        "--quota-response",
        type=Path,
        help="Recorded daily quota refusal for an incomplete run",
    )
    a = parser.parse_args()
    assemble(
        a.suite,
        a.release,
        a.source,
        a.out,
        a.authentication_diagnostic,
        a.quota_response,
        a.previous_public,
    )
    print(a.out / "report.md")


if __name__ == "__main__":
    main()
