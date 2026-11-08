"""Freeze an observation, seal the first forecast, then settle once per game."""

import argparse
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from production.build import snapshot, write_task
from production.evidence import add_pack_option, load_packs
from production.score import FIELDS, read_prediction, score
from production.specs import DEFAULT, load_spec
from production.schema import (
    SIDES,
    exact,
    instant,
    name,
    slug,
    source,
    task_id,
    template,
    validate_bp,
    validate_observation,
    validate_predecessors,
)
from production.store import (
    DEFAULT_STORE,
    digest,
    history,
    put_once,
    read,
    result_path,
    store_lock,
    trusted_case,
)


def now():
    return datetime.now(timezone.utc)


def freeze(o, store, *, task_spec=DEFAULT, evidence_packs=()):
    with store_lock(store):
        return _freeze(
            o, store, spec=load_spec(task_spec), evidence_packs=evidence_packs
        )


def _freeze(o, store, *, spec, evidence_packs):
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
    pack_meta = [pack.metadata() for pack in evidence_packs]
    cutoff = o["observed_at"]
    if sibling.exists():
        sibling_meta = trusted_case(sibling)
        if sibling_meta.get("evidence_packs", []) != pack_meta:
            raise ValueError("Both phases must use the same evidence packs")
        cutoff = sibling_meta["observed_at"]
        sibling_profile = trusted_case(sibling).get("task_spec")
        if (sibling_profile is None and spec.metadata["id"] != DEFAULT) or (
            sibling_profile is not None and sibling_profile != spec.metadata
        ):
            raise ValueError("Both phases must use the same task protocol")
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
        first_bp = sibling / "cutoff.json"
        if first_bp.exists() and instant(read(first_bp)["at"]) > instant(
            o["observed_at"]
        ):
            raise ValueError("Draft lock precedes the first public BP action")
    records = history(store)
    validate_predecessors(o, records)
    view = snapshot(
        records, g, o["phase"], evidence_packs=evidence_packs, evidence_cutoff=cutoff
    )
    if evidence_packs and sibling.exists():
        old_evidence = read(sibling / "task/environment/snapshot.json")["evidence"]
        if view["evidence"] != old_evidence:
            raise ValueError("Visible evidence changed since the lobby froze")
    view["observed_at_utc"] = instant(o["observed_at"]).isoformat()
    with tempfile.TemporaryDirectory(dir=store) as temp:
        stage = Path(temp) / "case"
        write_task(stage / "task", view, spec=spec)
        for pack in evidence_packs:
            put_once(stage / "evidence-packs" / (pack.sha256 + ".json"), pack.document)
        put_once(
            stage / "observation.json",
            dict(
                id=task_id(o),
                task_spec=spec.metadata,
                evidence_packs=pack_meta,
                source=o["source"],
                frozen_at=frozen.isoformat(),
                observed_at=view["observed_at_utc"],
                snapshot_sha256=digest(stage / "task/environment/snapshot.json"),
                prompt_sha256=digest(stage / "task/instruction.md"),
            ),
        )
        stage.rename(case)
    return case


def close_window(case, at, evidence):
    """Record the actual public event time on the organizer's side, including delayed reports."""
    with store_lock(case.parent):
        trusted_case(case)
        if result_path(case).exists():
            raise ValueError("Already settled")
        recorded = now()
        occurred = instant(at)
        if occurred > recorded:
            raise ValueError("Cannot record a future cutoff")
        lobby = case.name.endswith("-lobby")
        if lobby:
            locked = case.with_name(case.name.removesuffix("-lobby") + "-draft-lock")
            if locked.exists() and occurred > instant(
                trusted_case(locked)["observed_at"]
            ):
                raise ValueError(
                    "First public BP action must precede or equal draft lock"
                )
        elif occurred <= instant(trusted_case(case)["observed_at"]):
            raise ValueError("Game start must follow draft lock")
        event = dict(
            case=case.name,
            event="first_public_bp" if lobby else "game_start",
            at=occurred.isoformat(),
            recorded_at=recorded.isoformat(),
            source=source(evidence),
        )
        put_once(case / "cutoff.json", event)
        return event


