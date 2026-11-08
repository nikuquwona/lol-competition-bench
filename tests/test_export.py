import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from evaluation.dataset import (
    DATA_SOURCE,
    compute_score,
    inline_messages,
    iter_rows,
    materialize,
    snapshot_bytes,
)
from evaluation.suite import DEFAULT_RELEASE, select, unpack
from production.build import ROOT, eligible
from production.export import DEFAULT_BUNDLE, build_export, split_for
from production.schema import instant
from production.score import score
from production.store import digest, read


class PortableExportTest(unittest.TestCase):
    def test_results_public_before_first_later_split_fixture(self):
        groups = {"train": [], "validation": [], "test": []}
        for game in read(ROOT / "production/data/games.json"):
            if eligible(game):
                groups[split_for(instant(game["series_time"]))].append(game)
        for prior, later in (("train", "validation"), ("validation", "test")):
            last_publication = max(instant(g["replay_published"]) for g in groups[prior])
            first_game = min(instant(g["series_time"]) for g in groups[later])
            self.assertLess(last_publication, first_game)

    def test_each_row_joins_the_exact_harbor_input_and_label(self):
        manifest, tasks = select(DEFAULT_RELEASE)
        bundle = DEFAULT_BUNDLE
        info = read(bundle / "manifest.json")
        self.assertEqual(info["source_archive_sha256"], manifest["sha256"])
        for path, expected in info["files_sha256"].items():
            self.assertEqual(digest(bundle / path), expected)
        by_series = {}
        by_game = {}
        seen = set()
        when = -1
        with TemporaryDirectory() as tmp:
            work = Path(tmp)
            unpack(DEFAULT_RELEASE, manifest, tasks, work)
            for split in ("train", "validation", "test"):
                rows = iter_rows(bundle / "eval" / f"{split}.jsonl.gz")
                labels = iter_rows(bundle / "verifier" / f"{split}.jsonl.gz")
                for row, label in zip(rows, labels, strict=True):
                    self.assertNotIn("reward_model", row)
                    self.assertNotIn("labels", row)
                    self.assertEqual(row["id"], label["id"])
                    self.assertNotIn(row["id"], seen)
                    seen.add(row["id"])
                    x = row["extra_info"]
                    self.assertEqual(by_series.setdefault(x["series"], split), split)
                    self.assertLessEqual(when, x["series_start_unix"])
                    when = x["series_start_unix"]
                    by_game.setdefault((x["series"], x["game"]), []).append(x["phase"])
                    task = work / x["harbor_task"]
                    self.assertEqual(
                        snapshot_bytes(bundle, row),
                        (task / "environment/snapshot.json").read_bytes(),
                    )
                    self.assertEqual(
                        row["prompt"][0]["content"],
                        (task / "instruction.md").read_text(),
                    )
                    oracle = read(task / "tests/labels.json")
                    self.assertEqual(label["labels"], oracle)
                    pred = {"p_blue_win": 0.21, "p_blue_ahead_15": 0.68}
                    self.assertEqual(
                        compute_score(
                            DATA_SOURCE, json.dumps(pred), json.dumps(label), x
                        ),
                        score(pred, oracle),
                    )
        self.assertTrue(
            all(phases == ["lobby", "draft-lock"] for phases in by_game.values())
        )
        self.assertEqual(len(seen), 198)

    def test_rl_messages_and_held_out_workspace(self):
        bundle = DEFAULT_BUNDLE
        rl = iter_rows(bundle / "rl/train.jsonl.gz")
        train = iter_rows(bundle / "eval/train.jsonl.gz")
        tool_rl = iter_rows(bundle / "rl/train-workspace.jsonl.gz")
        for policy, tool, tool_policy in zip(rl, train, tool_rl, strict=True):
            self.assertEqual(tool_policy["reward_model"], policy["reward_model"])
            self.assertEqual(tool_policy["prompt"], tool["prompt"])
            self.assertEqual(tool_policy["extra_info"], tool["extra_info"])
            self.assertEqual(policy["id"], tool["id"])
            expected = inline_messages(snapshot_bytes(bundle, tool))
            self.assertEqual(policy["prompt"], expected)
            self.assertEqual(
                policy["extra_info"]["prompt_sha256"],
                hashlib.sha256(expected[0]["content"].encode()).hexdigest(),
            )
            reward = compute_score(
                DATA_SOURCE,
                '{"p_blue_win":0.5,"p_blue_ahead_15":0.5}',
                policy["reward_model"]["ground_truth"],
                policy["extra_info"],
            )
            self.assertEqual(reward, 0.75)
        pair = [
            r
            for r in iter_rows(bundle / "eval/test.jsonl.gz")
            if r["extra_info"]["series"].endswith("quarterfinals-4")
            and r["extra_info"]["game"] == 2
        ]
        self.assertEqual(len(pair), 2)
        with TemporaryDirectory() as tmp:
            out = materialize(bundle, pair[0], Path(tmp) / "app")
            self.assertEqual(
                sorted(p.name for p in out.iterdir()),
                ["instruction.md", "snapshot.json"],
            )
            self.assertNotIn("bp", read(out / "snapshot.json")["current"])
            self.assertEqual(
                len(json.loads(snapshot_bytes(bundle, pair[1]))["current"]["bp"]), 20
            )
            with self.assertRaises(FileExistsError):
                materialize(bundle, pair[0], out)
        wrong = dict(pair[0])
        wrong["extra_info"] = dict(
            pair[0]["extra_info"],
            snapshot_sha256=pair[1]["extra_info"]["snapshot_sha256"],
        )
        with self.assertRaisesRegex(ValueError, "different forecast"):
            snapshot_bytes(bundle, wrong)
        key = next(
            r
            for r in iter_rows(bundle / "verifier/test.jsonl.gz")
            if r["id"] == pair[1]["id"]
        )
        with self.assertRaisesRegex(ValueError, "IDs"):
            compute_score(DATA_SOURCE, "{}", json.dumps(key), pair[0]["extra_info"])
        self.assertEqual(
            compute_score(
                DATA_SOURCE, "invalid", json.dumps(key), pair[1]["extra_info"]
            ),
            0.0,
        )

    def test_export_reproducible_without_optional_dependencies(self):
        source = read(DEFAULT_BUNDLE / "manifest.json")
        with TemporaryDirectory() as tmp:
            target = build_export(DEFAULT_RELEASE, Path(tmp) / "portable")
            regenerated = read(target / "manifest.json")
            self.assertEqual(
                regenerated["files_sha256"],
                {
                    k: v
                    for k, v in source["files_sha256"].items()
                    if k != "rl/train.parquet"
                },
            )
            with self.assertRaises(FileExistsError):
                build_export(DEFAULT_RELEASE, target)
