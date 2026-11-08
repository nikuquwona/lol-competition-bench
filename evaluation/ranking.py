"""Compute comparable local replay rankings from validated individual trials."""

import hashlib
import json
import math
import re
from collections import Counter, defaultdict

from production.score import FIELDS

TRACKS = {
    "live": "controlled",
    "openrouter-free": "controlled",
    "baseline": "baseline",
    "vendor": "vendor",
    "fixture": "fixture",
}
RULES = [
    "正式回放榜要求可信发布清单、全量题号和全部终态记录；子集仅与完全相同的题号集合比较。",
    "发布版本、归档摘要、题号集合、执行后端和评测协议共同确定比较组。受控模型、选手历史基线、厂商通道和固定响应分别展示。",
    "同一模型与 CLI 的多轮完整尝试等权合并。失败或中断的单题计零，完成率使用全部计划题为分母。",
    "两项 Brier 只在成功交卷上计算，越低越好。按平均 reward、完成率降序，同分并列。",
    "这是组织者本机收录的回放结果。赛前封存、实时赛事、费用与安全探测单独核验。",
]


def probability(x):
    return type(x) in (int, float) and 0 <= x <= 1


def same(a, b):
    return probability(a) and math.isclose(a, b, abs_tol=1e-10, rel_tol=0)


def check_trial(t, trusted=None):
    status = t.get("status")
    if status == "environment_error" or (
        status == "failed"
        and not t.get("runtime")
        and str(t.get("error", "")).startswith(
            "Boundary test failed: sandbox-exec: sandbox_apply: Operation not permitted"
        )
    ):
        raise ValueError("CLI 启动前隔离检查失败，整轮仅保留为环境诊断")
    if status in ("failed", "interrupted"):
        if not same(t.get("reward", 0), 0):
            raise ValueError("失败题 reward 非零")
        return 0, None
    if status != "scored":
        raise ValueError("运行尚有未终态记录")
    pred, brier, labels = t.get("prediction"), t.get("brier"), t.get("observed_outcome")
    if trusted is not None:
        for field in ("prompt_sha256", "snapshot_sha256"):
            gold = trusted.get(field)
            if (
                not isinstance(gold, str)
                or not re.fullmatch(r"[a-f0-9]{64}", gold)
                or t.get(field) != gold
            ):
                raise ValueError("题面或输入快照与可信发布清单不符")
        gold = trusted.get("labels")
        if not isinstance(gold, dict) or set(gold) != set(FIELDS):
            raise ValueError("可信发布记录缺少赛果")
        if labels is not None and labels != gold:
            raise ValueError("报告赛果与发布包不一致")
        labels = gold
    if any(not isinstance(x, dict) or set(x) != set(FIELDS) for x in (pred, brier)):
        raise ValueError("预测或 Brier 字段不完整")
    if labels is not None and (
        not isinstance(labels, dict) or set(labels) != set(FIELDS)
    ):
        raise ValueError("赛果字段不完整")
    for f in FIELDS:
        if not probability(pred[f]) or not probability(brier[f]):
            raise ValueError("概率或 Brier 超出范围")
        outcomes = (0, 1)
        if labels is not None:
            if type(labels[f]) not in (int, bool) or labels[f] not in outcomes:
                raise ValueError("赛果不是二元值")
            outcomes = (labels[f],)
        if not any(same(brier[f], (pred[f] - y) ** 2) for y in outcomes):
            raise ValueError("Brier 与预测或已记录赛果不一致")
    if labels is not None:
        brier = {f: (pred[f] - labels[f]) ** 2 for f in FIELDS}
    reward = 1 - math.fsum(brier.values()) / len(FIELDS)
    if not same(t.get("reward"), reward):
        raise ValueError("reward 与 Brier 不一致")
    return reward, brier


