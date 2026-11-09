"""Private HTTP journal contracts; providers are mocked, native inference costs zero."""

import asyncio
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import http.client
import io
import json
from pathlib import Path
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from evaluation.cli.gateway import Handler
from evaluation.cli.wire import FILENAME, WireLog


def read_rows(path):
    return [json.loads(row) for row in path.read_bytes().splitlines()]


def decoded(row):
    raw = base64.b64decode(row["body_b64"], validate=True)
    assert len(raw) == row["captured_bytes"]
    if not row["truncated"]:
        assert len(raw) == row["body_bytes"]
        assert hashlib.sha256(raw).hexdigest() == row["sha256"]
    return raw


class Response:
    def __init__(
        self, chunks, status=200, mime="text/event-stream; charset=utf-8", expected=None
    ):
        self.chunks = iter(chunks)
        self.status = status
        self.headers = {"Content-Type": mime, "Set-Cookie": "provider-secret-cookie"}
        if expected is not None:
            self.headers["Content-Length"] = str(expected)

    def read1(self, n):
        chunk = next(self.chunks, b"")
        if isinstance(chunk, BaseException):
            raise chunk
        return chunk() if callable(chunk) else chunk

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class WireTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / FILENAME

    def handler(
        self,
        log,
        payload,
        *,
        router=False,
        fixture=False,
        route="/v1/responses",
        sink=None,
    ):
        handler = Handler.__new__(Handler)
        raw = json.dumps(payload, ensure_ascii=False).encode()
        handler.path = route
        handler.server = SimpleNamespace(
            model=payload["model"],
            wire=log,
            remaining=40,
            lock=threading.Lock(),
            fixture=fixture,
            openrouter_free=router,
        )
        handler.headers = {
            "Content-Length": str(len(raw)),
            "Authorization": "Bearer private-client-header",
        }
        handler.rfile = io.BytesIO(raw)
        handler.wfile = sink or io.BytesIO()
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        handler.send_error = MagicMock()
        return handler

    def test_openrouter_rewrite_and_byte_exact_sse_before_stream_ends(self):
        first = b'event: response.created\r\ndata: {"a":1}\r\n\r\n'
        last = 'data: {"answer":"晴"}\n\ndata: [DONE]\n\n'.encode()
        payload = {
            "model": "vendor/engine:free",
            "input": [{"role": "user", "content": "中文"}],
            "store": True,
            "stream": True,
            "client_metadata": {"not": "forwarded"},
        }
        with WireLog(self.path, secrets=("secret-gateway-key",)) as log:
            h = self.handler(log, payload, router=True)

            def next_chunk():
                self.assertEqual(h.wfile.getvalue(), first)
                self.assertEqual([r["type"] for r in read_rows(self.path)], ["request"])
                return last

            opener = MagicMock()
            opener.open.return_value = Response([first, next_chunk])
            with (
                patch(
                    "evaluation.cli.gateway.urllib.request.build_opener",
                    return_value=opener,
                ),
                patch.dict("os.environ", OPEN_ROUTER_API_KEY="secret-gateway-key"),
            ):
                h.do_POST()
        request, response = read_rows(self.path)
        upstream = opener.open.call_args.args[0]
        self.assertEqual(decoded(request), upstream.data)
        actual = json.loads(upstream.data)
        self.assertNotIn("client_metadata", actual)
        self.assertFalse(actual["store"])
        self.assertEqual(
            actual["provider"], {"max_price": {"prompt": 0, "completion": 0}}
        )
        self.assertEqual(request["route"], "/api/v1/responses")
        self.assertEqual(request["source"], "provider")
        self.assertEqual(decoded(response), h.wfile.getvalue())
        self.assertEqual(decoded(response), first + last)
        self.assertEqual(
            (response["status"], response["state"], response["content_type"]),
            (200, "complete", "text/event-stream"),
        )
        raw = self.path.read_bytes()
        for secret in (
            b"secret-gateway-key",
            b"private-client-header",
            b"provider-secret-cookie",
        ):
            self.assertNotIn(secret, raw)
            self.assertNotIn(secret, decoded(request) + decoded(response))
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)

    def test_deepseek_exact_post_body_and_native_http_error_body(self):
        raw = b'{  "error": {"message":"rate limited"} }\n'
        payload = {
            "model": "deepseek-v4-pro",
            "messages": [{"role": "user", "content": "Forecast."}],
        }
        with WireLog(self.path) as log:
            h = self.handler(log, payload, route="/v1/messages?beta=true")
            upstream = MagicMock()
            upstream.getresponse.return_value = Response([raw], 429, "application/json")
            with (
                patch(
                    "evaluation.cli.gateway.http.client.HTTPSConnection",
                    return_value=upstream,
                ),
                patch.dict("os.environ", DEEPSEEK_API_KEY="ignored-test-secret"),
            ):
                h.do_POST()
        request, response = read_rows(self.path)
        self.assertEqual(request["provider"], "deepseek")
        self.assertEqual(request["route"], "/anthropic/v1/messages")
        self.assertEqual(
            upstream.request.call_args.args[:3],
            ("POST", request["route"], decoded(request)),
        )
        self.assertEqual(request["call_id"], response["call_id"])
        self.assertEqual(
            (response["status"], response["state"], decoded(response)),
            (429, "http_error", raw),
        )

    def test_upstream_connect_failure_and_short_replies_are_distinct_from_client_disconnect(
        self,
    ):
        payload = {"model": "deepseek-v4-pro", "input": "x"}
        with (
            WireLog(self.path) as log,
            patch.dict("os.environ", DEEPSEEK_API_KEY="fake"),
        ):
            upstream = MagicMock()
            with patch(
                "evaluation.cli.gateway.http.client.HTTPSConnection",
                return_value=upstream,
            ):
                upstream.request.side_effect = TimeoutError()
                h = self.handler(log, payload)
                h.do_POST()
                h.send_error.assert_called_once()
                upstream.request.side_effect = None
                upstream.getresponse.return_value = Response([b"ab"], expected=4)
                self.handler(log, payload).do_POST()
                upstream.getresponse.return_value = Response(
                    [b"1", http.client.IncompleteRead(b"23", 2)]
                )
                self.handler(log, payload).do_POST()
                upstream.getresponse.return_value = Response([b"chunk"])
                sink = MagicMock()
                sink.write.side_effect = BrokenPipeError()
                self.handler(log, payload, sink=sink).do_POST()
        responses = [r for r in read_rows(self.path) if r["type"] == "response"]
        self.assertEqual(
            [(r["status"], r["state"], decoded(r)) for r in responses],
            [
                (None, "upstream_error", b""),
                (200, "upstream_error", b"ab"),
                (200, "upstream_error", b"123"),
                (200, "client_disconnected", b"chunk"),
            ],
        )

    def test_early_shutdown_and_capture_limits_preserve_contiguous_wire_prefix_and_total_hash(
        self,
    ):
        with WireLog(self.path, body_limit=4, trial_limit=8) as log:
            a = log.start("deepseek", "/responses", "m", b"123456")
            a.head(200, "text/event-stream")
            a.append(b"abcdefg")
            a.append(b"last")
            b = log.start("deepseek", "/responses", "m", b"later")
            b.head(200, "application/json")
            b.append(b"hello")
            b.finish()
        rows = read_rows(self.path)
        self.assertEqual(sum(r["captured_bytes"] for r in rows), 8)
        self.assertEqual(decoded(rows[0]), b"1234")
        self.assertEqual(decoded(rows[-1]), b"abcd")
        self.assertEqual(rows[-1]["state"], "interrupted")
        self.assertEqual(rows[-1]["sha256"], hashlib.sha256(b"abcdefglast").hexdigest())
        self.assertEqual([r["call_id"] for r in rows], [1, 2, 2, 1])

    def test_echoed_credentials_privately_withheld_even_across_chunks(self):
        with WireLog(self.path, secrets=("secret-test-key",)) as log:
            a = log.start(
                "openrouter", "/api/v1/responses", "m", b"echo secret-test-key"
            )
            a.head(401, "application/json")
            a.append(b'{"ref":"secr')
            a.append(b"et-test-")
            a.append(b'key"}')
            a.finish()
        for row in read_rows(self.path):
            self.assertEqual(decoded(row), b"")
            self.assertGreater(row["body_bytes"], 0)
            self.assertTrue(row["truncated"])
            self.assertEqual(row["withheld"], "credential_echo")

    def test_concurrent_requests_and_responses_are_never_cross_paired(self):
        with WireLog(self.path) as log:
            gate = threading.Barrier(6)

            def call(n):
                req = log.start("deepseek", "/responses", "m", str(n).encode())
                gate.wait()
                req.head(200, "application/json")
                req.append(str(100 + n).encode())
                req.finish()

            with ThreadPoolExecutor(max_workers=6) as pool:
                list(pool.map(call, range(6)))
        accepted = {}
        for r in read_rows(self.path):
            if r["type"] == "request":
                self.assertNotIn(r["call_id"], accepted)
                accepted[r["call_id"]] = int(decoded(r))
            else:
                self.assertEqual(int(decoded(r)), 100 + accepted[r["call_id"]])
        self.assertEqual(set(accepted), set(range(1, 7)))

    def test_fixture_is_labeled_and_real_shell_call_travels_through_matching_sse(self):
        with WireLog(self.path) as log:
            payload = {
                "model": "deepseek-v4-pro",
                "input": "forecast",
                "tools": [
                    {
                        "type": "function",
                        "name": "exec_command",
                        "parameters": {
                            "type": "object",
                            "properties": {"cmd": {"type": "string"}},
                        },
                    }
                ],
            }
            h = self.handler(log, payload, fixture=True)
            h.do_POST()
        req, res = read_rows(self.path)
        self.assertEqual(req["provider"], "fixture")
        self.assertEqual(req["source"], "fixture")
        self.assertEqual(json.loads(decoded(req)), payload)
        self.assertEqual(decoded(res), h.wfile.getvalue())
        self.assertIn(b"function_call", decoded(res))
        self.assertEqual(res["status"], 200)


