"""Operator-side lifecycle for a single game. All persisted inputs and receipts are write-once."""

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from production.build import ROOT, snapshot, write_task
from production.score import FIELDS, read_prediction, score

DEFAULT_STORE = ROOT / ".work/intake"
BASE_HISTORY = ROOT / "production/data/games.json"
SIDES = ("blue", "red")
FIRST_PICK_ORDER = "ABABAB" + "ABBAAB" + "BABA" + "BAAB"


@contextmanager
def store_lock(store):
    # The intake directory belongs to the organizer on a local POSIX filesystem.
    store.mkdir(parents=True, exist_ok=True)
    with (store / ".intake.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def now():
    return datetime.now(timezone.utc)


def instant(value):
    if not isinstance(value, str):
        raise ValueError("Expected an ISO-8601 timestamp")
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("Timestamp requires a UTC offset")
    return dt.astimezone(timezone.utc)


def slug(value):
    if not isinstance(value, str) or not re.fullmatch(
        r"[a-z0-9][a-z0-9-]{0,100}", value
    ):
        raise ValueError("Expected a lowercase slug")
    return value


def read(path):
    return json.loads(path.read_bytes())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put_once(path, value):
    """Atomic create without replacement, even with simultaneous submissions."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as tmp:
        tmp_path = Path(tmp.name)
        try:
            tmp.write((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode())
            tmp.flush()
            os.fsync(tmp.fileno())
            os.link(tmp_path, path)
        finally:
            tmp_path.unlink(missing_ok=True)


def exact(value, keys):
    if not isinstance(value, dict) or set(value) != set(keys.split()):
        raise ValueError(f"Expected exactly these fields: {keys}")


def name(s):
    if (
        not isinstance(s, str)
        or not 0 < len(s) <= 100
        or not all(c.isprintable() for c in s)
    ):
        raise ValueError("Invalid name")
    return s


def source(url):
    parts = urlsplit(url)
    if parts.scheme != "https" or not parts.hostname or parts.username:
        raise ValueError("Supply the HTTPS source of the observation")
    return url


def validate_observation(o):
    required = "event stage series n patch bo blue red starters draft_rule phase series_time observed_at source"
    if not isinstance(o, dict):
        raise ValueError("Observation must be an object")
    locked = o.get("phase") == "draft-lock"
    exact(o, required + (" bp" if locked else ""))
    if not locked and o["phase"] != "lobby":
        raise ValueError("Unknown phase")
    slug(o["series"])
    for k in ("event", "stage", "blue", "red"):
        name(o[k])
    if not isinstance(o["patch"], str) or not re.fullmatch(
        r"\d{1,2}\.\d{1,2}", o["patch"]
    ):
        raise ValueError("Invalid tournament patch")
    if (
        o["blue"] == o["red"]
        or type(o["bo"]) != int
        or o["bo"] not in (1, 3, 5, 7)
        or type(o["n"]) != int
        or not 1 <= o["n"] <= o["bo"]
    ):
        raise ValueError("Invalid teams or series format")
    if o["draft_rule"] not in ("Fearless", "Standard"):
        raise ValueError("Unknown draft rules")
    exact(o["starters"], "blue red")
    handles = []
    for side in SIDES:
        team = o["starters"][side]
        if not isinstance(team, list) or len(team) != 5:
            raise ValueError("Five starters required on each side")
        handles.extend(name(p).casefold() for p in team)
    if len(set(handles)) != 10:
        raise ValueError("Duplicate starter")
    source(o["source"])
    instant(o["series_time"])
    instant(o["observed_at"])
    if locked:
        validate_bp(o["bp"])


def validate_bp(bp):
    if not isinstance(bp, list) or len(bp) != 20:
        raise ValueError("20 BP turns required")
    exact(bp[0], "turn side action champion")
    first = bp[0]["side"]
    if first not in SIDES:
        raise ValueError("Invalid first side")
    other = "red" if first == "blue" else "blue"
    # Relative to first pick; the first side can be red.
    pattern = FIRST_PICK_ORDER
    champs = []
    for n, (e, side) in enumerate(zip(bp, pattern), 1):
        exact(e, "turn side action champion")
        action = "ban" if n <= 6 or 13 <= n <= 16 else "pick"
        if type(e["turn"]) != int or (e["turn"], e["side"], e["action"]) != (
            n,
            first if side == "A" else other,
            action,
        ):
            raise ValueError(f"Invalid BP action at turn {n}")
        champs.append(name(e["champion"]).casefold())
    if len(set(champs)) != 20:
        raise ValueError("A champion appears twice in BP")


def task_id(o):
    return f"{o['series']}-g{o['n']}-{o['phase']}"


def trusted_case(case):
    manifest = read(case / "observation.json")
    for filename, key in [
        ("environment/snapshot.json", "snapshot_sha256"),
        ("instruction.md", "prompt_sha256"),
    ]:
        if digest(case / "task" / filename) != manifest[key]:
            raise ValueError(f"Frozen file changed: {filename}")
    return manifest


def result_path(case):
    match = re.fullmatch(
        r"([a-z0-9][a-z0-9-]{0,100}-g[1-7])-(?:draft-lock|lobby)", case.name
    )
    if not match:
        raise ValueError("Expected a frozen game case")
    return case.parent / "results" / (match[1] + ".json")


def settled_cases(store):
    for path in sorted((store / "results").glob("*.json")):
        result = read(path)
        for identifier, fingerprint in sorted(result["observations"].items()):
            if Path(identifier).name != identifier:
                raise ValueError("Invalid result reference")
            case = store / identifier
            meta = trusted_case(case)
            if result_path(case) != path or meta["snapshot_sha256"] != fingerprint:
                raise ValueError("Settled observation identity mismatch")
            yield case, meta, result


def history(store):
    games = read(BASE_HISTORY)
    seen = {(g["series"], g["n"]) for g in games}
    for case, meta, result in settled_cases(store):
        view = read(case / "task/environment/snapshot.json")
        c = view["current"]
        if (c["series"], c["n"]) in seen:
            continue
        games.append(
            {
                **c,
                "series_time": view["series_time_utc"],
                "bp": result["bp"],
                "players": result["players"],
                "blue_win": result["winner"] == "blue",
                "blue_gd15": result["blue_gd15"],
                "game_published_at": result["published_at"],
                "replay_published": None,
            }
        )
        seen.add((c["series"], c["n"]))
    for path in sorted((store / "history").glob("*.json")):
        r = read(path)
        key = r["series"], r["n"]
        if key in seen:
            raise ValueError(f"Duplicate completed game: {key}")
        seen.add(key)
        games.append(r)
    series = {}
    for g in games:
        if "game_published_at" in g:
            series.setdefault(g["series"], []).append(g)
    for group in series.values():
        all_games = sorted(
            (g for g in games if g["series"] == group[0]["series"]),
            key=lambda g: g["n"],
        )
        winners = [g["blue"] if g["blue_win"] else g["red"] for g in all_games]
        clinched = any(winners.count(w) >= group[0]["bo"] // 2 + 1 for w in winners)
        if clinched and [g["n"] for g in all_games] == list(
            range(1, len(all_games) + 1)
        ):
            dates = [
                g.get("game_published_at") or g.get("replay_published")
                for g in all_games
            ]
            if all(dates):
                embargo = max(instant(d) for d in dates).isoformat()
                for g in group:
                    g["replay_published"] = embargo
    return games


def validate_predecessors(o, records):
    if any(r["series"] == o["series"] and r["n"] >= o["n"] for r in records):
        raise ValueError(
            "The history store already contains this game or a later game in the series"
        )
    previous = [r for r in records if r["series"] == o["series"]]
    if any(
        {r["blue"], r["red"]} != {o["blue"], o["red"]} or r["bo"] != o["bo"]
        for r in previous
    ):
        raise ValueError("Earlier series metadata disagrees")
    # Manually appended observations carry a publication timestamp for the individual game.
    if any(
        r.get("game_published_at")
        and instant(r["game_published_at"]) > instant(o["observed_at"])
        for r in previous
    ):
        raise ValueError("Earlier game was unavailable at the stated cutoff")
    if {r["n"] for r in previous} != set(range(1, o["n"])):
        raise ValueError("Record the earlier games of this series first")
    winners = [r["blue"] if r["blue_win"] else r["red"] for r in previous]
    if any(winners.count(team) >= o["bo"] // 2 + 1 for team in (o["blue"], o["red"])):
        raise ValueError("This series has already been won")
    if o["phase"] == "draft-lock" and o["draft_rule"] == "Fearless":
        if any(len(r["bp"]) != 20 for r in previous):
            raise ValueError("A previous Fearless game is missing its full draft")
        used = {
            e["champion"].casefold()
            for r in previous
            for e in r["bp"]
            if e["action"] == "pick"
        }
        if any(
            e["champion"].casefold() in used for e in o["bp"] if e["action"] == "pick"
        ):
            raise ValueError("Previously picked champion in Fearless draft")


def freeze(o, store):
    with store_lock(store):
        return _freeze(o, store)


def _freeze(o, store):
    validate_observation(o)
    frozen = now()
    if instant(o["observed_at"]) > frozen:
        raise ValueError("Observation is in the future")
    store.mkdir(parents=True, exist_ok=True)
    case = store / task_id(o)
    if result_path(case).exists():
        raise ValueError("Game already settled")
    if case.exists():
        raise FileExistsError(case)
    g = {
        **o,
        "series_time": instant(o["series_time"]).isoformat(),
        "players": [{"side": s, "name": p} for s in SIDES for p in o["starters"][s]],
    }
    other_phase = "lobby" if o["phase"] == "draft-lock" else "draft-lock"
    sibling = store / task_id({**o, "phase": other_phase})
    if sibling.exists():
        trusted_case(sibling)
        other = read(sibling / "task/environment/snapshot.json")["current"]
        keys = (
            "event",
            "stage",
            "series",
            "n",
            "bo",
            "patch",
            "blue",
            "red",
            "draft_rule",
        )
        if any(other[k] != o[k] for k in keys) or any(
            sorted(o["starters"][s]) != other["starters"][s] for s in SIDES
        ):
            raise ValueError("Lobby and draft identity disagree")
        if o["phase"] == "lobby":
            raise ValueError("Cannot freeze a pre-draft lobby after draft lock")
        if instant(trusted_case(sibling)["observed_at"]) > instant(o["observed_at"]):
            raise ValueError("Draft lock precedes lobby observation")
    records = history(store)
    validate_predecessors(o, records)
    view = snapshot(records, g, o["phase"])
    view["observed_at_utc"] = instant(o["observed_at"]).isoformat()
    with tempfile.TemporaryDirectory(dir=store) as temp:
        stage = Path(temp) / "case"
        write_task(stage / "task", view)
        put_once(
            stage / "observation.json",
            dict(
                id=task_id(o),
                source=o["source"],
                frozen_at=frozen.isoformat(),
                observed_at=view["observed_at_utc"],
                snapshot_sha256=digest(stage / "task/environment/snapshot.json"),
                prompt_sha256=digest(stage / "task/instruction.md"),
            ),
        )
        stage.rename(case)
    return case


def submit(case, entrant, prediction):
    with store_lock(case.parent):
        return _submit(case, entrant, prediction)


def _submit(case, entrant, prediction):
    meta = trusted_case(case)
    if result_path(case).exists():
        raise ValueError("Already settled")
    if (
        not isinstance(prediction, dict)
        or set(prediction) != set(FIELDS)
        or not all(type(p) in (float, int) and 0 <= p <= 1 for p in prediction.values())
    ):
        raise ValueError("Invalid probability submission")
    receipt = dict(
        id=meta["id"],
        entrant=slug(entrant),
        submitted_at=now().isoformat(),
        prediction=prediction,
        snapshot_sha256=meta["snapshot_sha256"],
        prompt_sha256=meta["prompt_sha256"],
    )
    put_once(case / "receipts" / (entrant + ".json"), receipt)
    return receipt


def settle(case, r):
    with store_lock(case.parent):
        return _settle(case, r)


def _settle(case, r):
    exact(
        r,
        "id winner blue_gd15 game_started_at published_at source"
        + (" players" if "players" in r else "")
        + (" bp" if "bp" in r else ""),
    )
    meta = trusted_case(case)
    if r["id"] != meta["id"] or r["winner"] not in SIDES or type(r["blue_gd15"]) != int:
        raise ValueError("Result identity, winner or gold difference invalid")
    start, published = instant(r["game_started_at"]), instant(r["published_at"])
    if not instant(meta["frozen_at"]) < start <= published <= now():
        raise ValueError("Require freeze < game start <= publication <= current time")
    source(r["source"])
    view = read(case / "task/environment/snapshot.json")
    c = view["current"]
    captures = {}
    actual_bp = r.get("bp", [])
    for phase in ("lobby", "draft-lock"):
        sibling = case.parent / task_id({**c, "phase": phase})
        if not sibling.is_dir():
            continue
        observation = trusted_case(sibling)
        if instant(observation["frozen_at"]) >= start:
            raise ValueError("An observation was frozen after game start")
        captures[sibling.name] = observation["snapshot_sha256"]
        if phase == "draft-lock":
            locked = read(sibling / "task/environment/snapshot.json")["current"]["bp"]
            if actual_bp and actual_bp != locked:
                raise ValueError("Result conflicts with frozen BP")
            actual_bp = locked
    if actual_bp:
        validate_bp(actual_bp)
    players = r.get("players", [])
    view = read(case / "task/environment/snapshot.json")
    if not isinstance(players, list):
        raise ValueError("Box scores must be an array")
    if players:
        c = view["current"]
        if len(players) != 10:
            raise ValueError("Ten box scores required")
        for p in players:
            exact(p, "side name role champion k d a")
            if (
                p["side"] not in SIDES
                or p["name"] not in c["starters"][p["side"]]
                or any(type(p[k]) != int or p[k] < 0 for k in ("k", "d", "a"))
            ):
                raise ValueError("Invalid player box score")
            name(p["role"])
            name(p["champion"])
        if len({p["name"] for p in players}) != 10:
            raise ValueError("Duplicate player")
        if actual_bp:
            for side in SIDES:
                if {p["champion"] for p in players if p["side"] == side} != {
                    e["champion"]
                    for e in actual_bp
                    if e["side"] == side and e["action"] == "pick"
                }:
                    raise ValueError("Box score champions disagree with BP")
    result = {
        **r,
        "observations": captures,
        "bp": actual_bp,
        "players": players,
        "published_at": published.isoformat(),
    }
    put_once(result_path(case), result)
    return standings(case)


def standings(case):
    meta = trusted_case(case)
    r = read(result_path(case))
    if r["observations"].get(case.name) != meta["snapshot_sha256"]:
        raise ValueError("Result identity mismatch")
    labels = dict(
        p_blue_win=int(r["winner"] == "blue"), p_blue_ahead_15=int(r["blue_gd15"] > 0)
    )
    rows = []
    for path in sorted((case / "receipts").glob("*.json")):
        receipt = read(path)
        valid = (
            receipt["snapshot_sha256"] == meta["snapshot_sha256"]
            and receipt["prompt_sha256"] == meta["prompt_sha256"]
            and instant(meta["frozen_at"])
            <= instant(receipt["submitted_at"])
            < instant(r["game_started_at"])
        )
        rows.append(
            dict(
                entrant=receipt["entrant"],
                status="scored" if valid else "ineligible",
                reward=score(receipt["prediction"], labels) if valid else None,
            )
        )
    return rows


def history_add(doc, store):
    """Import already completed games as evidence only (no retroactive benchmark score)."""
    exact(
        doc, "observation winner blue_gd15 game_started_at published_at result_source"
    )
    o = doc["observation"]
    validate_observation(o)
    if (
        o["phase"] != "draft-lock"
        or doc["winner"] not in SIDES
        or type(doc["blue_gd15"]) != int
    ):
        raise ValueError("Expected a complete historical draft and outcome")
    source(doc["result_source"])
    if (
        not instant(o["observed_at"])
        <= instant(doc["game_started_at"])
        < instant(doc["published_at"])
        <= now()
    ):
        raise ValueError("Invalid historical timestamps")
    g = {
        k: o[k]
        for k in (
            "event",
            "stage",
            "series",
            "n",
            "bo",
            "patch",
            "blue",
            "red",
            "bp",
            "draft_rule",
        )
    }
    g.update(
        series_time=instant(o["series_time"]).isoformat(),
        players=[],
        blue_win=doc["winner"] == "blue",
        blue_gd15=doc["blue_gd15"],
        game_published_at=instant(doc["published_at"]).isoformat(),
        replay_published=None,
        source=o["source"],
        result_source=doc["result_source"],
    )
    with store_lock(store):
        validate_predecessors(o, history(store))
        if any(
            (store / task_id({**o, "phase": phase})).exists()
            for phase in ("lobby", "draft-lock")
        ):
            raise ValueError("Use settle for an existing observation")
        path = store / "history" / f"{g['series']}-g{g['n']}.json"
        put_once(path, g)
        return path


def template(series, game, bo, phase, first):
    if not 1 <= game <= bo:
        raise ValueError("Game number must be inside the series")
    doc = dict(
        series=slug(series),
        event="",
        stage="",
        n=game,
        bo=bo,
        patch="",
        blue="",
        red="",
        starters={side: [""] * 5 for side in SIDES},
        draft_rule="Fearless",
        phase=phase,
        series_time="",
        observed_at="",
        source="",
    )
    if phase == "draft-lock":
        if first not in SIDES:
            raise ValueError("Specify --first-pick blue or red")
        other = "red" if first == "blue" else "blue"
        doc["bp"] = [
            dict(
                turn=n,
                side=first if side == "A" else other,
                action="ban" if n <= 6 or 13 <= n <= 16 else "pick",
                champion="",
            )
            for n, side in enumerate(FIRST_PICK_ORDER, 1)
        ]
    return doc


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    h = sub.add_parser("history-add")
    h.add_argument("record", type=Path)
    h.add_argument("--store", type=Path, default=DEFAULT_STORE)
    init = sub.add_parser("init-game")
    init.add_argument("--series", required=True)
    init.add_argument("--game", required=True, type=int)
    init.add_argument("--bo", type=int, required=True, choices=(1, 3, 5, 7))
    init.add_argument("--phase", choices=("lobby", "draft-lock"), required=True)
    init.add_argument("--first-pick", choices=SIDES)
    init.add_argument("--out", type=Path, required=True)
    f = sub.add_parser("freeze")
    f.add_argument("observation", type=Path)
    f.add_argument("--store", type=Path, default=DEFAULT_STORE)
    s = sub.add_parser("submit")
    s.add_argument("case", type=Path)
    s.add_argument("entrant")
    s.add_argument("prediction", type=Path)
    s = sub.add_parser("settle")
    s.add_argument("case", type=Path)
    s.add_argument("result", type=Path)
    s = sub.add_parser("scores")
    s.add_argument("case", type=Path)
    a = p.parse_args()
    if a.cmd == "init-game":
        put_once(a.out, template(a.series, a.game, a.bo, a.phase, a.first_pick))
        print(a.out)
    elif a.cmd == "freeze":
        print(freeze(read(a.observation), a.store))
    elif a.cmd == "history-add":
        print(history_add(read(a.record), a.store))
    elif a.cmd == "submit":
        print(json.dumps(submit(a.case, a.entrant, read_prediction(a.prediction))))
    elif a.cmd == "settle":
        print(json.dumps(settle(a.case, read(a.result))))
    else:
        print(json.dumps(standings(a.case)))
