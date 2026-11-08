"""Run on a disposable Linux Docker host. No host home or workspace inside either container."""

import argparse
import json
import os
import re
import signal
import subprocess
import sys
from collections import deque
import threading
import uuid
from pathlib import Path
from evaluation.cli.client import BIN, CURSOR_HOSTS

HERE = Path(__file__).resolve().parent
READ_PREDICTION = """
import json, os, stat
fd=os.open('/app/prediction.json', os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
s=os.fstat(fd)
assert stat.S_ISREG(s.st_mode) and 0<s.st_size<=4096
def unique(pairs):
    out=dict(pairs)
    assert len(out)==len(pairs)
    return out
raw=os.read(fd,4097)
assert len(raw)<=4096
data=json.loads(raw,object_pairs_hook=unique)
assert isinstance(data,dict) and set(data)=={'p_blue_win','p_blue_ahead_15'}
assert all(type(p) in (int,float) and 0<=p<=1 for p in data.values())
print(json.dumps(data,allow_nan=False))
"""


def docker(*args, capture=False, timeout=300, check=True):
    return subprocess.run(
        ["docker", *args],
        check=check,
        timeout=timeout,
        text=True,
        stdout=subprocess.PIPE if capture else None,
    )


def run(name, model, mode, snapshot, instruction, out):
    if not re.fullmatch(r"[a-zA-Z0-9._-]{1,90}", model):
        raise ValueError("Use an explicit model ID")
    if name == "cursor" and mode == "fixture":
        raise ValueError("Cursor requires vendor service; use check or vendor mode")
    if mode == "vendor" and name != "cursor" or mode == "live" and name == "cursor":
        raise ValueError("Cursor vendor trials are a separate, unranked mode")
    secret = {"live": "DEEPSEEK_API_KEY", "vendor": "CURSOR_API_KEY"}.get(mode)
    if secret and not os.getenv(secret):
        raise ValueError(f"Missing dedicated runner secret {secret}")
    tag = "lolbench-" + uuid.uuid4().hex[:12]
    worker, gateway, volume = tag + "-cli", tag + "-gateway", tag + "-sock"
    shared = os.environ.get("BENCH_SUITE_IMAGE")
    if shared and not re.fullmatch(r"lolbench-suite-[0-9a-f]{12}:trial", shared):
        raise ValueError("Invalid operator-supplied suite image")
    image = shared or tag + ":trial"
    out.mkdir(parents=True, exist_ok=False)
    try:
        if not shared:
            docker(
                "build",
                "-q",
                "-t",
                image,
                "--build-arg",
                f"HARNESS={name}",
                str(HERE),
                timeout=600,
            )
        docker("volume", "create", volume)
        # Gateway has no host port; its sole client interface is the shared socket volume.
        common = [
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges",
            "--pids-limit",
            "192",
            "--memory",
            "2g",
            "--cpus",
            "2",
            "--log-driver",
            "local",
            "--log-opt",
            "max-size=2m",
            "--read-only",
            "--tmpfs",
            "/tmp:rw,size=128m",
        ]
        if name != "cursor" and mode != "check":
            params = (
                ["--network", "none"]
                if mode == "fixture"
                else ["-e", "DEEPSEEK_API_KEY"]
            )
            docker(
                "run",
                "-d",
                "--name",
                gateway,
                *common,
                *params,
                "-v",
                f"{volume}:/relay",
                "--mount",
                f"type=bind,src={HERE / 'gateway.py'},dst=/opt/gateway.py,readonly",
                "--mount",
                f"type=bind,src={HERE / 'fixture.py'},dst=/opt/fixture.py,readonly",
                "--user",
                "0:0",
                image,
                "python3",
                "-u",
                "/opt/gateway.py",
                model,
                mode,
            )
        opts = []
        if name == "cursor" and mode in ("vendor", "check"):
            # TLS terminates at Cursor. Each relay has a fixed destination selected by the operator.
            commands = []
            for i, host in enumerate(CURSOR_HOSTS):
                commands.append(
                    f"socat UNIX-LISTEN:/relay/cursor-{i},mode=0666,fork TCP:{host}:443 &"
                )
                opts += ["--add-host", f"{host}:127.0.0.{i + 2}"]
            docker(
                "run",
                "-d",
                "--name",
                gateway,
                *common,
                "--user",
                "0:0",
                "-v",
                f"{volume}:/relay",
                image,
                "sh",
                "-ec",
                "\n".join(commands) + "\nwait",
            )
            opts += ["--sysctl", "net.ipv4.ip_unprivileged_port_start=0"]
        docker(
            "run",
            "-d",
            "--name",
            worker,
            *common,
            *opts,
            "--network",
            "none",
            "--tmpfs",
            "/app:rw,uid=1000,gid=1000,size=64m",
            "--tmpfs",
            "/home/node:rw,uid=1000,gid=1000,size=192m",
            "--tmpfs",
            "/input:rw,uid=1000,gid=1000,size=1m",
            "-v",
            f"{volume}:/relay:ro",
            image,
            "sleep",
            "infinity",
        )
        for source, dest in (
            (snapshot, "/app/snapshot.json"),
            (instruction, "/input/instruction.md"),
        ):
            with source.open("rb") as content:
                subprocess.run(
                    [
                        "docker",
                        "exec",
                        "-i",
                        worker,
                        "sh",
                        "-ec",
                        'cat > "$1"',
                        "copy",
                        dest,
                    ],
                    stdin=content,
                    check=True,
                    timeout=20,
                )
        # The API credential for the four strict clients exists only on the gateway.
        cmd = [
            "docker",
            "exec",
            "-e",
            f"BENCH_TIMEOUT={100 if mode == 'fixture' else 540}",
        ]
        if mode == "vendor":
            cmd += ["-e", "CURSOR_API_KEY"]
        cmd += [worker, "python3", "/opt/bench/client.py", name, model]
        if mode == "check":
            cmd += ["--check"]
        # Never let untrusted CLI stdout fill the host disk.
        tail = deque(maxlen=3)
        with subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        ) as proc:

            def drain():
                while chunk := proc.stdout.read(4096):
                    tail.append(chunk)

            reader = threading.Thread(target=drain, daemon=True)
            reader.start()
            try:
                rc = proc.wait(timeout=570)
            finally:
                proc.kill()
                reader.join(timeout=2)
            if rc:
                if mode in ("fixture", "check"):
                    print(b"".join(tail)[-6400:].decode(errors="replace"), flush=True)
                    if name != "cursor":
                        docker("logs", "--tail", "12", gateway, check=False)
                raise RuntimeError(f"{name} exited with status {rc}")
        api_calls = None
        if mode in ("fixture", "live"):
            lines = docker("logs", gateway, capture=True).stdout.splitlines()
            events = [json.loads(line) for line in lines if line.startswith("{")]
            api_calls = sum(e.get("stage") == "accepted" for e in events)
            if (
                not api_calls
                or mode == "live"
                and not any(e.get("status") == 200 for e in events)
            ):
                raise RuntimeError(
                    "No successful model inference to attribute this prediction to"
                )
        version = docker(
            "exec", worker, BIN[name], "--version", capture=True
        ).stdout.strip()
        if mode != "check":
            pred = json.loads(
                docker(
                    "exec", worker, "python3", "-I", "-c", READ_PREDICTION, capture=True
                ).stdout
            )
            (out / "prediction.json").write_text(json.dumps(pred) + "\n")
        (out / "run.json").write_text(
            json.dumps(
                dict(
                    cli=name,
                    version=version,
                    requested_model=model,
                    accepted_requests=api_calls,
                    mode=mode,
                    comparison="controlled" if mode == "live" else mode,
                ),
                indent=2,
            )
            + "\n"
        )
    finally:
        for container in (worker, gateway):
            docker("rm", "-f", container, check=False, capture=True)
        docker("volume", "rm", volume, check=False, capture=True)
        if not shared:
            docker("image", "rm", image, check=False, capture=True)
        for kind, identifier in (
            ("container", worker),
            ("container", gateway),
            ("volume", volume),
            ("image", image),
        ):
            if shared and kind == "image":
                continue
            if (
                docker(
                    kind, "inspect", identifier, check=False, capture=True
                ).returncode
                == 0
            ):
                raise RuntimeError("Failed cleanup: " + identifier)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("name", choices=BIN)
    p.add_argument("model")
    p.add_argument("mode", choices=["check", "fixture", "live", "vendor"])
    p.add_argument("snapshot", type=Path)
    p.add_argument("instruction", type=Path)
    p.add_argument("out", type=Path)
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    run(**vars(p.parse_args()))
