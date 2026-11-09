"""Run on a disposable Linux Docker host. No host home or workspace inside either container."""

import argparse
import base64
import json
import os
import re
import signal
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
import uuid
from pathlib import Path
from urllib.parse import quote
from evaluation.cli.client import BIN, CURSOR_HOSTS
from evaluation.cli.gateway import credential_name, free_model
from evaluation.cli.wire import FILENAME, create_private_file

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
        # Absence is the expected result of the final per-resource cleanup check.
        stderr=subprocess.PIPE if capture and not check else None,
    )


TRACE_LIMIT = 8 * 1024 * 1024
TRUNCATED = b'{"type":"trace.truncated","reason":"native log size limit reached"}\n'


def capture_stream(stream, path, redactions, limit=TRACE_LIMIT):
    """Persist whole native records, with bounded storage even for an unbroken line."""
    with path.open("xb") as log:
        while record := stream.readline(limit + 1):
            if len(record) <= limit:
                for secret in redactions:
                    record = record.replace(secret, b"[REDACTED]")
                if log.tell() + len(record) + len(TRUNCATED) <= limit:
                    log.write(record)
                    log.flush()
                    continue
            log.write(TRUNCATED)
            break
    # Keep the child moving after overflow, without allocating in proportion to its output.
    while stream.read(65536):
        pass


def run_cli_process(cmd, out, secret, timeout=570):
    redactions = set()
    if secret and (key := os.environ.get(secret)):
        raw = key.encode()
        redactions.update(
            (
                raw,
                json.dumps(key)[1:-1].encode(),
                quote(key, safe="").encode(),
                base64.b64encode(raw),
                base64.urlsafe_b64encode(raw),
            )
        )
    tokens = sorted(redactions, key=len, reverse=True)
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        with ThreadPoolExecutor(max_workers=2) as readers:
            stdout = readers.submit(
                capture_stream, proc.stdout, out / "cli-events.log", tokens
            )
            stderr = readers.submit(
                capture_stream, proc.stderr, out / "stderr.txt", tokens
            )
            try:
                return proc.wait(timeout=timeout)
            finally:
                if proc.poll() is None:
                    proc.kill()
                stdout.result()
                stderr.result()


def run(name, model, mode, snapshot, instruction, out, *, boundary_command=None):
    if boundary_command and mode not in ("fixture", "check"):
        raise ValueError("Boundary probes require a credential-free trial")
    if mode == "openrouter-free":
        if not free_model(model) or name == "cursor":
            raise ValueError("A pinned :free model and controlled harness are required")
    elif not re.fullmatch(r"[a-zA-Z0-9._-]{1,90}", model):
        raise ValueError("Use an explicit model ID")
    if name == "cursor" and mode == "fixture":
        raise ValueError("Cursor requires vendor service; use check or vendor mode")
    if mode == "vendor" and name != "cursor" or mode == "live" and name == "cursor":
        raise ValueError("Cursor vendor trials are a separate, unranked mode")
    secret = credential_name(mode)
    if secret and not os.getenv(secret):
        raise ValueError(f"Missing dedicated runner secret {secret}")
    tag = "lolbench-" + uuid.uuid4().hex[:12]
    worker, gateway, volume = tag + "-cli", tag + "-gateway", tag + "-sock"
    shared = os.environ.get("BENCH_SUITE_IMAGE")
    if shared and not re.fullmatch(r"lolbench-suite-[0-9a-f]{12}:trial", shared):
        raise ValueError("Invalid operator-supplied suite image")
    image = shared or tag + ":trial"
    out.mkdir(parents=True, exist_ok=False)
    controlled_gateway = name != "cursor" and mode != "check"
    wire_started = False
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
        if controlled_gateway:
            # Publish only a single organizer-owned output file to the trusted relay.
            # The worker gets the socket volume and never mounts this artifact or its directory.
            wire_path = (out / FILENAME).resolve()
            create_private_file(wire_path)
            params = ["--network", "none"] if mode == "fixture" else ["-e", secret]
            if boundary_command:
                params.extend(["-e", "BENCH_FIXTURE_COMMAND=" + boundary_command])
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
                "--mount",
                f"type=bind,src={HERE / 'wire.py'},dst=/opt/wire.py,readonly",
                "--mount",
                f"type=bind,src={wire_path},dst=/opt/{FILENAME}",
                "--user",
                "0:0",
                image,
                "python3",
                "-u",
                "/opt/gateway.py",
                model,
                mode,
            )
            wire_started = True
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
        if controlled_gateway:
            docker(
                "exec",
                worker,
                "sh",
                "-ec",
                'test ! -e "/opt/model-context.jsonl" && test ! -e "/relay/model-context.jsonl"',
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
        if boundary_command and mode == "check":
            # Cursor has a vendor-only control plane. Exercise the worker explicitly,
            # keeping this observation separate from a CLI-originated shell call.
            docker("exec", worker, "sh", "-ec", boundary_command, timeout=30)
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
        rc = run_cli_process(cmd, out, secret)
        if rc:
            if mode in ("fixture", "check"):
                with (out / "stderr.txt").open("rb") as diagnostics:
                    length = diagnostics.seek(0, os.SEEK_END)
                    diagnostics.seek(max(0, length - 6400))
                    print(diagnostics.read().decode(errors="replace"), flush=True)
                if name != "cursor":
                    docker("logs", "--tail", "12", gateway, check=False)
            raise RuntimeError(f"{name} exited with status {rc}")
        api_calls = None
        if mode in ("fixture", "live", "openrouter-free"):
            lines = docker("logs", gateway, capture=True).stdout.splitlines()
            events = [json.loads(line) for line in lines if line.startswith("{")]
            api_calls = sum(e.get("stage") == "accepted" for e in events)
            if (
                not api_calls
                or mode in ("live", "openrouter-free")
                and not any(e.get("status") == 200 for e in events)
            ):
                raise RuntimeError(
                    "No successful model inference to attribute this prediction to"
                )
        version = docker(
            "exec", worker, BIN[name], "--version", capture=True
        ).stdout.strip()
        if boundary_command:
            reader = """
import json, os, stat
fd = os.open('/app/boundary.json', os.O_NOFOLLOW | os.O_RDONLY | os.O_NONBLOCK)
assert stat.S_ISREG(os.fstat(fd).st_mode)
raw = os.read(fd, 16385)
assert len(raw) <= 16384
print(json.dumps(json.loads(raw)))
"""
            result = docker("exec", worker, "python3", "-I", "-c", reader, capture=True)
            (out / "boundary.json").write_text(result.stdout)
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
        docker("rm", "-f", worker, check=False, capture=True)
        if wire_started:
            # SIGTERM finalizes partially streamed calls before reclaiming the relay.
            try:
                docker(
                    "stop", "-t", "4", gateway, check=False, capture=True, timeout=15
                )
            except subprocess.TimeoutExpired:
                pass  # Force-remove the container below even if graceful shutdown stalls.
        docker("rm", "-f", gateway, check=False, capture=True)
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
    p.add_argument(
        "mode", choices=["check", "fixture", "live", "openrouter-free", "vendor"]
    )
    p.add_argument("snapshot", type=Path)
    p.add_argument("instruction", type=Path)
    p.add_argument("out", type=Path)
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    run(**vars(p.parse_args()))
