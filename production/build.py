"""Compile each forecast into an independent Harbor task with a physical as-of snapshot."""

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = """schema_version = "1.4"
artifacts = ["/app/prediction.json"]

[environment]
network_mode = "no-network"

[agent]
timeout_sec = 600
user = "agent"

[verifier]
environment_mode = "separate"
timeout_sec = 30

[verifier.environment]
network_mode = "no-network"
"""
AGENT_IMAGE = """FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends tmux asciinema && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home agent && mkdir -p /app && chown agent:agent /app
WORKDIR /app
COPY snapshot.json /app/snapshot.json
"""
PROMPT = Path(__file__).with_name("prompts") / "forecast.md"


def instruction(view):
    c = view["current"]
    locked = view["phase"] == "draft-lock"
    return PROMPT.read_text().format(
        game=c["n"],
        blue=c["blue"],
        red=c["red"],
        bo=c["bo"],
        patch=c["patch"],
        phase="draft lock" if locked else "the pre-draft lobby",
        observation="All draft actions are locked. The game has not started."
        if locked
        else "Starters and sides are known. The draft has not begun.",
        draft="Read current.bp in turn order; each action names its side, champion and ban or pick."
        if locked
        else "The target game's picks and bans are still unknown.",
        history_count=len(view["history"]),
    )


def eligible(g):
    return len(g["bp"]) == 20 and len(g["players"]) == 10 and g["blue_gd15"] is not None


def earlier(h, target):
    if h["series"] == target["series"]:
        return h["n"] < target["n"]
    if not h["replay_published"]:
        return False
    past = datetime.fromisoformat(h["series_time"])
    published = datetime.fromisoformat(h["replay_published"])
    cutoff = datetime.fromisoformat(target["series_time"])
    if "observed_at" in target:
        cutoff = min(
            cutoff, datetime.fromisoformat(target["observed_at"].replace("Z", "+00:00"))
        )
    return past < published < cutoff


def snapshot(records, target, phase):
    current = {
        k: target[k]
        for k in ("event", "stage", "series", "n", "patch", "bo", "blue", "red")
    }
    current["starters"] = {
        s: sorted(p["name"] for p in target["players"] if p["side"] == s)
        for s in ("blue", "red")
    }
    current["draft_rule"] = target.get("draft_rule", "Fearless")
    if phase == "draft-lock":
        current["bp"] = [
            {k: e[k] for k in ("turn", "side", "action", "champion")}
            for e in target["bp"]
        ]
    history = []
    for h in sorted(records, key=lambda r: (r["series_time"], r["series"], r["n"])):
        if not earlier(h, target):
            continue
        row = {
            k: h[k]
            for k in (
                "series",
                "series_time",
                "event",
                "n",
                "patch",
                "blue",
                "red",
                "blue_win",
                "blue_gd15",
                "bp",
            )
        }
        row["bp"] = [
            {k: e[k] for k in ("turn", "side", "action", "champion")} for e in row["bp"]
        ]
        # Ratings use a retrospective season-wide reference distribution. Never expose them.
        row["players"] = [
            {k: p[k] for k in ("name", "role", "side", "champion", "k", "d", "a")}
            for p in h["players"]
        ]
        history.append(row)
    return dict(
        phase=phase,
        series_time_utc=target["series_time"],
        current=current,
        history=history,
    )


def _write_task(out, context, target):
    out.mkdir(parents=True, exist_ok=True)
    for d in (
        ("environment",) if target is None else ("environment", "tests", "solution")
    ):
        (out / d).mkdir()
    (out / "instruction.md").write_text(instruction(context))
    (out / "task.toml").write_text(CONFIG)
    (out / "environment/Dockerfile").write_text(AGENT_IMAGE)
    # Do not rely on a phase-specific firewall for historical replay isolation.
    compose = "services:\n  main:\n    network_mode: none\n"
    (out / "environment/docker-compose.yaml").write_text(compose)
    (out / "environment/snapshot.json").write_text(
        json.dumps(context, ensure_ascii=False)
    )
    if target is None:
        return
    (out / "tests/docker-compose.yaml").write_text(compose)
    (out / "tests/Dockerfile").write_text(
        "FROM python:3.12-slim\nWORKDIR /app\nCOPY . /tests/\n"
    )
    labels = dict(
        p_blue_win=int(target["blue_win"]), p_blue_ahead_15=int(target["blue_gd15"] > 0)
    )
    (out / "tests/labels.json").write_text(json.dumps(labels))
    shutil.copyfile(ROOT / "production/score.py", out / "tests/score.py")
    (out / "tests/test.sh").write_text(
        "#!/bin/sh\nset -eu\nmkdir -p /logs/verifier\npython3 -I /tests/score.py\n"
    )
    (out / "solution/solve.sh").write_text(
        "#!/bin/sh\nset -eu\nprintf '%s\\n' '"
        + json.dumps(labels)
        + "' > /app/prediction.json\n"
    )
    for file in ("tests/test.sh", "solution/solve.sh"):
        (out / file).chmod(0o755)


def write_task(out, context, target=None):
    """Publish a complete directory atomically. Existing tasks are immutable."""
    import tempfile

    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        raise FileExistsError(out)
    with tempfile.TemporaryDirectory(dir=out.parent) as staging:
        task = Path(staging) / "task"
        _write_task(task, context, target)
        task.rename(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "tasks")
    parser.add_argument(
        "--phase", choices=["draft-lock", "lobby"], default="draft-lock"
    )
    parser.add_argument("--series")
    parser.add_argument("--game", type=int)
    args = parser.parse_args()
    records = json.loads((ROOT / "production/data/games.json").read_text())
    targets = [
        r
        for r in records
        if eligible(r)
        and (not args.series or r["series"] == args.series)
        and (not args.game or r["n"] == args.game)
    ]
    if not targets:
        parser.error("No eligible games match this selection.")
    for t in targets:
        directory = args.out / f"{t['series']}-g{t['n']}-{args.phase}"
        write_task(directory, snapshot(records, t, args.phase), t)
    print(f"{len(targets)} {args.phase} tasks under {args.out}")


if __name__ == "__main__":
    main()
