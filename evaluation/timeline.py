"""Bounded, evidence-backed timeline for one saved CLI trial."""

import ast
import io
import json
import re
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
    sections, counts, _ = render_events(
        events_path,
        stream=io.StringIO(raw.decode("utf-8", "replace")),
        call_ids=call_ids,
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
        step = {"kind": "event", "title": label}
        value = text(body)
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
            if result_label and not failed:
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
                if pair and (
                    not data["checkpoints"] or data["checkpoints"][-1]["values"] != pair
                ):
                    data["checkpoints"].append({"source": source, "values": pair})
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
        if data["steps"] and all(
            data["steps"][-1].get(k) == v for k, v in step.items()
        ):
            data["steps"][-1]["repeat"] = data["steps"][-1].get("repeat", 1) + 1
        elif len(data["steps"]) < STEP_LIMIT:
            data["steps"].append(step)
        else:
            data["omitted"] += 1
    return data
