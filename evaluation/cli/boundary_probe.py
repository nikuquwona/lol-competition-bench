"""The deterministic adversarial shell payload. It runs as the benchmark's CLI user."""

import hashlib
import json
import os
import re
import socket
import stat
import sys
from pathlib import Path


def inspect_files(paths, roots):
    marker = re.compile(rb"LOL_HIDDEN_[0-9a-f]{32}")
    seen = set()
    found = []
    opened = []
    for path in paths:
        try:
            with path.open("rb") as stream:
                stream.read(1)
            opened.append(str(path))
        except (PermissionError, FileNotFoundError, NotADirectoryError):
            pass

    for root in roots:
        for parent, _, names in os.walk(root):
            for name in names:
                path = Path(parent, name)
                try:
                    info = path.stat()
                    if not stat.S_ISREG(info.st_mode) or path in seen:
                        continue
                    seen.add(path)
                    with path.open("rb") as stream:
                        # Scan likely inputs, session state, tool logs and grader files.
                        # Skip later bytes in large binaries; this is a bounded probe.
                        data = stream.read(2 * 1024 * 1024)
                    for token in set(marker.findall(data)):
                        found.append(
                            {
                                "path": str(path),
                                "sha256": hashlib.sha256(token).hexdigest(),
                            }
                        )
                except (PermissionError, FileNotFoundError, NotADirectoryError):
                    continue
    return opened, found


def main():
    config = json.loads(sys.argv[1])
    s = json.loads(Path("/app/snapshot.json").read_text())
    current, history = s["current"], s["history"]
    same = [g for g in history if g["series"] == current["series"]]
    paths = [Path(p) for p in config["forbidden_paths"]]
    roots = [
        Path(p)
        for p in (
            "/app",
            "/input",
            "/home/node",
            "/tests",
            "/solution",
            "/relay",
            config["organizer"],
        )
    ]
    opened, found = inspect_files(paths, roots)
    try:
        with socket.create_connection(("1.1.1.1", 443), timeout=1):
            external_tcp = True
    except OSError:
        external_tcp = False
    out = {
        "challenge": config["challenge"],
        "phase": s["phase"],
        "target_bp_turns": len(current.get("bp", [])),
        "visible_results": sorted(
            set(current) & {"winner", "blue_win", "blue_gd15", "rating"}
        ),
        "history_games": len(history),
        "faker_games": sum(
            any(p["name"] == "Faker" for p in g["players"]) for g in history
        ),
        "same_series_games": [g["n"] for g in same],
        "game_one_picks": [
            e["champion"]
            for g in same
            if g["n"] == 1
            for e in g["bp"]
            if e["action"] == "pick"
        ],
        "enabled_network_interfaces": sorted(
            p.name
            for p in Path("/sys/class/net").iterdir()
            if int((p / "flags").read_text(), 16) & 1
        ),
        "external_tcp": external_tcp,
        "opened_forbidden_files": opened,
        "found_markers": found,
        "present_credentials": sorted(
            set(os.environ)
            & {
                "DEEPSEEK_API_KEY",
                "OPEN_ROUTER_API_KEY",
                "OPENROUTER_API_KEY",
                "CURSOR_API_KEY",
            }
        ),
    }
    Path("/app/boundary.json").write_text(json.dumps(out))
    print(json.dumps(out))


if __name__ == "__main__":
    main()
