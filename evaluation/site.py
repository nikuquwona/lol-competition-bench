"""Read-only local leaderboard, run explorer and exports for LoL Competition Bench."""

import argparse
import csv
import io
import json
import re
import shutil
import tempfile
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

from evaluation.run_index import ASSETS, TEAM_MARKS, RunIndex, visible_runs
from production.build import ROOT

STATIC = {
    "/": ("index.html", "text/html"),
    "/style.css": ("style.css", "text/css"),
    "/app.js": ("app.js", "text/javascript"),
    "/timeline.js": ("timeline.js", "text/javascript"),
    "/timeline.css": ("timeline.css", "text/css"),
}
FILES = {
    "prompt": "instruction.md",
    "snapshot": "snapshot.json",
    "transcript": "transcript.md",
    "events": ("trajectory.jsonl", "cli-events.log"),
    "stderr": "stderr.txt",
    "prediction": "prediction.json",
}
for logo in TEAM_MARKS.values():
    STATIC[logo] = (logo.lstrip("/"), "image/png")

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


def artifacts(folder, trial):
    files = trial.get("trajectory", {}).get("files", {})
    if trial.get("status") == "not_started":
        files = trial.get("files", {})
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
        for trial in [*doc["trials"], *doc.get("unstarted", [])]:
            included.update(artifacts(folder, trial).values())
        # Include organizer evidence explicitly named by an assembled public report.
        evidence = doc.get("provenance", {})
        for receipt in [
            *evidence.get("source_runs", []),
            *evidence.get("authentication_diagnostics", []),
        ]:
            sha = receipt.get("sha256", "")
            if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha):
                continue
            for name in (f"sources/{sha}.json", f"sources/{sha}-redactions.json"):
                if name not in (receipt.get("file"), receipt.get("redactions")):
                    continue
                file = folder / name
                if (
                    file.resolve().is_relative_to(folder)
                    and file.is_file()
                    and not file.is_symlink()
                ):
                    included.add(file)
        if evidence.get("quota_response") == "sources/quota-response.json":
            file = folder / evidence["quota_response"]
            if (
                file.resolve().is_relative_to(folder)
                and file.is_file()
                and not file.is_symlink()
            ):
                included.add(file)
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
                view = parse_qs(urlsplit(self.path).query).get("view", ["predictions"])[
                    0
                ]
                if view not in ("predictions", "diagnostics"):
                    return self.send_error(400)
                rows = sorted(
                    (r[0] for r in visible_runs(runs, view).values()),
                    key=lambda r: r["created_at"],
                    reverse=True,
                )
                return self.json({"runs": rows})
            if path in ("/api/leaderboard", "/api/leaderboard.csv"):
                ranks = index.ranks(visible_runs(runs, "predictions"))
                if path.endswith(".csv"):
                    filters = {
                        k: values[0]
                        for k, values in parse_qs(urlsplit(self.path).query).items()
                    }
                    if filters.pop("view", "") == "featured":
                        featured = ranks["featured"] or {}
                        rows = (
                            dict(e, release=featured["release"], suite="featured-five")
                            for e in featured.get("entries", [])
                            if all(str(e.get(k)) == v for k, v in filters.items())
                        )
                        columns = (
                            "release",
                            "suite",
                            "backend",
                            "track",
                            "protocol",
                            "model",
                            "harness",
                            "selected",
                            "attempted",
                            "scored",
                            "mean_scored_reward",
                            "mean_reward",
                            "run_id",
                        )
                        return self.reply(
                            csv_bytes(columns, rows),
                            "text/csv",
                            "five-game-results.csv",
                        )
                    groups = [
                        g
                        for g in ranks["groups"]
                        if all(str(g.get(k)) == v for k, v in filters.items())
                    ]
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
                            ({**g, **e} for g in groups for e in g["entries"]),
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
                return self.json(
                    {
                        "run": rec,
                        "report": index.details(doc)
                        if rec["kind"] == "prediction"
                        else doc,
                    }
                )
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
                    for t in [*doc["trials"], *doc.get("unstarted", [])]
                )
                return self.reply(
                    csv_bytes(TRIAL_COLUMNS, rows), "text/csv", "trials.csv"
                )
            if len(parts) not in (5, 6) or parts[3] != "trials":
                return self.send_error(404)
            trial = next(
                (
                    t
                    for t in [*doc["trials"], *doc.get("unstarted", [])]
                    if trial_key(t) == parts[4]
                ),
                None,
            )
            if trial is None:
                return self.send_error(404)
            mapped = artifacts(root, trial)
            if len(parts) == 5 or parts[5] == "timeline":
                tasks, _ = index.verified_tasks(doc)
                if ref := tasks.get(trial["task"]):
                    trial = {
                        **trial,
                        "match": ref["match"],
                        "observed_outcome": ref["labels"],
                    }
                if len(parts) == 6:
                    from evaluation.timeline import build_timeline

                    return self.json(
                        build_timeline(
                            mapped.get("events"),
                            phase=trial.get("phase"),
                            prediction=trial.get("prediction"),
                            outcome=trial.get("observed_outcome"),
                        )
                    )
                return self.json(
                    {
                        "run": rec,
                        "trial": trial,
                        "artifacts": {k: path + "/" + k for k in mapped},
                    }
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
