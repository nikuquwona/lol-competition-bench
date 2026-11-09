"""Build offline, navigable reports from native CLI events and the pinned task inputs."""

import argparse
import fcntl
import json
import re
import shutil
import tempfile
from collections import Counter
from os.path import relpath
from pathlib import Path

from production.catalog import display_names, resolve_release


def fenced(value):
    if not isinstance(value, str):
        value = json.dumps(value, ensure_ascii=False, indent=2)
    fence = "`" * max(3, 1 + max(map(len, re.findall(r"`+", value)), default=0))
    display = "\n".join(line.rstrip() for line in value.rstrip().split("\n"))
    return f"{fence}\n{display}\n{fence}"


def render_events(
    path, *, stream=None, call_ids=None, locations=None, turn_starts=None
):
    from evaluation.native_events import NativeEvents

    sections = []
    counts = Counter()
    usage = Counter()
    pending = {}
    native = NativeEvents(sections, counts, usage, call_ids)
    with stream if stream is not None else path.open(errors="replace") as stream:
        for line_no, line in enumerate(stream, 1):
            if not line.strip():
                continue
            counts["events"] += 1
            first = len(sections)
            try:
                event = json.loads(line)
            except ValueError:
                event = None
            if not isinstance(event, dict):
                sections.append(("CLI 输出", line))
                if locations is not None:
                    locations[first] = line_no
                continue
            if turn_starts is not None and event.get("type") in (
                "turn.started",
                "turn_start",
            ):
                turn_starts.append(line_no)
            if native.consume(event):
                if locations is not None:
                    for index in range(first, len(sections)):
                        locations[index] = line_no
                    if first and event.get("subtype") == "api_retry":
                        locations[len(sections) - 1] = line_no
                continue
            kind = event.get("type", "event")
            if kind == "turn.completed":
                usage.update(
                    {
                        k: v
                        for k, v in (event.get("usage") or {}).items()
                        if type(v) is int
                    }
                )
                continue
            if kind in ("thread.started", "turn.started"):
                continue
            item = event.get("item")
            if not isinstance(item, dict):
                item = {}
            if kind == "item.started" and item.get("type") == "command_execution":
                pending[item.get("id")] = (item.get("command", ""), line_no)
                continue
            if kind == "item.completed" and item.get("type") == "command_execution":
                start = pending.pop(item.get("id"), None)
                counts["shell_commands"] += 1
                rc = item.get("exit_code")
                if isinstance(rc, int) and rc != 0:
                    counts["failed_commands"] += 1
                sections.append((f"终端命令 · 退出码 {rc}", item.get("command", "")))
                sections.append(("命令输出", item.get("aggregated_output", "")))
                if locations is not None and start:
                    locations[first] = start[1]
            elif kind == "item.completed" and item.get("type") in (
                "agent_message",
                "error",
            ):
                label = "模型消息" if item["type"] == "agent_message" else "CLI 诊断"
                sections.append(
                    (label, item.get("text") or item.get("message") or item)
                )
            else:
                if kind == "trace.truncated":
                    counts["truncated"] += 1
                sections.append((str(kind), event))
            if locations is not None:
                for index in range(first, len(sections)):
                    locations.setdefault(index, line_no)
    for command, line_no in pending.values():
        if locations is not None:
            locations[len(sections)] = line_no
        sections.append(("终端命令 · 未收到完成事件", command))
    if pending:
        counts["unfinished_commands"] = len(pending)
    return sections, dict(counts), dict(usage)


def relative(path, root):
    return path.relative_to(root).as_posix()


def attach(out, record, task):
    identifier = record["task"]
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]+", identifier):
        raise ValueError("Unsafe task identifier")
    job = out / "jobs" / identifier
    dest = out / "traces" / identifier
    dest.mkdir(parents=True, exist_ok=True)
    files = {}
    for key, name in (("prompt", "instruction.md"), ("snapshot", "snapshot.json")):
        src = (task / "environment" / name) if key == "snapshot" else task / name
        if key == "prompt" and (job / name).is_file():
            src = job / name  # Exact prompt rewritten for the native workspace.
        dst = dest / name
        shutil.copyfile(src, dst)
        files[key] = relative(dst, out)
    for key, name in (
        ("events", "trajectory.jsonl"),
        ("native_log", "cli-events.log"),
        ("context", "model-context.jsonl"),
        ("stderr", "stderr.txt"),
        ("prediction", "prediction.json"),
    ):
        candidates = sorted(job.rglob(name)) if job.is_dir() else []
        if len(candidates) == 1:
            files[key] = relative(candidates[0], out)
    trace = files.get("events") or files.get("native_log")
    sections, counts, usage = render_events(out / trace) if trace else ([], {}, {})
    labels = json.loads((task / "tests/labels.json").read_bytes())
    current = json.loads((task / "environment/snapshot.json").read_bytes())["current"]
    record["observed_outcome"] = labels
    record["trajectory"] = {
        "availability": ("truncated" if counts.get("truncated") else "recorded")
        if counts.get("events")
        else "unavailable",
        **counts,
        "token_usage": usage,
        "files": files,
    }
    links = " · ".join(
        f"[{label}]({relpath(out / path, dest)})"
        for key, label in (
            ("prompt", "实际题面"),
            ("snapshot", "可查询的完整快照"),
            ("events", "原始事件 JSONL"),
            ("context", "逐次推理请求与响应"),
            ("native_log", "原生 CLI 日志"),
            ("stderr", "stderr"),
            ("prediction", "交卷文件"),
        )
        if (path := files.get(key))
    )
    stage = "BP 前" if record["phase"] == "lobby" else "BP 锁定"
    lines = [
        f"# {current['blue']} vs {current['red']} · G{current['n']} · {stage}",
        f"{current['event']} · {current['stage']} · {current['patch']} · BO{current['bo']}",
        links,
        "## 输入与可查询证据",
        f"蓝方首发为 {', '.join(current['starters']['blue'])}。",
        f"红方首发为 {', '.join(current['starters']['red'])}。",
    ]
    if card := record.get("coverage"):
        lines.append(
            f"冻结时可查 {card['history_games']} 个历史小局，"
            f"{card['starters_with_history']} 名首发有历史出场记录。"
        )
    lines.append(f"本局可见 {len(current.get('bp', []))} 手禁选。")
    lines.extend(
        [
            "## 预测与赛后结算",
            fenced(
                {
                    k: record[k]
                    for k in (
                        "status",
                        "prediction",
                        "observed_outcome",
                        "brier",
                        "reward",
                        "error",
                    )
                    if k in record
                }
            ),
        ]
    )
    if usage:
        lines.extend(["## CLI 报告的 token 用量", fenced(usage)])
    lines += ["## 执行轨迹"]
    if not sections:
        lines.append("此运行没有可展示的原生事件。")
    for i, (kind, value) in enumerate(sections, 1):
        lines.extend([f"### {i}. {kind}", fenced(value)])
    transcript = dest / "transcript.md"
    transcript.write_text("\n\n".join(lines) + "\n")
    files["transcript"] = relative(transcript, out)


