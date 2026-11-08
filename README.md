# LoL Competition Bench

用 Harbor 比较 coding agent / harness 在同一份历史资料上预测职业比赛的能力。每局有两个独立的观测时点，每个任务提交本局蓝方最终获胜、蓝方在 15:00 经济严格领先的两个概率。历史资料可以逐条检索，任务容器断网。

## 2026-11-08 回放数据

| 赛事范围 | 职业赛补丁 | 原始小局 | 可评分小局 |
|---|---|---:|---:|
| LPL 2026 Regional Finals | 26.17 | 12 | 12 |
| Worlds 2026 Play-In + Main Event | 26.20 | 90 | 87 |

47 个系列赛，21 家不同俱乐部的赛事名单，107 个实际出场的选手名，990 条带赛后表现评分的选手场次。世界赛第一场半决赛的 3 局缺少逐人技术统计和 15 分钟经济差，仅收录结果。范围限于这三项赛事，两个版本相隔的其他补丁未必没有职业比赛。版本按每局数据核对。资格赛阶段样本较少，应分补丁报告分数。

- Riot [世界赛赛制](https://lolesports.com/en-GB/news/worlds-2026-primer) 与 [官方赛程](https://lolesports.com/en-US/leagues/worlds)。在本次快照中按队伍、日期和比分关联到 40 个系列赛的 Riot ID。
- 腾讯 [世界赛](https://lpl.qq.com/web201612/data/LOL_MATCH2_MATCH_HOMEPAGE_BMATCH_LIST_246.js) 和 [LPL 赛程](https://lpl.qq.com/web201612/data/LOL_MATCH2_MATCH_HOMEPAGE_BMATCH_LIST_237.js)。47 个系列赛均有可核对的腾讯结果。每个链接和逐方得分见 [官方来源对照](data/official-matches.json)。
- Leaguepedia 的 [LPL BP](https://lol.fandom.com/wiki/LPL/2026_Season/Regional_Finals/Picks_and_Bans)、[Worlds 入围赛 BP](https://lol.fandom.com/wiki/2026_Season_World_Championship/Play-In/Picks_and_Bans)、[Worlds 正赛 BP](https://lol.fandom.com/wiki/2026_Season_World_Championship/Main_Event/Picks_and_Bans) 提供手工记录的动作顺序。每局核对补丁与两边选出的五个英雄。顺位保留先选方和红蓝方的区别。Leaguepedia 内容归原贡献者，按 [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) 署名；衍生 BP 数据沿用同一许可。
- [RiftWise 数据导出](https://riftwise.gg/stats/data) 的版本 20261108041551 提供赛事名单、实际首发、K/D/A、15 分钟经济差；赛后选手分按该站公开的 role/year 基线、权重与公式重算。例：T1 对 KC 第一局 Peyz 为 8.5。这个字段表示 RiftWise 表现分，腾讯观众投票分未收录。赛后评分会引用截至快照日的赛季分布，所有历史预测输入均剔除该字段。
- [完整来源清单](data/sources.json) 记录 URL、抓取时间和原始响应 SHA-256。[选手和教练名单](data/event-rosters.json) 是赛事级回顾档案；任务侧只给本局出场的十人，以及从历史小局可观察的队伍、位置、英雄和表现。

## 运行

使用 Python 3.12、Harbor 0.25.0 和具有 Docker Compose 的 Linux/Docker Desktop。数据已提交，生成和评分可离线。以下命令在仓库根目录执行。

```sh
python3 -m unittest discover -s tests
python3 scripts/build.py --series worlds-2026-main-event-quarterfinals-4 --game 2
pip install harbor==0.25.0
harbor run -p tasks/worlds-2026-main-event-quarterfinals-4-g2-draft-lock -a oracle
```

Oracle 只验证打包与打分，预期 reward 为 1。运行全部 99 个 draft-lock 或 lobby 任务时，指定不同的空输出目录。使用真实模型需要能在宿主侧调用模型、在离线容器内调用工具的 agent adapter。关闭 provider 的托管搜索、浏览器、远端 MCP 和跨局记忆；需要从容器直接连接模型 API 的 CLI 不能按默认断网配置直接参赛。每款 harness 使用独立的新会话、相同 checkpoint、推理预算和快照。

```sh
python3 scripts/build.py --phase lobby --out tasks/lobby
python3 scripts/build.py --phase draft-lock --out tasks/lock
```

输出协议示例为 `{"p_blue_win":0.64,"p_blue_ahead_15":0.52}`，写入容器的 `/app/prediction.json`。独立 verifier 读取这份文件，每局 reward 为 1 − (胜负 Brier + 15 分钟经济领先 Brier)/2。两个概率均报 0.5 的 reward 恒为 0.75。汇总时保留两项 Brier 原值，按相同小局配对比较 lobby 和 draft-lock，统计区间按系列赛分组重采样。

## 时间边界

- **lobby** 假定双方已确认首发和红蓝方，仅给选手名字。**draft-lock** 增加 20 个 BP 动作。两个时点均隐藏本局最终分路、经济曲线、赛后数据、系列赛最终局数及比分。
- 同一系列赛仅开放编号小于当前局的已完赛记录。例如第四局能看到前三局的结果和 Fearless 已用英雄，第二局不能看到第三局。跨系列赛仅开放完整回放已在腾讯编目的系列赛，且其最后一局回放发布时间必须严格早于目标系列赛时间。使用排期与统计源时间的较早值作保守边界。同日其他系列赛没有可靠回放时间则不进入历史。
- 每次构建都重新从允许字段生成快照。Docker 只接收该任务的 environment 目录。评分标签、全量数据、解决方案和其他任务均不挂到参赛环境。不要把仓库作为模型工作目录。
- 这一版是**历史回放**。回放证明当时已公开的比赛可以观看；赛后勘误仍可能改变归档字段。模型权重也可能记得公开比赛。正式盲测应使用赛前或 BP 锁定时实际截取的输入，并在开赛前由有时间戳的第三方存证预测与快照哈希，赛后再关联标签。回放分和前瞻盲测分应独立报告。

## 重新采集

```sh
pip install -r requirements-collect.txt
python3 scripts/fetch.py
python3 scripts/collect.py
```

原始响应保存在 git 忽略的 .cache；缓存同一 URL 可离线重复归一化。腾讯及 Leaguepedia 的当前页面可能更新，历史 RiftWise 版本也可能下线。应保存每次发布的冻结 JSON 与哈希。数据用途及转载受各来源条款约束。
