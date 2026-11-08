"""Freeze an unstarted Riot series and score timestamped receipts after it completes."""

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from production.build import ROOT


def now():
    return datetime.now(timezone.utc)


def riot_event(event_id):
    url = "https://lolesports.com/en-US/leagues/worlds"
    with urlopen(Request(url, headers={"Cache-Control": "no-cache"}), timeout=25) as r:
        html = r.read().decode()
    matches = []
    for m in re.finditer(r'\{"__typename":"EventMatch","id":', html):
        e, _ = json.JSONDecoder().raw_decode(html, m.start())
        if e["id"] == event_id:
            matches.append(e)
    if not matches or len({(e["state"], e["startTime"]) for e in matches}) != 1:
        raise ValueError("Riot event missing or conflicting")
    return matches[0]


def validate_open(e, ts):
    if e["state"] != "unstarted" or ts >= datetime.fromisoformat(
        e["startTime"].replace("Z", "+00:00")
    ):
        raise ValueError("Forecast window closed")


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def freeze(event_id, path):
    e = riot_event(event_id)
    ts = now()
    validate_open(e, ts)
    history = []
    for g in json.loads((ROOT / "production/data/games.json").read_text()):
        if g["replay_published"] and datetime.fromisoformat(g["replay_published"]) < ts:
            h = {
                k: g[k]
                for k in (
                    "series",
                    "n",
                    "event",
                    "series_time",
                    "blue",
                    "red",
                    "patch",
                    "bp",
                    "blue_win",
                    "blue_gd15",
                )
            }
            h["players"] = [
                {k: p[k] for k in ("name", "role", "side", "champion", "k", "d", "a")}
                for p in g["players"]
            ]
            history.append(h)
    doc = dict(
        frozen_at=ts.isoformat(),
        event_id=e["id"],
        scheduled=e["startTime"],
        stage=e["blockName"],
        teams=[t["code"] for t in e["matchTeams"]],
        best_of=e["match"]["strategy"]["count"],
        history=history,
        question="Probability that teams[0] wins this entire series, before game one.",
    )
    with path.open("x") as f:
        json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("freeze", "seal", "settle"))
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--event-id")
    parser.add_argument("--probability", type=float)
    parser.add_argument("--receipt", type=Path, default=Path("receipt.json"))
    args = parser.parse_args()
    if args.action == "freeze":
        if not args.event_id:
            parser.error("freeze requires --event-id")
        freeze(args.event_id, args.snapshot)
        return
    doc = json.loads(args.snapshot.read_text())
    e = riot_event(doc["event_id"])
    if (
        doc["teams"] != [t["code"] for t in e["matchTeams"]]
        or doc["scheduled"] != e["startTime"]
    ):
        raise ValueError("Fixture identity or schedule changed")
    if args.action == "seal":
        ts = now()
        validate_open(e, ts)
        if args.probability is None or not 0 <= args.probability <= 1:
            parser.error("probability must be finite and in [0,1]")
        with args.receipt.open("x") as f:
            json.dump(
                dict(
                    snapshot_sha256=fingerprint(args.snapshot),
                    sealed_at=ts.isoformat(),
                    event_id=e["id"],
                    p_team0_series_win=args.probability,
                ),
                f,
            )
        return
    receipt = json.loads(args.receipt.read_text())
    if (
        e["state"] != "completed"
        or receipt["event_id"] != e["id"]
        or receipt["snapshot_sha256"] != fingerprint(args.snapshot)
        or datetime.fromisoformat(receipt["sealed_at"])
        >= datetime.fromisoformat(doc["scheduled"].replace("Z", "+00:00"))
    ):
        raise ValueError(
            "Settlement requires a matching pre-start receipt and completed series"
        )
    outcomes = [t["result"]["outcome"] for t in e["matchTeams"]]
    if sorted(outcomes) != ["loss", "win"]:
        raise ValueError("Riot winner unavailable")
    p = receipt["p_team0_series_win"]
    if type(p) not in (float, int) or not 0 <= p <= 1:
        raise ValueError("Invalid probability")
    print(
        json.dumps(
            dict(
                winner=doc["teams"][outcomes.index("win")],
                brier=(p - int(outcomes[0] == "win")) ** 2,
            )
        )
    )


if __name__ == "__main__":
    main()
