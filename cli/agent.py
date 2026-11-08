"""Harbor host adapter. Only the cut-off snapshot and task instruction cross into the CLI worker."""

import asyncio
import os
import signal
import sys
import tempfile
from pathlib import Path

from harbor.agents.base import BaseAgent
from cli.client import BIN


class CompetitionCLI(BaseAgent):
    @staticmethod
    def name():
        return "lol-competition-cli"

    def version(self):
        return "1"

    async def setup(self, environment):
        pass

    async def run(self, instruction, environment, context):
        name = os.environ["BENCH_CLI"]
        if name not in BIN:
            raise ValueError("Unsupported CLI")
        mode = os.environ["BENCH_MODE"]
        if mode not in ("live", "vendor", "fixture"):
            raise ValueError("Unsupported trial mode")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            await environment.download_file(
                "/app/snapshot.json", root / "snapshot.json"
            )
            (root / "instruction.md").write_text(instruction)
            proc = await asyncio.create_subprocess_exec(
                sys.executable,
                "-m",
                "cli.worker",
                name,
                os.environ["BENCH_MODEL"],
                mode,
                str(root / "snapshot.json"),
                str(root / "instruction.md"),
                str(root / "out"),
            )
            try:
                if await proc.wait():
                    raise RuntimeError(
                        f"{name} worker failed; do not count as a valid forecast"
                    )
            finally:
                if proc.returncode is None:
                    proc.send_signal(signal.SIGTERM)
                    await proc.wait()
            self.logs_dir.mkdir(parents=True, exist_ok=True)
            self.logs_dir.joinpath("cli-run.json").write_bytes(
                (root / "out/run.json").read_bytes()
            )
            await environment.upload_file(
                root / "out/prediction.json", "/app/prediction.json"
            )
