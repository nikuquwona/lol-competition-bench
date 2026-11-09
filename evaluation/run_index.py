"""Index published and local forecasts, verify scores and assemble model comparison views."""

import hashlib
import json
import os
import re
import tarfile
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path

from evaluation.cli.client import BIN
from evaluation.draft import draft_view
from evaluation.selections import CURRENT_SUITE, SUITES, suite_ids
from production.build import ROOT
from production.catalog import display_names

ASSETS = Path(__file__).with_name("site_assets")
TEAM_MARKS = {
    club: "/teams/" + record["file"]
    for club, record in json.loads((ASSETS / "teams/sources.json").read_bytes()).items()
}
BILLING = {
    "live": "DeepSeek API · 账户计费",
    "openrouter-free": "OpenRouter · 免费路由",
    "vendor": "Cursor · 厂商账户",
}


@lru_cache(maxsize=96)
def _read(path, stamp, size):
    if size > 32 * 1024 * 1024:
        raise ValueError("Report exceeds the local index size limit")
    return json.loads(path.read_bytes())


def read_doc(path):
    stat = path.stat()
    return _read(path, stat.st_mtime_ns, stat.st_size)


def is_boundary(doc):
    return not doc.get("planned") and any(
        isinstance(t, dict) and "scope" in t for t in doc.get("trials", [])
    )


@lru_cache(maxsize=8)
def release_truth(archive, modified, size, expected, manifest_path, manifest_stamp):
    """Read the organizer's verifier records only after verifying the archive bytes."""
    manifest = read_doc(manifest_path)
    rows = {r["id"]: r for r in manifest["tasks"]}
    result = {
        task: {k: row[k] for k in ("snapshot_sha256", "prompt_sha256", "phase")}
        for task, row in rows.items()
    }
    with archive.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != expected:
            raise ValueError("Release archive identity mismatch")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as tar:
            for member in tar:
                task, _, rel = member.name.partition("/")
                if rel not in ("tests/labels.json", "environment/snapshot.json"):
                    continue
                if (
                    task not in result
                    or not member.isfile()
                    or member.size > 32 * 1024 * 1024
                ):
                    raise ValueError("Invalid release member")
                row = result[task]
                with tar.extractfile(member) as file:
                    data = file.read()
                if rel == "tests/labels.json":
                    if "labels" in row:
                        raise ValueError("Duplicate grader record")
                    row["labels"] = json.loads(data)
                else:
                    if (
                        hashlib.sha256(data).hexdigest() != row["snapshot_sha256"]
                        or "match" in row
                    ):
                        raise ValueError("Invalid release snapshot")
                    snapshot = json.loads(data)
                    row["draft"] = draft_view(snapshot, row["phase"])
                    current = snapshot["current"]
                    row["match"] = {
                        key: current[key]
                        for key in (
                            "series",
                            "n",
                            "blue",
                            "red",
                            "patch",
                            "stage",
                            "bo",
                        )
                    }
                    for side in ("blue", "red"):
                        if logo := TEAM_MARKS.get(current[side]):
                            row["match"][side + "_logo"] = logo
    if any("labels" not in r or "match" not in r for r in result.values()):
        raise ValueError("Incomplete release data")
    return result


def run_kind(doc, root):
    mode = doc.get("mode")
    if mode not in ("live", "openrouter-free", "vendor"):
        return "diagnostic"
    interacted = False
    for trial in doc["trials"]:
        runtime = trial.get("runtime")
        # A failed CLI can still have made real upstream calls.
        if not runtime and re.fullmatch(r"[a-z0-9-]+", trial.get("task", "")):
            receipt = root / "jobs" / trial["task"] / "run.json"
            if receipt.is_file() and receipt.resolve().is_relative_to(root):
                runtime = read_doc(receipt)
        if not isinstance(runtime, dict):
            continue
        if (
            runtime.get("mode", mode) != mode
            or runtime.get("requested_model", runtime.get("model", doc["model"]))
            != doc["model"]
        ):
            return "diagnostic"
        accepted = runtime.get("accepted_requests")
        interacted |= (
            (type(accepted) is int and accepted > 0)
            or any(
                isinstance(e, dict) and e.get("status") == 200
                for e in runtime.get("upstream", [])
            )
            or (
                mode == "vendor"
                and trial.get("status") == "scored"
                and runtime.get("mode") == "vendor"
            )
        )
    if interacted:
        return "prediction"
    if not doc.get("summary") and any(
        t.get("status") == "started" for t in doc["trials"]
    ):
        return "pending"
    return "diagnostic"


