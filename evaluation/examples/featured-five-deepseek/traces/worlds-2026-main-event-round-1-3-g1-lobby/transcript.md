# Movistar KOI vs Bilibili Gaming · G1 · BP 前

worlds-2026-main-event · Round 1 · 26.20 · BO1

[实际题面](instruction.md) · [可查询的完整快照](snapshot.json) · [原始事件 JSONL](../../jobs/worlds-2026-main-event-round-1-3-g1-lobby/trajectory.jsonl) · [stderr](../../jobs/worlds-2026-main-event-round-1-3-g1-lobby/stderr.txt) · [交卷文件](../../jobs/worlds-2026-main-event-round-1-3-g1-lobby/prediction.json)

## 输入与可查询证据

蓝方首发为 Alvaro, Elyoya, Jojopyun, Myrwn, Supa。

红方首发为 Bin, Knight, ON, Viper, Xun。

冻结时可查 34 个历史小局，0 名首发有历史出场记录。

本局可见 0 手禁选。

## 预测与赛后结算

```
{
  "status": "scored",
  "prediction": {
    "p_blue_win": 0.19,
    "p_blue_ahead_15": 0.24
  },
  "observed_outcome": {
    "p_blue_win": 1,
    "p_blue_ahead_15": 1
  },
  "brier": {
    "p_blue_win": 0.6561000000000001,
    "p_blue_ahead_15": 0.5776
  },
  "reward": 0.3831499999999999
}
```

## CLI 报告的 token 用量

```
{
  "input_tokens": 61408,
  "cached_input_tokens": 56832,
  "cache_write_input_tokens": 0,
  "output_tokens": 2930,
  "reasoning_output_tokens": 1626
}
```

## 执行轨迹

### 1. CLI 诊断

```
Model metadata for `deepseek-v4-pro` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
```

### 2. 终端命令 · 退出码 0

```
/bin/zsh -c 'cat ./snapshot.json | head -c 3000'
```

### 3. 命令输出

```
{"phase": "lobby", "series_time_utc": "2026-10-23T19:00:00+00:00", "current": {"event": "worlds-2026-main-event", "stage": "Round 1", "series": "worlds-2026-main-event-round-1-3", "n": 1, "patch": "26.20", "bo": 1, "blue": "Movistar KOI", "red": "Bilibili Gaming", "starters": {"blue": ["Alvaro", "Elyoya", "Jojopyun", "Myrwn", "Supa"], "red": ["Bin", "Knight", "ON", "Viper", "Xun"]}, "draft_rule": "Fearless"}, "history": [{"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": true, "blue_gd15": -38, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Syndra"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Renekton"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Jayce"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yorick"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Yorick", "k": 2, "d": 1, "a": 6}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 1, "d": 5, "a": 5}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Syndra", "k": 3, "d": 1, "a": 7}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 5, "d": 5, "a": 4}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Lulu", "k": 0, "d": 0, "a": 10}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Jayce", "k": 1, "d": 1, "a": 5}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Cho'Gath", "k": 1, "d": 6, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Orianna", "k": 7, "d": 0, "a": 1}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Lucian", "k": 2, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion
```

### 4. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json
d=json.load(open('snapshot.json'))
print('keys', list(d.keys()))
print('coverage', json.dumps(d['coverage'], indent=2))
print('current', json.dumps(d['current'], indent=2))
print('n history', len(d['history']))
for h in d['history']:
    print(h['series'], h.get('blue'), 'vs', h.get('red'), 'patch', h.get('patch'), 'win', h.get('blue_win'), 'gd15', h.get('blue_gd15'))
