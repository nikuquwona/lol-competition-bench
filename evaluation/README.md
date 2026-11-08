# 运行评测

| 场景 | 命令 | 依赖与产物 |
|---|---|---|
| 验证一道发布题 | `./bench simple` | Python 3.12，标准库；生成选手历史基线预测与本地评分 |
| 在题集上评估模型 | `./bench e2e --harness codex --model deepseek-v4-pro …` | 默认在 Linux Docker runner 上使用 Harbor；每题独立 CLI 会话、隔离容器和 verifier |
| 验证接线 | `./bench e2e --mode fixture --harness pi --model deepseek-v4-pro --limit 1` | 真实 CLI 使用固定协议回复；报告标为 fixture，不计模型能力成绩 |
| 对尚无赛果的比赛交卷 | `./bench forecast CASE --entrant NAME --harness codex --model deepseek-v4-pro --out DIR` | 调用无标签 Harbor 任务并封存首份预测 |

## 本地安装与验收

在仓库根目录运行以下命令。需要 [uv](https://docs.astral.sh/uv/getting-started/installation/)；若已有仓库专用的 Python 3.12+ 虚拟环境，可跳过第一行。

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python 'harbor==0.25.0'
.venv/bin/harbor --version
.venv/bin/harbor run --help
```

版本应为 `0.25.0`，帮助应显示 `harbor run [OPTIONS]`。项目使用 [Harbor 评测框架](https://pypi.org/project/harbor/0.25.0/)。若系统里的 `harbor --help` 列出 `artifact`、`repo`、`robot`，那是同名的镜像仓库管理工具。`./bench` 会优先在项目的 `.venv/bin` 查找 Harbor，无需修改 shell 配置。

**在 Mac 上跑 Codex + DeepSeek。** macOS 后端使用 Python 3.12+、原生 Codex CLI 和 Xcode Command Line Tools，自身无需 Docker 或 Harbor。先执行 `codex --version`，本项目固定版本为 `codex-cli 0.167.0`。若需在 Apple 芯片 Mac 上单独安装这个版本，可从[官方发行页](https://github.com/openai/codex/releases/tag/rust-v0.167.0)下载 `codex-aarch64-apple-darwin.tar.gz`，将解压得到的可执行文件放在 `.venv/bin/codex`。已有相同版本可直接使用。

先运行免密钥的安装验收。它在两个独立沙箱中启动真实 Codex，使用本地固定响应依次提交两个概率。终端应显示 `selected: 2`、`scored: 2`，报告的 `mode` 为 `fixture`。

```sh
./bench e2e --backend macos --mode fixture --harness codex --model deepseek-v4-pro --series worlds-2026-main-event-quarterfinals-4 --game 2
```

实际预测时，在已导出 `DEEPSEEK_API_KEY` 的终端执行：

```sh
./bench e2e --backend macos --harness codex --model deepseek-v4-pro --series worlds-2026-main-event-quarterfinals-4 --game 2
```

两道题各自使用 Seatbelt 沙箱，宿主按赛果评分。省略 `--out` 会为每次运行生成新的 `.work/runs/<id>/report.json`。如需固定位置，请指定一个新目录；`--resume` 只继续同一运行中尚未开始的题。

**验证 Docker + Harbor 后端。** 在已启动 Docker 且支持 Compose 和断网策略的机器上，下面的命令通过真实 Codex CLI 交卷，用固定响应代替付费推理：

```sh
docker info
docker compose version
./bench e2e --mode fixture --harness codex --model deepseek-v4-pro --series worlds-2026-main-event-quarterfinals-4 --game 2 --phase draft-lock
```

验收标准是终端汇总 `selected: 1`、`scored: 1`。若出现 `network_mode='no-network' is not supported`，检查 Docker 引擎的 Linux 内核。Harbor 0.25.0 会在引擎中探测 nftables 的 `CONFIG_NFT_FIB_INET` 支持，旧版 Docker Desktop 的 LinuxKit 内核可能缺少它。此时可在 Mac 上使用上面的 Seatbelt 命令，或在支持该策略的 Linux runner 上运行完整 Harbor 验收。

### 选择任务与读取报告

默认版本为 `datasets/replay-v3`。simple 默认选 KC–T1 第二局 BP 后；e2e 默认选整套。先用 `--list` 查看范围。可多次指定 `--task`，也可组合 `--phase`、`--series`、`--game`、`--patch` 与 `--limit`。同一系列赛、同一局号且不指定 phase，即为一组 BP 前后对照。

```sh
./bench simple --phase lobby --out .work/baseline-lobby
./bench e2e --list --patch 26.17 --phase draft-lock
./bench e2e --harness pi --model deepseek-v4-pro --patch 26.17 \
  --phase draft-lock --limit 2 --out .work/pi-first-two
```

`report.json` 记录 release、包 SHA-256、model、harness、mode、backend、完整任务计划和逐题结果。逐题记录包含 phase、补丁、输入及题面指纹、预测概率、两项 Brier、reward 或失败原因。报告随每题原子更新；任务全部结束后才写入 summary 与按时点汇总。分母包含失败题。长任务可用相同参数、相同 --out 并加 --resume 恢复；已成功或已失败的题保留首轮结果，已开始但中断的题记为 interrupted，继续运行尚未启动的题。按系列赛做统计推断时，多个小局及同局两个时点并非独立样本。

### 运行环境

在隔离的 Linux runner 上安装 Docker Compose、Python 3.12、`harbor==0.25.0`。Claude Code 2.1.319、Codex 0.167.0、Pi 1.5.0、Kimi Code 2.5.2 分别以原生 CLI 运行。宿主提供 DEEPSEEK_API_KEY，真实 key 只在受限推理网关中使用。Cursor CLI 2026.11.05-86047df 须显式传 `--mode vendor` 和账号可用的模型名，使用专用 CURSOR_API_KEY。供应商后端的检索行为无法由本地验证，Cursor 结果单列。

一次题集运行可复用已构建的 CLI 镜像；HOME、快照、工作区、socket 卷及模型会话按题隔离。CLI 容器仅有回环接口；受控推理网关拒绝模型切换、托管搜索、远程文件和远程 MCP。输出限 4096 字节，拒绝符号链接、FIFO、重复字段和额外字段。评测结束清理临时容器、卷和镜像；runner 生命周期负责最终回收。多人竞赛不得给参赛进程挂载仓库或 Docker socket。

[GitHub Actions 入口](https://github.com/nikuquwona/lol-competition-bench/actions/workflows/native-cli.yml)默认选一局。要选择全部，设置 series 为 `*`、game 为 `0`、phase 为 `both`；limit 限制每个 harness 的选题数量。smoke 不需密钥；live 读取 BENCH_DEEPSEEK_KEY，vendor 读取 BENCH_CURSOR_KEY。大型评测建议分赛段/补丁运行，避免托管任务时限截断。模型凭证由操作者在所选运行环境提供。

macOS 已安装同版本 Codex 时，可用 `--backend macos --harness codex --model deepseek-v4-pro` 在 Seatbelt 沙箱实跑，宿主本地重算分数。默认 Harbor 后端使用独立容器复核分数；报告会保留这一区别。旧版 Python harness、原生 Codex 的既有轨迹及首次未交卷记录在 [v1 示例](examples/kc-t1-g2/) 中。

### 旧版整场系列赛前瞻

小局 intake 以 BP 锁定后的两项概率评分。另保留原有 **整场 BO5 胜率** 入口：`python -m evaluation.live_series freeze …`、[GitHub 封存工作流](https://github.com/nikuquwona/lol-competition-bench/actions/workflows/seal.yml) 及 `python -m evaluation.live_series settle …`。整场赛道的回执按可信 GitHub run 时间验真，成绩与小局分开。

### 按覆盖度和 BP 阶段读分

逐题报告内的 `coverage` 与模型能查阅的历史一致。汇总 `by_coverage` 按十人都有历史（all）、部分有历史（partial）、全员无记录（none）分组。组内平均 reward 计入交卷失败，Brier 只统计成功提交。

`paired` 按系列赛和局号配对。`selected_pairs` 是两个阶段都已选择的小局数，`scored_pairs` 是两个阶段都成功交卷的小局数。`brier_improvement` 按 BP 前 Brier 减去 BP 后 Brier 计算，正值表示看到 BP 后该事件预测更准。全体均值按完整配对的小局等权计算。只跑单一阶段时，均值为 null。

## 验证 CLI 能查历史、读不到未来

`./bench boundary --out .work/kc-t1-boundary` 在临时 Docker 容器中运行 KC 对 T1 第二局的两个观测时点。指定 `--harness codex pi` 或 `--phase lobby` 可以缩小范围。四个可接本地网关的原生 CLI 用固定协议响应执行攻击命令，免用模型密钥。Cursor 走厂商服务，免密钥检查覆盖同一 worker 内的 shell、CLI 版本和未登录启动；认证后的 Cursor 工具执行另需厂商服务。

每次验收分别在一次性管理端副本的本局标签、另一阶段快照和系列第三局快照植入随机标记。攻击方知道这些文件的位置和标记格式，只收到本阶段原始快照与题面。它尝试打开指定文件，扫描工作区、会话目录等位置，记录可用网络接口、外部 TCP 与凭证变量，并从合法历史提取 Faker 的出场局数和第一局双方全部选人。报告包含标记哈希、实际观察值、差异及每个时点执行的 shell 命令。扫描有明确范围，每个文件最多检查前 2 MiB。测试 `tests/test_cli_boundary.py` 故意暴露管理端副本，验证三个标记都能被找回并触发失败。

## 阅读和恢复执行轨迹

每轮运行会输出一份适合阅读的 `report.md` 和一份用于分析的 `report.json`。从报告中点开某个时点的「逐步轨迹」，即可对照模型收到的题面、允许检索的完整快照、原生 CLI 消息、实际工具输入与回显、异常、最终交卷和两项 Brier。Codex 会报告命令退出码和 token 用量。其他 CLI 按各自支持的事件格式记录。报告中赛后观测仅供组织者复核，预测运行期间不提供给模型。

旧运行可以在本地补建报告。例如下面的命令会关联该轮保留的事件，不会发起模型请求：

```sh
./bench report .work/kc-t1-pair-test
```

对于未保存原生日志的旧运行，报告会注明轨迹不可用。Linux worker 分别保留 CLI 的 stdout 和 stderr，每份上限 8 MiB，超限会写明截断。原始 JSONL 和 Markdown 之间的链接使用相对路径，可以把整个运行目录一并移动。

## 使用 OpenRouter 免费模型

在宿主的登录 shell 导出 `OPEN_ROUTER_API_KEY` 或 `OPENROUTER_API_KEY` 后运行：

```sh
./bench e2e --backend macos --mode openrouter-free --harness codex \
  --model nvidia/nemotron-3.5-lightning:free \
  --series worlds-2026-main-event-quarterfinals-4 --game 2
```

网关限制为显式选定的 `:free` 模型，路由价格上限为输入、输出均为零。模型提供方仍可限制并发或返回限流错误；一次试验使用同一模型标识。真实凭证只交给宿主侧网关，模型工具仅能查询当前任务的本地证据。Cursor 的厂商通道另行运行。

## 本地站点、排名和导出

运行 `./bench serve`，在浏览器打开 `http://127.0.0.1:8765`。服务绑定本机回环地址；可用 `--port` 换端口，重复使用 `--runs-dir` 索引自己的报告根目录。新题集若保存在仓库外，用 `--datasets-dir <发布包父目录>` 加入组织者信任的归档，榜单会核对摘要并重算得分。首页按发布包、题号集合、执行后端和赛道展示排名。运行记录可以打开每道题的模型输入、工具命令与回显、预测和评分。边界探测与固定回复验收会标明类型。

每次评测写出 `report.json` 后，站点下一次读取即可看到。支持导出全榜 CSV、单轮 JSON、逐题 CSV、单项证据文件和该轮的完整 ZIP 包。ZIP 保留相对路径，可以离线打开 `report.md` 继续浏览。要生成完整 198 题的离线参照，运行 `./bench simple --all`。题目覆盖、失败计分、重复运行与新榜单的接入规则见[榜单规范](RANKING.md)。

## 固定五场样例

`featured-five` 含 5 个不同小局和 10 个阶段任务，选取时只使用赛程和队伍信息。同一题单可用于 `simple`、`e2e` 或只读的 `--list`。它固定发布归档 SHA-256，便于比较不同 harness。小样本结果独立于全题集排行榜。[具体题号和抽样规则](suites/featured-five.json)

```sh
./bench e2e --suite featured-five --list
./bench simple --suite featured-five
./bench e2e --suite featured-five --backend macos --mode openrouter-free \
  --harness codex --model nvidia/nemotron-3.5-lightning:free
```

[Codex 免费模型的原生轨迹与覆盖记录](examples/featured-five-openrouter/report.md)分别列出成功交卷、上游拒绝和未启动的任务。每个真实试验都有事件文件指纹、来源报告指纹和冻结输入指纹。可用 `python -m unittest discover -s tests -p test_featured_suite.py` 离线验证，含逐题重算成功提交的分数。

如需合并同配置、同题集、互不重叠的小批次，可在组织者侧用 `python -m evaluation.assemble --suite featured-five --source <第一批运行目录> --source <第二批运行目录> --out <新的目录>`。汇集器会核验发布包、CLI 回执、各题指纹和赛后真值，并拒绝重复尝试。全新复跑整组则用上面的 `--suite featured-five` 命令。
