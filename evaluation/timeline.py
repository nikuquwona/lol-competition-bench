"""Bounded, evidence-backed timeline for one saved CLI trial."""

import ast
import io
import json
import re
import shlex
from bisect import bisect_right
from collections import defaultdict, deque

from evaluation.traces import render_events
from production.score import FIELDS

READ_LIMIT = 8 * 1024 * 1024
STEP_LIMIT = 180
DETAIL_LIMIT = 4000
FIELD_NAMES = [
    ("coverage", "首发历史覆盖"),
    ("starters", "首发名单"),
    ("players", "选手记录"),
    ("champion", "英雄"),
    ("history", "历史对局"),
    ("blue_gd15", "15 分钟经济差"),
    ("blue_win", "历史胜负"),
    ("patch", "比赛版本"),
    ("bp", "禁选顺序"),
]


def text(value):
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)


def clipped(value, limit):
    return value if len(value) <= limit else value[:limit] + "…"


def forecast_object(value):
    return (
        isinstance(value, dict)
        and set(value) == set(FIELDS)
        and all(type(v) in (int, float) and 0 <= v <= 1 for v in value.values())
    )


def seen_prediction(output):
    """Recognize only complete forecast objects actually printed by the tool."""
    for candidate in reversed(re.findall(r"\{[^{}]{1,240}\}", output)):
        try:
            value = ast.literal_eval(candidate)
        except (ValueError, SyntaxError):
            continue
        if forecast_object(value):
            return value
    return None


def evidence_tags(command):
    if "snapshot.json" not in command:
        return []
    return [
        label for key, label in FIELD_NAMES if re.search(r"\b" + key + r"\b", command)
    ]


def source_reference(lines, number, call_id=None):
    """Locate the native record and the specific tool in a multi-call message."""
    if number is None:
        return {}
    line = lines[number - 1]
    ref = {"line": number, "raw": clipped(line, 1200), "raw_chars": len(line)}
    try:
        event = json.loads(line)
    except ValueError:
        return ref
    if not isinstance(event, dict):
        return ref
    msg = event.get("message")
    item = event.get("item")
    ref["type"] = event.get("type") or event.get("role")
    if isinstance(item, dict):
        ref["item_id"] = item.get("id")
        if item.get("type") == "command_execution":
            ref["tool"] = "Shell"
    if isinstance(msg, dict):
        ref["message_id"] = msg.get("id")
        blocks = msg.get("content")
        for b in blocks if isinstance(blocks, list) else []:
            if not isinstance(b, dict) or not call_id or b.get("id") != call_id:
                continue
            ref["tool"] = b.get("name")
            if isinstance(b.get("input"), dict):
                description = b["input"].get("description")
                if isinstance(description, str):
                    ref["description"] = clipped(description, 110)
    if call_id:
        ref["call_id"] = call_id
    if isinstance(event.get("toolName"), str):
        ref["tool"] = event["toolName"]
    return {k: v for k, v in ref.items() if v is not None}


def summarize_tool(cmd, output, failed):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if failed:
        err = next(
            (
                line
                for line in reversed(lines)
                if re.search(
                    r"\b\w+(?:Error|Exception)\b|not found|denied", line, re.IGNORECASE
                )
            ),
            None,
        )
        return "命令执行失败", clipped(err or (lines[-1] if lines else cmd), 180)
    if "prediction.json" in cmd:
        return "访问预测文件", clipped(" ".join(lines[:2]), 180)
    tags = evidence_tags(cmd)
    if "snapshot.json" in cmd and not tags and (not lines or lines[0].startswith("{")):
        return "读取冻结快照", f"返回 {len(output):,} 个字符" if output else ""
    if tags:
        return "查询" + "、".join(tags[:3]), clipped(" · ".join(lines[:3]), 180)
    fragment = (
        cmd.removeprefix("/bin/zsh -lc ").removeprefix("/bin/bash -lc ").strip("'\x22")
    )
    return clipped(fragment.splitlines()[0] if fragment else "终端命令", 78), clipped(
        " · ".join(lines[:2]), 180
    )


def readable_input(label, raw_input):
    if isinstance(raw_input, dict) and label == "工具调用 · Write":
        return raw_input.get("file_path"), text(raw_input.get("content", ""))
    if label.startswith("终端命令") and isinstance(raw_input, str):
        try:
            fields = shlex.split(raw_input)
        except ValueError:
            fields = []
        if (
            len(fields) == 3
            and fields[0] in ("/bin/bash", "/bin/zsh", "/bin/sh")
            and fields[1] in ("-c", "-lc")
        ):
            return None, fields[2]
    return None, text(raw_input)


