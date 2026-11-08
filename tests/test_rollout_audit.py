"""Audit frozen real runs plus adversarial transcripts. No shell commands are executed."""

import json
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from evaluation.rollout_audit import SOURCE_DIR, audit, inspect_calls
from evaluation.suite import DEFAULT_RELEASE, report_row, select, unpack
from production.build import ROOT
from production.store import digest, read

DRAFT = "worlds-2026-main-event-quarterfinals-4-g2-draft-lock"
FIELDS = {"p_blue_win": 0.31, "p_blue_ahead_15": 0.58}


def bash(command, output="", status=0, identifier="command_1"):
    return {
        "type": "item.completed",
        "item": {
            "id": identifier,
            "type": "command_execution",
            "command": command,
            "aggregated_output": output,
            "exit_code": status,
        },
    }


class RolloutAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.reference = Path(cls.temp.name) / "canonical"
        cls.organizer = {
            (r["series"], r["n"]): r for r in read(ROOT / "production/data/games.json")
        }
        report = read(SOURCE_DIR / "featured-five-deepseek/report.json")
        manifest, rows = select(DEFAULT_RELEASE, ids=report["planned"])
        unpack(DEFAULT_RELEASE, manifest, rows, cls.reference)

    def inspect(self, events, harness="codex"):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "trajectory.jsonl"
            path.write_text("".join(json.dumps(e) + "\n" for e in events))
            return inspect_calls(path, harness)

    def test_real_complete_and_partial_runs(self):
        samples = (
            ("featured-five-deepseek", {"scored": 10}, 0),
            ("featured-five-claude-deepseek", {"scored": 10}, 0),
            ("featured-five-openrouter", {"scored": 4, "failed": 2}, 4),
        )
        for name, statuses, unstarted in samples:
            with self.subTest(name=name):
                view = audit(SOURCE_DIR / name, self.reference, self.organizer)
                self.assertTrue(all(view["checks"].values()), view["checks"])
                self.assertEqual(Counter(t["status"] for t in view["trials"]), statuses)
                self.assertEqual(view["unstarted"], unstarted)
                for t in view["trials"]:
                    self.assertTrue(all(t["checks"].values()), (t["task"], t["checks"]))
                    self.assertEqual(t["access_flags"], [], t["task"])
                    if t["status"] == "failed":
                        self.assertTrue(t["checks"]["failure_excluded_from_scored"])
                if name == "featured-five-claude-deepseek":
                    game = next(t for t in view["trials"] if t["task"] == DRAFT)
                    self.assertEqual(game["last_checkpoint"]["values"], FIELDS)
                if name == "featured-five-openrouter":
                    failed_with_draft = next(
                        t
                        for t in view["trials"]
                        if t["status"] == "failed" and t["last_checkpoint"]
                    )
                    self.assertTrue(
                        failed_with_draft["checks"]["failure_excluded_from_scored"]
                    )

    def test_real_submission_changed_after_last_observed_write_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "run"
            shutil.copytree(SOURCE_DIR / "featured-five-claude-deepseek", folder)
            report = read(folder / "report.json")
            trial = next(t for t in report["trials"] if t["task"] == DRAFT)
            prediction = {"p_blue_win": 0.99, "p_blue_ahead_15": 0.02}
            path = folder / "jobs" / DRAFT / "prediction.json"
            path.write_text(json.dumps(prediction))
            # A replacement submission can carry a mathematically correct grade;
            # the independent observation of the final value must still catch it.
            trial.update(report_row(self.reference / DRAFT, prediction))
            trial["origin"]["files_sha256"]["prediction.json"] = digest(path)
            (folder / "report.json").write_text(json.dumps(report))
            view = audit(folder, self.reference, self.organizer)
            changed = next(t for t in view["trials"] if t["task"] == DRAFT)
            self.assertTrue(changed["checks"]["independent_grade"])
            self.assertFalse(
                changed["checks"]["last_recorded_forecast_matches_submission"]
            )

    def test_failed_external_attempt_is_flagged_but_permitted_snapshot_read_passes(
        self,
    ):
        good = self.inspect([bash("cat ./snapshot.json", '{"current":{}}')])
        self.assertIsNotNone(good["first_snapshot_line"])
        self.assertEqual(good["access_flags"], [])
        for command in (
            "curl https://example.invalid/result",
            "cat /tests/labels.json",
            "cat /solution/solve.sh",
            "python3 -c 'import os; print(os.environ)'",
        ):
            with self.subTest(command=command):
                bad = self.inspect([bash(command, "denied", status=1)])
                self.assertEqual(bad["failed_tools"], 1)
                self.assertTrue(any(f["line"] == 1 for f in bad["access_flags"]), bad)

    def test_forbidden_native_read_and_unsuccessful_native_write(self):
        events = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "r",
                            "name": "Read",
                            "input": {"file_path": "/tests/labels.json"},
                        }
                    ]
                },
            },
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "r",
                            "content": "permission denied",
                            "is_error": True,
                        }
                    ]
                },
            },
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "w",
                            "name": "Write",
                            "input": {
                                "file_path": "[ephemeral]/app/prediction.json",
                                "content": json.dumps(FIELDS),
                            },
                        }
                    ]
                },
            },
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "w",
                            "content": "write failed",
                            "is_error": True,
                        }
                    ]
                },
            },
        ]
        out = self.inspect(events, "claude")
        self.assertTrue(any(f["line"] == 1 for f in out["access_flags"]))
        self.assertIsNone(out["last_checkpoint"])
        self.assertEqual(out["failed_tools"], 2)

    def test_later_unobserved_overwrite_cannot_reuse_a_stale_readback(self):
        out = self.inspect(
            [
                bash("cat prediction.json", json.dumps(FIELDS)),
                bash(
                    'python3 -c \'from pathlib import Path; Path("prediction.json").write_text("{}")\'',
                    identifier="replace",
                ),
            ]
        )
        self.assertNotEqual((out["last_checkpoint"] or {}).get("values"), FIELDS)

    def test_hidden_canary_in_an_otherwise_ordinary_return_is_detected(self):
        marker = "LOL_HIDDEN_" + "a1" * 16
        out = self.inspect([bash("cat ./snapshot.json", '{"note":"' + marker + '"}')])
        self.assertTrue(any(f["line"] == 1 for f in out["access_flags"]), out)

    def test_printing_a_filename_does_not_prove_a_read_or_a_forecast(self):
        fake = self.inspect(
            [bash("echo snapshot.json prediction.json", json.dumps(FIELDS))]
        )
        self.assertIsNone(fake["first_snapshot_line"])
        self.assertIsNone(fake["last_checkpoint"])

    def test_unfinished_dangerous_commands_are_not_reported_as_paired_or_clean(self):
        started = {
            "type": "item.started",
            "item": {
                "type": "command_execution",
                "id": "ongoing",
                "command": "cat /tests/labels.json",
            },
        }
        claude = {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Read",
                        "id": "ongoing",
                        "input": {"file_path": "/tests/labels.json"},
                    }
                ]
            },
        }
        for harness, event in (("codex", started), ("claude", claude)):
            with self.subTest(harness=harness):
                result = self.inspect([event], harness)
                self.assertEqual(result["unpaired_calls"], [1])
                self.assertTrue(any(f["line"] == 1 for f in result["access_flags"]))

    def test_overlaps_or_omissions_in_a_partial_report_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "run"
            shutil.copytree(SOURCE_DIR / "featured-five-openrouter", dest)
            original = read(dest / "report.json")
            for records in (
                original["unstarted"][:-1],
                [*original["unstarted"], original["unstarted"][0]],
                [
                    {**original["unstarted"][0], "task": original["trials"][0]["task"]},
                    *original["unstarted"][1:],
                ],
            ):
                with self.subTest(ids=[t["task"] for t in records]):
                    (dest / "report.json").write_text(
                        json.dumps({**original, "unstarted": records})
                    )
                    result = audit(dest, self.reference, self.organizer)
                    self.assertFalse(result["checks"]["fixed_suite_partition"])
            manipulated = {
                **original,
                "attempted_summary": {
                    **original["attempted_summary"],
                    "mean_reward": 1,
                },
            }
            (dest / "report.json").write_text(json.dumps(manipulated))
            self.assertFalse(
                audit(dest, self.reference, self.organizer)["checks"]["summary"]
            )

    def test_omitted_raw_digest_and_unrelated_http_200_cannot_certify_trial(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "run"
            shutil.copytree(SOURCE_DIR / "featured-five-claude-deepseek", dest)
            doc = read(dest / "report.json")
            trial = next(t for t in doc["trials"] if t["task"] == DRAFT)
            del trial["origin"]["files_sha256"]["trajectory.jsonl"]
            runtime = dest / "jobs" / DRAFT / "run.json"
            run = read(runtime)
            run["upstream"] = [{"path": "/api/hello", "status": 200}]
            runtime.write_text(json.dumps(run))
            trial["runtime"] = run
            trial["origin"]["files_sha256"]["run.json"] = digest(runtime)
            (dest / "report.json").write_text(json.dumps(doc))
            results = audit(dest, self.reference, self.organizer)
            checks = next(t["checks"] for t in results["trials"] if t["task"] == DRAFT)
            self.assertFalse(checks["raw_artifacts_intact"])
            self.assertFalse(checks["upstream_inference"])
