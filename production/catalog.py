"""Public collection names and the immutable release each name currently selects."""

import json
from functools import lru_cache
from pathlib import Path

DATASETS = Path(__file__).resolve().parents[1] / "datasets"


@lru_cache(maxsize=1)
def collections():
    return json.loads((DATASETS / "catalog.json").read_text())


def resolve_release(value):
    spec = collections().get(str(value))
    return DATASETS / spec["current"] if spec else Path(value)


def display_names(version):
    for alias, spec in collections().items():
        if version in spec["editions"]:
            return {
                "collection": alias,
                "display_title": spec["title_zh"],
                "title_en": spec["title_en"],
                "short_title": spec["short_title"],
                "edition": spec["editions"][version],
            }
    return {
        "collection": None,
        "display_title": version,
        "title_en": version,
        "short_title": version,
        "edition": None,
    }
