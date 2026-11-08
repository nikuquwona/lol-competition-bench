"""Stage a public copy of a completed macOS Claude shard, preserving the source run."""

import argparse
import hashlib
import json
import re
import tempfile
from pathlib import Path

from evaluation.assemble import JOB_FILES

IDENTIFIER = re.compile(rb'"(session_id|sessionId|signature)"\s*:\s*"([^"\\]+)"')
TEMP = re.compile(
    rb"(?:/private/tmp/|/tmp/|-private-tmp-|-tmp-)lol-claude-[a-zA-Z0-9_]{5,16}"
)
SECRET = re.compile(
    rb"(?i)\b(?:sk-(?:or-v1-)?[a-z0-9_-]{18,}|bearer\s+[a-z0-9_.-]{16,})"
)


def strip_private(data, ids):
    for value, replacement in ids.items():
        data = data.replace(value, replacement)
    data = TEMP.sub(b"[ephemeral]", data)
    if b"/Users/" in data or SECRET.search(data):
        raise ValueError(
            "Staging refused: inspect remaining home paths or credentials locally"
        )
    return data


def stage(source, destination):
    if destination.exists():
        raise FileExistsError(destination)
    doc = json.loads((source / "report.json").read_bytes())
    if (doc.get("harness"), doc.get("backend")) != ("claude", "macos") or not doc.get(
        "summary"
    ):
        raise ValueError("Expected a terminal native macOS Claude run")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as tmp:
        staged = Path(tmp) / "staged"
        staged.mkdir()
        files = [Path("report.json")]
        for task in doc["planned"]:
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]+", task):
                raise ValueError("Invalid task identifier")
            job = Path("jobs") / task
            files.extend(
                job / name for name in JOB_FILES if (source / job / name).exists()
            )
        ids = {}
        receipts = {}
        for file in files:
            src = source / file
            if src.is_symlink() or not src.resolve().is_relative_to(source.resolve()):
                raise ValueError("Unsafe run artifact path")
            if src.name == "trajectory.jsonl":
                for k, v in IDENTIFIER.findall(src.read_bytes()):
                    if v not in ids:
                        group = b"signature" if k == b"signature" else b"session"
                        ids[v] = (
                            b"[redacted-"
                            + group
                            + b"-"
                            + str(len(ids) + 1).encode()
                            + b"]"
                        )
        for file in files:
            raw = (source / file).read_bytes()
            clean = strip_private(raw, ids)
            if file.suffix in (".json", ".jsonl"):
                if file.suffix == ".json":
                    json.loads(clean)
                else:
                    for line in clean.splitlines():
                        json.loads(line)
            tgt = staged / file
            tgt.parent.mkdir(parents=True, exist_ok=True)
            tgt.write_bytes(clean)
            receipts[file.as_posix()] = {
                "original_sha256": hashlib.sha256(raw).hexdigest(),
                "public_sha256": hashlib.sha256(clean).hexdigest(),
            }
        (staged / "redactions.json").write_text(json.dumps(receipts, indent=2) + "\n")
        staged.rename(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    stage(args.run, args.out)


if __name__ == "__main__":
    main()
