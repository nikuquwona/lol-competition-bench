"""Credential-free protocol fixture: ask the real CLI to write a known prediction."""

import json

COMMAND = """printf '%s' '{"p_blue_win":0.41,"p_blue_ahead_15":0.57}' > ./prediction.json"""
FINAL = "Forecast written."
MODEL = "deepseek-v4-pro"


def command_for(tools):
    for t in tools:
        entry = t.get("function", t)
        name = entry.get("name", "")
        if name.lower() in (
            "bash",
            "shell",
            "exec_command",
            "run_shell_command",
            "shell_command",
            "exec",
            "run_command",
            "term",
        ):
            schema = entry.get("input_schema", entry.get("parameters", {}))
            props = schema.get("properties", {})
            key = next((k for k in ("command", "cmd", "script") if k in props), None)
            if key:
                args = {
                    key: ["/bin/sh", "-c", COMMAND]
                    if props[key].get("type") == "array"
                    else COMMAND
                }
                if "description" in schema.get("required", []):
                    args["description"] = "Write the benchmark forecast"
                return name, args
    raise ValueError(
        "Fixture needs shell tool; available: "
        + str([t.get("name") or t.get("function", {}).get("name") for t in tools])
    )


def respond(handler, url, body):
    finished = "bench_fixture_call" in json.dumps(
        body.get("messages", body.get("input", []))
    )
    # Some clients rewrite call IDs, so also recognize a local tool result.
    finished = finished or any(
        isinstance(m, dict)
        and (
            m.get("role") == "tool"
            or m.get("type") == "function_call_output"
            or isinstance(m.get("content"), list)
            and any(
                isinstance(b, dict) and b.get("type") == "tool_result"
                for b in m["content"]
            )
        )
        for m in body.get("messages", body.get("input", []))
    )
    try:
        name, args = ("unused", {}) if finished else command_for(body.get("tools", []))
    except ValueError as exc:
        print(str(exc), flush=True)
        return handler.send_error(422)
    handler.send_response(200)
    streaming = body.get("stream") or url.endswith("/responses")
    handler.send_header(
        "Content-Type", "text/event-stream" if streaming else "application/json"
    )
    handler.end_headers()

    def send(obj, event=None):
        prefix = f"event: {event}\n" if event else ""
        handler.wfile.write((prefix + "data: " + json.dumps(obj) + "\n\n").encode())

    call = "bench_fixture_call"
    if url.endswith("/messages"):
        block = (
            {"type": "text", "text": FINAL}
            if finished
            else {"type": "tool_use", "id": call, "name": name, "input": args}
        )
        msg = dict(
            id="msg_fixture",
            model=MODEL,
            type="message",
            role="assistant",
            content=[block],
            stop_reason="end_turn" if finished else "tool_use",
            stop_sequence=None,
            usage={"input_tokens": 10, "output_tokens": 10},
        )
        if not streaming:
            return handler.wfile.write(json.dumps(msg).encode())

        def event(kind, **kw):
            send(dict(type=kind, **kw), kind)

        event("message_start", message=dict(msg, content=[], stop_reason=None))
        event(
            "content_block_start",
            index=0,
            content_block={"type": "text", "text": ""}
            if finished
            else dict(block, input={}),
        )
        event(
            "content_block_delta",
            index=0,
            delta={"type": "text_delta", "text": FINAL}
            if finished
            else {"type": "input_json_delta", "partial_json": json.dumps(args)},
        )
        event("content_block_stop", index=0)
        event(
            "message_delta",
            delta={"stop_reason": msg["stop_reason"], "stop_sequence": None},
            usage={"output_tokens": 10},
        )
        event("message_stop")
    elif url.endswith("/responses"):
        item = (
            {
                "type": "message",
                "id": "msg_done",
                "role": "assistant",
                "status": "completed",
                "content": [{"type": "output_text", "text": FINAL, "annotations": []}],
            }
            if finished
            else {
                "type": "function_call",
                "id": "fc_bench",
                "call_id": call,
                "name": name,
                "arguments": json.dumps(args),
                "status": "completed",
            }
        )
        response = dict(
            id="resp_bench",
            object="response",
            model=MODEL,
            created_at=1,
            status="completed",
            output=[item],
            usage={"input_tokens": 10, "output_tokens": 10, "total_tokens": 20},
        )
        for kind, payload in [
            (
                "response.created",
                {"response": dict(response, status="in_progress", output=[])},
            ),
            ("response.output_item.added", {"output_index": 0, "item": dict(item)}),
            ("response.output_item.done", {"output_index": 0, "item": item}),
            ("response.completed", {"response": response}),
        ]:
            send(dict(type=kind, **payload), kind)
    else:
        msg = {"role": "assistant", "content": FINAL if finished else None}
        if not finished:
            msg["tool_calls"] = [
                {
                    "id": call,
                    "type": "function",
                    "function": {"name": name, "arguments": json.dumps(args)},
                }
            ]
        end = "stop" if finished else "tool_calls"
        template = dict(id="chatcmpl_bench", model=MODEL, created=1)
        if not streaming:
            return handler.wfile.write(
                json.dumps(
                    dict(
                        template,
                        object="chat.completion",
                        choices=[dict(index=0, message=msg, finish_reason=end)],
                    )
                ).encode()
            )
        for t in msg.get("tool_calls", []):
            t["index"] = 0
        for delta, reason in ((msg, None), ({}, end)):
            send(
                dict(
                    template,
                    object="chat.completion.chunk",
                    choices=[dict(index=0, delta=delta, finish_reason=reason)],
                )
            )
        handler.wfile.write(b"data: [DONE]\n\n")
