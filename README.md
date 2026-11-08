# LoL Competition Bench

给模型一场职业比赛在某一时点的资料，让它预测蓝方赢下本局的概率，以及蓝方在 15:00 经济领先的概率。同一小局在 **BP 前**和 **BP 锁定后**各出一题。两道题共享历史，模型使用独立会话。

![LoL Competition Bench 框架图：按观测时间冻结比赛资料，模型通过 CLI 检索快照并提交两个概率，独立评分器读取赛后真值。](figures/lol-competition-bench-framework.png)

当前回放版本 **replay-v2** 含 99 小局、198 道 Harbor 题。覆盖 26.17 的 LPL 资格赛及 26.20 的世界赛。打开一份[实际题面](datasets/sample-draft-lock.md)，可以看到参赛模型收到的完整指令。

| 目录 | 职责 | 从这里看 |
|---|---|---|
| **production/** | 整理比赛事实，校验版本和 BP 顺序，按时间截取证据，生成任务 | [出题与新增对局](production/README.md) · [题面模板](production/prompts/forecast.md) |
| **datasets/** | 保存已发布的 Harbor 题集、版本清单和摘要 | [题集目录](datasets/README.md) · [v2 清单](datasets/replay-v2/manifest.json) |
| **evaluation/** | 启动 baseline 或真实 CLI，收取预测、独立评分、汇总失败和完成率 | [运行手册](evaluation/README.md) · [v2 实跑报告](evaluation/examples/replay-v2-codex/report.json) |

## 先跑一题

从仓库根目录直接运行 `./bench simple`。入口会查找本机可执行的 Python 3.12 或更高版本。也可显式使用 `python3.12 bench simple`，或用 uv 创建仓库专用环境：

```sh
uv venv --python 3.12 .venv
. .venv/bin/activate
./bench simple
```

这条命令从发布包选出 KC–T1 第二局的 BP 后任务，验证摘要，交给只读选手历史的基线，再用真值计算分数。终端显示完成率、两个 Brier 分数及报告路径。全程离线，无需 Docker 和密钥。

## 跑一个 model × harness 组合

在配备 Docker Compose 的一次性 Linux runner 上安装 Harbor 0.25.0，并在宿主提供专用推理凭证。下面先列出题目，再让原生 Codex 使用 DeepSeek 完成同一局的两个时点。

```sh
./bench e2e --list --series worlds-2026-main-event-quarterfinals-4 --game 2
./bench e2e --harness codex --model deepseek-v4-pro \
  --series worlds-2026-main-event-quarterfinals-4 --game 2 --out .work/kc-t1-pair
```

省略选题条件会运行整个版本的 198 道题，并产生相应推理费用。可按 `--phase`、`--patch`、`--task` 或 `--limit` 缩小范围。在 GitHub 的[隔离运行工作流](https://github.com/nikuquwona/lol-competition-bench/actions/workflows/native-cli.yml)触发时，无需给个人电脑安装参赛 CLI。

## 模型能查什么

| 信息 | BP 前 | BP 锁定后 |
|---|---|---|
| 赛事、阶段、补丁、BO、局号、红蓝方和当局十名首发 | 可见 | 可见 |
| 截止时点前的比赛、历史英雄和 K/D/A、胜负及 15 分钟经济差 | 可在本地检索 | 同一份历史 |
| 当局禁选的英雄、动作与真实顺位 | 隐藏 | 完整 20 手 |
| 当局赛果、15 分钟经济、赛后评分、后续局、全量数据库 | 隐藏 | 隐藏 |

比赛采集器可以联网。参赛模型通过 shell 或 Python 搜索冻结的 JSON；实时网页、外部搜索、远程 MCP 和跨局记忆都在评测范围之外。四款受控 CLI 的联网权限仅通向指定推理服务。Cursor 走厂商后端，单列结果。历史回放无法排除模型权重已经记住名局，严格盲测应在真实开赛前冻结资料并封存预测。

## 下一场比赛怎么加入

`init-game → freeze → forecast / submit → settle → release`

BP 结束时，录入实际首发和 20 手动作即可生成没有答案的 Harbor 任务。赛后另交胜方与有符号的 15 分钟经济差。发布时沿用当初冻结的输入和题面，结果迟到也不会重建一份不同的赛前历史。[完整命令、示例字段与时间规则](production/README.md#新增一场小局)

## 如何读成绩

每题两项 Brier 等权，reward = 1 − 平均 Brier。蓝方恰好平经济算未领先。始终报两个 50% 的 reward 为 0.75。题集报告同时给出选择数、成功数、失败数、平均 reward 和成功提交上的两项 Brier。失败按零 reward 进入全题均值；不同提示词版本、模拟工具测试、Cursor 厂商组和真实前瞻结果分别报告。
