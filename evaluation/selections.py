"""Versioned task selections shared by the runner and the leaderboard."""

import json
from pathlib import Path

SUITES = Path(__file__).with_name("suites")
CURRENT_SUITE = "featured-five"


def suite_names():
    return [CURRENT_SUITE]


def suite_ids(name, release):
    """Return the exact set in canonical order for this release manifest or directory."""
    if name not in suite_names():
        raise ValueError(f"Unknown evaluation suite: {name}")
    spec = json.loads((SUITES / (name + ".json")).read_bytes())
    manifest = (
        release
        if isinstance(release, dict)
        else json.loads((Path(release) / "manifest.json").read_bytes())
    )
    if (spec["release"], spec["archive_sha256"]) != (
        manifest["version"],
        manifest["sha256"],
    ):
        raise ValueError(f"{name} requires its pinned release archive")
    ids = [
        f"{game['series']}-g{game['game']}-{phase}"
        for game in spec["games"]
        for phase in ("lobby", "draft-lock")
    ]
    if len(ids) != len(set(ids)) or not set(ids) <= {
        t["id"] for t in manifest["tasks"]
    }:
        raise ValueError(f"Inconsistent task identities in {name}")
    return tuple(sorted(ids))
