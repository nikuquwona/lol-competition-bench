"""Build an immutable, deterministic Harbor release from archived and settled games."""

import argparse
import gzip
import json
import tarfile
import tempfile
from pathlib import Path

from production.build import ROOT, eligible, snapshot, write_task
from production.intake import digest, read, slug, trusted_case


def publish(out, version, intake=None):
    slug(version)
    out.mkdir(parents=True, exist_ok=True)
    destination = out / version
    if destination.exists():
        raise FileExistsError(destination)
    records = read(ROOT / "production/data/games.json")
    with tempfile.TemporaryDirectory(dir=out) as tmp:
        temp = Path(tmp)
        release = temp / "release"
        release.mkdir()
        directory = temp / "tasks"
        directory.mkdir()
        items = []

        def add(identifier, view, labels, existing=None):
            if any(row["id"] == identifier for row in items):
                raise ValueError(f"Duplicate task: {identifier}")
            task = directory / identifier
            write_task(task, view, labels)
            if existing:
                # Use the exact observed input and instructions, even if templates evolve.
                for rel in ("environment/snapshot.json", "instruction.md"):
                    (task / rel).write_bytes((existing / rel).read_bytes())
            items.append(
                dict(
                    id=identifier,
                    series=view["current"]["series"],
                    game=view["current"]["n"],
                    phase=view["phase"],
                    patch=view["current"]["patch"],
                    snapshot_sha256=digest(task / "environment/snapshot.json"),
                    prompt_sha256=digest(task / "instruction.md"),
                )
            )

        for g in records:
            if eligible(g):
                for phase in ("lobby", "draft-lock"):
                    add(
                        f"{g['series']}-g{g['n']}-{phase}",
                        snapshot(records, g, phase),
                        g,
                    )
        if intake is not None:
            if not intake.is_dir():
                raise ValueError(f"Unknown intake directory: {intake}")
            for path in sorted(intake.glob("*/result.json")):
                case = path.parent
                m = trusted_case(case)
                r = read(path)
                if r["snapshot_sha256"] != m["snapshot_sha256"]:
                    raise ValueError("Result digest mismatch")
                view = read(case / "task/environment/snapshot.json")
                add(
                    m["id"],
                    view,
                    dict(blue_win=r["winner"] == "blue", blue_gd15=r["blue_gd15"]),
                    case / "task",
                )
        archive = release / "tasks.tar.gz"
        with (
            archive.open("wb") as raw,
            gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as gz,
            tarfile.open(fileobj=gz, mode="w", format=tarfile.GNU_FORMAT) as tar,
        ):
            for path in sorted(directory.rglob("*")):
                if not path.is_file():
                    continue
                info = tar.gettarinfo(
                    str(path), arcname=path.relative_to(directory).as_posix()
                )
                info.uid = info.gid = info.mtime = 0
                info.uname = info.gname = ""
                info.mode = 0o755 if path.suffix == ".sh" else 0o644
                with path.open("rb") as content:
                    tar.addfile(info, content)
        manifest = dict(
            format=1,
            version=version,
            archive=archive.name,
            sha256=digest(archive),
            count=len(items),
            tasks=sorted(items, key=lambda x: x["id"]),
        )
        (release / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        release.rename(destination)
    return destination


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--version", required=True)
    p.add_argument("--out", type=Path, default=ROOT / "datasets")
    p.add_argument("--intake", type=Path)
    a = p.parse_args()
    print(publish(a.out, a.version, a.intake))
