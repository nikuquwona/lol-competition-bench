import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from evaluation.suite import DEFAULT_RELEASE, SAMPLE, select, unpack, summary
from production.build import ROOT
from production.intake import (
    close_window,
    freeze,
    history,
    history_add,
    read,
    settle,
    standings,
    submit,
    template,
    trusted_case,
    validate_observation,
)
from production.release import publish

NOW = datetime(2027, 1, 2, 12, tzinfo=timezone.utc)
ARCHIVE = read(ROOT / "production/data/games.json")


def observation(n=1, first="red", bo=3):
    # Synthetic test series; champion slots use a verified real draft.
    row = next(g for g in ARCHIVE if len(g["bp"]) == 20 and g["bp"][0]["side"] == first)
    o = template("test-cup-final", n, bo, "draft-lock", first)
    o.update(
        blue="Blue Club",
        red="Red Club",
        event="test-cup",
        stage="final",
        patch="26.20",
        starters={side: [side + str(i) for i in range(5)] for side in ("blue", "red")},
        observed_at=NOW.isoformat(),
        series_time=NOW.isoformat(),
        source="https://example.org/test-fixture",
    )
    for to, src in zip(o["bp"], row["bp"]):
        assert (src["side"], src["action"]) == (to["side"], to["action"])
        to["champion"] = src["champion"] + str(n)
    return o


