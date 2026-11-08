# 社区选手证据包

一条记录描述一位选手在一场**已经发生且可查**的小局里的表现。例如，示例记录给出 Faker 在 2026 世界赛首轮对 LOS 的 6/0/7。它可以进入随后 KC 对 T1 第二局的两份题目。选手未首发、引用比赛未进入题目历史、材料发布时间等于或晚于截止点时，生成器会跳过该记录。[示例数据](faker-scoreline.json) · [JSON Schema](schema.json)

## 制作和使用

复制示例并填写包 ID、语义版本、维护方、来源署名和许可。每条证据须标明选手 ID、具体小局、带时区的公开时间、HTTPS 来源及审阅人。一个包内同一选手、同一小局、同一特征只能出现一次。不同包对同一个可见事实重复声明时需要贡献者先协调。特征类型标识带有自己的版本号。

| 特征类型 | 可提交的值 | 验证方法 |
| --- | --- | --- |
| `player.scoreline.v1` | 一个小局的 k、d、a 非负整数 | 与该历史小局公开统计逐项核对 |
| `player.role.v1` | Top、Jungle、Mid、Bot 或 Support | 与该历史小局的位置核对 |
| `player.style.v1` | roaming、lane-focused、engage、peel、split-push 或 teamfight-carry 中的一项 | 人工据有时间标记的公开材料判断，解释仅在所标小局内有效 |

```sh
PACK=production/evidence-packs/faker-scoreline.json
./bench validate-pack "$PACK"
./bench build --series worlds-2026-main-event-quarterfinals-4 --game 2 --phase lobby \
  --with-pack "$PACK" --task-spec scout-one-shot-v1 --out .work/scout-lobby
./bench release --version scout-kda-v1 --with-pack "$PACK" --task-spec scout-one-shot-v1 --out .work/releases
./bench export --release .work/releases/scout-kda-v1 --out .work/scout-training
```

`build`、`release` 和 `freeze` 接受可重复的 `--with-pack` 或 `--evidence-pack`。运行层用发布清单、源包 SHA-256 和逐题输入哈希区分实验。版本包的 `evidence-packs/` 存储完整贡献者元数据；可用 `validate-pack` 重算排序、紧凑 UTF-8 JSON 的规范化 SHA-256。现场 freeze 会记录相同的元数据和指纹，结算后 release 必须选择当时使用的包。同一小局两阶段必须选择相同包，BP 后沿用 BP 前的证据截止。旧回放缺少逐局精确观测时间时，按系列开赛时间截取。阈值相等的记录排除。打包和现场出题均从可见历史检查人物及引用局。

模型快照的 `evidence` 仅含截止时间、首发姓名、结构化值、引用的历史小局和公开时间。来源链接、维护者说明和评语留在组织者侧，以免 URL 或文本提示后续赛果。允许词表约束字段含义，无法自动证明发表日期、来源版权或人工评定的真实性；采用社区包前由组织者核对原始材料、检查时点、批准来源和标注规则。社区可以在 JSON 中直接声明一个具名维度。

## 示例来源和边界

Faker 样例以腾讯归档中的整场回放发布时间 2026-10-24 12:14:41 UTC 作为保守的历史凭据，K/D/A 来自本仓库已冻结的小局技术统计。它展示确定性的数据联结与历史范围校验。该归档在赛事后整理，不能证明组织者曾在当时实际抓取。上游数据使用各自的条款。[腾讯比赛记录 13627](https://lpl.qq.com/web201612/data/LOL_MATCH_DETAIL_13627.js) · [RiftWise 技术统计](https://riftwise.gg/stats/20261108041551/hub/game/worlds-2026-main-event-round-1-7.json) · [仓库来源记录](../data/sources.json)

带任务变体的 RL 导出保留完整原始题面，包括背景、示例和证据说明。`training-tools` 保留原始指令；`training` 用显式纯文本协议呈现原指令和冻结快照。工具型评测数据转换成对应的纯消息输入时可调用 `inline_evaluation_messages(bundle, row)`。

## 仅用 JSON 贡献一个新维度

[完整示例](kill-involvements.json)在 `feature_definitions` 中声明了 `community.matchstats.kill-involvements.v1`，度量选手在指定小局的击杀与助攻数之和。Faker 在示例小局有 6 次击杀、7 次助攻，这条记录的取值为 13。将该文件交给 `./bench validate-pack`，并在上述命令中替换 `PACK`，即可编译、冻结和导出带此维度的题目。

```json
{
  "community.matchstats.kill-involvements.v1": {
    "kind": "integer",
    "description": "Kills plus assists by the player in the referenced game.",
    "minimum": 0, "maximum": 200, "unit": "takedowns"
  }
}
```

每个包最多声明 32 个 `community.<命名空间>.<特征>.v<版本>`。可选 `boolean`、`enum`（2 至 16 个短标识）、`integer`（上下界在 ±1,000,000 内，须提供单位）。记录的值须符合本包声明。多包可引用同一定义，冲突的定义和重复的有效观测会被拒绝。含义变更时增加类型版本。声明的含义说明和完整取值表留在组织者的发布清单与原始证据包中。模型只看到已通过时间窗口、历史小局和首发检查的值、有意义的类型名、数值种类及单位。JSON Schema 可检查对象结构；命令行验证器还会检查动态类型引用、范围和跨包冲突。自定义维度的观测真实性、标注口径和来源时间由审阅者负责。审阅时也要检查特征名、枚举值与单位是否暗示未来赛果。
