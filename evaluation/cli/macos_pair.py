"""Run the Codex pair with an isolated macOS Seatbelt profile and a host-side inference relay."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import http.server
import json
import os
from pathlib import Path
import secrets
import shutil
import signal
import subprocess
import tempfile
import threading

from evaluation.cli.gateway import Handler, MAX_CALLS

ROOT = Path(__file__).resolve().parents[2]
TASKS = ROOT / "datasets/examples/replay-v1-kc-t1-g2"
MODEL = "deepseek-v4-pro"
PREFIX = "worlds-2026-main-event-quarterfinals-4-g2-"
PROFILE = """
(version 1)
(deny default)
(import "system.sb")
(allow process-exec* process-fork sysctl-read)
(allow signal process-info* (target same-sandbox))
(allow file-read-metadata)
(allow mach-lookup (global-name "com.apple.system.opendirectoryd.libinfo"))
(allow file-read* file-map-executable
  (subpath "/bin") (subpath "/usr/bin") (subpath "/usr/lib") (subpath "/System")
  (subpath "/Library/Developer/CommandLineTools") (subpath (param "RUN")))
(allow file-write* (subpath (param "RUN")) (literal "/dev/null"))
(allow file-read* file-ioctl (subpath "/dev/fd") (literal "/dev/null") (literal "/dev/urandom"))
(allow pseudo-tty)
(allow file-read* file-write* file-ioctl (literal "/dev/ptmx"))
(allow file-read* file-write* file-ioctl (require-all (regex #"^/dev/ttys[0-9]+") (extension "com.apple.sandbox.pty")))
(allow network-outbound (remote ip "localhost:PORT"))
"""
PROBE = """
import os, socket, sys, json
from pathlib import Path
def denied(path):
    try:
        with open(path,'rb') as f: f.read(1)
    except PermissionError: return True
    return False
def blocked(endpoint):
    with socket.socket() as s:
        s.settimeout(2)
        try: s.connect(endpoint)
        except PermissionError: return True
        return False
assert 'DEEPSEEK_API_KEY' not in os.environ
assert Path('snapshot.json').is_file()
assert denied(sys.argv[1]) and denied(sys.argv[2])
assert blocked(('1.1.1.1',443)) and blocked(('127.0.0.1',int(sys.argv[3])))
print('snapshot accessible; labels, personal shell config, public IP and second loopback listener denied')
"""


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def run(
    phase, out, binary, check_only, budget_prompt, *, task=None, model=MODEL, fixture=False
):
    out.mkdir(parents=True, exist_ok=False)
    task = task or TASKS / (PREFIX + phase)
    token = secrets.token_hex(24)
    audit = []

    class Relay(Handler):
        def do_POST(self):
            if self.headers.get("Authorization") != "Bearer " + token:
                return self.send_error(403)
            super().do_POST()

        def send_response(self, code, message=None):
            audit.append({"path": self.path, "status": code, "detail": message})
            return super().send_response(code, message)

    with (
        tempfile.TemporaryDirectory(prefix="lol-codex-", dir="/private/tmp") as temp,
        http.server.ThreadingHTTPServer(("127.0.0.1", 0), Relay) as srv,
    ):
        root = Path(temp)
        srv.fixture = fixture
        srv.remaining = MAX_CALLS
        srv.lock = threading.Lock()
        srv.model = model
        port = srv.server_port
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        for folder in ("app", "home", "tmp", "codex-home", "bin"):
            (root / folder).mkdir()
        exe = root / "bin/codex"
        shutil.copy2(binary, exe)
        work = root / "app"
        src = task / "environment/snapshot.json"
        shutil.copyfile(src, work / "snapshot.json")
        profile = root / "sandbox.sb"
        profile.write_text(PROFILE.replace("PORT", str(port)))
        env = {
            "PATH": "/Library/Developer/CommandLineTools/usr/bin:/usr/bin:/bin",
            "HOME": str(root / "home"),
            "CODEX_HOME": str(root / "codex-home"),
            "TMPDIR": str(root / "tmp"),
            "SHELL": "/bin/bash",
            "LANG": "en_US.UTF-8",
            "BENCH_DUMMY_KEY": token,
            "ZDOTDIR": str(root / "home"),
        }
        seat = ["/usr/bin/sandbox-exec", "-D", f"RUN={root}", "-f", str(profile)]
        with http.server.HTTPServer(
            ("127.0.0.1", 0), http.server.BaseHTTPRequestHandler
        ) as decoy:
            probe = subprocess.run(
                [
                    *seat,
                    "/Library/Developer/CommandLineTools/usr/bin/python3",
                    "-I",
                    "-c",
                    PROBE,
                    str(task / "tests/labels.json"),
                    str(Path.home() / ".zshrc"),
                    str(decoy.server_port),
                ],
                cwd=work,
                env=env,
                capture_output=True,
                text=True,
                timeout=20,
            )
        if probe.returncode:
            raise RuntimeError("Boundary test failed: " + probe.stderr[-700:])
        version = subprocess.check_output(
            [*seat, str(exe), "--version"], cwd=work, env=env, text=True, timeout=20
        ).strip()
        if version != "codex-cli 0.167.0":
            raise ValueError("Unexpected CLI version " + version)
        if check_only:
            print(version, probe.stdout.strip(), flush=True)
            srv.shutdown()
            return
        prompt = (task / "instruction.md").read_text().replace("/app/", "./")
        (root / "home/.zshenv").write_text('export TMPPREFIX="$TMPDIR/zsh"\n')
        if budget_prompt:
            prompt += (
                "\nBudget: make at most six shell calls. Use the first calls to inspect this snapshot "
                "and query the starters and past games. Write a valid prediction.json by the fourth "
                "shell call. You may revise it using the remaining calls. Then end the session. "
                "Only use Python standard library or shell tools.\n"
            )
        (out / "instruction.md").write_text(prompt)
        args = [
            str(exe),
            "exec",
            "--json",
            "--skip-git-repo-check",
            "--ephemeral",
            "--dangerously-bypass-approvals-and-sandbox",
            "-m",
            model,
            "-c",
            'web_search="disabled"',
            "-c",
            'model_provider="bench"',
            "-c",
            'model_providers.bench.name="bench"',
            "-c",
            f'model_providers.bench.base_url="http://127.0.0.1:{port}/v1"',
            "-c",
            'model_providers.bench.wire_api="responses"',
            "-c",
            'model_providers.bench.env_key="BENCH_DUMMY_KEY"',
            prompt,
        ]
        try:
            with (
                (out / "trajectory.jsonl").open("w") as trace,
                (out / "stderr.txt").open("w") as err,
            ):
                with subprocess.Popen(
                    [*seat, *args],
                    cwd=work,
                    env=env,
                    stdin=subprocess.DEVNULL,
                    stdout=trace,
                    stderr=err,
                    start_new_session=True,
                ) as child:
                    try:
                        rc = child.wait(timeout=600)
                    finally:
                        try:
                            os.killpg(child.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
            if rc or not any(r["status"] == 200 for r in audit):
                raise RuntimeError(
                    f"{phase}: CLI exit {rc}, HTTP statuses {[r['status'] for r in audit]}"
                )
            from production.score import read_prediction

            prediction = read_prediction(work / "prediction.json")
            if set(prediction) != {"p_blue_win", "p_blue_ahead_15"} or not all(
                type(x) in (int, float) and 0 <= x <= 1 for x in prediction.values()
            ):
                raise ValueError("Invalid CLI submission")
            save(out / "prediction.json", prediction)
        finally:
            srv.shutdown()
            save(
                out / "run.json",
                dict(
                    cli=version,
                    mode="fixture" if fixture else "live",
                    model=model,
                    phase=phase,
                    snapshot_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
                    boundary_probe=probe.stdout.strip(),
                    upstream=audit,
                ),
            )
            for log in ("trajectory.jsonl", "stderr.txt"):
                path = out / log
                if path.exists():
                    raw = (
                        path.read_bytes()
                        .replace(token.encode(), b"[relay-token]")
                        .replace(str(root).encode(), b"[ephemeral]")
                    )
                    path.write_bytes(raw)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--budget-prompt", action="store_true")
    opts = parser.parse_args()
    binary = Path(shutil.which("codex")).resolve()
    if not opts.check_only and not os.environ.get("DEEPSEEK_API_KEY"):
        parser.error("Missing local DeepSeek credential")
    phases = ["lobby"] if opts.check_only else ["lobby", "draft-lock"]
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [
            pool.submit(
                run, p, opts.out / p, binary, opts.check_only, opts.budget_prompt
            )
            for p in phases
        ]
        for f in futures:
            f.result()
