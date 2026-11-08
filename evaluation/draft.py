"""Project the champion select UI strictly from one verified task's frozen current view."""

from functools import lru_cache
import json
from pathlib import Path
import re

ASSETS = Path(__file__).with_name("site_assets")


@lru_cache(maxsize=1)
def portrait_index():
    catalog = json.loads((ASSETS / "champions/sources.json").read_bytes())
    patches = {}
    for patch, source in catalog["patches"].items():
        entries = {}
        for cid, data in source["champions"].items():
            file = data["file"]
            if not re.fullmatch(r"[a-z0-9]+-[a-f0-9]{12}\.webp", file):
                raise ValueError("Invalid portrait asset filename")
            ref = {"icon": "/champions/" + file, "label": data["zh"]}
            for alias in (cid, data["name"], *data["aliases"]):
                entries[re.sub(r"[^a-z0-9]", "", alias.casefold())] = ref
        patches[patch] = entries
    return patches


def draft_static():
    routes = {
        "/draft.js": ("draft.js", "text/javascript"),
        "/draft.css": ("draft.css", "text/css"),
    }
    for patch in portrait_index().values():
        for item in patch.values():
            url = item["icon"]
            routes[url] = (url.lstrip("/"), "image/webp")
    return routes


def draft_view(snapshot, expected_phase):
    if (
        expected_phase not in ("lobby", "draft-lock")
        or snapshot.get("phase") != expected_phase
    ):
        return None
    current = snapshot["current"]
    teams = {}
    for side in ("blue", "red"):
        teams[side] = {
            "name": current[side],
            "starters": list(current.get("starters", {}).get(side, [])),
        }
    view = {"phase": expected_phase, "patch": current["patch"], "teams": teams}
    if expected_phase == "draft-lock":
        portraits = portrait_index().get(current["patch"], {})
        actions = []
        for item in current.get("bp", []):
            if item["side"] not in teams or item["action"] not in ("pick", "ban"):
                continue
            name = item["champion"]
            ref = portraits.get(re.sub(r"[^a-z0-9]", "", name.casefold()))
            actions.append(
                {
                    "turn": item["turn"],
                    "side": item["side"],
                    "action": item["action"],
                    "champion": name,
                    "label": ref["label"] if ref else name,
                    "icon": ref["icon"] if ref else None,
                }
            )
        view["actions"] = sorted(actions, key=lambda a: a["turn"])
    return view
