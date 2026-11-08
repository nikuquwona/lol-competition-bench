"""Validate and project reviewed community observations into a single frozen forecast."""

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re

from production.schema import exact, instant, name, slug, source
from production.score import unique_fields

STYLES = {"roaming", "lane-focused", "engage", "peel", "split-push", "teamfight-carry"}
ROLES = {"Top", "Jungle", "Mid", "Bot", "Support"}
KDA = ("k", "d", "a")
CUSTOM_FEATURE = re.compile(
    r"community\.[a-z][a-z0-9-]{0,31}\.[a-z][a-z0-9-]{0,47}\.v[1-9][0-9]{0,2}"
)
TOKEN = re.compile(r"[a-z][a-z0-9-]{0,31}")


@dataclass(frozen=True)
class Pack:
    document: dict
    sha256: str

    def metadata(self):
        result = {
            k: self.document[k]
            for k in ("id", "version", "owner", "attribution", "license")
        } | {"sha256": self.sha256}
        if "feature_definitions" in self.document:
            result["feature_definitions"] = self.document["feature_definitions"]
        return result


def validate_definitions(definitions):
    if not isinstance(definitions, dict) or len(definitions) > 32:
        raise ValueError("A pack can declare at most 32 custom feature types")
    for key, spec in definitions.items():
        if not CUSTOM_FEATURE.fullmatch(key) or not isinstance(spec, dict):
            raise ValueError(
                "Expected a namespaced and versioned community feature definition"
            )
        kind = spec.get("kind")
        fields = {"boolean": "", "enum": " choices", "integer": " minimum maximum unit"}
        if not isinstance(kind, str) or kind not in fields:
            raise ValueError("Use boolean, enum or bounded integer as the feature kind")
        exact(spec, "kind description" + fields[kind])
        desc = spec["description"]
        if (
            not isinstance(desc, str)
            or not desc.strip()
            or len(desc) > 240
            or not desc.isprintable()
        ):
            raise ValueError(
                "Give the organizer a description of up to 240 printable characters"
            )
        if kind == "enum":
            choices = spec["choices"]
            if (
                not isinstance(choices, list)
                or not 2 <= len(choices) <= 16
                or not all(isinstance(v, str) and TOKEN.fullmatch(v) for v in choices)
                or len(set(choices)) != len(choices)
            ):
                raise ValueError("Use 2 to 16 distinct lowercase enum tokens")
        if kind == "integer":
            low, high = spec["minimum"], spec["maximum"]
            if (
                type(low) is not int
                or type(high) is not int
                or not -1_000_000 <= low < high <= 1_000_000
            ):
                raise ValueError(
                    "Custom integer features require finite bounds inside ±1,000,000"
                )
            if not isinstance(spec["unit"], str) or not TOKEN.fullmatch(spec["unit"]):
                raise ValueError("Give integer features a lowercase unit token")


def validate_custom_value(value, spec):
    kind = spec["kind"]
    if kind == "boolean":
        valid = type(value) is bool
    elif kind == "enum":
        valid = isinstance(value, str) and value in spec["choices"]
    else:
        valid = type(value) is int and spec["minimum"] <= value <= spec["maximum"]
    if not valid:
        raise ValueError("Value violates its declared community feature type")


