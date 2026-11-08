# Invictus Gaming vs Top Esports · G2 · BP 前

lpl-2026-regional-finals · Round 1 · 26.17 · BO5

[实际题面](instruction.md) · [可查询的完整快照](snapshot.json) · [原始事件 JSONL](../../jobs/lpl-2026-regional-finals-round-1-1-g2-lobby/trajectory.jsonl) · [stderr](../../jobs/lpl-2026-regional-finals-round-1-1-g2-lobby/stderr.txt) · [交卷文件](../../jobs/lpl-2026-regional-finals-round-1-1-g2-lobby/prediction.json)

## 输入与可查询证据

蓝方首发为 JiaQi, Meiko, Rookie, TheShy, Wei。

红方首发为 Creme, JackeyLove, Tian, ZUIAN, Zhuo。

冻结时可查 1 个历史小局，10 名首发有历史出场记录。

本局可见 0 手禁选。

## 预测与赛后结算

```
{
  "status": "scored",
  "prediction": {
    "p_blue_win": 0.56,
    "p_blue_ahead_15": 0.48
  },
  "observed_outcome": {
    "p_blue_win": 0,
    "p_blue_ahead_15": 0
  },
  "brier": {
    "p_blue_win": 0.31360000000000005,
    "p_blue_ahead_15": 0.2304
  },
  "reward": 0.728
}
```

## CLI 报告的 token 用量

```
{
  "input_tokens": 5869,
  "cache_creation_input_tokens": 0,
  "cache_read_input_tokens": 12672,
  "output_tokens": 3952
}
```

## 执行轨迹

### 1. 工具调用 · Read

```
{
  "file_path": "[ephemeral]/app/snapshot.json"
}
```

### 2. 工具结果

```
1	{"phase": "lobby", "series_time_utc": "2026-09-17T09:00:00+00:00", "current": {"event": "lpl-2026-regional-finals", "stage": "Round 1", "series": "lpl-2026-regional-finals-round-1-1", "n": 2, "patch": "26.17", "bo": 5, "blue": "Invictus Gaming", "red": "Top Esports", "starters": {"blue": ["JiaQi", "Meiko", "Rookie", "TheShy", "Wei"], "red": ["Creme", "JackeyLove", "Tian", "ZUIAN", "Zhuo"]}, "draft_rule": "Fearless"}, "history": [{"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": true, "blue_gd15": -38, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Syndra"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Renekton"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Jayce"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yorick"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Yorick", "k": 2, "d": 1, "a": 6}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 1, "d": 5, "a": 5}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Syndra", "k": 3, "d": 1, "a": 7}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 5, "d": 5, "a": 4}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Lulu", "k": 0, "d": 0, "a": 10}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Jayce", "k": 1, "d": 1, "a": 5}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Cho'Gath", "k": 1, "d": 6, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Orianna", "k": 7, "d": 0, "a": 1}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Lucian", "k": 2, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion": "Milio", "k": 1, "d": 2, "a": 10}]}], "coverage": {"history_games": 1, "starters": [{"side": "blue", "name": "JiaQi", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Meiko", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Rookie", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "TheShy", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Wei", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Creme", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "JackeyLove", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Tian", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "ZUIAN", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Zhuo", "games": 1, "same_patch_games": 1}], "starters_with_history": 10, "coverage_group": "all", "previous_series_games": [1], "missing_previous_series_games": []}}
```

### 3. 工具调用 · Write

```
{
  "file_path": "[ephemeral]/app/prediction.json",
  "content": "{\n  \"p_blue_win\": 0.56,\n  \"p_blue_ahead_15\": 0.48\n}\n"
}
```

### 4. 工具结果

```
File created successfully at: [ephemeral]/app/prediction.json (file state is current in your context — no need to Read it back)
```

### 5. 模型消息

```
I've written the forecast. Here's my reasoning:

**Evidence available:** Only 1 prior game in the series (game 1, same patch 26.17, same sides — IG blue, TES red).

**Key signals:**
- **IG won game 1** (1-0 series lead), but it was close early: blue gold at 15 was **−38** (essentially dead even, TES slightly ahead).
- Creme carried hard for TES (7/0/1 on Orianna) while Tian fed (1/6/6) — TES had the early lead but IG closed it out.
- **Fearless draft:** every game-1 pick/ban is unavailable to both sides. IG loses its winning comp (Syndra, Yorick, Yunara, Lulu, Skarner); TES loses its carries (Orianna, Lucian, Jayce, Milio, Cho'Gath).

**Estimates:**
- `p_blue_win = 0.56` — IG has series momentum and blue side, but the single-game sample is tiny, TES is a strong org that will adapt, and both teams lose their game-1 compositions. A modest IG lean.
- `p_blue_ahead_15 = 0.48` — Game 1's early game was a dead heat with a hair of a TES lead (−38 gold), so I shade slightly under 50% for IG being strictly ahead at 15, roughly balancing blue-side early-game edge against the observed TES early pressure.

The single game of history is a very thin sample, so I'm keeping both estimates close to even rather than over-weighting one result.
```
