# Harbor 题集

| 版本 | 题数 | 用途 |
|---|---:|---|
| [2026 世界赛与 LPL 区域资格赛预测集 · 选手履历版](replay-v3/manifest.json) | 198 | 当前版本。逐题快照包含选手历史覆盖数据卡。[全题集数据卡](replay-v3/coverage.json) |
| [rl-eval-v1](rl-eval-v1/README.md) | 126 训练 / 44 验证 / 28 测试 | 同一批比赛的 JSONL 和训练 Parquet，附原生工具环境与纯消息协议、按 ID 评分的 Brier 回调、HF 加载与拼接示例。 |
| [2026 世界赛与 LPL 区域资格赛预测集 · 基础快照版](replay-v2/manifest.json) | 198 | 清单逐题记录系列赛、时点、补丁、输入与题面 SHA-256；发布包可离线展开。 |
| [replay-v1](lol-2026-replay-v1.tar.gz) | 198 | 旧提示词及其评分器；用于重放既有成绩。[展开的 KC–T1 两道样题](examples/replay-v1-kc-t1-g2/)。 |
| [live](live/) | 独立系列赛赛道 | 赛前冻结的整场 BO5 输入，与逐小局题分开结算。 |

**获取与复现。** 当前 v3 压缩包约 2.3 MiB。将同一版本的 `manifest.json`、`coverage.json` 与 `tasks.tar.gz` 放在同一目录，即可用 `--release /path/to/version` 指定本地副本。复现实验时记录仓库提交与清单中的包摘要。未开赛的观测、提交回执及评分真值由组织者单独保管。[数据来源与署名](../production/README.md#既有赛季数据)

```sh
./bench e2e --release worlds-lpl-2026 --list --patch 26.17
mkdir -p .work/unpacked
tar -xzf datasets/replay-v3/tasks.tar.gz -C .work/unpacked
```

发布包包含 verifier 与 oracle，仅供组织者部署；参赛容器只接收该题的 environment。运行入口先校验包摘要、拒绝符号链接和越界路径，再检查所选题目的输入与题面摘要。摘要可检测传输损坏，发布身份取决于你信任的仓库提交或来源。

## 选手历史覆盖

每题的 `snapshot.json` 包含 `coverage`。选手计数只使用本题可见的历史，每个选手 ID 在一局最多计一次，按大小写无关的现用 ID 匹配。同补丁计数属于总出场数的子集。缺少选手明细的历史对局仍计入 `history_games`。卡片还列出本系列已经收录、以及按局号应存在但缺失的先前小局。

[完整数据卡](replay-v3/coverage.json)按题号索引。99 个小局中，85 局十名首发均有历史，5 局只有部分首发有历史，9 局十名首发都没有可查出场。两个阶段各有一份卡。以 KC–T1 第二局为例，快照有 96 局历史，含本系列第 1 局。KC 五名首发各有 19 次出场记录，T1 五名首发各有 6 次，这些出场都在本题使用的 26.20 补丁。
