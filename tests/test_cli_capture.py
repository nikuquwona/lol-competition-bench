import asyncio
import base64
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from evaluation.cli.worker import TRUNCATED, capture_stream, run_cli_process


class CaptureTest(unittest.TestCase):
    def test_failed_cli_preserves_events_and_redacts_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            key = "private/test-credential"
            script = (
                "import json,os,sys,base64; k=os.environ['CURSOR_API_KEY']; "
                "print(json.dumps({'type':'tool_call','text':k})); "
                "print(base64.b64encode(k.encode()).decode(),file=sys.stderr); sys.exit(7)"
            )
            with patch.dict("os.environ", CURSOR_API_KEY=key):
                code = run_cli_process(
                    [sys.executable, "-c", script], out, "CURSOR_API_KEY"
                )
            self.assertEqual(code, 7)
            self.assertEqual(
                json.loads((out / "cli-events.log").read_text())["text"], "[REDACTED]"
            )
            self.assertEqual((out / "stderr.txt").read_text(), "[REDACTED]\n")
            self.assertNotIn(
                base64.b64encode(key.encode()), (out / "stderr.txt").read_bytes()
            )

    def test_log_cap_drains_an_unbroken_line_and_keeps_valid_records(self):
        first = b'{"type":"turn.started"}\n'
        data = io.BytesIO(first + b"z" * 65537 + b"\nignored\n")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "capture"
            capture_stream(data, path, [], limit=160)
            self.assertEqual(path.read_bytes(), first + TRUNCATED)
            self.assertEqual(data.read(), b"")

    def test_harbor_preserves_failed_worker_logs(self):
        try:
            from evaluation.cli.agent import CompetitionCLI
        except ModuleNotFoundError as exc:
            if exc.name == "harbor":
                self.skipTest("Harbor extra is not installed")
            raise
        with tempfile.TemporaryDirectory() as tmp:
            agent = SimpleNamespace(logs_dir=Path(tmp) / "agent")
            environment = SimpleNamespace(
                download_file=AsyncMock(), upload_file=AsyncMock()
            )

            async def worker(*args):
                root = Path(args[-1])
                root.mkdir()
                (root / "cli-events.log").write_text('{"type":"error"}\n')
                (root / "stderr.txt").write_text("worker failed\n")
                return SimpleNamespace(wait=AsyncMock(return_value=7), returncode=7)

            with (
                patch.dict(
                    "os.environ",
                    BENCH_CLI="codex",
                    BENCH_MODE="fixture",
                    BENCH_MODEL="fake",
                ),
                patch("asyncio.create_subprocess_exec", worker),
                self.assertRaisesRegex(RuntimeError, "worker failed"),
            ):
                asyncio.run(CompetitionCLI.run(agent, "forecast", environment, None))
            self.assertEqual(
                json.loads((agent.logs_dir / "cli-events.log").read_text()),
                {"type": "error"},
            )
            self.assertEqual(
                (agent.logs_dir / "stderr.txt").read_text(), "worker failed\n"
            )
            environment.upload_file.assert_not_awaited()