def overview(out, report):
    title = display_names(report["release"])
    lines = [
        f"# {report['harness']} × {report.get('model') or 'baseline'}",
        f"{title['display_title']} · {title['edition'] or report['release']} · {report['backend']} · {report['mode']}",
        "| 题目 | 状态 | 蓝方胜率 | 蓝方 15 分钟领先概率 | reward | 执行记录 |",
        "|---|---|---:|---:|---:|---|",
    ]
    for r in sorted(
        report["trials"],
        key=lambda row: (
            row["task"].removesuffix("-" + row["phase"]),
            row["phase"] != "lobby",
        ),
    ):
        trace = r.get("trajectory", {})
        files = trace.get("files", {})
        entry = f"[逐步轨迹]({files['transcript']})" if "transcript" in files else "—"
        if "shell_commands" in trace:
            entry += f" · {trace['shell_commands']} 条命令，{trace.get('failed_commands', 0)} 条失败"
        pred = r.get("prediction", {})
        probs = [
            f"{pred[k]:.1%}" if k in pred else "—"
            for k in ("p_blue_win", "p_blue_ahead_15")
        ]
        lines.append(
            "| "
            + " | ".join(
                [
                    r["task"],
                    r["status"],
                    *probs,
                    format(r["reward"], ".6g")
                    if isinstance(r.get("reward"), (int, float))
                    else "—",
                    entry,
                ]
            )
            + " |"
        )
    if report.get("summary"):
        lines.extend(
            [
                "",
                f"已评分 {report['summary']['scored']} / {report['summary']['selected']}，平均 reward {report['summary']['mean_reward']:.5f}。",
            ]
        )
    if report.get("unstarted"):
        progress = report["progress"]
        lines += [
            "",
            f"原计划 {progress['planned']} 题，启动 {progress['attempted']} 题，成功交卷 {progress['scored']} 题。",
        ]
        lines += ["", "免费推理日配额耗尽，以下题目尚未启动。"]
        for trial in report["unstarted"]:
            lines += [
                f"- {trial['task']} · [题面]({trial['files']['prompt']}) · [快照]({trial['files']['snapshot']})"
            ]
    for trial in report["trials"]:
        if draft := trial.get("unsettled_draft"):
            lines += [
                "",
                f"{trial['task']} 的 CLI 在事件 `{draft['native_event']}` 读回草稿 "
                f"`{json.dumps(draft['values'], ensure_ascii=False)}`。运行因 HTTP 429 中止，该草稿未结算。",
            ]
    lines.extend(["", "[机器可读报告](report.json)"])
    (out / "report.md").write_text(
        "\n".join([lines[0], "", lines[1], "", *lines[2:]]) + "\n"
    )


def main():
    from evaluation.suite import ROOT, select, summarize_report, unpack, write_report
    from production.coverage import history_card

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--release", type=resolve_release)
    a = parser.parse_args()
    out = a.run.resolve()
    with (out / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        report = json.loads((out / "report.json").read_bytes())
        name = report["release"]
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
            raise ValueError("Unsafe release ID")
        release = a.release or ROOT / "datasets" / name
        ids = [r["task"] for r in report["trials"]]
        manifest, planned = select(release, report["planned"])
        rows = {row["id"]: row for row in planned}
        if len(ids) != len(set(ids)) or set(ids) - rows.keys():
            raise ValueError("Invalid trial identities in saved report")
        if manifest["sha256"] != report["archive_sha256"]:
            raise ValueError("This run requires its original release archive")
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            unpack(release, manifest, [rows[i] for i in ids], directory)
            for r in report["trials"]:
                row = rows[r["task"]]
                for key in ("snapshot_sha256", "prompt_sha256"):
                    if key in r and r[key] != row[key]:
                        raise ValueError(
                            "Saved trial fingerprints differ from original release"
                        )
                task = directory / r["task"]
                view = json.loads((task / "environment/snapshot.json").read_bytes())
                r["coverage"] = history_card(view["current"], view["history"])
                if report["mode"] != "baseline":
                    attach(out, r, task)
        if len(ids) == len(planned) and all(
            r["status"] != "started" for r in report["trials"]
        ):
            summarize_report(report, planned)
        write_report(out, report)
        overview(out, report)
    print(out / "report.md")
