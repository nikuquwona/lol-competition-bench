"""Organizer-owned local storage. Never copy this store into an agent environment."""

from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

from production.build import ROOT
from production.schema import instant

DEFAULT_STORE = ROOT / ".work/intake"
BASE_HISTORY = ROOT / "production/data/games.json"


@contextmanager
def store_lock(store):
    # The intake directory belongs to the organizer on a local POSIX filesystem.
    store.mkdir(parents=True, exist_ok=True)
    with (store / ".intake.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


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
