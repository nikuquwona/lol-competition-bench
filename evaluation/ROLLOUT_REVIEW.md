# 五场预测的轨迹核查

这次核查覆盖固定五场题单的 26 个实际会话。两个 DeepSeek 组合在同一套十道题上独立运行。每道题有自己的原生 CLI 日志、冻结快照和组织者评分。官方 DeepSeek API 使用操作者账户计费，回执没有返回账单金额。

| 模型 | CLI | 通道 | 已交卷 | 失败 | 未启动 | 原生工具调用 | 十题平均 reward |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| DeepSeek V4 Pro | Codex | DeepSeek 官方 | 10 | 0 | 0 | 83 | 0.68284 |
| DeepSeek V4 Pro | Claude Code | DeepSeek 官方 | 10 | 0 | 0 | 69 | 0.68065 |
| Nemotron 3.5 Lightning | Codex | OpenRouter 免费 | 4 | 2 | 4 | 36 | — |

免费组有 2 个会话在 OpenRouter 日配额耗尽时中断，另有 4 题未启动。失败前的写入和读回可在轨迹中查看，正式评分以 runner 收到的最终交卷为准。[免费组报告与配额回执](examples/featured-five-openrouter/report.md)

## 离线复核

```sh
./bench audit
./bench audit --json /tmp/lol-rollout-audit.json
```

核查程序打开随仓发布的原生事件，核对输入与当前发布包的哈希，按时间和局号重建各题可查历史，再用组织者持有的标签重算得分。逐题 JSON 含首次查快照的行号、首次写入时的 shell 调用数、最后一次可核实的概率、工具错误及访问异常。命令全程离线。

20 个官方会话都读取了冻结快照，最终可核实的概率与交卷文件一致。核查了 152 次工具调用，没有在这些已记录的命令中发现外部检索或读取当局答案。Codex 和 Claude Code 各有 4 题用了超过四次 shell 调用才首次写入。题面将四次设为建议；这八题仍按提交的概率正常评分。运行回执记录了沙箱探针的结果，公开轨迹无法证明模型训练时是否见过比赛。

工具输出中出现一组概率，只有能关联到相应的文件写入或读回时才进入预测记录。例如 KC–T1 G2 的 BP 后，Codex 两次经 Python 写文件并打印写入值，Claude Code 两次使用原生 `Write`。程序另外列出无法静态判定全部副作用的工具调用行号：两组 DeepSeek 分别为 54 和 41，免费组为 21；可在 `unknown_lines` 逐行复查。

## 三条模型陈述

| 会话 | 模型陈述与冻结快照的核对 |
| --- | --- |
| Claude Code · LØS–LYON G2 · BP 前 | 原生第 8618 行称 LØS 只输给过 T1 和 G2。快照中 LØS 为 5 胜 3 负，第三场失利是 10 月 30 日对 Team Liquid 的第二局。当天蓝方 LØS 在 15 分钟落后 1,870 金且最终落败。[原生消息](examples/featured-five-claude-deepseek/jobs/worlds-2026-main-event-round-5-2-g2-lobby/trajectory.jsonl#L8618) · [当题快照](examples/featured-five-claude-deepseek/traces/worlds-2026-main-event-round-5-2-g2-lobby/snapshot.json) |
| Codex · KC–T1 G2 · BP 后 | 原生第 45 行引用了上一局的战况。G1 中 T1 五名选手共 23 杀，KC 共 7 杀。15 分钟 KC 领先 660 金，最终 T1 获胜。[原生消息](examples/featured-five-deepseek/jobs/worlds-2026-main-event-quarterfinals-4-g2-draft-lock/trajectory.jsonl#L45) · [当题快照](examples/featured-five-deepseek/traces/worlds-2026-main-event-quarterfinals-4-g2-draft-lock/snapshot.json) |
| Codex · Movistar KOI–BLG G1 · BP 前 | 原生第 12 行称当时的 34 局历史没有覆盖本场首发。检索每局选手名单后，双方十人的命中数均为零。模型随后用背景知识判断 BLG 更强。[原生消息](examples/featured-five-deepseek/jobs/worlds-2026-main-event-round-1-3-g1-lobby/trajectory.jsonl#L12) · [当题快照](examples/featured-five-deepseek/traces/worlds-2026-main-event-round-1-3-g1-lobby/snapshot.json) |

站点将这些核查附在对应的原生消息上。每条标注绑定公开日志的完整 SHA-256 和行号，回归测试检查原句和冻结证据。标注仅覆盖列出的陈述。运行得分由两项概率的 Brier 误差决定。[核查标注](rollout_reviews.json) · [标注回归测试](../tests/test_rollout_reviews.py)
