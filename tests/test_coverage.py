import json
import shutil
import subprocess
import sys
import tarfile
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from evaluation.suite import DEFAULT_RELEASE, SAMPLE, paired_summary, select, unpack
from production.coverage import history_card
from production.score import FIELDS
from production.store import digest, read


class CoverageTest(unittest.TestCase):
    def test_observed_appearances_only(self):
        current = {
            "series": "final",
            "n": 3,
            "patch": "26.20",
            "starters": {"blue": ["A"], "red": ["B"]},
        }
        history = [
            {
                "series": "prior",
                "n": 1,
                "patch": "26.17",
                "players": [{"name": "A"}, {"name": "a"}],
            },
            {"series": "final", "n": 1, "patch": "26.20", "players": []},
        ]
        card = history_card(current, history)
        self.assertEqual(card["coverage_group"], "partial")
        self.assertEqual(
            card["starters"][0],
            {"name": "A", "side": "blue", "games": 1, "same_patch_games": 0},
        )
        self.assertEqual(card["starters"][1]["games"], 0)
        self.assertEqual(card["previous_series_games"], [1])
        self.assertEqual(card["missing_previous_series_games"], [2])

    def test_release_cards_match_archived_evidence(self):
        release = DEFAULT_RELEASE
        manifest = read(release / "manifest.json")
        self.assertEqual(manifest["coverage_sha256"], digest(release / "coverage.json"))
        release_cards = read(release / "coverage.json")
        self.assertEqual(
            set(release_cards["by_task"]), {row["id"] for row in manifest["tasks"]}
        )
        with tarfile.open(release / "tasks.tar.gz") as archive:
            for row in manifest["tasks"]:
                with self.subTest(task=row["id"]):
                    name = row["id"] + "/environment/snapshot.json"
                    view = json.load(archive.extractfile(name))
                    card = history_card(view["current"], view["history"])
                    self.assertEqual(release_cards["by_task"][row["id"]], card)
                    self.assertEqual(view["coverage"], card)
                    self.assertEqual(row["coverage_group"], card["coverage_group"])
        self.assertEqual(release_cards["unique_games"], 99)
        for phase in ("lobby", "draft-lock"):
            self.assertEqual(
                release_cards["by_phase"][phase]["coverage_groups"],
                {"all": 85, "partial": 5, "none": 9},
            )
        card = release_cards["by_task"][SAMPLE]
        self.assertEqual(
            card, release_cards["by_task"][SAMPLE.replace("draft-lock", "lobby")]
        )
        self.assertEqual(
            [(p["games"], p["same_patch_games"]) for p in card["starters"]],
            [(19, 19)] * 5 + [(6, 6)] * 5,
        )
        self.assertEqual(card["previous_series_games"], [1])
        self.assertFalse(card["missing_previous_series_games"])

    def test_paired_score_counts_only_matched_submissions(self):
        tasks = [
            {"series": "s", "game": n, "phase": phase, "id": f"t{n}{phase}"}
            for n in [1, 2]
            for phase in ["lobby", "draft-lock"]
        ]
        trials = [
            {
                "task": t["id"],
                "status": "scored",
                "brier": dict.fromkeys(
                    FIELDS, 0.25 if t["phase"] == "lobby" else 0.125
                ),
            }
            for t in tasks
        ]
        trials[-1] = {"task": tasks[-1]["id"], "status": "failed"}
        result = paired_summary(tasks, trials)
        self.assertEqual(result["selected_pairs"], 2)
        self.assertEqual(result["scored_pairs"], 1)
        self.assertEqual(result["mean_brier_improvement"], dict.fromkeys(FIELDS, 0.125))
        self.assertEqual(paired_summary(tasks[:1], trials)["selected_pairs"], 0)

    def test_rebuild_existing_report_preserves_forecast_and_scores(self):
        root = DEFAULT_RELEASE.parents[1]
        old_file = root / "evaluation/examples/replay-v2-codex/report.json"
        before = read(old_file)
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            shutil.copyfile(old_file, path)
            subprocess.run(
                [sys.executable, str(root / "bench"), "report", tmp],
                check=True,
                capture_output=True,
            )
            rebuilt = read(path)
            self.assertTrue((Path(tmp) / "report.md").is_file())
        self.assertEqual(before["summary"], rebuilt["summary"])
        self.assertEqual(rebuilt["by_coverage"]["all"], before["summary"])
        self.assertEqual(rebuilt["paired"]["selected_pairs"], 0)
        for old, new in zip(before["trials"], rebuilt["trials"], strict=True):
            for field in ("status", "prediction", "brier", "reward", "runtime"):
                self.assertEqual(old.get(field), new.get(field))
            self.assertEqual(new["coverage"]["history_games"], 96)

    def test_v2_reader_preserves_original_inputs(self):
        release = DEFAULT_RELEASE.parent / "replay-v2"
        manifest, rows = select(release, [SAMPLE])
        with TemporaryDirectory() as tmp:
            unpack(release, manifest, rows, Path(tmp))
            view = read(Path(tmp) / SAMPLE / "environment/snapshot.json")
        self.assertNotIn("coverage", view)
        self.assertEqual(
            history_card(view["current"], view["history"])["history_games"], 96
        )
