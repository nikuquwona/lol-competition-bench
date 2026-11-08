import unittest
from collections import Counter
from pathlib import Path

from evaluation.timeline import build_timeline
from production.store import digest, read

SOURCE_DIR = Path(__file__).resolve().parents[1] / "evaluation/examples"


class RolloutReviewTest(unittest.TestCase):
    def test_published_claims_link_to_native_messages_and_frozen_evidence(self):
        notes = read(SOURCE_DIR.parent / "rollout_reviews.json")
        found = set()
        for run in ("featured-five-deepseek", "featured-five-claude-deepseek"):
            for raw in (SOURCE_DIR / run / "jobs").glob("*/trajectory.jsonl"):
                sha = digest(raw)
                if sha not in notes:
                    continue
                found.add(sha)
                task = raw.parent.name
                snapshot = read(SOURCE_DIR / run / "traces" / task / "snapshot.json")
                timeline = build_timeline(raw, phase=snapshot["phase"])
                for review in notes[sha]:
                    (message,) = [
                        s
                        for s in timeline["steps"]
                        if s["kind"] == "message"
                        and s["source"]["line"] == review["line"]
                    ]
                    self.assertIn(review["quote"], message["body"])
                current, history = snapshot["current"], snapshot["history"]
                if current["blue"] == "LØS":
                    losses = [
                        row["red"] if row["blue"] == "LØS" else row["blue"]
                        for row in history
                        if "LØS" in (row["blue"], row["red"])
                        and (row["blue"] == "LØS") != row["blue_win"]
                    ]
                    self.assertCountEqual(losses, ["Team Liquid", "T1", "G2 Esports"])
                    self.assertEqual(notes[sha][0]["kind"], "evidence_mismatch")
                elif current["blue"] == "Karmine Corp":
                    (game,) = [g for g in history if g["series"] == current["series"]]
                    kills = Counter()
                    for player in game["players"]:
                        kills[player["side"]] += player["k"]
                    self.assertEqual(dict(kills), {"blue": 23, "red": 7})
                    self.assertEqual(
                        (game["blue"], game["blue_gd15"], game["blue_win"]),
                        ("T1", -660, True),
                    )
                else:
                    self.assertEqual(current["blue"], "Movistar KOI")
                    starters = {
                        p for side in current["starters"].values() for p in side
                    }
                    players = {p["name"] for g in history for p in g["players"]}
                    self.assertEqual((len(history), len(starters)), (34, 10))
                    self.assertTrue(starters.isdisjoint(players))
        self.assertEqual(found, set(notes))
