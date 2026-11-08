import copy
import unittest

from evaluation.ranking import leaderboard

WIN, AHEAD = "p_blue_win", "p_blue_ahead_15"


def report(ids=("game-1", "game-2"), **extra):
    r = {
        "release": "replay-v3",
        "archive_sha256": "a" * 64,
        "mode": "live",
        "backend": "harbor",
        "harness": "codex",
        "model": "m:free",
        "planned": list(ids),
        "trials": [
            {
                "task": t,
                "status": "scored",
                "prediction": {WIN: 0.5, AHEAD: 0.5},
                "brier": {WIN: 0.25, AHEAD: 0.25},
                "reward": 0.75,
            }
            for t in ids
        ],
    }
    return {**r, **extra}


class RankingTests(unittest.TestCase):
    def test_pool_attempts_count_failures_and_do_not_pick_best(self):
        full = {"game-1", "game-2"}
        # Also check set equality is independent of task order and provider.
        a = report()
        b = report(tuple(reversed(a["planned"])), mode="openrouter-free")
        b["trials"][0] = {"task": "game-2", "status": "failed"}
        c = report(harness="pi")
        out = leaderboard([("b", b, full), ("c", c, full), ("a", a, full)])
        self.assertEqual(out["excluded"], [])
        (g,) = out["groups"]
        self.assertFalse(g["official"])
        good, pooled = g["entries"]
        self.assertEqual((good["rank"], pooled["rank"]), (1, 2))
        self.assertEqual(
            (pooled["attempts"], pooled["selected"], pooled["scored"]), (2, 4, 3)
        )
        self.assertEqual(pooled["mean_reward"], 0.5625)
        self.assertEqual((pooled["completion_rate"], pooled["brier_win"]), (0.75, 0.25))
        self.assertEqual(pooled["run_ids"], ["a", "b"])

    def test_group_isolation(self):
        full = {"game-1", "game-2"}
        runs = [
            ("full", report(), full),
            ("subset", report(["game-1"]), full),
            ("vendor", report(mode="vendor", harness="cursor"), full),
            (
                "baseline",
                report(
                    mode="baseline",
                    backend="local",
                    harness="player-baseline",
                    model=None,
                ),
                full,
            ),
            ("fixture", report(mode="fixture"), full),
            ("other_backend", report(backend="macos"), full),
            ("other_archive", report(archive_sha256="b" * 64), full),
            ("protocol", report(protocol_sha256="c" * 64), full),
        ]
        out = leaderboard(runs)
        self.assertEqual(len(out["groups"]), len(runs))
        self.assertFalse(
            next(g["official"] for g in out["groups"] if g["scope"] == "subset")
        )

    def test_reject_invalid_and_unfinished_old_records(self):
        variations = []
        for change in (
            {"reward": 1},
            {"prediction": {WIN: True, AHEAD: 0.5}},
            {"brier": {WIN: float("nan"), AHEAD: 0.25}},
            {"observed_outcome": {WIN: 2, AHEAD: 1}},
            {"status": "started"},
            {"runtime": {"mode": "fixture"}},
        ):
            r = report()
            r["trials"][0].update(change)
            variations.append(r)
        r = report()
        r["trials"].pop()
        variations.append(r)
        r = report()
        r["trials"][1] = copy.deepcopy(r["trials"][0])
        variations.append(r)
        variations += [
            report(summary={"mean_reward": 1}),
            report(planned=["game-1", "game-1"]),
            report(archive_sha256="bogus"),
        ]
        attempts = [
            (str(i), r, {"game-1", "game-2"}) for i, r in enumerate(variations)
        ] + [("unknown", report(), None)]
        out = leaderboard(attempts)
        self.assertEqual(out["groups"], [])
        self.assertEqual(len(out["excluded"]), len(attempts))

    def test_trusted_release_rescores_and_rejects_fabricated_result(self):
        clean = report()
        evidence = {
            t: {
                "labels": {WIN: 0, AHEAD: 1},
                "snapshot_sha256": "b" * 64,
                "prompt_sha256": "c" * 64,
            }
            for t in clean["planned"]
        }
        for t in clean["trials"]:
            t.update(snapshot_sha256="b" * 64, prompt_sha256="c" * 64)
        wrong = copy.deepcopy(clean)
        # Internally consistent with a fabricated all-blue winner label.
        wrong["trials"][0].update(
            prediction={WIN: 1, AHEAD: 1},
            observed_outcome={WIN: 1, AHEAD: 1},
            brier={WIN: 0, AHEAD: 0},
            reward=1,
        )
        concealed = copy.deepcopy(wrong)
        del concealed["trials"][0]["observed_outcome"]
        different_input = copy.deepcopy(clean)
        different_input["trials"][0]["snapshot_sha256"] = "d" * 64
        out = leaderboard(
            [
                ("clean", clean, evidence),
                ("forged", wrong, evidence),
                ("hidden", concealed, evidence),
                ("input", different_input, evidence),
            ]
        )
        self.assertEqual(
            {v["run_id"] for v in out["excluded"]}, {"forged", "hidden", "input"}
        )
        self.assertTrue(out["groups"][0]["official"])
        self.assertEqual(out["groups"][0]["entries"][0]["attempts"], 1)

    def test_tie_and_no_successful_brier(self):
        r = report()
        for t in r["trials"]:
            t.update(status="interrupted", reward=0)
        s = {**r, "harness": "kimi"}
        entries = leaderboard(
            [("r", r, set(r["planned"])), ("s", s, set(s["planned"]))]
        )["groups"][0]["entries"]
        self.assertEqual([t["rank"] for t in entries], [1, 1])
        self.assertTrue(
            all(t["brier_win"] is None and t["mean_reward"] == 0 for t in entries)
        )
