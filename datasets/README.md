# Harbor 题集

| 版本 | 题数 | 用途 |
|---|---:|---|
| [replay-v2](replay-v2/manifest.json) | 198 | 当前版本。清单逐题记录系列赛、时点、补丁、输入与题面 SHA-256；发布包可离线展开。 |
| [replay-v1](lol-2026-replay-v1.tar.gz) | 198 | 旧提示词及其评分器；用于重放既有成绩。[展开的 KC–T1 两道样题](examples/replay-v1-kc-t1-g2/)。 |
| [live](live/) | 独立系列赛赛道 | 赛前冻结的整场 BO5 输入，与逐小局题分开结算。 |

**获取与复现。** 当前 v2 压缩包约 2.26 MiB，随本仓库公开分发。将同一版本的 `manifest.json` 与 `tasks.tar.gz` 放在同一目录，即可用 `--release /path/to/version` 指定本地副本。复现实验时记录仓库提交与清单中的包摘要。未开赛的观测、提交回执及评分真值由组织者单独保管。[数据来源与署名](../production/README.md#既有赛季数据)

```sh
./bench e2e --release datasets/replay-v2 --list --patch 26.17
mkdir -p .work/unpacked
tar -xzf datasets/replay-v2/tasks.tar.gz -C .work/unpacked
```

发布包包含 verifier 与 oracle，仅供组织者部署；参赛容器只接收该题的 environment。运行入口先校验包摘要、拒绝符号链接和越界路径，再检查所选题目的输入与题面摘要。摘要可检测传输损坏，发布身份取决于你信任的仓库提交或来源。
