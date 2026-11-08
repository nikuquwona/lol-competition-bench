"""Read-only local leaderboard, run explorer and exports for LoL Competition Bench."""

import argparse
import csv
import hashlib
import io
import json
import os
import re
import shutil
import tarfile
import tempfile
import zipfile
from datetime import UTC, datetime
from functools import lru_cache
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from production.build import ROOT
from production.catalog import display_names

ASSETS = Path(__file__).with_name("site_assets")
STATIC = {
    "/": ("index.html", "text/html"),
    "/style.css": ("style.css", "text/css"),
    "/app.js": ("app.js", "text/javascript"),
}
FILES = {
    "prompt": "instruction.md",
    "snapshot": "snapshot.json",
    "transcript": "transcript.md",
    "events": ("trajectory.jsonl", "cli-events.log"),
    "stderr": "stderr.txt",
    "prediction": "prediction.json",
}
MIME = {".json": "application/json", ".jsonl": "application/x-ndjson"}
TRIAL_COLUMNS = (
    "task",
    "phase",
    "harness",
    "status",
    "reward",
    "p_blue_win",
    "p_blue_ahead_15",
    "brier_win",
    "brier_ahead15",
    "error",
)


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


def trial_key(trial):
    return (trial["harness"] + "--" if "scope" in trial else "") + trial["task"]


def csv_bytes(fields, rows):
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow(
            {
                k: "'" + v
                if isinstance(v, str)
                and v.lstrip().startswith(("=", "+", "-", "@", "\t", "\r"))
                else v
                for k, v in row.items()
            }
        )
    return buf.getvalue().encode("utf-8-sig")


@lru_cache(maxsize=8)
def release_truth(archive, modified, size, expected, manifest_path, manifest_stamp):
    """Read the organizer's verifier records only after verifying the archive bytes."""
    manifest = read_doc(manifest_path)
    rows = {r["id"]: r for r in manifest["tasks"]}
    result = {}
    with archive.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != expected:
            raise ValueError("Release archive identity mismatch")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as tar:
            for m in tar:
                parts = m.name.split("/")
                if len(parts) != 3 or parts[1:] != ["tests", "labels.json"]:
                    continue
                task = parts[0]
                if (
                    task not in rows
                    or task in result
                    or not m.isfile()
                    or m.size > 4096
                ):
                    raise ValueError("Invalid grader record")
                row = rows[task]
                result[task] = {
                    "labels": json.load(tar.extractfile(m)),
                    "snapshot_sha256": row["snapshot_sha256"],
                    "prompt_sha256": row["prompt_sha256"],
                }
    if result.keys() != rows.keys():
        raise ValueError("Missing grader records")
    return result


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
                    rec.update(display_names(doc["release"]))
                    found[key] = (rec, doc, path.parent)
                except (OSError, TypeError, KeyError, ValueError):
                    continue
        return found

    def ranks(self, runs):
        from evaluation.ranking import leaderboard

        inputs = []
        for key, (rec, doc, _) in runs.items():
            if is_boundary(doc) or rec["origin"] == "example":
                continue
            ids = None
            release = doc["release"]
            if isinstance(release, str) and re.fullmatch(
                r"[a-z0-9][a-z0-9-]*", release
            ):
                for base in self.dataset_roots:
                    try:
                        manifest = read_doc(base / release / "manifest.json")
                        if (
                            manifest["sha256"] == doc.get("archive_sha256")
                            and manifest["version"] == release
                        ):
                            archive = base / release / "tasks.tar.gz"
                            manifest_file = archive.with_name("manifest.json")
                            stat = archive.stat()
                            ids = release_truth(
                                archive,
                                stat.st_mtime_ns,
                                stat.st_size,
                                manifest["sha256"],
                                manifest_file,
                                manifest_file.stat().st_mtime_ns,
                            )
                            break
                    except (OSError, KeyError, ValueError, tarfile.TarError):
                        continue
            inputs.append((key, doc, ids))
        ranks = leaderboard(inputs)
        for group in ranks["groups"]:
            group.update(display_names(group["release"]))
        return ranks


def artifacts(folder, trial):
    files = trial.get("trajectory", {}).get("files", {})
    boundary = "scope" in trial
    if boundary:
        files = trial.get("artifacts", {})
    task = trial["task"]
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", task):
        return {}
    result = {}
    for key, names in FILES.items():
        if isinstance(names, str):
            names = (names,)
        hint = files.get(key) or (
            files.get("native_log") or files.get("cli_events")
            if key == "events"
            else None
        )
        candidates = []
        if isinstance(hint, str):
            candidates.append(folder / hint)
        # Older suites may have native files without the new artifact index.
        for name in names:
            trial_dir = folder / "jobs" / task
            candidates += [folder / "traces" / task / name, trial_dir / name]
        if boundary:
            phase = "draft-lock" if task.endswith("-draft-lock") else "lobby"
            candidates += [folder / trial["harness"] / phase / n for n in names]
        for path in candidates:
            actual = path.resolve()
            if (
                actual.name in names
                and actual.is_relative_to(folder.resolve())
                and actual.is_file()
                and not path.is_symlink()
            ):
                result[key] = actual
                break
    return result


def write_bundle(target, folder, doc):
    """Export the same file allowlist as the trial viewer, preserving portable links."""
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("report.json", json.dumps(doc, ensure_ascii=False, indent=2))
        included = set()
        overview = folder / "report.md"
        if overview.is_file() and not overview.is_symlink():
            included.add(overview)
        for trial in doc["trials"]:
            included.update(artifacts(folder, trial).values())
        for file in sorted(included):
            archive.write(file, file.relative_to(folder).as_posix())


