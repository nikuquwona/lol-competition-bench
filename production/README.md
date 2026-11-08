# 题集生产

出题单位是「系列赛 × 小局号 × 观测时点」。标识如 `worlds-2026-main-event-quarterfinals-4-g2-draft-lock`。赛事资料与评分真值留在组织者侧，任务生成器按字段白名单建立参赛快照。

## 新增一场小局

**1 · 在 BP 锁定时记录观察。** 在可信采集机上执行下列命令；将示例系列赛标识换为实际标识。先选方可以是红方。命令生成 20 行已编号的禁选槽，操作者只需依顺位填英雄，写入实际的赛事、阶段、补丁、双方队名和十名首发。只知道首发时可以单独生成 `--phase lobby`。

```sh
./bench init-game --series next-final --game 1 --bo 5 \
  --phase draft-lock --first-pick red --out .work/observation.json
# 填完表单后执行
./bench freeze .work/observation.json --store .work/intake
```

`series_time` 是系列赛时间；`observed_at` 是本局实际确认首发或 BP 的时刻。两者均需带时区，例如 `2026-11-08T22:00:00Z`。在 `source` 填入当时的 HTTPS 赛事来源；记录时间和 URL 不会自动证实来源内容，赛事组织者应保留当时的源快照或录像。当前支持 BO1/3/5/7、Standard 和 Fearless、完整的 20 手禁选。跳过禁用、缺首发或特殊赛制应先增加对应规则和测试。

`freeze` 创建 `.work/intake/next-final-g1-draft-lock/`。其中 `task/` 是可运行的无标签 Harbor 任务，`observation.json` 是管理端的来源、冻结时间和指纹。重复冻结同一标识会失败。BP 前与 BP 后属于两个不同标识，各自独立冻结。

**2 · 在对应阶段的窗口内提交预测。** 两个窗口均从各自快照冻结起算，截止点本身算迟交。lobby 在首手选禁公开时截止，draft-lock 在游戏开局时截止。可从冻结任务运行原生 CLI 并封存结果，也可提交已在合规环境中生成的文件。组织者的时钟记录首次提交时间。

```sh
CASE=.work/intake/next-final-g1-draft-lock
./bench forecast "$CASE" --entrant codex-deepseek --harness codex \
  --model deepseek-v4-pro --out .work/next-final-run

# 或从已有预测文件封存；文件须含两个数值概率
./bench submit "$CASE" codex-deepseek .work/prediction.json
```

`forecast` 使用 Harbor 的 `--disable-verification`。此时没有胜负标签，不能返回预测质量分数。开赛窗口很短时，模型可能来不及交卷；迟交不能作为前瞻成绩。多人赛事应将提交入口部署在组织者控制的机器上，参赛者仅获得允许字段，自行编辑的本地回执不能作为公开存证。

组织者在事件发生时执行 `close`，将示例时间和链接换为真实值。事件延迟上报时，`--at` 仍取来源中首手 BP 或开局的实际时间。`cutoff.json` 在组织者侧同时保留事件时间、入库时间和证据来源，首次登记后即锁定。

```sh
./bench close .work/intake/next-final-g1-lobby \
  --at 2026-11-08T21:56:00Z --source https://example.org/first-public-ban
./bench close .work/intake/next-final-g1-draft-lock \
  --at 2026-11-08T22:05:00Z --source https://example.org/game-start
```

关窗后，`submit` 立即拒收，`forecast` 在启动模型前检查一次，交卷时再检查一次。组织者即使忘记录入第一手，冻结完整 BP 后也会停止接受 lobby 提交。赛后按实际截止时间复核已收回执。缺少第一手时间证据的 lobby（包括旧记录）显示 `unverified`，分数留空。应在 `settle` 前补录可靠的关窗证据。draft-lock 也可以使用赛果中的 `game_started_at` 结算，若已有实时关窗记录，两处时间必须一致。

