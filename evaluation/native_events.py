"""Readable views over native stream-json logs; the original event stream stays intact."""

import json


def content_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            b["text"]
            for b in content
            if isinstance(b, dict)
            and b.get("type") == "text"
            and isinstance(b.get("text"), str)
        )
    return ""


class NativeEvents:
    def __init__(self, sections, counts, usage):
        self.sections = sections
        self.counts = counts
        self.usage = usage
        self.calls = {}
        self.saw_message = False

    def message(self, text):
        if text:
            self.sections.append(("模型消息", text))
            self.saw_message = True

    def start(self, identifier, name, args):
        if not isinstance(identifier, str) or not isinstance(name, str):
            return
        shell = name.lower() in {
            "bash",
            "shell",
            "shell_command",
            "exec_command",
            "shelltoolcall",
        }
        self.calls[identifier] = shell
        self.counts["tool_calls"] += 1
        if shell:
            self.counts["shell_commands"] += 1
            self.counts["unfinished_commands"] += 1
        value = (
            args.get("command", args.get("cmd", args))
            if shell and isinstance(args, dict)
            else args
        )
        self.sections.append(("终端命令" if shell else "工具调用 · " + name, value))

    def result(self, identifier, value, failed=False, code=None):
        shell = (
            self.calls.pop(identifier, False) if isinstance(identifier, str) else False
        )
        if shell:
            self.counts["unfinished_commands"] -= 1
            if not self.counts["unfinished_commands"]:
                del self.counts["unfinished_commands"]
            if failed or (type(code) is int and code != 0):
                self.counts["failed_commands"] += 1
        label = "命令结果" if shell else "工具结果"
        if type(code) is int:
            label += f" · 退出码 {code}"
        elif failed:
            label += " · 失败"
        self.sections.append((label, value))

    def consume(self, event):
        kind, role = event.get("type"), event.get("role")
        # Claude Code and Cursor use message envelopes. Cursor exposes its tools
        # as separate tool_call records; Claude uses tool_use/tool_result blocks.
        if kind in ("assistant", "user") and isinstance(event.get("message"), dict):
            blocks = event["message"].get("content")
            if kind == "assistant":
                self.message(content_text(blocks))
            for block in blocks if isinstance(blocks, list) else []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    self.start(block.get("id"), block.get("name"), block.get("input"))
                elif block.get("type") == "tool_result":
                    body = block.get("content")
                    self.result(
                        block.get("tool_use_id"),
                        content_text(body) or body,
                        block.get("is_error"),
                    )
            return True
        if kind == "system" and event.get("subtype") == "init":
            return True
        if kind == "result":
            for k, v in (event.get("usage") or {}).items():
                if type(v) is int:
                    self.usage[k] = v
            if event.get("is_error"):
                self.sections.append(
                    ("CLI 诊断", event.get("errors") or event.get("result") or event)
                )
            elif not self.saw_message:
                self.message(event.get("result"))
            return True
        if kind == "tool_call" and isinstance(event.get("tool_call"), dict):
            for name, payload in event["tool_call"].items():
                if not isinstance(payload, dict):
                    return False
                identifier = event.get("call_id")
                if event.get("subtype") == "started":
                    self.start(identifier, name, payload.get("args", {}))
                elif event.get("subtype") == "completed":
                    if identifier not in self.calls and "args" in payload:
                        self.start(identifier, name, payload["args"])
                    data = payload.get("result", {})
                    self.result(
                        identifier, data, isinstance(data, dict) and "error" in data
                    )
                else:
                    return False
            return True

        # Kimi uses chat-completion-style assistant and tool messages.
        if role == "assistant":
            self.message(content_text(event.get("content")))
            for call in event.get("tool_calls") or []:
                if not isinstance(call, dict) or not isinstance(
                    call.get("function"), dict
                ):
                    continue
                fn = call["function"]
                args = fn.get("arguments", {})
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except ValueError:
                        pass
                self.start(call.get("id"), fn.get("name"), args)
            return True
        if role == "tool":
            body = event.get("content")
            self.result(
                event.get("tool_call_id"),
                content_text(body) or body,
                event.get("is_error"),
            )
            return True
        if role == "meta" and kind in ("system.version", "session.resume_hint"):
            return True

        # Pi repeats messages during streaming, at turn end, and at session end.
        # Keep only final assistant messages and actual tool execution events.
        if kind == "message_end" and isinstance(event.get("message"), dict):
            msg = event["message"]
            if msg.get("role") == "assistant":
                self.message(content_text(msg.get("content")))
                if msg.get("errorMessage"):
                    self.sections.append(("CLI 诊断", msg["errorMessage"]))
                self.usage.update(
                    {
                        k: v
                        for k, v in (msg.get("usage") or {}).items()
                        if type(v) is int
                    }
                )
            return True
        if kind == "tool_execution_start":
            self.start(
                event.get("toolCallId"), event.get("toolName"), event.get("args")
            )
            return True
        if kind == "tool_execution_end":
            result = event.get("result") or {}
            if not isinstance(result, dict):
                return False
            details = result.get("structuredContent") or {}
            code = details.get("exit_code") if isinstance(details, dict) else None
            self.result(
                event.get("toolCallId"),
                content_text(result.get("content")) or result,
                event.get("isError"),
                code,
            )
            return True
        return kind in {
            "session",
            "agent_start",
            "turn_start",
            "message_start",
            "message_update",
            "tool_execution_update",
            "turn_end",
            "agent_end",
            "agent_settled",
        }
