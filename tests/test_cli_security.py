"""Check wrappers against future results, hosted tools, result exfiltration and non-files."""

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evaluation.cli.gateway import validate
from evaluation.cli.worker import READ_PREDICTION
from production.build import snapshot
from production.score import read_prediction


class IsolationTests(unittest.TestCase):
    def test_future_poison(self):
        games = json.loads((ROOT / "production/data/games.json").read_text())
        target = next(
            g
            for g in games
            if g["series"].endswith("main-event-quarterfinals-4") and g["n"] == 2
        )
        for phase in ("lobby", "draft-lock"):
            original = snapshot(games, target, phase)
            poisoned = copy.deepcopy(games)
            for game in poisoned:
                future_game = (
                    game["series"] == target["series"] and game["n"] >= target["n"]
                )
                unpublished = game["series"] != target["series"] and (
                    not game["replay_published"]
                    or game["replay_published"] >= target["series_time"]
                )
                if future_game or unpublished:
                    game.update(blue_win="FUTURE WINNER", blue_gd15="FUTURE GOLD")
                for player in game["players"]:
                    player["rating"] = "SEASON END RATING"
            changed = next(
                g for g in poisoned if g["series"] == target["series"] and g["n"] == 2
            )
            self.assertEqual(original, snapshot(poisoned, changed, phase))

    def test_gateway_rejects_remote_actions(self):
        model = "deepseek-v4-pro"
        good = {
            "model": model,
            "input": "forecast",
            "tools": [{"type": "function", "name": "exec_command", "parameters": {}}],
        }
        validate(good, model)
        for override in [
            {"model": "other"},
            {"previous_response_id": "future"},
            {"conversation": "shared"},
            {"tools": [{"type": "web_search"}]},
            {"tools": [{"type": "mcp", "server_url": "https://example.com"}]},
            {"tools": [{"type": "namespace", "tools": [{"type": "file_search"}]}]},
            {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_file",
                                "file_url": "https://example.com/score",
                            }
                        ],
                    }
                ]
            },
            {"tools": [{"type": "code_interpreter"}]},
            {"input": [{"type": "item_reference", "id": "earlier-agent"}]},
        ]:
            with self.subTest(override=override), self.assertRaises(ValueError):
                validate({**good, **override}, model)

    def test_worker_output_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file = root / "prediction.json"
            reader = READ_PREDICTION.replace("/app/prediction.json", str(file))

            def passed():
                return (
                    subprocess.run(
                        [sys.executable, "-I", "-c", reader],
                        capture_output=True,
                        timeout=2,
                    ).returncode
                    == 0
                )

            wanted = {"p_blue_win": 0.41, "p_blue_ahead_15": 0.57}
            file.write_text(json.dumps(wanted))
            self.assertTrue(passed())
            self.assertEqual(wanted, read_prediction(file))
            for content in (
                "[]",
                '{"p_blue_win":0,"p_blue_win":1,"p_blue_ahead_15":1}',
                '{"p_blue_win":NaN,"p_blue_ahead_15":1}',
                json.dumps({**wanted, "hint": "label"}),
                " " * 4097,
            ):
                file.write_text(content)
                self.assertFalse(passed())
            file.unlink()
            labels = root / "truth.json"
            labels.write_text(json.dumps(wanted))
            file.symlink_to(labels)
            with self.assertRaises(OSError):
                read_prediction(file)
            self.assertFalse(passed())
            file.unlink()
            os.mkfifo(file)
            with self.assertRaises(ValueError):
                read_prediction(file)
            self.assertFalse(passed())