class HarborWireTests(unittest.TestCase):
    def test_failed_worker_capture_remains_private_in_harbor_agent_directory(self):
        from evaluation.cli.agent import CompetitionCLI

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            agent = SimpleNamespace(logs_dir=root / "agent")
            environment = SimpleNamespace(
                download_file=AsyncMock(), upload_file=AsyncMock()
            )

            async def worker(*cmd):
                out = Path(cmd[-1])
                out.mkdir()
                with WireLog(out / FILENAME) as w:
                    c = w.start("fixture", "/v1/responses", "m", b"{}")
                    c.finish("interrupted")
                return SimpleNamespace(wait=AsyncMock(return_value=7), returncode=7)

            with (
                patch.dict(
                    "os.environ", BENCH_CLI="pi", BENCH_MODE="fixture", BENCH_MODEL="m"
                ),
                patch("asyncio.create_subprocess_exec", worker),
                self.assertRaises(RuntimeError),
            ):
                asyncio.run(CompetitionCLI.run(agent, "fixture", environment, None))
            capture = agent.logs_dir / FILENAME
            self.assertEqual(capture.stat().st_mode & 0o777, 0o600)
            self.assertEqual(read_rows(capture)[-1]["state"], "interrupted")
            environment.upload_file.assert_not_called()
