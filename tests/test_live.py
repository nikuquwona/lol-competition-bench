import hashlib
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
from evaluation import live_series


class LiveTest(unittest.TestCase):
    def test_receipt_lifecycle(self):
        when = "2026-11-08T22:00:00Z"
        teams = [
            {"code": "T1", "result": {"outcome": "win"}},
            {"code": "BLG", "result": {"outcome": "loss"}},
        ]
        event = dict(id="1", state="unstarted", startTime=when, matchTeams=teams)
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "input.json"
            receipt = Path(d) / "receipt.json"
            path.write_text(
                json.dumps(dict(teams=["T1", "BLG"], event_id="1", scheduled=when))
            )
            cmd = [
                "live_series",
                "seal",
                str(path),
                "--receipt",
                str(receipt),
                "--probability",
                "0.6",
            ]
            with (
                patch.object(live_series, "riot_event", return_value=event),
                patch.object(sys, "argv", cmd),
            ):
                with patch.object(
                    live_series,
                    "now",
                    return_value=datetime(2026, 11, 8, 22, tzinfo=timezone.utc),
                ):
                    with self.assertRaises(ValueError):
                        live_series.main()
                with patch.object(
                    live_series,
                    "now",
                    return_value=datetime(2026, 11, 8, 20, tzinfo=timezone.utc),
                ):
                    live_series.main()
                    with self.assertRaises(FileExistsError):
                        live_series.main()
            self.assertEqual(
                json.loads(receipt.read_text())["snapshot_sha256"],
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )
            cmd[1] = "settle"
            with (
                patch.object(sys, "argv", cmd),
                patch.object(
                    live_series,
                    "riot_event",
                    return_value=dict(event, state="completed"),
                ),
                patch("builtins.print") as output,
            ):
                live_series.main()
                result = json.loads(output.call_args.args[0])
                self.assertAlmostEqual(result["brier"], 0.16)
                path.write_text(path.read_text() + " ")
                with self.assertRaises(ValueError):
                    live_series.main()
