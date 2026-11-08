"""Load declarative task categories, background briefs and runtime instruction profiles."""

import argparse
import hashlib
import json
import re
import string
from dataclasses import dataclass
from pathlib import Path

from production.score import unique_fields

HERE = Path(__file__).resolve().parent
DEFAULT = "forecast-v1"
GRADER = "binary-brier-pair-v1"
TOKENS = {
    "game",
    "blue",
    "red",
    "bo",
    "patch",
    "phase",
    "observation",
    "draft",
    "history_count",
}


def fingerprint(data):
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class TaskSpec:
    template: str
    background: str
    example: str
    metadata: dict


def catalog(directory=HERE):
    registry = json.loads(
        (directory / "registry/catalog.json").read_bytes(),
        object_pairs_hook=unique_fields,
    )
    if (
        not isinstance(registry, dict)
        or set(registry)
        != {"schema_version", "categories", "backgrounds", "instructions", "tasks"}
        or type(registry["schema_version"]) is not int
        or registry["schema_version"] != 1
    ):
        raise ValueError("Unsupported registry format")
    for section in ("categories", "backgrounds", "instructions", "tasks"):
        if not isinstance(registry[section], dict) or not all(
            re.fullmatch(r"[a-z][a-z0-9-]*", k) for k in registry[section]
        ):
            raise ValueError("Invalid registry section: " + section)
    return registry


def load_spec(spec_id=DEFAULT, directory=HERE):
    registry = catalog(directory)
    try:
        spec = registry["tasks"][spec_id]
        if (
            not isinstance(spec, dict)
            or set(spec) != {"category", "background", "instruction", "grader"}
            or spec["grader"] != GRADER
        ):
            raise ValueError("Unsupported task or scoring contract")
        category = registry["categories"][spec["category"]]
        profile = registry["instructions"][spec["instruction"]]
        background = (
            registry["backgrounds"][spec["background"]]
            if spec["background"] is not None
            else None
        )
    except (KeyError, TypeError) as exc:
        raise ValueError(f"Unknown task or registry reference: {spec_id}") from exc
    if (
        not isinstance(category, str)
        or not category.strip()
        or not isinstance(profile, dict)
        or set(profile) != {"template", "example"}
    ):
        raise ValueError("Invalid category description or instruction profile")
    components = {}

    def asset(kind, filename, optional=False):
        if filename is None and optional:
            return ""
        if not isinstance(filename, str) or not re.fullmatch(
            r"[a-z0-9][a-z0-9-]*\.md", filename
        ):
            raise ValueError("Invalid prompt asset name")
        root = (directory / "prompts").resolve()
        path = (root / filename).resolve()
        if not path.is_relative_to(root):
            raise ValueError("Prompt asset escapes its directory")
        data = path.read_bytes()
        if not data.strip():
            raise ValueError("Empty prompt component")
        components[kind] = {"file": filename, "sha256": fingerprint(data)}
        return data.decode("utf-8")

    template = asset("template", profile["template"])
    bg = asset("background", background, optional=True)
    example = asset("example", profile["example"], optional=True)
    for _, key, fmt, conv in string.Formatter().parse(template):
        if key is not None and (key not in TOKENS or fmt or conv):
            raise ValueError(f"Unsupported template field: {key}")
    meta = {
        "id": spec_id,
        **spec,
        "category_description": category,
        "components": components,
    }
    meta["protocol_sha256"] = fingerprint(
        json.dumps(
            meta, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
    )
    return TaskSpec(template, bg, example, meta)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "spec",
        nargs="?",
        help="Print one resolved task or validate and list the whole catalog",
    )
    selected = parser.parse_args().spec
    ids = [selected] if selected else sorted(catalog()["tasks"])
    print(
        json.dumps([load_spec(i).metadata for i in ids], ensure_ascii=False, indent=2)
    )
