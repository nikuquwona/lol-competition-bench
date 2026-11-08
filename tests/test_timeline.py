import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evaluation.timeline import build_timeline
from production.build import ROOT


class TimelineTests(unittest.TestCase):
    def test_committed_forecast_has_real_evidence_commands_and_readbacks(self):
        base = ROOT / "evaluation/examples/worlds-2026-kc-t1-openrouter/jobs"
        for phase, total, failed, prob in [
            ("lobby", 9, 1, 0.45),
            ("draft-lock", 12, 3, 0.60),
        ]:
            with self.subTest(phase=phase):
                file = next(base.glob(f"*{phase}/trajectory.jsonl"))
                submitted = json.loads(file.with_name("prediction.json").read_text())
                data = build_timeline(file, phase=phase, prediction=submitted)
                tools = [s for s in data["steps"] if s["kind"] == "tool"]
                self.assertEqual(
                    (len(tools), sum(s["failed"] for s in tools)), (total, failed)
                )
                self.assertEqual(
                    data["readbacks"], [{"p_blue_win": prob, "p_blue_ahead_15": 0.55}]
                )
                self.assertEqual(submitted, data["submission"])
                self.assertEqual(data["availability"], "recorded")
                self.assertGreater(tools[0]["output_chars"], 200_000)
                self.assertLess(len(tools[0]["output"]), 5000)
                self.assertIn("15 分钟经济差", data["evidence"])

    def test_interleaved_calls_use_matching_ids(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "events.log"
            events = [
                {
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": "x",
                            "function": {
                                "name": "Bash",
                                "arguments": '{"command":"echo first"}',
                            },
                        },
                        {
                            "id": "y",
                            "function": {
                                "name": "Bash",
                                "arguments": '{"command":"echo second"}',
                            },
                        },
                    ],
                },
                {"role": "tool", "tool_call_id": "y", "content": "second"},
                {"role": "tool", "tool_call_id": "x", "content": "first"},
            ]
            path.write_text("".join(json.dumps(e) + "\n" for e in events))
            data = build_timeline(path, phase="lobby")
            self.assertEqual(
                [(s["command"], s["output"]) for s in data["steps"]],
                [("echo first", "first"), ("echo second", "second")],
            )
            with patch("evaluation.timeline.READ_LIMIT", 20):
                self.assertEqual(
                    build_timeline(path, phase="lobby")["availability"], "truncated"
                )

    def test_claude_checkpoints_link_to_original_write_and_matching_reply(self):
        root = ROOT / "evaluation/examples/featured-five-claude-deepseek/jobs"
        path = next(root.glob("*quarterfinals-4-g2-draft-lock/trajectory.jsonl"))
        lines = path.read_bytes().splitlines()
        timeline = build_timeline(path, phase="draft-lock")
        steps = {s["id"]: s for s in timeline["steps"]}
        self.assertEqual(
            [m["values"] for m in timeline["checkpoints"]],
            [
                {"p_blue_win": 0.26, "p_blue_ahead_15": 0.57},
                {"p_blue_win": 0.31, "p_blue_ahead_15": 0.58},
            ],
        )
        for checkpoint in timeline["checkpoints"]:
            step = steps[checkpoint["step_id"]]
            call = json.loads(lines[step["source"]["line"] - 1])["message"]["content"]
            result = json.loads(lines[step["result_source"]["line"] - 1])["message"][
                "content"
            ]
            (write,) = [
                b
                for b in call
                if b.get("type") == "tool_use"
                and b.get("id") == step["source"]["call_id"]
            ]
            self.assertEqual(
                json.loads(write["input"]["content"]), checkpoint["values"]
            )
            self.assertTrue(
                any(
                    b.get("tool_use_id") == write["id"] and not b.get("is_error")
                    for b in result
                )
            )

    def test_successful_claude_file_revisions_are_distinct_from_stdout(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "events.jsonl"
            lines = []
            for i, p in enumerate((0.26, 0.9, 0.31)):
                identifier = str(i)
                values = {"p_blue_win": p, "p_blue_ahead_15": 0.58}
                call = {
                    "type": "tool_use",
                    "id": identifier,
                    "name": "Write",
                    "input": {
                        "file_path": "[ephemeral]/app/prediction.json",
                        "content": json.dumps(values),
                    },
                }
                result = {
                    "type": "tool_result",
                    "tool_use_id": identifier,
                    "is_error": i == 1,
                    "content": "denied" if i == 1 else "file saved",
                }
                lines.extend(
                    [
                        {"type": "assistant", "message": {"content": [call]}},
                        {"type": "user", "message": {"content": [result]}},
                    ]
                )
            path.write_text("".join(json.dumps(e) + "\n" for e in lines))
            timeline = build_timeline(path, phase="draft-lock")
            self.assertEqual(timeline["readbacks"], [])
            self.assertEqual(
                [e["values"]["p_blue_win"] for e in timeline["checkpoints"]],
                [0.26, 0.31],
            )

    def test_no_record_and_partial_log(self):
        self.assertEqual(
            build_timeline(None, phase="lobby")["availability"], "unavailable"
        )
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "log"
            p.write_text('{"type":"trace.truncated","limit":999}\n')
            self.assertEqual(
                build_timeline(p, phase="lobby")["availability"], "truncated"
            )