def mirror_key(report):
    # Older repository examples are copies without a shared run ID. Match their
    # original runtime receipts and trial contents, ignoring later UI enrichment.
    identity = {
        k: report.get(k)
        for k in ("archive_sha256", "harness", "model", "mode", "backend", "planned")
    }
    identity["trials"] = [
        {
            k: t.get(k)
            for k in (
                "task",
                "snapshot_sha256",
                "prompt_sha256",
                "status",
                "runtime",
                "prediction",
                "brier",
                "reward",
            )
        }
        for t in report["trials"]
    ]
    return hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).digest()


@lru_cache(maxsize=128)
def file_sha(path, modified, size):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def report_digest(folder):
    path = folder / "report.json"
    st = path.stat()
    return file_sha(path, st.st_mtime_ns, st.st_size)


def visible_runs(runs, view):
    if view == "diagnostics":
        return {k: v for k, v in runs.items() if v[0]["kind"] == "diagnostic"}
    # Source shards stay accessible by their original links. Once published as a
    # suite, they are evidence for its score rather than additional model runs.
    incorporated = {
        t["origin"]["source_report_sha256"]
        for rec, doc, _ in runs.values()
        if rec["kind"] == "prediction" and doc.get("suite")
        for t in doc["trials"]
        if isinstance(t.get("origin"), dict)
        and isinstance(t["origin"].get("source_report_sha256"), str)
    }
    candidates = {
        k: v
        for k, v in runs.items()
        if v[0]["kind"] in ("prediction", "pending")
        and report_digest(v[2]) not in incorporated
    }
    local_copies = {
        mirror_key(doc)
        for rec, doc, folder in candidates.values()
        if rec["origin"] != "example" and not (folder / "redactions.json").is_file()
    }
    return {
        k: v
        for k, v in candidates.items()
        if (
            (v[0]["origin"] != "example" and not (v[2] / "redactions.json").is_file())
            or mirror_key(v[1]) not in local_copies
        )
    }


def game_rows(ids, tasks):
    games = {}
    for task in ids:
        ref = tasks[task]
        info = ref["match"]
        row = games.setdefault(
            (info["series"], info["n"]),
            {**info, "game": info["n"], "tasks": {}, "observed_outcome": ref["labels"]},
        )
        row["tasks"][ref["phase"].replace("-", "_")] = task
    return list(games.values())


