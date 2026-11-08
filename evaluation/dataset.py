"""Load one training/evaluation record, materialize its workspace, or score its response."""

import gzip
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

from production.score import FIELDS, score, unique_fields

DATA_SOURCE = "lol-competition-bench/game-forecast-v1"
WORKSPACE = "harbor-workspace-v1"
INLINE = "inline-json-v1"


def iter_rows(path):
    """Read one standard JSONL record at a time."""
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            yield json.loads(line)


def snapshot_bytes(bundle, row):
    extra = row["extra_info"]
    digest = extra["snapshot_sha256"]
    with zipfile.ZipFile(Path(bundle) / "snapshots.zip") as archive:
        blob = archive.read(digest + ".json")
    if hashlib.sha256(blob).hexdigest() != digest:
        raise ValueError("Frozen snapshot checksum mismatch")
    view = json.loads(blob)
    current = view["current"]
    task = f"{current['series']}-g{current['n']}-{view['phase']}"
    expected_id = f"lol-competition-bench/{extra['harbor_release']}/{task}"
    if (
        row["id"] != expected_id
        or extra["id"] != expected_id
        or extra["harbor_task"] != task
    ):
        raise ValueError("Snapshot belongs to a different forecast")
    return blob


def inline_messages(blob, workspace_prompt=None):
    """Text-only protocol for policies without filesystem tools."""
    if workspace_prompt is not None:
        # Preserve the rendered task, including any demonstration and background.
        # The sole protocol change is how evidence arrives and the answer is returned.
        return [{"role": "user", "content": (
            "Text-only version of the following file-based forecast. The entire snapshot.json follows the task. "
            "Use it directly. Return the requested JSON as your final answer in place of writing prediction.json. "
            "The original shell calls, file paths and save-time advice describe the workspace interface.\n\n"
            + workspace_prompt + "\n\nFrozen snapshot.json\n" + blob.decode("utf-8")
        )}]
    return [
        {
            "role": "user",
            "content": (
                "Forecast this one professional League of Legends game at the observation in the frozen JSON below. "
                "The lobby is before the first ban or pick. At draft lock all current BP actions are known. "
                "Use the teams, sides, starters, patch, series format, and dated evidence in this snapshot. "
                "Consider player and champion history, sample size and the series draft rules. "
                "Missing records are unknown. General League knowledge is allowed. "
                "External search, remembered outcomes and evidence from later games are outside the forecast. "
                "Return exactly one JSON object containing p_blue_win (probability that blue wins) and "
                "p_blue_ahead_15 (probability that blue has strictly more gold at 15:00). "
                "Use finite numbers from 0 to 1. The reward is one minus the mean of the two squared errors.\n\n"
                + blob.decode("utf-8")
            ),
        }
    ]


def materialize(bundle, row, out):
    """Create a fresh directory to mount at /app, without surrounding trials or labels."""
    extra = row["extra_info"]
    if row["id"] != extra["id"] or extra["protocol"] != WORKSPACE:
        raise ValueError("Expected one identified workspace evaluation row")
    prompt = row["prompt"][0]["content"].encode()
    if hashlib.sha256(prompt).hexdigest() != extra["prompt_sha256"]:
        raise ValueError("Frozen task instruction checksum mismatch")
    blob = snapshot_bytes(bundle, row)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        raise FileExistsError(out)
    with tempfile.TemporaryDirectory(dir=out.parent) as tmp:
        workspace = Path(tmp) / "workspace"
        workspace.mkdir()
        (workspace / "instruction.md").write_bytes(prompt)
        (workspace / "snapshot.json").write_bytes(blob)
        workspace.rename(out)
    return out


def inline_evaluation_messages(bundle, row):
    """Apply exactly the same transport as the matching training export."""
    text = row["prompt"][0]["content"] if "task_spec" in row["extra_info"] else None
    return inline_messages(snapshot_bytes(bundle, row), text)


def compute_score(data_source, solution_str, ground_truth, extra_info=None, **kwargs):
    """verl custom reward. A broken label join is a dataset error; a bad prediction earns zero."""
    if data_source != DATA_SOURCE:
        raise ValueError(f"Unexpected reward data source: {data_source}")
    truth = json.loads(ground_truth, object_pairs_hook=unique_fields)
    if not extra_info or not truth.get("id") or truth["id"] != extra_info.get("id"):
        raise ValueError("Prediction and label task IDs must agree")
    labels = truth["labels"]
    if set(labels) != set(FIELDS) or any(
        type(v) is not int or v not in (0, 1) for v in labels.values()
    ):
        raise ValueError("Expected binary outcome labels for both forecast events")
    if not isinstance(solution_str, str) or len(solution_str.encode("utf-8")) > 4096:
        return 0.0
    try:
        prediction = json.loads(solution_str, object_pairs_hook=unique_fields)
    except (ValueError, RecursionError):
        return 0.0
    return score(prediction, labels)