def build_timeline(events_path, *, phase, prediction=None, outcome=None):
    data = {
        "phase": phase,
        "availability": "unavailable",
        "metrics": {},
        "steps": [],
        "evidence": [],
        "readbacks": [],
        "checkpoints": [],
        "submission": prediction,
        "outcome": outcome,
        "omitted": 0,
    }
    if events_path is None or not events_path.is_file():
        return data
    with events_path.open("rb") as f:
        raw = f.read(READ_LIMIT + 1)
    cut = len(raw) > READ_LIMIT
    if cut:
        raw = raw[:READ_LIMIT].rpartition(b"\n")[0]
    call_ids = {}
    locations = {}
    turn_starts = []
    decoded = raw.decode("utf-8", "replace")
    native_lines = decoded.split("\n")
    sections, counts, _ = render_events(
        events_path,
        stream=io.StringIO(decoded),
        call_ids=call_ids,
        locations=locations,
        turn_starts=turn_starts,
    )
    data["metrics"] = counts
    if cut or counts.get("truncated"):
        data["availability"] = "truncated"
    elif not counts.get("events"):
        return data
    else:
        data["availability"] = "recorded"
    results = defaultdict(deque)
    for offset, call_id in call_ids.items():
        if sections[offset][0].startswith(("命令结果", "工具结果")):
            results[call_id].append(offset)
    consumed = set()
    for i, (label, body) in enumerate(sections):
        if i in consumed:
            continue
        step = {
            "id": f"s{i}",
            "kind": "event",
            "title": label,
            "source": source_reference(native_lines, locations.get(i), call_ids.get(i)),
        }
        value = text(body)
        turn = bisect_right(turn_starts, locations.get(i, 0))
        if turn:
            step["turn"] = turn
        if label.startswith(("终端命令", "工具调用")):
            cmd = value
            result = ""
            result_label = ""
            result_index = None
            if i in call_ids:
                matches = results[call_ids[i]]
                while matches and matches[0] < i:
                    matches.popleft()
                if matches:
                    result_index = matches.popleft()
            elif i + 1 < len(sections) and sections[i + 1][0] == "命令输出":
                # The Codex renderer emits one command/output pair from the same
                # completed item. Other native providers pair by their call IDs.
                result_index = i + 1
            if result_index is not None:
                result_label, payload = sections[result_index]
                result = text(payload)
                consumed.add(result_index)
                step["result_source"] = source_reference(
                    native_lines,
                    locations.get(result_index),
                    call_ids.get(result_index),
                )
            match = re.search(r"退出码 (-?\d+)", label + " " + result_label)
            code = int(match[1]) if match else None
            failed = (code is not None and code != 0) or "失败" in result_label
            shell = label.startswith("终端命令")
            title, preview = (
                summarize_tool(cmd, result, failed)
                if shell
                else (label, clipped(result, 180))
            )
            step.update(
                kind="tool",
                title=title,
                preview=preview,
                command=clipped(cmd, DETAIL_LIMIT),
                output=clipped(result, DETAIL_LIMIT),
                command_chars=len(cmd),
                output_chars=len(result),
                exit_code=code,
                failed=failed,
                has_result=bool(result_label),
                unfinished="未收到完成事件" in label,
            )
            if step["source"].get("description"):
                step["title"] = step["source"]["description"]
            path, readable = readable_input(label, body)
            if path:
                step["file"] = path
            step["input_display"] = clipped(readable, DETAIL_LIMIT)
            step["input_chars"] = len(readable)
            if result_label and not failed:
                step["queries_snapshot"] = "snapshot.json" in cmd
                tags = evidence_tags(cmd)
                step["fields"] = tags
                for tag in tags:
                    if tag not in data["evidence"]:
                        data["evidence"].append(tag)
                pair = seen_prediction(result) if "prediction.json" in cmd else None
                if pair:
                    step["prediction"] = pair
                    if not data["readbacks"] or pair != data["readbacks"][-1]:
                        data["readbacks"].append(pair)
                source = "output"
                if label == "工具调用 · Write" and isinstance(body, dict):
                    target = body.get("file_path")
                    if target in (
                        "./prediction.json",
                        "prediction.json",
                        "/app/prediction.json",
                        "[ephemeral]/app/prediction.json",
                    ) and isinstance(body.get("content"), str):
                        # Claude's Write can confirm a full file write without
                        # echoing its contents. Bind its call ID to the success
                        # result and retain the successfully written arguments.
                        try:
                            payload = json.loads(body["content"])
                        except ValueError:
                            payload = None
                        pair = payload if forecast_object(payload) else None
                        if pair:
                            step.update(title="写入预测文件", prediction=pair)
                            source = "write_tool"
                if (
                    pair
                    and (
                        not data["checkpoints"]
                        or data["checkpoints"][-1]["values"] != pair
                    )
                    and len(data["steps"]) < STEP_LIMIT
                ):
                    data["checkpoints"].append(
                        {"source": source, "values": pair, "step_id": step["id"]}
                    )
        else:
            kind = (
                "message"
                if label == "模型消息"
                else "diagnostic"
                if "诊断" in label or label == "trace.truncated"
                else "event"
            )
            step.update(
                kind=kind,
                preview=clipped(value.strip(), 180),
                body=clipped(value, DETAIL_LIMIT),
                body_chars=len(value),
            )
        if len(data["steps"]) < STEP_LIMIT:
            data["steps"].append(step)
        else:
            data["omitted"] += 1
    return data