class RunIndex:
    def __init__(self, roots, datasets=ROOT / "datasets"):
        self.roots = [(label, path.resolve()) for label, path in roots]
        self.dataset_roots = (
            [datasets] if isinstance(datasets, Path) else list(datasets)
        )

    def runs(self):
        found = {}
        for label, root in self.roots:
            for folder, dirs, files in os.walk(root):
                dirs[:] = [
                    d
                    for d in dirs
                    if d not in ("jobs", "traces", "artifacts", ".git")
                    and not d.startswith(".")
                ]
                if "report.json" not in files:
                    continue
                path = Path(folder) / "report.json"
                if path.is_symlink():
                    continue
                try:
                    doc = read_doc(path)
                    if not isinstance(doc, dict) or not isinstance(
                        doc.get("trials"), list
                    ):
                        continue
                    if not all(
                        isinstance(t, dict) and isinstance(t.get("task"), str)
                        for t in doc["trials"]
                    ):
                        continue
                    boundary = is_boundary(doc)
                    if not boundary and not isinstance(doc.get("planned"), list):
                        continue
                    rel = path.parent.relative_to(root).as_posix()
                    key = hashlib.sha256(f"{label}/{rel}".encode()).hexdigest()[:20]
                    trials = doc["trials"]
                    summary = doc.get("summary", {})
                    passed = sum(t.get("status") == "passed" for t in trials)
                    selected = len(trials) if boundary else len(doc["planned"])
                    scored = (
                        passed
                        if boundary
                        else sum(t.get("status") == "scored" for t in trials)
                    )
                    finished = (
                        bool(summary) or boundary and all("status" in t for t in trials)
                    )
                    stat = path.parent.stat()
                    time = (
                        doc.get("started_at")
                        or datetime.fromtimestamp(
                            getattr(stat, "st_birthtime", stat.st_mtime), UTC
                        ).isoformat()
                    )
                    rec = {
                        "id": key,
                        "name": rel,
                        "origin": label,
                        "release": doc["release"],
                        "backend": doc.get("backend", "docker"),
                        "harness": doc.get("harness")
                        or (
                            " / ".join(sorted({t["harness"] for t in trials}))
                            if boundary
                            else "baseline"
                        ),
                        "model": doc.get("model"),
                        "mode": doc.get("mode", "boundary"),
                        "selected": selected,
                        "scored": scored,
                        "mean_reward": summary.get("mean_reward"),
                        "coverage": scored / selected if selected else None,
                        "status": (
                            "completed"
                            if scored == selected
                            else "partial"
                            if scored
                            else "failed"
                        )
                        if finished
                        else "unfinished",
                        "created_at": time,
                    }
                    if doc.get("unstarted"):
                        rec["status"] = "partial"
                    rec["kind"] = run_kind(doc, path.parent)
                    rec["billing_source"] = BILLING.get(doc.get("mode"))
                    rec.update(display_names(doc["release"]))
                    found[key] = (rec, doc, path.parent)
                except (OSError, TypeError, KeyError, ValueError):
                    continue
        return found

    def verified_tasks(self, doc):
        release = doc["release"]
        if not isinstance(release, str) or not re.fullmatch(
            r"[a-z0-9][a-z0-9-]*", release
        ):
            return {}, None
        for base in self.dataset_roots:
            try:
                manifest_file = base / release / "manifest.json"
                manifest = read_doc(manifest_file)
                if (manifest["version"], manifest["sha256"]) != (
                    release,
                    doc.get("archive_sha256"),
                ):
                    continue
                archive = manifest_file.with_name("tasks.tar.gz")
                stat = archive.stat()
                tasks = release_truth(
                    archive,
                    stat.st_mtime_ns,
                    stat.st_size,
                    manifest["sha256"],
                    manifest_file,
                    manifest_file.stat().st_mtime_ns,
                )
                return tasks, manifest
            except (OSError, KeyError, ValueError, tarfile.TarError):
                continue
        return {}, None

    def details(self, doc):
        tasks, _ = self.verified_tasks(doc)
        trials = []
        for trial in doc["trials"]:
            reference = tasks.get(trial.get("task"))
            if reference:
                trial = {
                    **trial,
                    "match": reference["match"],
                    "observed_outcome": reference["labels"],
                }
            trials.append(trial)
        return {
            **doc,
            "trials": trials,
            "unstarted": [
                {**t, "match": tasks[t["task"]]["match"]} if t["task"] in tasks else t
                for t in doc.get("unstarted", [])
            ],
        }

    def featured(self, runs):
        """Show coverage on the fixed five games, including when a suite stops early."""
        from evaluation.ranking import check_trial

        spec = read_doc(SUITES / (CURRENT_SUITE + ".json"))
        tasks, manifest = self.verified_tasks(
            {"release": spec["release"], "archive_sha256": spec["archive_sha256"]}
        )
        if not manifest:
            return None
        featured_ids = set(suite_ids(CURRENT_SUITE, manifest))
        games = game_rows(sorted(featured_ids), tasks)
        order = {(g["series"], g["game"]): n for n, g in enumerate(spec["games"])}
        games.sort(key=lambda g: order[(g["series"], g["game"])])
        entries = []
        for key, (rec, doc, _) in runs.items():
            if doc.get("archive_sha256") != spec["archive_sha256"] or rec[
                "kind"
            ] not in ("prediction", "pending"):
                continue
            # The overview follows one run at a time; combining per-game bests would
            # overstate the results. Non-comparable cohorts remain separate in ranks().
            selected = featured_ids.intersection(doc["planned"])
            if not selected:
                continue
            subset = [t for t in doc["trials"] if t["task"] in selected]
            if (
                len(set(doc["planned"])) != len(doc["planned"])
                or len({t["task"] for t in doc["trials"]}) != len(doc["trials"])
                or any(t["task"] not in doc["planned"] for t in doc["trials"])
                or any(t.get("phase") != tasks[t["task"]]["phase"] for t in subset)
            ):
                continue
            submitted = [t for t in subset if t["status"] == "scored"]
            try:
                for t in submitted:
                    check_trial(t, tasks[t["task"]])
            except (TypeError, ValueError):
                continue
            attempted = sum(
                t["status"] not in ("unstarted", "not_run", "environment_error")
                for t in subset
            )
            finished = len(subset) == len(featured_ids) and all(
                t["status"] in ("scored", "failed", "interrupted") for t in subset
            )
            exact = set(doc["planned"]) == featured_ids
            phases = {}
            for phase in ("lobby", "draft-lock"):
                scores = [t["reward"] for t in submitted if t["phase"] == phase]
                count = sum(tasks[task]["phase"] == phase for task in featured_ids)
                phases[phase] = dict(
                    scored=len(scores),
                    selected=count,
                    mean_scored_reward=sum(scores) / len(scores) if scores else None,
                    mean_reward=sum(scores) / count if finished and exact else None,
                )
            entries.append(
                dict(
                    run_id=key,
                    model=rec["model"],
                    harness=rec["harness"],
                    backend=rec["backend"],
                    track="vendor" if doc["mode"] == "vendor" else "controlled",
                    protocol=doc.get("protocol_sha256", "suite-v1"),
                    selected=len(featured_ids),
                    attempted=attempted,
                    scored=len(submitted),
                    finished=finished,
                    status=rec["status"],
                    is_suite=exact,
                    created_at=rec["created_at"],
                    by_phase=phases,
                    rank=None,
                    mean_scored_reward=sum(t["reward"] for t in submitted)
                    / len(submitted)
                    if submitted
                    else None,
                    mean_reward=(
                        sum(t["reward"] for t in submitted) / len(featured_ids)
                    )
                    if finished and set(doc["planned"]) == featured_ids
                    else None,
                )
            )
        # Choose a representative by coverage and recency, independently of its score.
        entries.sort(
            key=lambda e: (
                e["is_suite"],
                e["scored"] == e["selected"],
                e["scored"],
                e["attempted"],
                e["created_at"],
                e["run_id"],
            ),
            reverse=True,
        )
        unique = {}
        for entry in entries:
            combo = (
                entry["backend"],
                entry["track"],
                entry["protocol"],
                entry["model"],
                entry["harness"],
            )
            unique.setdefault(combo, entry)
        entries = list(unique.values())
        eligible = [
            e
            for e in entries
            if e["track"] == "controlled"
            and e["is_suite"]
            and e["mean_reward"] is not None
            and e["scored"] == e["selected"]
        ]
        for entry in eligible:
            entry["rank"] = 1 + sum(
                e["protocol"] == entry["protocol"]
                and e["backend"] == entry["backend"]
                and round(e["mean_reward"], 12) > round(entry["mean_reward"], 12)
                for e in eligible
            )
        entries.sort(
            key=lambda e: (
                e["rank"] is None,
                e["backend"],
                e["track"],
                e["protocol"],
                e["rank"] or 0,
                -e["scored"],
                e["model"],
                e["harness"],
            )
        )
        return {
            "suite": CURRENT_SUITE,
            "release": spec["release"],
            **display_names(spec["release"]),
            "games": games,
            "entries": entries,
            "game_count": len(games),
        }

    def ranks(self, runs):
        from evaluation.ranking import leaderboard

        inputs = []
        for key, (rec, doc, _) in runs.items():
            if rec["kind"] != "prediction":
                continue
            tasks, _ = self.verified_tasks(doc)
            inputs.append((key, doc, tasks or None))
        ranks = leaderboard(inputs)
        lineup = []
        for group in ranks["groups"]:
            group.update(display_names(group["release"]))
            first = runs[group["entries"][0]["run_id"]][1]
            tasks, manifest = self.verified_tasks(first)
            group["games"] = game_rows(first["planned"], tasks)
            group["game_count"] = len(group["games"])
            try:
                group["is_featured"] = set(first["planned"]) == set(
                    suite_ids(CURRENT_SUITE, manifest)
                )
            except (KeyError, ValueError):
                group["is_featured"] = False
            for entry in group["entries"]:
                lineup.append(
                    {
                        **{
                            k: group[k]
                            for k in (
                                "release",
                                "backend",
                                "track",
                                "game_count",
                                "is_featured",
                            )
                        },
                        **{
                            k: entry[k]
                            for k in ("harness", "model", "run_id", "scored")
                        },
                    }
                )
        ranks["groups"].sort(
            key=lambda g: (
                not g["is_featured"],
                g["track"] != "controlled",
                -g["game_count"],
                -len(g["entries"]),
            )
        )
        ranks.update(lineup=lineup, harnesses=list(BIN), featured=self.featured(runs))
        return ranks