class Pipeline(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.store = self.base / "store"
        self.clock = patch("production.intake.now", return_value=NOW).start()
        self.addCleanup(patch.stopall)

    def result(self, case, minutes=1):
        return dict(
            id=case.name,
            winner="red",
            blue_gd15=-200,
            game_started_at=(NOW + timedelta(minutes=minutes)).isoformat(),
            published_at=(NOW + timedelta(hours=minutes)).isoformat(),
            source="https://example.org/result",
        )

    def test_new_game_through_release(self):
        o = observation()
        case = freeze(o, self.store)
        frozen = trusted_case(case)
        task = case / "task"
        self.assertFalse((task / "tests").exists())
        self.assertFalse((task / "solution").exists())
        self.assertNotIn(
            "example.org", (task / "environment/snapshot.json").read_text()
        )
        try:
            from harbor.models.task.task import Task
        except ImportError:
            pass
        else:
            Task(task, disable_verification=True)
        with self.assertRaises(FileExistsError):
            freeze(o, self.store)
        pred = dict(p_blue_win=0.2, p_blue_ahead_15=0.3)
        submit(case, "codex-run", pred)
        with self.assertRaises(FileExistsError):
            submit(case, "codex-run", pred)
        self.clock.return_value = NOW + timedelta(minutes=10)
        submit(case, "late", pred)
        self.clock.return_value = NOW + timedelta(hours=2)
        rows = settle(case, self.result(case))
        self.assertEqual([r["status"] for r in rows], ["scored", "ineligible"])
        self.assertAlmostEqual(rows[0]["reward"], 0.935)
        with self.assertRaises(ValueError):
            submit(case, "new", pred)
        self.assertEqual(standings(case), rows)
        with self.assertRaises(FileExistsError):
            settle(case, self.result(case))
        self.assertIsNone(history(self.store)[-1]["replay_published"])
        second = observation(2)
        second["observed_at"] = self.clock.return_value.isoformat()
        c2 = freeze(second, self.store)
        self.assertEqual(
            read(c2 / "task/environment/snapshot.json")["history"][-1]["series"],
            o["series"],
        )
        release = publish(self.base, "test-release", self.store)
        m, selected = select(release, [case.name])
        self.assertEqual(m["count"], 199)
        unpack(release, m, selected, self.base / "expanded")
        self.assertEqual(frozen["prompt_sha256"], selected[0]["prompt_sha256"])
        self.assertEqual(
            (task / "instruction.md").read_bytes(),
            (self.base / "expanded" / case.name / "instruction.md").read_bytes(),
        )
        self.assertEqual(
            read(self.base / "expanded" / case.name / "tests/labels.json"),
            dict(p_blue_win=0, p_blue_ahead_15=0),
        )
        with self.assertRaises(FileExistsError):
            publish(self.base, "test-release", self.store)

    def test_schema_cutoff_tampering(self):
        o = observation()
        for bad in [
            {"winner": "blue"},
            {"observed_at": "tomorrow"},
            {"observed_at": (NOW + timedelta(seconds=1)).isoformat()},
            {"series": "../escape"},
            {"bp": list(reversed(o["bp"]))},
            {"phase": "lobby"},
        ]:
            with self.subTest(bad=list(bad)), self.assertRaises(ValueError):
                freeze({**o, **bad}, self.store)
        for g in ARCHIVE:
            if len(g["bp"]) == 20:
                candidate = {**o, "patch": g["patch"], "bp": g["bp"]}
                validate_observation(candidate)
        with self.assertRaises(ValueError):
            freeze(observation(2), self.store)
        c = freeze(o, self.store)
        with self.assertRaises(ValueError):
            settle(c, {**self.result(c), "game_started_at": NOW.isoformat()})
        (c / "task/environment/snapshot.json").write_text("{}")
        with self.assertRaises(ValueError):
            trusted_case(c)

    def test_shared_game_result_and_phase_order(self):
        locked = observation()
        lobby = {k: v for k, v in locked.items() if k != "bp"}
        lobby["phase"] = "lobby"
        a = freeze(lobby, self.store)
        submit(a, "same-entrant", {"p_blue_win": 0.4, "p_blue_ahead_15": 0.5})
        self.clock.return_value += timedelta(seconds=10)
        close_window(a, self.clock.return_value.isoformat(), lobby["source"])
        with self.assertRaisesRegex(ValueError, "closed"):
            submit(a, "late", {"p_blue_win": 0.5, "p_blue_ahead_15": 0.5})
        self.clock.return_value += timedelta(seconds=10)
        locked["observed_at"] = self.clock.return_value.isoformat()
        b = freeze(locked, self.store)
        submit(b, "same-entrant", {"p_blue_win": 0.3, "p_blue_ahead_15": 0.5})
        self.clock.return_value = NOW + timedelta(hours=2)
        settle(b, self.result(b))
        self.assertEqual(standings(a)[0]["status"], "scored")
        self.assertNotEqual(standings(a)[0]["reward"], standings(b)[0]["reward"])
        with self.assertRaises(FileExistsError):
            settle(a, self.result(a))
        self.assertEqual(
            len([g for g in history(self.store) if g["series"] == locked["series"]]), 1
        )

    def test_lobby_missing_public_time_never_earns_a_score(self):
        locked = observation()
        lobby = {**locked, "phase": "lobby"}
        del lobby["bp"]
        a = freeze(lobby, self.store)
        pred = {"p_blue_win": 0.5, "p_blue_ahead_15": 0.5}
        submit(a, "early", pred)
        self.clock.return_value += timedelta(seconds=20)
        locked["observed_at"] = self.clock.return_value.isoformat()
        b = freeze(locked, self.store)
        with self.assertRaisesRegex(ValueError, "closed"):
            submit(a, "after-lock", pred)
        self.clock.return_value += timedelta(seconds=10)
        with self.assertRaisesRegex(ValueError, "precede"):
            close_window(a, self.clock.return_value.isoformat(), lobby["source"])
        self.clock.return_value = NOW + timedelta(hours=2)
        settle(b, self.result(b))
        unverified = standings(a)[0]
        self.assertEqual(unverified["status"], "unverified")
        self.assertIsNone(unverified["reward"])

    def test_history_backfill_embargo(self):
        for n in (1, 2):
            o = observation(n)
            o["observed_at"] = (NOW + timedelta(hours=n - 1)).isoformat()
            doc = dict(
                observation=o,
                winner="blue",
                blue_gd15=100,
                game_started_at=o["observed_at"],
                published_at=(NOW + timedelta(hours=n)).isoformat(),
                result_source="https://example.org/score",
            )
            self.clock.return_value = NOW + timedelta(hours=n + 1)
            history_add(doc, self.store)
            with self.assertRaises(ValueError):
                history_add(doc, self.store)
        added = [g for g in history(self.store) if g["series"] == o["series"]]
        self.assertEqual(len(added), 2)
        self.assertTrue(
            all(
                g["replay_published"] == (NOW + timedelta(hours=2)).isoformat()
                for g in added
            )
        )

    def test_resume_does_not_rerun_an_attempt(self):
        out = self.base / "run"
        cmd = [
            sys.executable,
            str(ROOT / "bench"),
            "simple",
            "--series",
            "worlds-2026-main-event-quarterfinals-4",
            "--game",
            "2",
            "--out",
            str(out),
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        first = read(out / "report.json")
        self.assertEqual(first["summary"]["scored"], 2)
        first["trials"][0] = {
            "task": first["planned"][0],
            "phase": "draft-lock",
            "status": "started",
        }
        first["trials"] = first["trials"][:1]
        (out / "report.json").write_text(json.dumps(first))
        result = subprocess.run([*cmd, "--resume"], capture_output=True)
        self.assertEqual(result.returncode, 1)
        final = read(out / "report.json")
        self.assertEqual(final["summary"]["statuses"], {"interrupted": 1, "scored": 1})
        original = (out / "report.json").read_bytes()
        self.assertNotEqual(
            subprocess.run(
                [*cmd, "--limit", "1", "--resume"], capture_output=True
            ).returncode,
            0,
        )
        self.assertEqual(original, (out / "report.json").read_bytes())

    def test_archive_checksum_and_failure_denominator(self):
        manifest, rows = select(DEFAULT_RELEASE, [SAMPLE])
        with self.assertRaises(ValueError):
            unpack(DEFAULT_RELEASE, {**manifest, "sha256": "wrong"}, rows, self.base)
        stat = summary(
            [
                dict(status="failed", reward=0),
                dict(
                    status="scored",
                    reward=1,
                    brier={"p_blue_win": 0, "p_blue_ahead_15": 0},
                ),
            ]
        )
        self.assertEqual(stat["mean_reward"], 0.5)
