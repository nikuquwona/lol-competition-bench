# Invictus Gaming vs Top Esports · G2 · BP 前

lpl-2026-regional-finals · Round 1 · 26.17 · BO5

[实际题面](instruction.md) · [可查询的完整快照](snapshot.json) · [原始事件 JSONL](../../jobs/lpl-2026-regional-finals-round-1-1-g2-lobby/trajectory.jsonl) · [stderr](../../jobs/lpl-2026-regional-finals-round-1-1-g2-lobby/stderr.txt)

## 输入与可查询证据

蓝方首发为 JiaQi, Meiko, Rookie, TheShy, Wei。

红方首发为 Creme, JackeyLove, Tian, ZUIAN, Zhuo。

冻结时可查 1 个历史小局，10 名首发有历史出场记录。

本局可见 0 手禁选。

## 预测与赛后结算

```
{
  "status": "failed",
  "observed_outcome": {
    "p_blue_win": 0,
    "p_blue_ahead_15": 0
  },
  "reward": 0,
  "error": "lobby: CLI exit 1, HTTP statuses [200, 200, 200, 200, 200, 429]"
}
```

## 执行轨迹

### 1. CLI 诊断

```
Model metadata for `nvidia/nemotron-3.5-lightning:free` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
```

### 2. 终端命令 · 退出码 0

```
/bin/zsh -lc 'cat [ephemeral]/app/snapshot.json'
```

### 3. 命令输出

```
{"phase": "lobby", "series_time_utc": "2026-09-17T09:00:00+00:00", "current": {"event": "lpl-2026-regional-finals", "stage": "Round 1", "series": "lpl-2026-regional-finals-round-1-1", "n": 2, "patch": "26.17", "bo": 5, "blue": "Invictus Gaming", "red": "Top Esports", "starters": {"blue": ["JiaQi", "Meiko", "Rookie", "TheShy", "Wei"], "red": ["Creme", "JackeyLove", "Tian", "ZUIAN", "Zhuo"]}, "draft_rule": "Fearless"}, "history": [{"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": true, "blue_gd15": -38, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Syndra"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Renekton"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Jayce"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yorick"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Yorick", "k": 2, "d": 1, "a": 6}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 1, "d": 5, "a": 5}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Syndra", "k": 3, "d": 1, "a": 7}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 5, "d": 5, "a": 4}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Lulu", "k": 0, "d": 0, "a": 10}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Jayce", "k": 1, "d": 1, "a": 5}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Cho'Gath", "k": 1, "d": 6, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Orianna", "k": 7, "d": 0, "a": 1}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Lucian", "k": 2, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion": "Milio", "k": 1, "d": 2, "a": 10}]}], "coverage": {"history_games": 1, "starters": [{"side": "blue", "name": "JiaQi", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Meiko", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Rookie", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "TheShy", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Wei", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Creme", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "JackeyLove", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Tian", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "ZUIAN", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Zhuo", "games": 1, "same_patch_games": 1}], "starters_with_history": 10, "coverage_group": "all", "previous_series_games": [1], "missing_previous_series_games": []}}
```

### 4. 模型消息

```
Now I have the snapshot data. Let me analyze the key information:

**Current game**: Game 2 of best-of-5, LPL Regional Finals, patch 26.17, IG (blue) vs TES (red)
**Game 1 history**: Blue (IG) won, but was behind in gold at 15:00 (-38 GD15 - red was ahead)
**All 10 starters appeared in game 1** on the same patch

Key observations:
- Blue won game 1 despite being down 38 gold at 15:00
- This is game 2 with sides the same (IG blue again)
- Fearless draft mode

Let me make the initial estimates and save them.
```

### 5. 终端命令 · 退出码 0

```
/bin/zsh -lc "echo '{\"p_blue_win\": 0.6, \"p_blue_ahead_15\": 0.45}' > [ephemeral]/app/prediction.json"
```

### 6. 命令输出

```

```

### 7. 终端命令 · 退出码 0

```
/bin/zsh -lc 'cat [ephemeral]/app/prediction.json'
```

### 8. 命令输出

```
{"p_blue_win": 0.6, "p_blue_ahead_15": 0.45}
```

### 9. 模型消息

```
The prediction file has been created with both required fields:

- **`p_blue_win`**: 0.6 — Blue side (Invictus Gaming) wins the game. In game 1, IG won despite being down 38 gold at 15:00, demonstrating comeback capability. With the same teams/patch in game 2 (same blue side), blue has a slight edge.
- **`p_blue_ahead_15`**: 0.45 — Blue has strictly more team gold at 15:00. Game 1 showed red starting stronger (blue trailed by 38 gold), but blue's ability to come back keeps this probability above 0.5.

Both values are finite numbers between 0 and 1, and the file is saved to `./prediction.json`.
```

### 10. 终端命令 · 退出码 0

```
/bin/zsh -lc 'cat [ephemeral]/app/prediction.json'
```

### 11. 命令输出

```
{"p_blue_win": 0.6, "p_blue_ahead_15": 0.45}
```

### 12. error

```
{
  "type": "error",
  "message": "exceeded retry limit, last status: 429 Too Many Requests"
}
```

### 13. turn.failed

```
{
  "type": "turn.failed",
  "error": {
    "message": "exceeded retry limit, last status: 429 Too Many Requests"
  }
}
```
