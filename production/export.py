"""Export an immutable Harbor release for streaming RL training and held-out evaluation."""

import argparse
import gzip
import hashlib
import io
import json
import re
import tempfile
import zipfile
from collections import Counter
from contextlib import ExitStack
from datetime import UTC, datetime
from pathlib import Path

from evaluation.dataset import (
    DATA_SOURCE,
    INLINE,
    WORKSPACE,
    inline_messages,
    iter_rows,
)
from evaluation.suite import DEFAULT_RELEASE, select, unpack
from production.build import ROOT
from production.catalog import resolve_release
from production.evidence import load_packs
from production.schema import instant, slug
from production.specs import GRADER
from production.store import digest, read

DEFAULT_BUNDLE = ROOT / "datasets/rl-eval-v1"
# Fixed timeline boundaries keep existing memberships stable when future games arrive.
VALID_FROM = datetime(2026, 10, 28, tzinfo=UTC)
TEST_FROM = datetime(2026, 11, 3, tzinfo=UTC)


def split_for(when):
    if when < VALID_FROM:
        return "train"
    if when < TEST_FROM:
        return "validation"
    return "test"


def encode(row):
    return json.dumps(row, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def jsonl_writer(stack, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = stack.enter_context(path.open("xb"))
    compressed = stack.enter_context(
        gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0)
    )
    return stack.enter_context(
        io.TextIOWrapper(compressed, encoding="utf-8", newline="\n")
    )


def build_export(release, destination, parquet=False):
    manifest, tasks = select(release)
    version = slug(manifest["version"])
    spec = manifest.get("task_spec")
    if spec and (
        spec["grader"] != GRADER
        or spec["components"]["template"]["file"] != "forecast.md"
    ):
        raise ValueError("No inline forecast adapter for this task template or grader")
    if manifest.get("evidence_packs") and not spec:
        raise ValueError("Evidence treatment requires a versioned task protocol")
    if destination.exists():
        raise FileExistsError(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as temp:
        root = Path(temp)
        expanded = root / "tasks"
        bundle = root / "bundle"
        bundle.mkdir()
        unpack(release, manifest, tasks, expanded)
        sized = Counter()
        series_times = {}
        ordered = []
        for task in tasks:
            view = read(expanded / task["id"] / "environment/snapshot.json")
            when = instant(view["series_time_utc"])
            series = task["series"]
            if series_times.setdefault(series, when) != when:
                raise ValueError(f"Inconsistent series time for {series}")
            ordered.append((when, series, task["game"], task["phase"] != "lobby", task))
        splits = ("train", "validation", "test")
        with ExitStack() as stack:
            eval_files = {
                s: jsonl_writer(stack, bundle / "eval" / f"{s}.jsonl.gz")
                for s in splits
            }
            label_files = {
                s: jsonl_writer(stack, bundle / "verifier" / f"{s}.jsonl.gz")
                for s in splits
            }
            rl = jsonl_writer(stack, bundle / "rl/train.jsonl.gz")
            tool_rl = jsonl_writer(stack, bundle / "rl/train-workspace.jsonl.gz")
            archive = stack.enter_context(
                zipfile.ZipFile(bundle / "snapshots.zip", "x")
            )
            seen = set()
            for when, series, game, _, task in sorted(
                ordered, key=lambda item: item[:-1]
            ):
                split = split_for(when)
                sized[split] += 1
                task_id = task["id"]
                case = expanded / task_id
                blob = (case / "environment/snapshot.json").read_bytes()
                sha = task["snapshot_sha256"]
                if sha not in seen:
                    member = zipfile.ZipInfo(
                        sha + ".json", date_time=(1980, 1, 1, 0, 0, 0)
                    )
                    archive.writestr(
                        member,
                        blob,
                        compress_type=zipfile.ZIP_DEFLATED,
                        compresslevel=6,
                    )
                    seen.add(sha)
                rid = f"lol-competition-bench/{version}/{task_id}"
                extra = {
                    "id": rid,
                    "split": split,
                    "series": series,
                    "game": game,
                    "phase": task["phase"],
                    "patch": task["patch"],
                    "series_start_unix": int(when.timestamp()),
                    "harbor_release": version,
                    "harbor_task": task_id,
                    "snapshot_sha256": sha,
                    "prompt_sha256": task["prompt_sha256"],
                    "protocol": WORKSPACE,
                }
                row = {
                    "id": rid,
                    "data_source": DATA_SOURCE,
                    "ability": "esports_probability_forecasting",
                    "prompt": [
                        {
                            "role": "user",
                            "content": (case / "instruction.md").read_text(),
                        }
                    ],
                    "extra_info": extra,
                }
                if spec:
                    extra.update(
                        task_spec=spec["id"],
                        protocol_sha256=spec["protocol_sha256"],
                        evidence_pack_sha256=[
                            p["sha256"] for p in manifest.get("evidence_packs", [])
                        ],
                    )
                truth = {"id": rid, "labels": read(case / "tests/labels.json")}
                eval_files[split].write(encode(row) + "\n")
                label_files[split].write(encode(truth) + "\n")
                if split == "train":
                    reward = {"style": "rule", "ground_truth": encode(truth)}
                    tool_rl.write(encode(dict(row, reward_model=reward)) + "\n")
                    messages = inline_messages(
                        blob, row["prompt"][0]["content"] if spec else None
                    )
                    policy_row = dict(
                        row,
                        prompt=messages,
                        extra_info=dict(
                            extra,
                            protocol="inline-workspace-json-v1" if spec else INLINE,
                            prompt_sha256=hashlib.sha256(
                                messages[0]["content"].encode()
                            ).hexdigest(),
                        ),
                        reward_model=reward,
                    )
                    rl.write(encode(policy_row) + "\n")
        info = {
            "format": "lol-competition-bench/rl-eval-v1",
            "data_source": DATA_SOURCE,
            "release": version,
            "source_archive_sha256": manifest["sha256"],
            "validation_from": VALID_FROM.isoformat(),
            "test_from": TEST_FROM.isoformat(),
            "split_unit": "series",
            "tasks_by_split": {s: sized[s] for s in splits},
            "series_by_split": dict(
                Counter(split_for(t) for t in series_times.values())
            ),
            "unique_snapshots": len(seen),
        }
        for key in ("task_spec", "protocol_sha256", "evidence_packs"):
            if key in manifest:
                info[key] = manifest[key]
        if parquet:
            # Bound memory to a small group of inline prompts, even on larger releases.
            from itertools import batched

            import pyarrow as pa
            import pyarrow.parquet as pq

            with ExitStack() as stack:
                writer = None
                for batch in batched(iter_rows(bundle / "rl/train.jsonl.gz"), 16):
                    table = pa.Table.from_pylist(list(batch))
                    if writer is None:
                        writer = stack.enter_context(
                            pq.ParquetWriter(
                                bundle / "rl/train.parquet",
                                table.schema,
                                compression="zstd",
                            )
                        )
                    writer.write_table(table)
                if writer is None:
                    raise ValueError(
                        "A release with no training games has no training Parquet schema"
                    )
            info["pyarrow_version"] = pa.__version__
        card = Path(__file__).with_name("rl_eval_card.md").read_text()
        if spec:
            card = card.replace(
                "compute_score, inline_messages, iter_rows, materialize, snapshot_bytes",
                "compute_score, inline_evaluation_messages, iter_rows, materialize",
            )
            card = card.replace(
                "inline_messages(snapshot_bytes(bundle, row))",
                "inline_evaluation_messages(bundle, row)",
            )
            card += (
                "\n## Selected treatment\n\nThe original workspace instructions, examples, "
                "background and frozen evidence are retained in the training messages. "
                "The inline wrapper maps file reads and writes to prompt input and reply output. "
                "The manifest identifies the task specification and selected evidence pack digests.\n"
            )
        for meta in manifest.get("evidence_packs", []):
            sha = meta["sha256"]
            if not re.fullmatch(r"[0-9a-f]{64}", sha):
                raise ValueError("Invalid evidence pack digest")
            path = Path("evidence-packs") / (sha + ".json")
            (pack,) = load_packs([release / path])
            if pack.metadata() != meta:
                raise ValueError("Evidence pack provenance mismatch")
            (bundle / path.parent).mkdir(exist_ok=True)
            (bundle / path).write_bytes((release / path).read_bytes())
        (bundle / "README.md").write_text(card)
        info["files_sha256"] = {
            p.relative_to(bundle).as_posix(): digest(p)
            for p in sorted(bundle.rglob("*"))
            if p.is_file()
        }
        (bundle / "manifest.json").write_text(
            json.dumps(info, ensure_ascii=False, indent=2) + "\n"
        )
        bundle.rename(destination)
    return destination


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--release", type=resolve_release, default=DEFAULT_RELEASE)
    p.add_argument("--out", type=Path, default=DEFAULT_BUNDLE)
    p.add_argument(
        "--parquet",
        action="store_true",
        help="Also write rl/train.parquet (requires pyarrow)",
    )
    args = p.parse_args()
    print(build_export(args.release, args.out, args.parquet))