def make_handler(index):
    class Site(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def reply(self, content, mime, filename=None):
            self.send_response(200)
            self.send_header(
                "Content-Type",
                mime + ("; charset=utf-8" if mime.startswith("text/") else ""),
            )
            self.send_header(
                "Content-Length",
                str(
                    content.stat().st_size
                    if isinstance(content, Path)
                    else len(content)
                ),
            )
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; style-src 'self' 'unsafe-inline'; object-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'",
            )
            if filename:
                self.send_header(
                    "Content-Disposition", f'attachment; filename="{filename}"'
                )
            self.end_headers()
            if isinstance(content, Path):
                with content.open("rb") as stream:
                    shutil.copyfileobj(stream, self.wfile)
            else:
                self.wfile.write(content)

        def json(self, obj, filename=None):
            self.reply(
                json.dumps(obj, ensure_ascii=False, allow_nan=False).encode(),
                "application/json",
                filename,
            )

        def do_GET(self):
            # Accept only the local origin even when a browser resolves another domain to loopback.
            port = self.server.server_port
            if self.headers.get("Host", "") not in (
                f"localhost:{port}",
                f"127.0.0.1:{port}",
            ):
                return self.send_error(403)
            origin = self.headers.get("Origin")
            if origin and origin not in (
                f"http://localhost:{port}",
                f"http://127.0.0.1:{port}",
            ):
                return self.send_error(403)
            if (
                self.headers.get("Sec-Fetch-Site") == "cross-site"
                and self.headers.get("Sec-Fetch-Mode") != "navigate"
            ):
                return self.send_error(403)
            path = unquote(urlsplit(self.path).path)
            if path in STATIC:
                file, mime = STATIC[path]
                return self.reply(ASSETS / file, mime)
            if not path.startswith("/api/"):
                return self.send_error(404)
            runs = index.runs()
            if path == "/api/rules.md":
                return self.reply(ASSETS.parent / "RANKING.md", "text/plain")
            if path == "/api/runs":
                rows = sorted(
                    (r[0] for r in runs.values()),
                    key=lambda r: r["created_at"],
                    reverse=True,
                )
                return self.json({"runs": rows})
            if path in ("/api/leaderboard", "/api/leaderboard.csv"):
                ranks = index.ranks(runs)
                if path.endswith(".csv"):
                    fields = (
                        "release",
                        "archive_sha256",
                        "backend",
                        "track",
                        "scope",
                        "selection_sha256",
                        "selected",
                        "rank",
                        "harness",
                        "model",
                        "attempts",
                        "scored",
                        "completion_rate",
                        "mean_reward",
                        "brier_win",
                        "brier_ahead15",
                        "run_id",
                    )
                    return self.reply(
                        csv_bytes(
                            fields,
                            ({**g, **e} for g in ranks["groups"] for e in g["entries"]),
                        ),
                        "text/csv",
                        "leaderboard.csv",
                    )
                return self.json(ranks)
            parts = path.strip("/").split("/")
            if len(parts) < 3 or parts[:2] != ["api", "runs"] or parts[2] not in runs:
                return self.send_error(404)
            rec, doc, root = runs[parts[2]]
            if len(parts) == 3:
                return self.json({"run": rec, "report": doc})
            if parts[3:] == ["bundle.zip"]:
                with tempfile.TemporaryDirectory() as tmp:
                    file = Path(tmp) / "run.zip"
                    write_bundle(file, root, doc)
                    return self.reply(file, "application/zip", f"run-{rec['id']}.zip")
            if parts[3:] == ["report.json"]:
                return self.json(doc, "report.json")
            if parts[3:] == ["trials.csv"]:
                rows = (
                    {
                        **t,
                        **(t.get("prediction") or {}),
                        "harness": t.get("harness", rec["harness"]),
                        "brier_win": (t.get("brier") or {}).get("p_blue_win"),
                        "brier_ahead15": (t.get("brier") or {}).get("p_blue_ahead_15"),
                    }
                    for t in doc["trials"]
                )
                return self.reply(
                    csv_bytes(TRIAL_COLUMNS, rows), "text/csv", "trials.csv"
                )
            if len(parts) not in (5, 6) or parts[3] != "trials":
                return self.send_error(404)
            trial = next((t for t in doc["trials"] if trial_key(t) == parts[4]), None)
            if trial is None:
                return self.send_error(404)
            mapped = artifacts(root, trial)
            if len(parts) == 5:
                if "snapshot" in mapped:
                    current = read_doc(mapped["snapshot"]).get("current", {})
                    trial = {
                        **trial,
                        "match": {
                            k: current[k]
                            for k in ("blue", "red", "stage", "bo", "n")
                            if k in current
                        },
                    }
                return self.json(
                    {"trial": trial, "artifacts": {k: path + "/" + k for k in mapped}}
                )
            if parts[5] not in mapped:
                return self.send_error(404)
            file = mapped[parts[5]]
            return self.reply(file, MIME.get(file.suffix, "text/plain"))

    return Site


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--port", type=int, default=8765)
    p.add_argument(
        "--runs-dir",
        action="append",
        type=Path,
        help="Root containing run reports; repeat to add more",
    )
    p.add_argument(
        "--datasets-dir",
        action="append",
        type=Path,
        default=[],
        help="Additional trusted directories containing release manifests and archives",
    )
    a = p.parse_args()
    roots = [
        (f"local-{i + 1}", root.resolve())
        for i, root in enumerate(a.runs_dir or [ROOT / ".work"])
    ]
    roots.append(("example", ROOT / "evaluation/examples"))
    with ThreadingHTTPServer(
        ("127.0.0.1", a.port),
        make_handler(RunIndex(roots, [ROOT / "datasets", *a.datasets_dir])),
    ) as server:
        print(
            f"LoL Competition Bench  http://127.0.0.1:{server.server_port}", flush=True
        )
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
