# Movistar KOI vs Bilibili Gaming · G1 · BP 锁定

worlds-2026-main-event · Round 1 · 26.20 · BO1

[实际题面](instruction.md) · [可查询的完整快照](snapshot.json) · [原始事件 JSONL](../../jobs/worlds-2026-main-event-round-1-3-g1-draft-lock/trajectory.jsonl) · [stderr](../../jobs/worlds-2026-main-event-round-1-3-g1-draft-lock/stderr.txt) · [交卷文件](../../jobs/worlds-2026-main-event-round-1-3-g1-draft-lock/prediction.json)

## 输入与可查询证据

蓝方首发为 Alvaro, Elyoya, Jojopyun, Myrwn, Supa。

红方首发为 Bin, Knight, ON, Viper, Xun。

冻结时可查 34 个历史小局，0 名首发有历史出场记录。

本局可见 20 手禁选。

## 预测与赛后结算

```
{
  "status": "scored",
  "prediction": {
    "p_blue_win": 0.13,
    "p_blue_ahead_15": 0.22
  },
  "observed_outcome": {
    "p_blue_win": 1,
    "p_blue_ahead_15": 1
  },
  "brier": {
    "p_blue_win": 0.7569,
    "p_blue_ahead_15": 0.6084
  },
  "reward": 0.31735
}
```

## CLI 报告的 token 用量

```
{
  "input_tokens": 7719,
  "cache_creation_input_tokens": 0,
  "cache_read_input_tokens": 33408,
  "output_tokens": 3539
}
```

## 执行轨迹

### 1. 终端命令

```
ls -la && python3 -c "import json; d=json.load(open('snapshot.json')); print(json.dumps(d['current'], indent=2))"
```

### 2. 命令结果

```
total 184
drwxr-xr-x@ 3 [local-user]  [local-group]     96 Nov  9 01:58 .
drwx------@ 8 [local-user]  [local-group]    256 Nov  9 01:58 ..
-rw-r--r--@ 1 [local-user]  [local-group]  91154 Nov  9 01:58 snapshot.json
{
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
  "draft_rule": "Fearless",
  "bp": [
    {
      "turn": 1,
      "side": "red",
      "action": "ban",
      "champion": "Galio"
    },
    {
      "turn": 2,
      "side": "blue",
      "action": "ban",
      "champion": "Vi"
    },
    {
      "turn": 3,
      "side": "red",
      "action": "ban",
      "champion": "Nocturne"
    },
    {
      "turn": 4,
      "side": "blue",
      "action": "ban",
      "champion": "Rumble"
    },
    {
      "turn": 5,
      "side": "red",
      "action": "ban",
      "champion": "Qiyana"
    },
    {
      "turn": 6,
      "side": "blue",
      "action": "ban",
      "champion": "Cassiopeia"
    },
    {
      "turn": 7,
      "side": "red",
      "action": "pick",
      "champion": "Seraphine"
    },
    {
      "turn": 8,
      "side": "blue",
      "action": "pick",
      "champion": "Jarvan IV"
    },
    {
      "turn": 9,
      "side": "blue",
      "action": "pick",
      "champion": "Ezreal"
    },
    {
      "turn": 10,
      "side": "red",
      "action": "pick",
      "champion": "Ashe"
    },
    {
      "turn": 11,
      "side": "red",
      "action": "pick",
      "champion": "Akali"
    },
    {
      "turn": 12,
      "side": "blue",
      "action": "pick",
      "champion": "Karma"
    },
    {
      "turn": 13,
      "side": "blue",
      "action": "ban",
      "champion": "Lee Sin"
    },
    {
      "turn": 14,
      "side": "red",
      "action": "ban",
      "champion": "Twisted Fate"
    },
    {
      "turn": 15,
      "side": "blue",
      "action": "ban",
      "champion": "Skarner"
    },
    {
      "turn": 16,
      "side": "red",
      "action": "ban",
      "champion": "Olaf"
    },
    {
      "turn": 17,
      "side": "blue",
      "action": "pick",
      "champion": "Sylas"
    },
    {
      "turn": 18,
      "side": "red",
      "action": "pick",
      "champion": "Pantheon"
    },
    {
      "turn": 19,
      "side": "red",
      "action": "pick",
      "champion": "Ambessa"
    },
    {
      "turn": 20,
      "side": "blue",
      "action": "pick",
      "champion": "Renekton"
    }
  ]
}
```