def verified_round(report, manifest):
    if manifest is None:
        raise ValueError("本地没有摘要匹配的发布清单")
    if not isinstance(report, dict):
        raise TypeError("运行报告格式无效")
    mode, backend = report.get("mode"), report.get("backend")
    if (
        not isinstance(mode, str)
        or mode not in TRACKS
        or backend not in ("local", "macos", "harbor")
    ):
        raise ValueError("未知评测模式或执行后端")
    if (mode == "baseline") != (backend == "local"):
        raise ValueError("基线模式与后端不匹配")
    release, archive, harness, model = (
        report.get(k) for k in ("release", "archive_sha256", "harness", "model")
    )
    if not all(isinstance(x, str) and x.strip() for x in (release, archive, harness)):
        raise ValueError("缺少发布版本、归档摘要或 CLI")
    if not re.fullmatch(r"[a-f0-9]{64}", archive):
        raise ValueError("归档摘要格式无效")
    if mode == "baseline" and model is None:
        model = "player-history"
    if not isinstance(model, str) or not model.strip():
        raise ValueError("缺少模型标识")
    if mode == "openrouter-free" and not model.endswith(":free"):
        raise ValueError("免费通道缺少固定免费模型标识")
    planned = report.get("planned")
    if (
        not isinstance(planned, list)
        or not planned
        or not all(isinstance(t, str) and t for t in planned)
    ):
        raise ValueError("缺少有效的计划题号")
    task_ids = set(planned)
    manifest_ids = set(manifest)
    trusted = isinstance(manifest, dict)
    if len(task_ids) != len(planned) or not task_ids <= manifest_ids:
        raise ValueError("计划题号有重复或不属于发布清单")
    trials = report.get("trials")
    if not isinstance(trials, list) or len(trials) != len(planned):
        raise ValueError("计划题目尚未全部产生终态记录")
    if (
        not all(isinstance(t, dict) and isinstance(t.get("task"), str) for t in trials)
        or {t["task"] for t in trials} != task_ids
    ):
        raise ValueError("试题记录与计划不匹配")
    scored = []
    rewards = []
    for trial in trials:
        runtime = trial.get("runtime")
        if isinstance(runtime, dict):
            if runtime.get("mode", mode) != mode:
                raise ValueError("实际运行模式与报告不一致")
            runtime_model = runtime.get("requested_model", runtime.get("model", model))
            if runtime_model != model:
                raise ValueError("实际运行模型与报告不一致")
        evidence = manifest[trial["task"]] if trusted else None
        if trusted and not isinstance(evidence, dict):
            raise ValueError("可信发布记录格式无效")
        reward, brier = check_trial(trial, evidence)
        rewards.append(reward)
        if brier is not None:
            scored.append(brier)
    n = len(task_ids)
    mean = math.fsum(rewards) / n
    summary = report.get("summary")
    if summary is not None and (
        not isinstance(summary, dict)
        or summary.get("selected") != n
        or summary.get("scored") != len(scored)
        or not same(summary.get("mean_reward"), mean)
    ):
        raise ValueError("汇总与逐题记录不符")
    if (
        summary is not None
        and "statuses" in summary
        and summary["statuses"] != dict(Counter(t["status"] for t in trials))
    ):
        raise ValueError("状态汇总与逐题记录不符")
    if summary is not None and "brier_on_scored" in summary:
        by_metric = summary["brier_on_scored"]
        if not isinstance(by_metric, dict) or set(by_metric) != set(FIELDS):
            raise ValueError("Brier 汇总缺少指标")
        for f in FIELDS:
            if scored:
                if not same(
                    by_metric[f], math.fsum(x[f] for x in scored) / len(scored)
                ):
                    raise ValueError("Brier 汇总与逐题记录不符")
            elif by_metric[f] is not None:
                raise ValueError("没有交卷时 Brier 应为空")
    fingerprint = hashlib.sha256(
        json.dumps(sorted(task_ids), ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()
    protocol = report.get("protocol_sha256", "suite-v1")
    if protocol != "suite-v1" and (
        not isinstance(protocol, str) or not re.fullmatch(r"[a-f0-9]{64}", protocol)
    ):
        raise ValueError("协议摘要格式无效")
    scope = "full" if task_ids == manifest_ids else "subset"
    key = (
        release,
        archive,
        backend,
        TRACKS[mode],
        protocol,
        fingerprint,
        scope,
        n,
        trusted,
    )
    return (
        key,
        (harness, model),
        (mean, len(scored), [math.fsum(r[f] for r in scored) for f in FIELDS]),
    )


def leaderboard(runs):
    """manifest IDs must be passed only after the caller verifies the archive identity."""
    by_group = defaultdict(lambda: defaultdict(list))
    excluded = []
    runs = list(runs)
    frequency = Counter(run_id for run_id, _, _ in runs)
    for run_id, report, ids in runs:
        try:
            if frequency[run_id] > 1:
                raise ValueError("run_id 重复")
            key, entrant, stats = verified_round(report, ids)
            by_group[key][entrant].append((run_id, *stats))
        except (TypeError, ValueError) as e:
            excluded.append({"run_id": run_id, "reason": str(e)})

    groups = []
    for key, contestants in sorted(by_group.items()):
        release, archive, backend, track, protocol, fingerprint, scope, n, trusted = key
        entries = []
        for (harness, model), attempts in contestants.items():
            run_ids = sorted(run[0] for run in attempts)
            selected = n * len(attempts)
            scored = sum(run[2] for run in attempts)
            brier = [
                math.fsum(run[3][i] for run in attempts) / scored if scored else None
                for i in range(len(FIELDS))
            ]
            entries.append(
                {
                    "harness": harness,
                    "model": model,
                    "run_id": run_ids[0],
                    "run_ids": run_ids,
                    "attempts": len(attempts),
                    "selected": selected,
                    "scored": scored,
                    "completion_rate": scored / selected,
                    "mean_reward": math.fsum(run[1] for run in attempts)
                    / len(attempts),
                    "brier_win": brier[0],
                    "brier_ahead15": brier[1],
                }
            )
        entries.sort(
            key=lambda e: (
                -round(e["mean_reward"], 12),
                -e["completion_rate"],
                e["harness"],
                e["model"],
            )
        )
        last_key = None
        for i, entry in enumerate(entries, 1):
            tie = (round(entry["mean_reward"], 12), entry["completion_rate"])
            if tie != last_key:
                rank = i
            entry["rank"] = rank
            last_key = tie
        groups.append(
            {
                "release": release,
                "archive_sha256": archive,
                "backend": backend,
                "track": track,
                "protocol": protocol,
                "selection_sha256": fingerprint,
                "selected": n,
                "scope": scope,
                "verification": "release_labels" if trusted else "report_consistency",
                "official": scope == "full" and track == "controlled" and trusted,
                "entries": entries,
            }
        )
    return {"groups": groups, "rules": list(RULES), "excluded": excluded}