\""
```

### 5. 命令输出

```
keys ['phase', 'series_time_utc', 'current', 'history', 'coverage']
coverage {
  "history_games": 34,
  "starters": [
    {
      "side": "blue",
      "name": "Alvaro",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "blue",
      "name": "Elyoya",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "blue",
      "name": "Jojopyun",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "blue",
      "name": "Myrwn",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "blue",
      "name": "Supa",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "red",
      "name": "Bin",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "red",
      "name": "Knight",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "red",
      "name": "ON",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "red",
      "name": "Viper",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "red",
      "name": "Xun",
      "games": 0,
      "same_patch_games": 0
    }
  ],
  "starters_with_history": 0,
  "coverage_group": "none",
  "previous_series_games": [],
  "missing_previous_series_games": []
}
current {
  "event": "worlds-2026-main-event",
  "stage": "Round 1",
  "series": "worlds-2026-main-event-round-1-3",
  "n": 1,
  "patch": "26.20",
  "bo": 1,
  "blue": "Movistar KOI",
  "red": "Bilibili Gaming",
  "starters": {
    "blue": [
      "Alvaro",
      "Elyoya",
      "Jojopyun",
      "Myrwn",
      "Supa"
    ],
    "red": [
      "Bin",
      "Knight",
      "ON",
      "Viper",
      "Xun"
    ]
  },
  "draft_rule": "Fearless"
}
n history 34
lpl-2026-regional-finals-round-1-1 Invictus Gaming vs Top Esports patch 26.17 win True gd15 -38
lpl-2026-regional-finals-round-1-1 Invictus Gaming vs Top Esports patch 26.17 win False gd15 -1351
lpl-2026-regional-finals-round-1-1 Top Esports vs Invictus Gaming patch 26.17 win True gd15 2775
lpl-2026-regional-finals-round-1-1 Top Esports vs Invictus Gaming patch 26.17 win True gd15 898
lpl-2026-regional-finals-round-1-2 Team WE vs JD Gaming patch 26.17 win True gd15 -3500
lpl-2026-regional-finals-round-1-2 JD Gaming vs Team WE patch 26.17 win True gd15 3715
lpl-2026-regional-finals-round-1-2 Team WE vs JD Gaming patch 26.17 win False gd15 -2080
lpl-2026-regional-finals-round-1-2 JD Gaming vs Team WE patch 26.17 win True gd15 -1804
lpl-2026-regional-finals-round-2-1 JD Gaming vs Invictus Gaming patch 26.17 win False gd15 232
lpl-2026-regional-finals-round-2-1 JD Gaming vs Invictus Gaming patch 26.17 win False gd15 -4965
lpl-2026-regional-finals-round-2-1 Invictus Gaming vs JD Gaming patch 26.17 win False gd15 -423
lpl-2026-regional-finals-round-2-1 JD Gaming vs Invictus Gaming patch 26.17 win False gd15 3731
worlds-2026-play-in-round-1-1 Karmine Corp vs Cloud9 patch 26.20 win False gd15 -1525
worlds-2026-play-in-round-1-1 Cloud9 vs Karmine Corp patch 26.20 win False gd15 395
worlds-2026-play-in-round-1-1 Karmine Corp vs Cloud9 patch 26.20 win False gd15 -236
worlds-2026-play-in-round-1-1 Cloud9 vs Karmine Corp patch 26.20 win False gd15 -4476
worlds-2026-play-in-round-1-1 Karmine Corp vs Cloud9 patch 26.20 win True gd15 622
worlds-2026-play-in-round-1-2 MVK Esports vs FURIA patch 26.20 win True gd15 -947
worlds-2026-play-in-round-1-2 MVK Esports vs FURIA patch 26.20 win True gd15 2286
worlds-2026-play-in-round-1-2 MVK Esports vs FURIA patch 26.20 win True gd15 5303
worlds-2026-play-in-round-2-1 Karmine Corp vs MVK Esports patch 26.20 win True gd15 3377
worlds-2026-play-in-round-2-1 Karmine Corp vs MVK Esports patch 26.20 win True gd15 -3003
worlds-2026-play-in-round-2-1 MVK Esports vs Karmine Corp patch 26.20 win False gd15 -2837
worlds-2026-play-in-round-1-3 FURIA vs Cloud9 patch 26.20 win False gd15 -1173
worlds-2026-play-in-round-1-3 Cloud9 vs FURIA patch 26.20 win False gd15 1875
worlds-2026-play-in-round-1-3 FURIA vs Cloud9 patch 26.20 win True gd15 -432
worlds-2026-play-in-round-1-3 FURIA vs Cloud9 patch 26.20 win True gd15 -678
worlds-2026-play-in-round-2-2 MVK Esports vs FURIA patch 26.20 win True gd15 3139
worlds-2026-play-in-round-2-2 MVK Esports vs FURIA patch 26.20 win True gd15 1704
worlds-2026-play-in-round-2-2 MVK Esports vs FURIA patch 26.20 win False gd15 -2091
worlds-2026-play-in-round-2-2 MVK Esports vs FURIA patch 26.20 win True gd15 3077
worlds-2026-play-in-round-3-1 Karmine Corp vs MVK Esports patch 26.20 win True gd15 3288
worlds-2026-play-in-round-3-1 Karmine Corp vs MVK Esports patch 26.20 win True gd15 6558
worlds-2026-play-in-round-3-1 MVK Esports vs Karmine Corp patch 26.20 win False gd15 -2294
```

### 6. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json
pred={'p_blue_win':0.20,'p_blue_ahead_15':0.26}
json.dump(pred, open('prediction.json','w'))
print(open('prediction.json').read())
\""
```

### 7. 命令输出

```
{"p_blue_win": 0.2, "p_blue_ahead_15": 0.26}
```

### 8. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json
pred={'p_blue_win':0.19,'p_blue_ahead_15':0.24}
json.dump(pred, open('prediction.json','w'))
print(open('prediction.json').read())
\""
```

### 9. 命令输出

```
{"p_blue_win": 0.19, "p_blue_ahead_15": 0.24}
```

### 10. 模型消息

```
Wrote `./prediction.json` with `p_blue_win: 0.19` and `p_blue_ahead_15: 0.24`.

**Reasoning**
- No starter in this game has any recorded appearance in the 34-game history (coverage `none`), so there is no direct player/team sample to aggregate.
- I relied on general team strength: Bilibili Gaming (Bin, Xun, Knight, Viper, ON) is an elite LPL roster and heavy favorite over Movistar KOI in a Worlds BO1, even with blue-side advantage and BO1 variance.
- Set KOI's win probability modestly above pure "talent gap" to account for BO1 upset risk, and `p_blue_ahead_15` slightly higher since underdogs can hold early gold leads without converting.
```
