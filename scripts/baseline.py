"""Reference forecast: Laplace-smoothed historical win and lane-lead rates of starters."""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from build import ROOT, eligible, snapshot
from score import FIELDS


def predict(view):
    current = view["current"]["starters"]
    counts = defaultdict(Counter)
    for game in view["history"]:
        for player in game["players"]:
            side = player["side"]
            record = counts[player["name"]]
            record["games"] += 1
            record["wins"] += game["blue_win"] == (side == "blue")
            if game["blue_gd15"] is not None:
                record["observed15"] += 1
                diff = game["blue_gd15"] * (1 if side == "blue" else -1)
                record["ahead"] += diff > 0
    out = {}
    for key, success, total in [
        (FIELDS[0], "wins", "games"),
        (FIELDS[1], "ahead", "observed15"),
    ]:
        rates = {}
        for side, players in current.items():
            rates[side] = sum(
                (counts[p][success] + 1) / (counts[p][total] + 2) for p in players
            ) / len(players)
        out[key] = (rates["blue"] + 1 - rates["red"]) / 2
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--snapshot",
        type=Path,
        help="Only read this agent-visible JSON and print the forecast.",
    )
    args = parser.parse_args()
    if args.snapshot:
        print(json.dumps(predict(json.loads(args.snapshot.read_text()))))
        return
    games = json.loads((ROOT / "data/games.json").read_text())
    groups = defaultdict(list)
    for g in filter(eligible, games):
        prediction = predict(snapshot(games, g, "lobby"))
        errors = [
            (prediction[k] - y) ** 2
            for k, y in zip(FIELDS, (g["blue_win"], g["blue_gd15"] > 0))
        ]
        groups[g["patch"]].append(errors)
        groups["overall"].append(errors)
    for patch, rows in groups.items():
        print(patch, len(rows), *(round(sum(e) / len(e), 4) for e in zip(*rows)))


if __name__ == "__main__":
    main()
