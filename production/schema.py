"""Contracts for observations, draft actions, series continuity and timestamps."""

import re
from datetime import datetime, timezone
from urllib.parse import urlsplit

SIDES = ("blue", "red")
FIRST_PICK_ORDER = "ABABAB" + "ABBAAB" + "BABA" + "BAAB"


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
        or type(o["bo"]) is not int
        or o["bo"] not in (1, 3, 5, 7)
        or type(o["n"]) is not int
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
        if type(e["turn"]) is not int or (e["turn"], e["side"], e["action"]) != (
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
