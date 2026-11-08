import json
import tempfile
import unittest
from pathlib import Path

from evaluation.traces import render_events


class NativeEventTests(unittest.TestCase):
    def render(self, events):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "events"
            f.write_text("".join(json.dumps(e) + "\n" for e in events))
            return render_events(f)

    def test_pi_deduplication_and_failure(self):
        result = {
            "content": [{"type": "text", "text": "missing file"}],
            "structuredContent": {"exit_code": 2},
        }
        sections, counts, _ = self.render(
            [
                {
                    "type": "tool_execution_start",
                    "toolCallId": "id",
                    "toolName": "bash",
                    "args": {"command": "cat missing"},
                },
                {
                    "type": "tool_execution_end",
                    "toolCallId": "id",
                    "result": result,
                    "isError": True,
                },
                {"type": "turn_end", "toolResults": [result]},
            ]
        )
        self.assertEqual(
            sections,
            [("终端命令", "cat missing"), ("命令结果 · 退出码 2", "missing file")],
        )
        self.assertEqual(counts["failed_commands"], 1)

    def test_kimi_unfinished_and_unreported_usage(self):
        sections, counts, usage = self.render(
            [
                {
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": "c",
                            "function": {
                                "name": "Bash",
                                "arguments": '{"command":"pwd"}',
                            },
                        }
                    ],
                }
            ]
        )
        self.assertEqual(counts["unfinished_commands"], 1)
        self.assertEqual(sections, [("终端命令", "pwd")])
        self.assertEqual(usage, {})

    def test_cursor_documented_events(self):
        params = {"path": "notes.md"}
        sections, counts, _ = self.render(
            [
                {
                    "type": "tool_call",
                    "subtype": "started",
                    "call_id": "r",
                    "tool_call": {"readToolCall": {"args": params}},
                },
                {
                    "type": "tool_call",
                    "subtype": "completed",
                    "call_id": "r",
                    "tool_call": {
                        "readToolCall": {
                            "args": params,
                            "result": {"success": {"content": "example"}},
                        }
                    },
                },
            ]
        )
        self.assertEqual(counts["tool_calls"], 1)
        self.assertNotIn("shell_commands", counts)
        self.assertEqual(sections[0], ("工具调用 · readToolCall", params))
        self.assertIn("example", str(sections[1]))

    def test_claude_thinking_meter_and_rate_limit_backoff(self):
        retry = {
            "type": "system",
            "subtype": "api_retry",
            "error_status": 429,
            "max_retries": 10,
        }
        sections, counts, _ = self.render(
            [
                {
                    "type": "system",
                    "subtype": "thinking_tokens",
                    "estimated_tokens": 34,
                },
                {**retry, "attempt": 1, "retry_delay_ms": 600},
                {**retry, "attempt": 2, "retry_delay_ms": 1300},
            ]
        )
        self.assertEqual(counts["api_retries"], 2)
        self.assertEqual(len(sections), 1)
        self.assertIn("HTTP 429", sections[0][0])
        self.assertIn("2 / 10", sections[0][1])