def validate_pack(doc):
    optional = (
        " feature_definitions"
        if isinstance(doc, dict) and "feature_definitions" in doc
        else ""
    )
    exact(doc, "schema_version id version owner attribution license records" + optional)
    if type(doc["schema_version"]) is not int or doc["schema_version"] != 1:
        raise ValueError("Unsupported evidence schema version")
    slug(doc["id"])
    if not isinstance(doc["version"], str) or not re.fullmatch(
        r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", doc["version"]
    ):
        raise ValueError("Expected a semantic pack version")
    for key in ("owner", "license", "attribution"):
        if (
            not isinstance(doc[key], str)
            or not doc[key].strip()
            or len(doc[key]) > 2000
        ):
            raise ValueError("Missing or oversized pack attribution")
    if not isinstance(doc["records"], list) or not doc["records"]:
        raise ValueError("Expected a nonempty records array")
    definitions = doc.get("feature_definitions", {})
    validate_definitions(definitions)
    identities = set()
    for row in doc["records"]:
        exact(
            row,
            "entity_type entity_id feature_type anchor value published_at source reviewed_by",
        )
        if row["entity_type"] != "player":
            raise ValueError("Expected a player entity")
        name(row["entity_id"])
        exact(row["anchor"], "series game")
        series = slug(row["anchor"]["series"])
        game = row["anchor"]["game"]
        if type(game) is not int or not 1 <= game <= 7:
            raise ValueError("Expected a positive game number <= 7")
        source(row["source"])
        name(row["reviewed_by"])
        instant(row["published_at"])
        feature, value = row["feature_type"], row["value"]
        if feature == "player.scoreline.v1":
            exact(value, "k d a")
            if any(type(v) is not int or v < 0 or v > 999 for v in value.values()):
                raise ValueError("Invalid historical K/D/A")
        elif feature == "player.role.v1":
            if not isinstance(value, str) or value not in ROLES:
                raise ValueError("Unexpected role")
        elif feature == "player.style.v1":
            if not isinstance(value, str) or value not in STYLES:
                raise ValueError(
                    "Use a reviewed game-scoped style from the allowed vocabulary"
                )
        elif isinstance(feature, str) and feature in definitions:
            validate_custom_value(value, definitions[feature])
        else:
            raise ValueError("Unregistered evidence feature type")
        identity = row["entity_id"].casefold(), feature, series, game
        if identity in identities:
            raise ValueError("Duplicate player observation")
        identities.add(identity)


def load_packs(paths):
    packs = []
    seen = set()
    definitions = {}
    for path in paths:
        doc = json.loads(Path(path).read_bytes(), object_pairs_hook=unique_fields)
        validate_pack(doc)
        if doc["id"] in seen:
            raise ValueError("Select one version per evidence pack ID")
        seen.add(doc["id"])
        for feature, spec in doc.get("feature_definitions", {}).items():
            if definitions.setdefault(feature, spec) != spec:
                raise ValueError(f"Conflicting feature definitions for {feature}")
        canonical = json.dumps(
            doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        )
        packs.append(Pack(doc, hashlib.sha256(canonical.encode()).hexdigest()))
    return tuple(sorted(packs, key=lambda p: p.document["id"]))


def emit_evidence(view, packs, cutoff):
    """Project only eligible facts; links, prose, and other players stay off the agent side."""
    cutoff = instant(cutoff)
    games = {(h["series"], h["n"]): h for h in view["history"]}
    starters = {
        p.casefold(): p for names in view["current"]["starters"].values() for p in names
    }
    entries = {}
    visible_types = {}
    for pack in packs:
        for row in pack.document["records"]:
            anchor = row["anchor"]
            key = anchor["series"], anchor["game"]
            player = row["entity_id"].casefold()
            published = instant(row["published_at"])
            if player not in starters or key not in games or published >= cutoff:
                continue
            game = games[key]
            if published <= instant(game["series_time"]):
                raise ValueError(
                    "A completed-game observation must postdate the start of its series"
                )
            observed = next(
                (p for p in game["players"] if p["name"].casefold() == player), None
            )
            if observed is None:
                raise ValueError(
                    "Evidence subject has no recorded appearance in its referenced game"
                )
            kind, value = row["feature_type"], row["value"]
            if kind == "player.scoreline.v1" and value != {k: observed[k] for k in KDA}:
                raise ValueError("Scoreline contradicts visible history")
            if kind == "player.role.v1" and value != observed["role"]:
                raise ValueError("Role contradicts visible history")
            identity = key, player, kind
            if identity in entries:
                raise ValueError(
                    "Conflicting or duplicated evidence across selected packs"
                )
            entries[identity] = {
                "player": starters[player],
                "feature_type": kind,
                "value": value,
                "anchor": anchor,
                "published_at": published.isoformat(),
            }
            if definition := pack.document.get("feature_definitions", {}).get(kind):
                visible_types[kind] = {
                    k: definition[k] for k in ("kind", "unit") if k in definition
                }
    result = {
        "cutoff_utc": cutoff.isoformat(),
        "records": [entries[k] for k in sorted(entries)],
    }
    if visible_types:
        result["feature_types"] = dict(sorted(visible_types.items()))
    return result


def add_pack_option(parser):
    parser.add_argument(
        "--evidence-pack",
        "--with-pack",
        type=Path,
        action="append",
        default=[],
        help="Reviewed community JSON evidence pack (repeat to combine)",
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("pack", type=Path, nargs="+")
    for pack in load_packs(p.parse_args().pack):
        print(
            json.dumps(
                dict(**pack.metadata(), records=len(pack.document["records"])),
                ensure_ascii=False,
            )
        )