**3 · 赛后结算。** 将真实结果写入一个单独的 JSON。下方仅表示字段格式，日期、赛果和来源均要替换。

```json
{
  "id": "next-final-g1-draft-lock",
  "winner": "red",
  "blue_gd15": -1200,
  "game_started_at": "2026-11-08T22:05:00Z",
  "published_at": "2026-11-08T23:10:00Z",
  "source": "https://example.org/replace-with-official-game-result"
}
```

```sh
./bench settle "$CASE" .work/result.json
./bench scores "$CASE"
./bench release --version replay-next --out .work/releases --intake .work/intake
./bench e2e --release .work/releases/replay-next --list --series next-final
```

胜局用 `winner: blue/red`，`blue_gd15` 始终是蓝方减红方。可选 `players` 包含十行实名单局技术统计，每行使用 name、side、role、champion、k、d、a。有效回执满足 **冻结 ≤ 提交 < 对应阶段的截止时间**，且赛果公布时间不早于开局、不晚于采集机当前时间。一个小局只录入一次赛果，两个阶段分别用冻结快照和各自的截止时间评分。如果只冻结过 lobby，可在赛果的可选 bp 字段中补入已经公开的完整禁选，供下一局 Fearless 校验。结算把迟交标成 `ineligible`。新发布包纳入已结算的任务，并逐字沿用观测时冻结的题面及快照。

## 历史从哪里来

同系列只允许查更小局号。其他系列必须在目标系列开赛前已有完整公开回放；新观察还受实际观察时间约束。新增小局先供同系列后续局使用，资料齐全且整个系列胜负已定，才按最晚可用时间向其他系列开放。赛季重算的表现评分、赛后报道标题、观众评论和完整赛事名单均不进入模型输入。

如果今天才从第 2 局开始观测，第 1 局可从正式结果补录为历史证据。用 `./bench history-add prior.json --store .work/intake`，其中 `prior.json` 含完整的 `observation` 表单、`winner`、`blue_gd15`、`game_started_at`、`published_at` 和 `result_source`。该操作不会给昨天的比赛补造一份赛前预测。Fearless 下一局会核对双方之前实际选过的英雄。

## 既有赛季数据

- [Riot 官方赛制](https://lolesports.com/en-GB/news/worlds-2026-primer)和[腾讯赛事记录](https://lpl.qq.com/web201612/data/LOL_MATCH2_MATCH_HOMEPAGE_BMATCH_LIST_246.js)用于核对对阵及系列赛比分。47 个系列赛均对上腾讯记录，40 个关联到 Riot 比赛 ID。[逐系列对照](data/official-matches.json)
- 游戏内 BP 顺序按 Leaguepedia 手工记录核对两侧英雄和单局胜者，衍生 BP 数据按 [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) 署名共享。[世界赛 BP](https://lol.fandom.com/wiki/2026_Season_World_Championship/Main_Event/Picks_and_Bans)
- [RiftWise](https://riftwise.gg/stats/data) 冻结版本 20261108041551 提供赛事名单、K/D/A、15 分钟经济差；按其公式重算的赛后表现分保存在归档中。21 家俱乐部、107 名实际出场选手，共 990 条选手场次评分。102 局中有 3 局技术字段不足，99 局进入回放评测。[来源与摘要](data/sources.json)
- 重新采集该批数据使用 `python -m pip install -r production/requirements-collect.txt`、`python -m production.fetch`、`python -m production.collect`。上游页面会修订，采集脚本面向该批赛事；新增观测使用上述 intake 入口。赛季归档和缓存不交给参赛 CLI。

## 社区选手证据

使用 `./bench validate-pack` 检查贡献者的 JSON 文件，再在 `build`、`freeze` 或 `release` 添加 `--with-pack PATH`。已发布的回放可用新版本名合并证据包做配对实验。[证据定义、贡献规则和 KC–T1 示例](evidence-packs/README.md)