### 3. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
print('COVERAGE:', json.dumps(d.get('coverage'), indent=2))
h=d['history']
print('num history', len(h))
print('keys sample:', list(h[0].keys()))
"
```

### 4. 命令结果

```
COVERAGE: {
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
num history 34
keys sample: ['series', 'series_time', 'event', 'n', 'patch', 'blue', 'red', 'blue_win', 'blue_gd15', 'bp', 'players']
```

### 5. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
h=d['history']
for i,g in enumerate(h):
    print(i, g['patch'], g['blue'], 'vs', g['red'], 'blue_win=',g['blue_win'], 'gd15=',g.get('blue_gd15'))
"
```

### 6. 命令结果

```
0 26.17 Invictus Gaming vs Top Esports blue_win= True gd15= -38
1 26.17 Invictus Gaming vs Top Esports blue_win= False gd15= -1351
2 26.17 Top Esports vs Invictus Gaming blue_win= True gd15= 2775
3 26.17 Top Esports vs Invictus Gaming blue_win= True gd15= 898
4 26.17 Team WE vs JD Gaming blue_win= True gd15= -3500
5 26.17 JD Gaming vs Team WE blue_win= True gd15= 3715
6 26.17 Team WE vs JD Gaming blue_win= False gd15= -2080
7 26.17 JD Gaming vs Team WE blue_win= True gd15= -1804
8 26.17 JD Gaming vs Invictus Gaming blue_win= False gd15= 232
9 26.17 JD Gaming vs Invictus Gaming blue_win= False gd15= -4965
10 26.17 Invictus Gaming vs JD Gaming blue_win= False gd15= -423
11 26.17 JD Gaming vs Invictus Gaming blue_win= False gd15= 3731
12 26.20 Karmine Corp vs Cloud9 blue_win= False gd15= -1525
13 26.20 Cloud9 vs Karmine Corp blue_win= False gd15= 395
14 26.20 Karmine Corp vs Cloud9 blue_win= False gd15= -236
15 26.20 Cloud9 vs Karmine Corp blue_win= False gd15= -4476
16 26.20 Karmine Corp vs Cloud9 blue_win= True gd15= 622
17 26.20 MVK Esports vs FURIA blue_win= True gd15= -947
18 26.20 MVK Esports vs FURIA blue_win= True gd15= 2286
19 26.20 MVK Esports vs FURIA blue_win= True gd15= 5303
20 26.20 Karmine Corp vs MVK Esports blue_win= True gd15= 3377
21 26.20 Karmine Corp vs MVK Esports blue_win= True gd15= -3003
22 26.20 MVK Esports vs Karmine Corp blue_win= False gd15= -2837
23 26.20 FURIA vs Cloud9 blue_win= False gd15= -1173
24 26.20 Cloud9 vs FURIA blue_win= False gd15= 1875
25 26.20 FURIA vs Cloud9 blue_win= True gd15= -432
26 26.20 FURIA vs Cloud9 blue_win= True gd15= -678
27 26.20 MVK Esports vs FURIA blue_win= True gd15= 3139
28 26.20 MVK Esports vs FURIA blue_win= True gd15= 1704
29 26.20 MVK Esports vs FURIA blue_win= False gd15= -2091
30 26.20 MVK Esports vs FURIA blue_win= True gd15= 3077
31 26.20 Karmine Corp vs MVK Esports blue_win= True gd15= 3288
32 26.20 Karmine Corp vs MVK Esports blue_win= True gd15= 6558
33 26.20 MVK Esports vs Karmine Corp blue_win= False gd15= -2294
```

### 7. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
h=d['history']
bw=sum(1 for g in h if g['blue_win'])
print('blue wins', bw, 'of', len(h), '=', bw/len(h))
p26=[g for g in h if g['patch']=='26.20']
bw26=sum(1 for g in p26 if g['blue_win'])
print('patch 26.20 blue wins', bw26, 'of', len(p26), '=', bw26/len(p26))
ahead=sum(1 for g in h if (g.get('blue_gd15') or 0)>0)
print('blue ahead15', ahead, 'of', sum(1 for g in h if g.get('blue_gd15') is not None))
# players sample to confirm none match
for g in h[:2]:
    print(g['players'])
"
```

### 8. 命令结果

```
blue wins 19 of 34 = 0.5588235294117647
patch 26.20 blue wins 13 of 22 = 0.5909090909090909
blue ahead15 16 of 34
[{'name': 'TheShy', 'role': 'Top', 'side': 'blue', 'champion': 'Yorick', 'k': 2, 'd': 1, 'a': 6}, {'name': 'Wei', 'role': 'Jungle', 'side': 'blue', 'champion': 'Skarner', 'k': 1, 'd': 5, 'a': 5}, {'name': 'Rookie', 'role': 'Mid', 'side': 'blue', 'champion': 'Syndra', 'k': 3, 'd': 1, 'a': 7}, {'name': 'JiaQi', 'role': 'Bot', 'side': 'blue', 'champion': 'Yunara', 'k': 5, 'd': 5, 'a': 4}, {'name': 'Meiko', 'role': 'Support', 'side': 'blue', 'champion': 'Lulu', 'k': 0, 'd': 0, 'a': 10}, {'name': 'ZUIAN', 'role': 'Top', 'side': 'red', 'champion': 'Jayce', 'k': 1, 'd': 1, 'a': 5}, {'name': 'Tian', 'role': 'Jungle', 'side': 'red', 'champion': "Cho'Gath", 'k': 1, 'd': 6, 'a': 6}, {'name': 'Creme', 'role': 'Mid', 'side': 'red', 'champion': 'Orianna', 'k': 7, 'd': 0, 'a': 1}, {'name': 'JackeyLove', 'role': 'Bot', 'side': 'red', 'champion': 'Lucian', 'k': 2, 'd': 2, 'a': 7}, {'name': 'Zhuo', 'role': 'Support', 'side': 'red', 'champion': 'Milio', 'k': 1, 'd': 2, 'a': 10}]
[{'name': 'TheShy', 'role': 'Top', 'side': 'blue', 'champion': 'Camille', 'k': 1, 'd': 6, 'a': 2}, {'name': 'Wei', 'role': 'Jungle', 'side': 'blue', 'champion': 'Maokai', 'k': 1, 'd': 2, 'a': 6}, {'name': 'Rookie', 'role': 'Mid', 'side': 'blue', 'champion': 'Yone', 'k': 1, 'd': 2, 'a': 4}, {'name': 'JiaQi', 'role': 'Bot', 'side': 'blue', 'champion': 'Ashe', 'k': 4, 'd': 3, 'a': 1}, {'name': 'Meiko', 'role': 'Support', 'side': 'blue', 'champion': 'Seraphine', 'k': 1, 'd': 1, 'a': 6}, {'name': 'ZUIAN', 'role': 'Top', 'side': 'red', 'champion': 'Olaf', 'k': 7, 'd': 2, 'a': 3}, {'name': 'Tian', 'role': 'Jungle', 'side': 'red', 'champion': 'Lee Sin', 'k': 3, 'd': 3, 'a': 6}, {'name': 'Creme', 'role': 'Mid', 'side': 'red', 'champion': 'Ryze', 'k': 2, 'd': 0, 'a': 6}, {'name': 'JackeyLove', 'role': 'Bot', 'side': 'red', 'champion': 'Ezreal', 'k': 1, 'd': 2, 'a': 7}, {'name': 'Zhuo', 'role': 'Support', 'side': 'red', 'champion': 'Karma', 'k': 1, 'd': 1, 'a': 8}]
```

### 9. 工具调用 · Write

```
{
  "file_path": "[ephemeral]/app/prediction.json",
  "content": "{\n  \"p_blue_win\": 0.13,\n  \"p_blue_ahead_15\": 0.22\n}\n"
}
```

### 10. 工具结果

```
File created successfully at: [ephemeral]/app/prediction.json (file state is current in your context — no need to Read it back)
```

### 11. 模型消息

```
Prediction written to `./prediction.json`.

**Reasoning:**

- **No direct evidence:** Every starter on both sides has 0 recorded appearances in the 34-game history — the `coverage` group is "none". The history is other regions/teams (LPL on 26.17, plus Karmine Corp / Cloud9 / MVK / FURIA on 26.20), so it only establishes a loose blue-side baseline (~56–59% overall), not team strength here.
- **Massive roster gap:** Bilibili Gaming fields an elite LPL superteam (Bin, Xun, Knight, Viper, ON), while Movistar KOI is a mid-tier LEC roster (Myrwn, Elyoya, Jojopyun, Supa, Alvaro). In a best-of-1 at Worlds, BLG should win the large majority of the time.
- **Draft:** KOI's comp (Renekton/Jarvan IV/Sylas/Ezreal/Karma) is early-game oriented, which slightly raises the chance they're ahead at 15:00 relative to winning outright, but gold@15 remains dominated by the skill gap. Blue-side map advantage is minor and can't close it.

Final estimates:
- `p_blue_win`: **0.13**
- `p_blue_ahead_15`: **0.22**
```
