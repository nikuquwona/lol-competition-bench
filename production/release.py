"""Build an immutable, deterministic Harbor release from archived and settled games."""

import argparse
import gzip
import json
import tarfile
import tempfile
from collections import Counter
from pathlib import Path

from production.build import ROOT, eligible, snapshot, write_task
from production.coverage import history_card
from production.evidence import add_pack_option, load_packs
from production.store import digest, read, settled_cases
from production.schema import slug
from production.specs import DEFAULT, load_spec


def publish(out, version, intake=None, *, task_spec=DEFAULT, evidence_packs=()):
    slug(version)
    spec = load_spec(task_spec)
    if task_spec != DEFAULT and version in ("replay-v2", "replay-v3"):
        raise ValueError("Choose a new release version for an experimental task specification")
    if evidence_packs and version in ("replay-v2", "replay-v3"):
        raise ValueError("Publish an evidence treatment under a new release version")
    pack_meta = [p.metadata() for p in evidence_packs]
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
        cards = {}

        def add(identifier, view, labels, existing=None):
            if any(row["id"] == identifier for row in items):
                raise ValueError(f"Duplicate task: {identifier}")
            task = directory / identifier
            write_task(task, view, labels, spec=spec)
            if existing:
                # Use the exact observed input and instructions, even if templates evolve.
                for rel in ("environment/snapshot.json", "instruction.md"):
                    (task / rel).write_bytes((existing / rel).read_bytes())
            # Older frozen tasks retain their original prompt and snapshot bytes.
            # Their release card can still be computed from that exact evidence.
            card = history_card(view["current"], view["history"])
            cards[identifier] = card
            items.append(
                dict(
                    id=identifier,
                    series=view["current"]["series"],
                    game=view["current"]["n"],
                    phase=view["phase"],
                    patch=view["current"]["patch"],
                    coverage_group=card["coverage_group"],
                    snapshot_sha256=digest(task / "environment/snapshot.json"),
                    prompt_sha256=digest(task / "instruction.md"),
                )
            )

        for g in records:
            if eligible(g):
                for phase in ("lobby", "draft-lock"):
                    add(
                        f"{g['series']}-g{g['n']}-{phase}",
                        snapshot(records, g, phase, evidence_packs=evidence_packs),
                        g,
                    )
        if intake is not None:
            if not intake.is_dir():
                raise ValueError(f"Unknown intake directory: {intake}")
            for case, m, r in settled_cases(intake):
                if m.get("evidence_packs", []) != pack_meta:
                    raise ValueError(
                        f"Frozen task uses different evidence packs: {case.name}"
                    )
                frozen_spec = m.get("task_spec")
                if (frozen_spec is None and task_spec != DEFAULT) or (
                    frozen_spec is not None and frozen_spec != spec.metadata
                ):
                    raise ValueError(
                        f"Frozen task uses a different specification: {case.name}"
                    )
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
        by_phase = {}
        for phase in sorted({row["phase"] for row in items}):
            phase_rows = [row for row in items if row["phase"] == phase]
            by_phase[phase] = dict(
                games=len(phase_rows),
                coverage_groups=dict(
                    Counter(row["coverage_group"] for row in phase_rows)
                ),
                games_with_no_history=sum(
                    cards[row["id"]]["history_games"] == 0 for row in phase_rows
                ),
            )
        coverage_path = release / "coverage.json"
        coverage_path.write_text(
            json.dumps(
                dict(
                    version=version,
                    unique_games=len({(row["series"], row["game"]) for row in items}),
                    by_phase=by_phase,
                    by_task=dict(sorted(cards.items())),
                ),
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )
        manifest = dict(
            format=1,
            version=version,
            archive=archive.name,
            sha256=digest(archive),
            coverage_sha256=digest(coverage_path),
            count=len(items),
            tasks=sorted(items, key=lambda x: x["id"]),
        )
        if version != "replay-v3" or task_spec != DEFAULT:
            manifest.update(
                task_spec=spec.metadata,
                protocol_sha256=spec.metadata["protocol_sha256"],
            )
        if evidence_packs:
            manifest["evidence_packs"] = pack_meta
            sources = release / "evidence-packs"
            sources.mkdir()
            for pack in evidence_packs:
                (sources / (pack.sha256 + ".json")).write_text(
                    json.dumps(pack.document, ensure_ascii=False, indent=2) + "\n"
                )
        (release / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        release.rename(destination)
    return destination


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--version", required=True)
    p.add_argument("--out", type=Path, default=ROOT / "datasets")
    p.add_argument("--intake", type=Path)
    p.add_argument("--task-spec", default=DEFAULT)
    add_pack_option(p)
    a = p.parse_args()
    print(
        publish(
            a.out,
            a.version,
            a.intake,
            task_spec=a.task_spec,
            evidence_packs=load_packs(a.evidence_pack),
        )
    )
