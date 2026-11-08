# Invictus Gaming vs Top Esports · G2 · BP 锁定

lpl-2026-regional-finals · Round 1 · 26.17 · BO5

[实际题面](instruction.md) · [可查询的完整快照](snapshot.json) · [原始事件 JSONL](../../jobs/lpl-2026-regional-finals-round-1-1-g2-draft-lock/trajectory.jsonl) · [stderr](../../jobs/lpl-2026-regional-finals-round-1-1-g2-draft-lock/stderr.txt) · [交卷文件](../../jobs/lpl-2026-regional-finals-round-1-1-g2-draft-lock/prediction.json)

## 输入与可查询证据

蓝方首发为 JiaQi, Meiko, Rookie, TheShy, Wei。

红方首发为 Creme, JackeyLove, Tian, ZUIAN, Zhuo。

冻结时可查 1 个历史小局，10 名首发有历史出场记录。

本局可见 20 手禁选。

## 预测与赛后结算

```
{
  "status": "scored",
  "prediction": {
    "p_blue_win": 0.57,
    "p_blue_ahead_15": 0.42
  },
  "observed_outcome": {
    "p_blue_win": 0,
    "p_blue_ahead_15": 0
  },
  "brier": {
    "p_blue_win": 0.32489999999999997,
    "p_blue_ahead_15": 0.17639999999999997
  },
  "reward": 0.74935
}
```

## CLI 报告的 token 用量

```
{
  "input_tokens": 6562,
  "cache_creation_input_tokens": 0,
  "cache_read_input_tokens": 23680,
  "output_tokens": 5093
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
1	{"phase": "draft-lock", "series_time_utc": "2026-09-17T09:00:00+00:00", "current": {"event": "lpl-2026-regional-finals", "stage": "Round 1", "series": "lpl-2026-regional-finals-round-1-1", "n": 2, "patch": "26.17", "bo": 5, "blue": "Invictus Gaming", "red": "Top Esports", "starters": {"blue": ["JiaQi", "Meiko", "Rookie", "TheShy", "Wei"], "red": ["Creme", "JackeyLove", "Tian", "ZUIAN", "Zhuo"]}, "draft_rule": "Fearless", "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Trundle"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Olaf"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Ashe"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Seraphine"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Ryze"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Lee Sin"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Camille"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Nautilus"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Galio"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Renata Glasc"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Naafiri"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Maokai"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Ezreal"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Karma"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yone"}]}, "history": [{"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": true, "blue_gd15": -38, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Syndra"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Renekton"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Jayce"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yorick"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Yorick", "k": 2, "d": 1, "a": 6}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 1, "d": 5, "a": 5}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Syndra", "k": 3, "d": 1, "a": 7}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 5, "d": 5, "a": 4}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Lulu", "k": 0, "d": 0, "a": 10}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Jayce", "k": 1, "d": 1, "a": 5}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Cho'Gath", "k": 1, "d": 6, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Orianna", "k": 7, "d": 0, "a": 1}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Lucian", "k": 2, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion": "Milio", "k": 1, "d": 2, "a": 10}]}], "coverage": {"history_games": 1, "starters": [{"side": "blue", "name": "JiaQi", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Meiko", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Rookie", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "TheShy", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Wei", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Creme", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "JackeyLove", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Tian", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "ZUIAN", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Zhuo", "games": 1, "same_patch_games": 1}], "starters_with_history": 10, "coverage_group": "all", "previous_series_games": [1], "missing_previous_series_games": []}}
```

### 3. 工具调用 · Write

```
{
  "file_path": "[ephemeral]/app/prediction.json",
  "content": "{\n  \"p_blue_win\": 0.56,\n  \"p_blue_ahead_15\": 0.42\n}\n"
}
```

### 4. 工具结果

```
File created successfully at: [ephemeral]/app/prediction.json (file state is current in your context — no need to Read it back)
```

### 5. 工具调用 · Write

```
{
  "file_path": "[ephemeral]/app/prediction.json",
  "content": "{\n  \"p_blue_win\": 0.57,\n  \"p_blue_ahead_15\": 0.42\n}\n"
}
```

### 6. 工具结果

```
The file [ephemeral]/app/prediction.json has been updated successfully. (file state is current in your context — no need to Read it back)
```

### 7. 模型消息

````
Prediction saved to `./prediction.json`:

```json
{
  "p_blue_win": 0.57,
  "p_blue_ahead_15": 0.42
}
```

**Reasoning from the snapshot:**

- **Series state:** Invictus Gaming (blue) won Game 1 over Top Esports (red) on the same patch (26.17) with identical sides. Game 1 was essentially even at 15:00 (IG −38 gold), yet IG closed it out despite Creme going 7/0/1 on Orianna — a signal that IG's teamfighting/macro was the stronger of the two.
- **Fearless draft:** Game 1 picks (Yorick, Skarner, Syndra, Yunara, Lulu vs Jayce, Cho'Gath, Orianna, Lucian, Milio) are all unavailable, and neither team re-picked them, as expected.

**Game 2 compositions:**
- **IG (blue):** Camille / Maokai / Yone / Ashe / Seraphine — a scaling, teamfight-oriented comp with heavy engage (Camille, Maokai, Ashe arrow, Seraphine ult) and a strong late-game side-lane carry in Yone.
- **TES (red):** Olaf / Lee Sin / Ryze / Ezreal / Karma — an early-game, skirmish/poke comp (Olaf + Lee Sin early pressure, Ezreal/Karma poke lane, Ryze ult synergy with Olaf).

**Estimates:**
- `p_blue_win = 0.57` — IG gets the edge from winning Game 1 (momentum + demonstrated stronger late game) and the better-scaling comp, but TES's early comp and the presence of JackeyLove/Tian keep it close.
- `p_blue_ahead_15 = 0.42` — TES's early-game comp (Olaf, Lee Sin, Ezreal/Karma) is more likely to be ahead at 15 than IG's scaling draft, even though IG is the better overall team. This diverges from the win probability, reflecting a plausible "TES ahead early, IG wins late" dynamic that matches Game 1's shape.
````
