import copy
import json
from datetime import timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from evaluation.dataset import inline_evaluation_messages, iter_rows, snapshot_bytes
from production.build import ROOT, snapshot
from production.evidence import emit_evidence, load_packs, validate_pack
from production.export import build_export
from production.intake import freeze
from production.release import publish
from production.schema import instant
from production.specs import load_spec
from production.store import read

SAMPLE = ROOT / "production/evidence-packs/faker-scoreline.json"
CUSTOM = SAMPLE.with_name("kill-involvements.json")
PACKS = load_packs([SAMPLE])
RECORDS = read(ROOT / "production/data/games.json")
SERIES = "worlds-2026-main-event-quarterfinals-4"
TARGET = next(g for g in RECORDS if (g["series"], g["n"]) == (SERIES, 2))


class EvidenceTest(unittest.TestCase):
    def test_community_can_declare_new_features_using_data_alone(self):
        doc = read(CUSTOM)
        (key,) = doc["feature_definitions"]
        expected = next(
            p["k"] + p["a"]
            for g in RECORDS
            if g["series"] == doc["records"][0]["anchor"]["series"] and g["n"] == 1
            for p in g["players"]
            if p["name"] == "Faker"
        )
        self.assertEqual(expected, 13)
        for kind, definition, valid, rejected in (
            (
                "integer",
                {"unit": "takedowns", "minimum": 0, "maximum": 200},
                13,
                [True, -1, 201, 3.5, "13"],
            ),
            (
                "enum",
                {"choices": ["low", "high"]},
                "high",
                ["T1 wins", 1, {"high": True}],
            ),
            ("boolean", {}, True, [1, "true", None]),
        ):
            with self.subTest(kind=kind):
                doc["feature_definitions"][key] = {
                    "description": "Reviewed historical observation",
                    "kind": kind,
                    **definition,
                }
                doc["records"][0]["value"] = valid
                validate_pack(doc)
                for value in rejected:
                    bad = copy.deepcopy(doc)
                    bad["records"][0]["value"] = value
                    with self.assertRaisesRegex(ValueError, "declared community"):
                        validate_pack(bad)
                for bad_def in (
                    dict(doc["feature_definitions"][key], kind="text"),
                    dict(doc["feature_definitions"][key], future="mid wins"),
                ):
                    wrong = copy.deepcopy(doc)
                    wrong["feature_definitions"][key] = bad_def
                    with self.assertRaises(ValueError):
                        validate_pack(wrong)
        doc = read(CUSTOM)
        with self.assertRaisesRegex(ValueError, "Unregistered"):
            validate_pack({k: v for k, v in doc.items() if k != "feature_definitions"})
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "second.json"
            doc["id"] += "-other"
            path.write_text(json.dumps(doc))
            self.assertEqual(len(load_packs([CUSTOM, path])), 2)
            doc["feature_definitions"][key]["maximum"] += 1
            path.write_text(json.dumps(doc))
            with self.assertRaisesRegex(ValueError, "Conflicting feature definitions"):
                load_packs([CUSTOM, path])

    def test_rejects_free_text_unknown_features_and_result_fields(self):
        for delta in [
            {"value": "T1 wins the next three games"},
            {"feature_type": "winner.v1", "value": "red"},
            {"source": "file:///private/labels.json"},
            {"published_at": "2026-10-24T12:14:41"},
            {"result": "red"},
            {"feature_type": "player.style.v1", "value": "wins-finals"},
        ]:
            doc = copy.deepcopy(PACKS[0].document)
            doc["records"][0].update(delta)
            with self.subTest(delta=delta), self.assertRaises(ValueError):
                validate_pack(doc)
        with self.assertRaisesRegex(ValueError, "one version"):
            load_packs([SAMPLE, SAMPLE])

    def test_cutoffs_starters_history_and_structured_projection(self):
        view = snapshot(RECORDS, TARGET, "lobby", evidence_packs=PACKS)
        card = view["evidence"]
        self.assertEqual(
            card,
            snapshot(RECORDS, TARGET, "draft-lock", evidence_packs=PACKS)["evidence"],
        )
        self.assertEqual(len(card["records"]), 1)
        fact = card["records"][0]
        self.assertEqual(fact["player"], "Faker")
        self.assertEqual(fact["value"], {"k": 6, "d": 0, "a": 7})
        for field in ("source", "reviewed_by", "attribution", "license", "owner"):
            self.assertNotIn(field, fact)
        self.assertEqual(
            emit_evidence(view, PACKS, fact["published_at"])["records"], []
        )
        no_history = dict(view, history=[])
        self.assertEqual(
            emit_evidence(no_history, PACKS, card["cutoff_utc"])["records"], []
        )
        no_starter = dict(
            view, current=dict(view["current"], starters={"blue": [], "red": []})
        )
        self.assertEqual(
            emit_evidence(no_starter, PACKS, card["cutoff_utc"])["records"], []
        )
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "later.json"
            for delta in (
                {"published_at": "2026-11-08T00:00:00Z"},
                {"anchor": {"series": SERIES, "game": 2}},
                {"anchor": {"series": SERIES, "game": 3}},
            ):
                doc = copy.deepcopy(PACKS[0].document)
                doc["records"][0].update(delta)
                path.write_text(json.dumps(doc))
                self.assertEqual(
                    emit_evidence(view, load_packs([path]), card["cutoff_utc"])[
                        "records"
                    ],
                    [],
                )
        doc = copy.deepcopy(PACKS[0].document)
        doc["records"][0]["value"]["k"] += 1
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "mutated.json"
            path.write_text(json.dumps(doc))
            with self.assertRaisesRegex(ValueError, "contradicts"):
                emit_evidence(view, load_packs([path]), card["cutoff_utc"])

    def test_frozen_phases_keep_identical_pack_and_lobby_cutoff(self):
        when = instant(TARGET["series_time"]) + timedelta(hours=1)
        params = {
            k: TARGET[k]
            for k in (
                "event",
                "stage",
                "series",
                "n",
                "bo",
                "blue",
                "red",
                "patch",
                "series_time",
            )
        }
        params.update(
            starters={
                side: [p["name"] for p in TARGET["players"] if p["side"] == side]
                for side in ("blue", "red")
            },
            observed_at=when.isoformat(),
            draft_rule="Fearless",
            source="https://example.org/test-clock",
        )
        with TemporaryDirectory() as tmp, patch("production.intake.now") as clock:
            root = Path(tmp)
            store = root / "intake"
            archive = root / "history.json"
            archive.write_text(
                json.dumps([g for g in RECORDS if g["series"] != SERIES or g["n"] == 1])
            )
            with patch("production.store.BASE_HISTORY", archive):
                clock.return_value = when
                first = freeze(dict(params, phase="lobby"), store, evidence_packs=PACKS)
                second = dict(
                    params,
                    phase="draft-lock",
                    bp=TARGET["bp"],
                    observed_at=(when + timedelta(minutes=5)).isoformat(),
                )
                clock.return_value += timedelta(minutes=5)
                with self.assertRaisesRegex(ValueError, "same evidence"):
                    freeze(second, store)
                locked = freeze(second, store, evidence_packs=PACKS)
                for case in (first, locked):
                    evidence = read(case / "task/environment/snapshot.json")["evidence"]
                    self.assertEqual(evidence["cutoff_utc"], when.isoformat())
                    self.assertEqual(
                        load_packs((case / "evidence-packs").glob("*.json")), PACKS
                    )

    def test_one_shot_export_preserves_original_semantics(self):
        spec = load_spec("scout-one-shot-v1")
        packs = load_packs([SAMPLE, CUSTOM])
        with TemporaryDirectory() as tmp:
            base = Path(tmp)
            release = publish(
                base, "scout-test", task_spec=spec.metadata["id"], evidence_packs=packs
            )
            bundle = build_export(release, base / "bundle")
            meta = read(bundle / "manifest.json")
            self.assertEqual(meta["task_spec"], spec.metadata)
            self.assertEqual(meta["evidence_packs"], [p.metadata() for p in packs])
            q = next(
                r
                for r in iter_rows(bundle / "eval/test.jsonl.gz")
                if r["extra_info"]["series"] == SERIES and r["extra_info"]["game"] == 2
            )
            body = inline_evaluation_messages(bundle, q)[0]["content"]
            ev = json.loads(snapshot_bytes(bundle, q))["evidence"]
            feat = "community.matchstats.kill-involvements.v1"
            self.assertEqual(
                ev["feature_types"][feat], {"kind": "integer", "unit": "takedowns"}
            )
            self.assertEqual(
                next(r["value"] for r in ev["records"] if r["feature_type"] == feat), 13
            )
            self.assertIn(feat, body)
            self.assertNotIn(
                read(CUSTOM)["feature_definitions"][feat]["description"], body
            )
            for text in (
                spec.background.strip(),
                spec.example.strip(),
                q["prompt"][0]["content"],
            ):
                self.assertIn(text, body)
            self.assertIn(
                "Faker",
                json.loads(snapshot_bytes(bundle, q))["evidence"]["records"][0][
                    "player"
                ],
            )
            for rl in iter_rows(bundle / "rl/train.jsonl.gz"):
                self.assertEqual(rl["extra_info"]["task_spec"], spec.metadata["id"])
                self.assertIn(spec.example.strip(), rl["prompt"][0]["content"])
