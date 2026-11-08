import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from evaluation.assemble import CONFIG
from evaluation.selections import suite_ids
from evaluation.suite import DEFAULT_RELEASE, report_row, select, unpack
from production.build import ROOT
from production.store import digest, read


class FeaturedSuiteTests(unittest.TestCase):
    def test_official_deepseek_run_scores_all_ten_fresh_native_forecasts(self):
        out = ROOT / "evaluation/examples/featured-five-deepseek"
        report = read(out / "report.json")
        self.assertEqual(
            (report["model"], report["harness"], report["mode"], report["backend"]),
            ("deepseek-v4-pro", "codex", "live", "macos"),
        )
        self.assertEqual(report["summary"]["scored"], 10)
        self.assertEqual(report["paired"]["scored_pairs"], 5)
        self.assertFalse(report["unstarted"])
        self.assertEqual(len({r["origin"]["trial_id"] for r in report["trials"]}), 10)
        manifest, rows = select(
            DEFAULT_RELEASE, suite_ids(report["suite"], DEFAULT_RELEASE)
        )
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            unpack(DEFAULT_RELEASE, manifest, rows, root)
            for r in report["trials"]:
                origin = r["origin"]
                src = out / origin["source_report"]
                self.assertEqual(digest(src), origin["source_report_sha256"])
                job = out / "jobs" / r["task"]
                for name, h in origin["files_sha256"].items():
                    artifact = (
                        out / r["trajectory"]["files"]["snapshot"]
                        if name == "snapshot.json"
                        else job / name
                    )
                    self.assertEqual(digest(artifact), h)
                grade = report_row(root / r["task"], read(job / "prediction.json"))
                self.assertEqual({k: r[k] for k in grade}, grade)
                self.assertEqual(r["runtime"]["cli"], "codex-cli 0.167.0")
                self.assertTrue(
                    any(e["status"] == 200 for e in r["runtime"]["upstream"])
                )

    def test_fixed_set_and_selection_rule_from_model_visible_inputs(self):
        ids = suite_ids("featured-five", DEFAULT_RELEASE)
        self.assertEqual(len(ids), 10)
        self.assertEqual(len(set(ids)), 10)
        with self.assertRaisesRegex(ValueError, "pinned release"):
            suite_ids("featured-five", DEFAULT_RELEASE.parent / "replay-v2")
        manifest, tasks = select(DEFAULT_RELEASE, phase="lobby")
        with TemporaryDirectory() as temp:
            root = Path(temp)
            unpack(DEFAULT_RELEASE, manifest, tasks, root)
            seen_teams = {"Karmine Corp", "T1"}
            games = {("worlds-2026-main-event-quarterfinals-4", 2)}
            for prefix, game in (
                ("lpl-2026-", 2),
                ("worlds-2026-play-in-", 2),
                ("worlds-2026-main-event-round-1-", 1),
                ("worlds-2026-main-event-round-5-", 2),
            ):
                choices = []
                for row in tasks:
                    if row["series"].startswith(prefix) and row["game"] == game:
                        view = read(root / row["id"] / "environment/snapshot.json")
                        teams = (view["current"]["blue"], view["current"]["red"])
                        choices.append(
                            (
                                len(seen_teams.intersection(teams)),
                                view["series_time_utc"],
                                row["series"],
                                teams,
                            )
                        )
                _, _, series, teams = min(choices)
                games.add((series, game))
                seen_teams.update(teams)
            self.assertEqual(len(seen_teams), 10)
            self.assertEqual(
                set(ids),
                {
                    f"{series}-g{n}-{ph}"
                    for series, n in games
                    for ph in ("lobby", "draft-lock")
                },
            )

    def test_published_example_has_auditable_attempts_and_explicit_coverage(self):
        out = ROOT / "evaluation/examples/featured-five-openrouter"
        doc = read(out / "report.json")
        ids = suite_ids(doc["suite"], DEFAULT_RELEASE)
        self.assertEqual(set(ids), set(doc["planned"]))
        attempts = {t["task"] for t in doc["trials"]}
        unstarted = {t["task"] for t in doc["unstarted"]}
        self.assertFalse(attempts & unstarted)
        self.assertEqual(attempts | unstarted, set(ids))
        manifest, rows = select(DEFAULT_RELEASE, ids)
        with TemporaryDirectory() as temp:
            root = Path(temp)
            unpack(DEFAULT_RELEASE, manifest, rows, root)
            identities = set()
            for t in doc["trials"]:
                origin = t["origin"]
                source_path = out / origin["source_report"]
                self.assertEqual(digest(source_path), origin["source_report_sha256"])
                source = next(
                    tr for tr in read(source_path)["trials"] if tr["task"] == t["task"]
                )
                self.assertEqual(source["status"], t["status"])
                job = out / "jobs" / t["task"]
                hashes = origin["files_sha256"]
                for name, sha in hashes.items():
                    path = (
                        out / t["trajectory"]["files"]["snapshot"]
                        if name == "snapshot.json"
                        else job / name
                    )
                    self.assertEqual(digest(path), sha)
                data = [
                    *[doc[k] for k in CONFIG],
                    t["task"],
                    hashes["trajectory.jsonl"],
                ]
                idsig = hashlib.sha256(
                    json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode()
                ).hexdigest()
                self.assertEqual(origin["trial_id"], idsig)
                self.assertNotIn(idsig, identities)
                identities.add(idsig)
                if t["status"] == "scored":
                    grade = report_row(root / t["task"], read(job / "prediction.json"))
                    self.assertEqual({k: t[k] for k in grade}, grade)
                    self.assertEqual(source["reward"], t["reward"])
                else:
                    self.assertEqual(t["failure_class"], "provider_daily_quota")
                    self.assertNotIn("prediction", t)
            for u in doc["unstarted"]:
                self.assertNotIn("reward", u)
                self.assertNotIn("runtime", u)
                self.assertEqual(
                    digest(out / u["files"]["snapshot"]), u["snapshot_sha256"]
                )
                self.assertEqual(digest(out / u["files"]["prompt"]), u["prompt_sha256"])
            if unstarted:
                self.assertNotIn("summary", doc)
        for s in doc["provenance"]["authentication_diagnostics"]:
            self.assertEqual(digest(out / s["file"]), s["sha256"])
            for i in s["planned"]:
                run = read(out / "diagnostics" / s["sha256"] / i / "run.json")
                self.assertTrue(run["upstream"])
                self.assertEqual({e["status"] for e in run["upstream"]}, {401})
