# 扩充预测题、背景与运行规程

[目录](catalog.json) 注册题目类别、背景资料、运行指令和任务规格。[JSON Schema](catalog.schema.json) 用于编辑器与 CI 校验。运行 `./bench specs` 可解析已注册的每道规格，核对资源引用、模板占位符、评分合同并得到精确内容指纹。运行 `./bench specs scout-one-shot-v1` 可查看单个规格的全部组件。

| 数据种类 | 存放内容与扩展方式 |
|---|---|
| `categories` | 类别 ID 对应职责描述。多个任务可以共用类别，类别与预测目标分别演进。 |
| `backgrounds` | 独立版本 ID 指向通用分析背景的 Markdown 文件。有关真实选手或具体比赛的事实应走带来源、公开时间和适用赛事的 evidence pack。 |
| `instructions` | 每个版本选择题面模板和可选的一条完整示例。模板可引用 `game`、`blue`、`red`、`bo`、`patch`、`phase`、`observation`、`draft`、`history_count`。其余花括号按 Python format 规则转义。背景和示例按原文附加，里面的 JSON 无需转义。 |
| `tasks` | 一个规格绑定类别、背景 ID、指令 ID 和评分合同。修改任何组件内容时创建新版本 ID，保留旧文件以重现已有归档。 |

`forecast-v1` 使用默认的双概率题面。`scout-one-shot-v1` 复用同一评分器，加入赛前分析背景和一组虚构战队的输出示例。示例里的队名、概率均为虚构。两项任务目前都提交蓝方胜率和蓝方 15 分钟领先概率，评分采用两项 Brier 的算术平均。新增预测目标、BP 动作题或证据检索题时，需要独立实现输出 schema、真值来源、grader、安全测试及新的评分合同，然后在目录中引用该合同。

## 本地制作与验题

```sh
./bench specs scout-one-shot-v1
./bench build --task-spec scout-one-shot-v1 \
  --series worlds-2026-main-event-quarterfinals-4 --game 2 --phase lobby --out .work/scout-tasks
./bench release --task-spec scout-one-shot-v1 --version scout-v1 --out .work/releases
./bench simple --release .work/releases/scout-v1 --series worlds-2026-main-event-quarterfinals-4 --game 2
./bench freeze .work/observation.json --task-spec scout-one-shot-v1 --store .work/scout-intake
```

背景和示例由组织者审核。通用文本应独立于赛果和赛后数据，真实案例应满足预测时点可用性要求。冻结的题面、快照和规格指纹随任务存证。同一局的两个时点共用任务规格。需要同时开多种协议时，使用独立 intake 目录和 release 版本。新发布包的 manifest 携带类别、组件文件摘要、完整规格与 `protocol_sha256`，运行报告记录对应指纹。默认的历史 `replay-v3` 保留其既有序列化格式；其出题字节可直接与已发布的题面、快照和归档 SHA-256 对照。