def require_open(case):
    if result_path(case).exists():
        raise ValueError("Already settled")
    if (case / "cutoff.json").exists():
        raise ValueError("Submission window is closed")
    if case.name.endswith("-lobby"):
        locked = case.with_name(case.name.removesuffix("-lobby") + "-draft-lock")
        if locked.exists():
            raise ValueError("Lobby submission window is closed at draft lock")


def submit(case, entrant, prediction):
    with store_lock(case.parent):
        return _submit(case, entrant, prediction)


def _submit(case, entrant, prediction):
    meta = trusted_case(case)
    require_open(case)
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
    if (
        r["id"] != meta["id"]
        or r["winner"] not in SIDES
        or type(r["blue_gd15"]) is not int
    ):
        raise ValueError("Result identity, winner or gold difference invalid")
    start, published = instant(r["game_started_at"]), instant(r["published_at"])
    if not instant(meta["frozen_at"]) < start <= published <= now():
        raise ValueError("Require freeze < game start <= publication <= current time")
    source(r["source"])
    view = read(case / "task/environment/snapshot.json")
    c = view["current"]
    captures = {}
    cutoffs = {}
    actual_bp = r.get("bp", [])
    for phase in ("lobby", "draft-lock"):
        sibling = case.parent / task_id({**c, "phase": phase})
        if not sibling.is_dir():
            continue
        observation = trusted_case(sibling)
        if instant(observation["frozen_at"]) >= start:
            raise ValueError("An observation was frozen after game start")
        captures[sibling.name] = observation["snapshot_sha256"]
        if (sibling / "cutoff.json").exists():
            cutoff = read(sibling / "cutoff.json")
            occurred = instant(cutoff["at"])
            if (phase == "draft-lock" and occurred != start) or (
                phase == "lobby" and occurred >= start
            ):
                raise ValueError("Recorded phase cutoff conflicts with game start")
            cutoffs[phase] = cutoff
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
                or any(type(p[k]) is not int or p[k] < 0 for k in ("k", "d", "a"))
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
        "cutoffs": cutoffs,
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
    if case.name.endswith("-lobby"):
        cutoff = r.get("cutoffs", {}).get("lobby", {}).get("at")
    else:
        cutoff = r["game_started_at"]
    rows = []
    for path in sorted((case / "receipts").glob("*.json")):
        receipt = read(path)
        valid = (
            cutoff is not None
            and receipt["snapshot_sha256"] == meta["snapshot_sha256"]
            and receipt["prompt_sha256"] == meta["prompt_sha256"]
            and instant(meta["frozen_at"])
            <= instant(receipt["submitted_at"])
            < instant(cutoff)
        )
        rows.append(
            dict(
                entrant=receipt["entrant"],
                status=(
                    "unverified"
                    if cutoff is None
                    else "scored"
                    if valid
                    else "ineligible"
                ),
                cutoff_at=cutoff,
                submitted_at=receipt["submitted_at"],
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
        or type(doc["blue_gd15"]) is not int
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
    f.add_argument("--task-spec", default=DEFAULT)
    add_pack_option(f)
    f.add_argument("--store", type=Path, default=DEFAULT_STORE)
    closing = sub.add_parser(
        "close", help="Record the actual first BP action or game start"
    )
    closing.add_argument("case", type=Path)
    closing.add_argument(
        "--at", required=True, help="Public event timestamp with UTC offset"
    )
    closing.add_argument(
        "--source", required=True, help="HTTPS source for the event time"
    )
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
        print(
            freeze(
                read(a.observation),
                a.store,
                task_spec=a.task_spec,
                evidence_packs=load_packs(a.evidence_pack),
            )
        )
    elif a.cmd == "close":
        print(json.dumps(close_window(a.case, a.at, a.source)))
    elif a.cmd == "history-add":
        print(history_add(read(a.record), a.store))
    elif a.cmd == "submit":
        print(json.dumps(submit(a.case, a.entrant, read_prediction(a.prediction))))
    elif a.cmd == "settle":
        print(json.dumps(settle(a.case, read(a.result))))
    else:
        print(json.dumps(standings(a.case)))


if __name__ == "__main__":
    main()
