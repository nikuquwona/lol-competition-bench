import base64
import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from evaluation.model_context import model_context


class ModelContextTests(unittest.TestCase):
    def test_interleaved_calls_missing_response_and_clipped_input(self):
        def record(call_id, part, body, **extra):
            return dict(
                type=part,
                call_id=call_id,
                schema_version=1,
                captured_bytes=len(body),
                body_bytes=len(body),
                sha256=hashlib.sha256(body).hexdigest(),
                truncated=False,
                body_b64=base64.b64encode(body).decode(),
                **extra,
            )

        with TemporaryDirectory() as folder:
            path = Path(folder) / "model-context.jsonl"
            prompt = b'{"tools":[{"name":"shell"}],"input":[{"role":"user","content":"first"}]}'
            events = [
                record(1, "request", prompt, source="provider", route="/responses"),
                record(2, "request", b'{"input":', source="fixture"),
                record(2, "response", b"rate limited", status=429, state="http_error"),
                record(1, "response", b"data: hello\n\n", status=200, state="complete"),
                record(3, "request", b"{}", source="provider"),
            ]
            events[1].update(truncated=True, body_bytes=12345)
            path.write_text("".join(json.dumps(item) + "\n" for item in events))
            index = model_context(path)["calls"]
            self.assertEqual([c["id"] for c in index], [1, 2, 3])
            self.assertNotIn("request", index[0])
            self.assertEqual(index[2]["state"], "response_unrecorded")
            self.assertFalse(index[2]["complete"])
            first = model_context(path, 1)
            self.assertEqual(first["request"], json.loads(prompt))
            self.assertEqual(first["response"], "data: hello\n\n")
            second = model_context(path, 2)
            self.assertEqual(second["source"], "fixture")
            self.assertEqual(second["request_excerpt"], '{"input":')
            self.assertIsNone(second["request"])
            self.assertFalse(second["complete"])
            self.assertEqual(second["status"], 429)
            with self.assertRaises(KeyError):
                model_context(path, 4)
            events[0]["sha256"] = "0" * 64
            path.write_text("".join(json.dumps(item) + "\n" for item in events))
            with self.assertRaisesRegex(ValueError, "integrity"):
                model_context(path, 1)
