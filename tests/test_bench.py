import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
from production.build import earlier, eligible, snapshot, write_task
from production.score import score

GAMES = json.loads((ROOT / "production/data/games.json").read_text())


class BenchmarkTest(unittest.TestCase):
    def test_all_slices(self):
        self.assertEqual(len({(g["series"], g["n"]) for g in GAMES}), len(GAMES))
        for target in filter(eligible, GAMES):
            lobby = snapshot(GAMES, target, "lobby")
            locked = snapshot(GAMES, target, "draft-lock")
            self.assertNotIn("bp", lobby["current"])
            self.assertEqual(lobby["history"], locked["history"])
            self.assertEqual(
                set(locked["current"]),
                set(
                    "event stage series n patch bo blue red starters draft_rule bp".split()
                ),
            )
            for h in locked["history"]:
                if h["series"] == target["series"]:
                    self.assertLess(h["n"], target["n"])
                else:
                    self.assertLess(h["series_time"], target["series_time"])
                self.assertTrue(all("rating" not in p for p in h["players"]))
            self.assertEqual([x["turn"] for x in target["bp"]], list(range(1, 21)))
            for side in ("red", "blue"):
                picks = [
                    x["champion"]
                    for x in target["bp"]
                    if x["side"] == side and x["action"] == "pick"
                ]
                self.assertCountEqual(
                    picks,
                    [p["champion"] for p in target["players"] if p["side"] == side],
                )

    def test_delayed_publication_and_equality(self):
        target = GAMES[-1]
        h = dict(GAMES[0], replay_published=target["series_time"])
        self.assertFalse(earlier(h, target))
        self.assertFalse(earlier(dict(h, replay_published=None), target))
        self.assertFalse(
            earlier(dict(h, replay_published="2027-01-01T00:00:00+00:00"), target)
        )
        self.assertFalse(earlier(dict(target, n=target["n"] + 1), target))

    def test_score_and_files(self):
        t = next(g for g in GAMES if eligible(g))
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "task"
            write_task(root, snapshot(GAMES, t, "draft-lock"), t)
            self.assertEqual(
                {p.name for p in (root / "environment").iterdir()},
                {"Dockerfile", "snapshot.json", "docker-compose.yaml"},
            )
            y = json.loads((root / "tests/labels.json").read_text())
            self.assertEqual(score(y, y), 1)
            self.assertEqual(score(dict.fromkeys(y, 0.5), y), 0.75)
            for bad in (True, float("nan"), 1.1, "0.8", None):
                self.assertEqual(score(dict.fromkeys(y, bad), y), 0)
