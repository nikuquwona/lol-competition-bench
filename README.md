# LoL Competition Bench

LoL Competition Bench 是一个基于 Harbor 的《英雄联盟》职业比赛预测基准，用于评估语言模型及其 CLI harness 如何利用赛前信息做概率预测。每个小局在英雄禁选（BP）前后各出一道题。模型可以检索截至该时点的比赛和选手记录，提交**蓝方获胜概率**与**蓝方在 15 分钟时经济领先的概率**，由真实赛果评分。

固定模型、更换 harness，可以比较不同 CLI 在同一批题上的交卷率与预测质量。固定模型和 harness，按小局配对比较两个时点的得分，则可以检验看到完整 BP 后预测是否更准。

**当前回放题集 `replay-v2`** · 2026 赛季 · 46 个系列赛 · 99 小局 · 198 道题

[查看题集清单](datasets/replay-v2/manifest.json) · [阅读完整题面](datasets/sample-draft-lock.md) · [查看真实运行报告](evaluation/examples/replay-v2-codex/report.json) · [安装与运行](evaluation/README.md#本地安装与验收)

![框架图：从赛事记录生成带时间截止点的 Harbor 任务，由 CLI harness 调用模型，提交概率后按实际赛果评分。](figures/lol-competition-bench-framework.png)

## 一道题如何工作

**样例取自 2026 全球总决赛四分之一决赛，Karmine Corp（蓝方）对 T1（红方），BO5 第 2 局，版本 26.20。** 两个会话从各自的 `snapshot.json` 开始。它们都能检索 96 局历史，其中包含本系列第 1 局。比如，按选手名筛选历史可以找到 Faker 的 6 场出场记录；他在上一局用过 Viktor，因此按本系列的 Fearless 规则，双方在第 2 局都不能再选这个英雄。

| 观测时点 | 两题共有的输入 | 当局 BP |
| --- | --- | --- |
| BP 前 · `lobby` | 比赛版本、赛制、局号、红蓝方、十名首发及已公开的历史对局 | 尚未开始 |
| BP 锁定 · `draft-lock` | 相同的比赛背景和历史对局 | 完整 20 手禁选，含顺位、阵营、动作和英雄 |

模型可以用通用游戏知识解释对局，用本地 shell 或 Python 检索快照中的英雄选择、K/D/A、比赛胜负和 15 分钟经济差。评测规则禁止外部搜索及引用记忆中的本局赛果。最终交卷文件为 `prediction.json`。下表是 **Codex CLI × DeepSeek V4 Pro** 在这道 BP 后任务上的一次实际提交。[题面原文](datasets/sample-draft-lock.md) · [逐题报告](evaluation/examples/replay-v2-codex/report.json)

| 提交字段 | 预测事件 | 提交概率 | 赛后观测 |
| --- | --- | ---: | --- |
| `p_blue_win` | KC 赢下本局 | 35% | T1 获胜 |
| `p_blue_ahead_15` | KC 在 15:00 的团队经济严格高于 T1 | 61% | KC 落后 4,026 金 |

两项预测的平方误差分别为 `0.1225` 和 `0.3721`，这一题的得分为 `1 − (0.1225 + 0.3721) / 2 = 0.7527`。

## 快速开始

从仓库根目录运行以下命令。**离线基线**只需 Python 3.12+，默认选择上述 KC–T1 的 BP 后任务，用双方首发的历史表现估计概率。终端会显示 `selected: 1`、`scored: 1` 和本次报告路径。

```sh
./bench simple
```

**运行 Codex × DeepSeek。** 先列出两道题，再针对自己的运行环境选择一条预测命令。实际推理需要在宿主导出 `DEEPSEEK_API_KEY`，按 API 用量计费。

```sh
./bench e2e --list --series worlds-2026-main-event-quarterfinals-4 --game 2
```

```sh
# macOS · 原生 Codex CLI 0.167.0，Seatbelt 隔离，宿主评分
./bench e2e --backend macos --harness codex --model deepseek-v4-pro --series worlds-2026-main-event-quarterfinals-4 --game 2
```

```sh
# Linux · Harbor 0.25.0，Docker Compose，独立验证容器
./bench e2e --backend harbor --harness codex --model deepseek-v4-pro --series worlds-2026-main-event-quarterfinals-4 --game 2
```

其中 `--model` 选择推理模型，`--harness` 选择读取资料、调用工具并写入预测的原生 CLI，`--backend` 选择隔离与评分环境。首次安装可以给同一条命令追加 `--mode fixture`，用固定响应验证交卷链路，免用 API 密钥。每次运行默认创建独立的 `.work/runs/<id>/report.json`。省略所有选题条件时，`e2e` 会运行当前版本的全部 198 道题。[安装与验收](evaluation/README.md#本地安装与验收) · [运行手册](evaluation/README.md) · [GitHub Actions](.github/workflows/native-cli.yml)

| 运行方式 | 可选 harness | 推理与评分 |
| --- | --- | --- |
| Harbor · 受控推理 | Claude Code、Codex、Pi、Kimi Code | CLI 通过受限网关调用指定模型，Harbor 单独运行评分器 |
| macOS · 本地验证 | Codex | 每题使用独立 Seatbelt 沙箱，宿主使用同一评分函数 |
| Harbor · 厂商服务 | Cursor CLI | `--mode vendor` 使用 Cursor 账号可用的模型；厂商侧检索行为无法在本地核验，成绩单列 |

## 数据来源与时间边界

归档收录 47 个系列赛的 102 小局。发布回放题要求十名首发、完整 20 手禁选及 15 分钟经济差齐备，最终有 99 小局入选。26.17 版本的 LPL 资格赛贡献 12 小局，26.20 版本的全球总决赛贡献 87 小局。Riot 与腾讯赛事记录用于核对赛制、对阵和系列赛比分，Leaguepedia 用于核对逐手 BP，RiftWise 提供出场记录与局内统计。按赛季数据重算的选手赛后评分仅保存在归档中。[逐系列对照](production/data/official-matches.json) · [数据来源与署名](production/README.md#既有赛季数据)

**历史回放。** 同系列中局号更小的对局可进入历史。其他系列只有在目标系列开赛前已发布完整回放，才进入快照。每题在独立会话中运行，当局结果、后续对局和验证器答案都留在参赛环境之外。回放包随仓库公开，历史赛果也可能已进入模型训练数据。

**新赛前瞻。** 组织者在首发确认或 BP 锁定时用 `freeze` 冻结输入，用 `forecast` 或 `submit` 封存首份预测，赛后用 `settle` 关联真值，再用 `release` 发布新题。程序按实际开赛时间判定迟交。若比赛要求 BP 前预测必须在第一手禁选前交卷，组织者还应单独记录并核验这个截止时点。[新增一场比赛的完整流程](production/README.md#新增一场小局)

## 评分与比较

两个二元事件分别计算 Brier 分数，即预测概率与实际标签之差的平方。蓝方在 15:00 经济持平时，该项标签为 0。每题的 `reward` 为 1 减去两项 Brier 的平均值，越高越好；超时、缺失或无效提交计 0 分。报告中的 `mean_reward` 包含全部选题，`brier_on_scored` 只统计成功交卷的题，因此比较 harness 时应同时报告 `scored / selected`。

下表给出 `replay-v2` 的参照值。每个时点各有 99 题。选手历史基线只使用首发和历史统计，因此 BP 前后给出相同预测。可用 `./bench simple --phase lobby` 或 `./bench simple --phase draft-lock` 复算。[基线实现](evaluation/baseline.py) · [评分实现](production/score.py)

| 基线 | 胜负 Brier ↓ | 15 分钟领先 Brier ↓ | 平均 reward ↑ |
| --- | ---: | ---: | ---: |
| 两项恒报 50% | 0.2500 | 0.2500 | 0.7500 |
| 选手历史基线 | 0.2465 | 0.2554 | 0.7491 |

比较 BP 的影响时，按小局配对两个时点，并列出缺少任一侧提交的小局数。比较 harness 时，应固定题集版本、观测时点、模型和预算；同一系列中的多局相关，统计不确定性应按系列赛分组估计。

## 仓库结构

| 模块 | 输入 → 产物 | 入口 |
| --- | --- | --- |
| `production/` | 赛事记录 → 校验后的比赛归档、赛前快照与 Harbor 任务 | [采集、冻结与赛后结算](production/README.md) |
| `datasets/` | 已发布任务 → 可离线使用的版本包和逐题 SHA-256 清单 | [题集目录与版本](datasets/README.md) |
| `evaluation/` | 指定题集、模型与 CLI → 逐题提交、失败原因和汇总报告 | [运行与复现](evaluation/README.md) |
