import json
import shutil
import tempfile
import unittest
from pathlib import Path

from production.build import ROOT, instruction, snapshot, write_task
from production.intake import freeze
from production.release import publish
from production.specs import DEFAULT, HERE, load_spec
from production.store import read, trusted_case

SCOUT = "scout-one-shot-v1"


class TaskSpecTests(unittest.TestCase):
    def test_registry_validates_assets_and_hashes_content(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            shutil.copytree(HERE / "prompts", root / "prompts")
            shutil.copytree(HERE / "registry", root / "registry")
            meta = load_spec(SCOUT, root).metadata
            example = root / "prompts" / meta["components"]["example"]["file"]
            example.write_text(example.read_text() + "\nNew fictional example.\n")
            self.assertNotEqual(
                meta["protocol_sha256"],
                load_spec(SCOUT, root).metadata["protocol_sha256"],
            )
            catalog = root / "registry/catalog.json"
            content = json.loads(catalog.read_bytes())
            content["instructions"]["forecast-with-example-v1"]["example"] = (
                "../secret.md"
            )
            catalog.write_text(json.dumps(content))
            with self.assertRaises(ValueError):
                load_spec(SCOUT, root)
            with self.assertRaises(ValueError):
                load_spec("unknown-task", root)

    def test_two_variants_share_view_and_grader_but_not_example(self):
        games = read(ROOT / "production/data/games.json")
        g = next(
            r
            for r in games
            if r["series"].endswith("main-event-quarterfinals-4") and r["n"] == 2
        )
        view = snapshot(games, g, "lobby")
        spec = load_spec(SCOUT)
        self.assertNotIn("Blue Finch", instruction(view))
        with tempfile.TemporaryDirectory() as d:
            task = Path(d) / "scout"
            write_task(task, view, g, spec=spec)
            self.assertEqual(read(task / "environment/snapshot.json"), view)
            self.assertEqual(read(task / "task-profile.json"), spec.metadata)
            self.assertEqual(
                (task / "tests/score.py").read_bytes(), (HERE / "score.py").read_bytes()
            )
            self.assertIn("Blue Finch", (task / "instruction.md").read_text())

    def test_freeze_rejects_mixed_pair(self):
        with tempfile.TemporaryDirectory() as d:
            store = Path(d) / "intake"
            o = {
                "event": "fixture",
                "stage": "final",
                "series": "registry-test",
                "n": 1,
                "bo": 3,
                "blue": "blue",
                "red": "red",
                "patch": "26.20",
                "phase": "lobby",
                "draft_rule": "Fearless",
                "starters": {
                    s: [s + str(i) for i in range(5)] for s in ("blue", "red")
                },
                "observed_at": "2020-01-01T00:00:00Z",
                "series_time": "2020-01-01T00:00:00Z",
                "source": "https://example.org/match",
            }
            frozen = freeze(o, store, task_spec=SCOUT)
            self.assertIn("Blue Finch", (frozen / "task/instruction.md").read_text())
            self.assertEqual(
                trusted_case(frozen)["task_spec"], load_spec(SCOUT).metadata
            )
            g = next(r for r in read(HERE / "data/games.json") if len(r["bp"]) == 20)
            bp = [
                {k: b[k] for k in ("turn", "side", "action", "champion")}
                for b in g["bp"]
            ]
            with self.assertRaisesRegex(ValueError, "same task protocol"):
                freeze({**o, "phase": "draft-lock", "bp": bp}, store, task_spec=DEFAULT)
            with self.assertRaisesRegex(ValueError, "new release"):
                publish(Path(d), "replay-v3", task_spec=SCOUT)
