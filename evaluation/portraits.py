"""Build the offline draft portrait library from matching Riot Data Dragon releases."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile
import time
import urllib.error
import urllib.request

from production.build import ROOT
from production.store import digest, read

CDN = "https://ddragon.leagueoflegends.com/cdn"
VERSIONS = {"26.17": "16.17.1", "26.20": "16.20.1"}
DEST = Path(__file__).with_name("site_assets") / "champions"


def normalized(name):
    return re.sub(r"[^a-z0-9]", "", name.casefold())


def selected_champions(release):
    meta = read(release / "manifest.json")
    archive = release / "tasks.tar.gz"
    if digest(archive) != meta["sha256"]:
        raise ValueError("Release digest mismatch")
    targets = {r["id"]: r for r in meta["tasks"] if r["phase"] == "draft-lock"}
    names = {}
    with tarfile.open(archive, "r:gz") as tar:
        for member in tar:
            task, _, suffix = member.name.partition("/")
            if task not in targets or suffix != "environment/snapshot.json":
                continue
            row = targets.pop(task)
            with tar.extractfile(member) as stream:
                raw = stream.read()
            if hashlib.sha256(raw).hexdigest() != row["snapshot_sha256"]:
                raise ValueError("Snapshot digest mismatch")
            view = json.loads(raw)
            if view["phase"] != "draft-lock":
                raise ValueError("Unexpected snapshot phase")
            current = view["current"]
            names.setdefault(current["patch"], set()).update(
                a["champion"] for a in current["bp"]
            )
    if targets:
        raise ValueError("Incomplete release")
    return names


def sync(release, cache, dest):
    if not shutil.which("cwebp"):
        raise ValueError("Regenerating portraits requires cwebp")
    cache.mkdir(parents=True, exist_ok=True)
    dest.mkdir(parents=True, exist_ok=True)

    def fetch(url):
        path = cache / hashlib.sha256(url.encode()).hexdigest()
        if path.exists():
            return path.read_bytes()
        for attempt in range(3):
            try:
                with urllib.request.urlopen(url, timeout=35) as response:
                    data = response.read()
                path.write_bytes(data)
                return data
            except (TimeoutError, urllib.error.URLError):
                if attempt == 2:
                    raise
                time.sleep(attempt + 1)

    def portrait(item):
        patch, filename, detail, names = item
        url = f"{CDN}/{VERSIONS[patch]}/img/champion/{filename}"
        png = fetch(url)
        if png[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"Unexpected asset at {url}")
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "portrait.png"
            src.write_bytes(png)
            out = Path(tmp) / "portrait.webp"
            subprocess.run(
                [
                    "cwebp",
                    "-quiet",
                    "-resize",
                    "96",
                    "96",
                    "-q",
                    "83",
                    "-m",
                    "5",
                    "-metadata",
                    "none",
                    str(src),
                    "-o",
                    str(out),
                ],
                check=True,
            )
            webp = out.read_bytes()
        hexdigest = hashlib.sha256(webp).hexdigest()
        icon = f"{detail['id'].lower()}-{hexdigest[:12]}.webp"
        (dest / icon).write_bytes(webp)
        return (
            patch,
            detail["id"],
            {
                "name": detail["name"],
                "zh": detail["zh"],
                "aliases": sorted(names),
                "file": icon,
                "source_png": filename,
                "source_sha256": hashlib.sha256(png).hexdigest(),
                "sha256": hexdigest,
            },
        )

    patches = {}
    required = []
    for patch, names in sorted(selected_champions(release).items()):
        if patch not in VERSIONS:
            raise ValueError(
                f"Map game patch {patch} to a matching Data Dragon release first"
            )
        v = VERSIONS[patch]
        catalogs = {
            loc: json.loads(fetch(f"{CDN}/{v}/data/{loc}/champion.json"))
            for loc in ("en_US", "zh_CN")
        }
        if any(c["version"] != v for c in catalogs.values()):
            raise ValueError("Data Dragon catalog version mismatch")
        catalog = catalogs["en_US"]["data"]
        by_name = {
            normalized(alias): cid
            for cid, row in catalog.items()
            for alias in (row["id"], row["name"])
        }
        by_id = {}
        missing = []
        for name in sorted(names):
            if cid := by_name.get(normalized(name)):
                by_id.setdefault(cid, set()).add(name)
            else:
                missing.append(name)
        patches[patch] = {
            "data_dragon": v,
            "catalogs": {
                loc: f"{CDN}/{v}/data/{loc}/champion.json" for loc in catalogs
            },
            "source_template": f"{CDN}/{v}/img/champion/{{source_png}}",
            "missing": missing,
            "champions": {},
        }
        for cid, aliases in sorted(by_id.items()):
            row = catalog[cid]
            if (
                not re.fullmatch(r"[A-Za-z0-9]+", cid)
                or row["image"]["full"] != cid + ".png"
            ):
                raise ValueError(f"Unexpected Data Dragon asset ID: {cid!r}")
            zh = catalogs["zh_CN"]["data"][cid]
            required.append(
                (
                    patch,
                    row["image"]["full"],
                    dict(id=cid, name=row["name"], zh=zh["title"]),
                    aliases,
                )
            )
    with ThreadPoolExecutor(max_workers=8) as pool:
        for patch, cid, record in pool.map(portrait, required):
            patches[patch]["champions"][cid] = record
    doc = {
        "source": "Riot Games Data Dragon",
        "docs": "https://developer.riotgames.com/docs/lol#data-dragon",
        "processing": "cwebp -resize 96 96 -q 83 -m 5 -metadata none",
        "patches": patches,
    }
    (dest / "sources.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
    )
    return doc


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=ROOT / "datasets/replay-v3")
    parser.add_argument("--cache", type=Path, default=ROOT / ".work/riot-ddragon")
    p = parser.parse_args()
    doc = sync(p.release, p.cache, DEST)
    for patch, data in doc["patches"].items():
        print(
            patch,
            len(data["champions"]),
            "portraits; name-only:",
            data["missing"],
            flush=True,
        )
