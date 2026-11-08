# Karmine Corp vs T1 · G2 · BP 前

worlds-2026-main-event · Quarterfinals · 26.20 · BO5

[实际题面](instruction.md) · [可查询的完整快照](snapshot.json) · [原始事件 JSONL](../../jobs/worlds-2026-main-event-quarterfinals-4-g2-lobby/trajectory.jsonl) · [stderr](../../jobs/worlds-2026-main-event-quarterfinals-4-g2-lobby/stderr.txt) · [交卷文件](../../jobs/worlds-2026-main-event-quarterfinals-4-g2-lobby/prediction.json)

## 输入与可查询证据

蓝方首发为 Busio, Caliste, Canna, Kyeahoo, Yike。

红方首发为 Doran, Faker, Keria, Oner, Peyz。

冻结时可查 96 个历史小局，10 名首发有历史出场记录。

本局可见 0 手禁选。

## 预测与赛后结算

```
{
  "status": "scored",
  "prediction": {
    "p_blue_win": 0.4,
    "p_blue_ahead_15": 0.58
  },
  "observed_outcome": {
    "p_blue_win": 0,
    "p_blue_ahead_15": 0
  },
  "brier": {
    "p_blue_win": 0.16000000000000003,
    "p_blue_ahead_15": 0.3364
  },
  "reward": 0.7518
}
```

## CLI 报告的 token 用量

```
{
  "input_tokens": 9033,
  "cache_creation_input_tokens": 0,
  "cache_read_input_tokens": 98304,
  "output_tokens": 9206
}
```

## 执行轨迹

### 1. 终端命令

```
ls -la && cat snapshot.json | head -c 2000
```

### 2. 命令结果

```
total 496
drwxr-xr-x@ 3 [local-user]  [local-group]      96 Nov  9 01:52 .
drwx------@ 8 [local-user]  [local-group]     256 Nov  9 01:52 ..
-rw-r--r--@ 1 [local-user]  [local-group]  251772 Nov  9 01:52 snapshot.json
{"phase": "lobby", "series_time_utc": "2026-11-06T22:00:00+00:00", "current": {"event": "worlds-2026-main-event", "stage": "Quarterfinals", "series": "worlds-2026-main-event-quarterfinals-4", "n": 2, "patch": "26.20", "bo": 5, "blue": "Karmine Corp", "red": "T1", "starters": {"blue": ["Busio", "Caliste", "Canna", "Kyeahoo", "Yike"], "red": ["Doran", "Faker", "Keria", "Oner", "Peyz"]}, "draft_rule": "Fearless"}, "history": [{"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": true, "blue_gd15": -38, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Syndra"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Renekton"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Jayce"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "sid
```

### 3. 终端命令

```
python3 -c "
import json
d = json.load(open('snapshot.json'))
print('TOP KEYS:', list(d.keys()))
print('CURRENT:', json.dumps(d['current'], indent=2))
print('COVERAGE:', json.dumps(d.get('coverage', {}), indent=2))
print('N history:', len(d['history']))
"
```

### 4. 命令结果

```
TOP KEYS: ['phase', 'series_time_utc', 'current', 'history', 'coverage']
CURRENT: {
  "event": "worlds-2026-main-event",
  "stage": "Quarterfinals",
  "series": "worlds-2026-main-event-quarterfinals-4",
  "n": 2,
  "patch": "26.20",
  "bo": 5,
  "blue": "Karmine Corp",
  "red": "T1",
  "starters": {
    "blue": [
      "Busio",
      "Caliste",
      "Canna",
      "Kyeahoo",
      "Yike"
    ],
    "red": [
      "Doran",
      "Faker",
      "Keria",
      "Oner",
      "Peyz"
    ]
  },
  "draft_rule": "Fearless"
}
COVERAGE: {
  "history_games": 96,
  "starters": [
    {
      "side": "blue",
      "name": "Busio",
      "games": 19,
      "same_patch_games": 19
    },
    {
      "side": "blue",
      "name": "Caliste",
      "games": 19,
      "same_patch_games": 19
    },
    {
      "side": "blue",
      "name": "Canna",
      "games": 19,
      "same_patch_games": 19
    },
    {
      "side": "blue",
      "name": "Kyeahoo",
      "games": 19,
      "same_patch_games": 19
    },
    {
      "side": "blue",
      "name": "Yike",
      "games": 19,
      "same_patch_games": 19
    },
    {
      "side": "red",
      "name": "Doran",
      "games": 6,
      "same_patch_games": 6
    },
    {
      "side": "red",
      "name": "Faker",
      "games": 6,
      "same_patch_games": 6
    },
    {
      "side": "red",
      "name": "Keria",
      "games": 6,
      "same_patch_games": 6
    },
    {
      "side": "red",
      "name": "Oner",
      "games": 6,
      "same_patch_games": 6
    },
    {
      "side": "red",
      "name": "Peyz",
      "games": 6,
      "same_patch_games": 6
    }
  ],
  "starters_with_history": 10,
  "coverage_group": "all",
  "previous_series_games": [
    1
  ],
  "missing_previous_series_games": []
}
N history: 96
```

### 5. 终端命令

```
python3 -c "
import json
d = json.load(open('snapshot.json'))
h = d['history']
# Aggregate by team (blue/red side) win rates and gd15
from collections import defaultdict
teams = defaultdict(lambda: {'w':0,'l':0,'gd15':[],'blue_w':0,'blue_n':0,'red_w':0,'red_n':0})
for g in h:
    b = g['blue']; r = g['red']
    bw = g.get('blue_win')
    if bw is None:
        continue
    gd = g.get('blue_gd15')
    for side, name in [('blue', b), ('red', r)]:
        t = teams[name]
        won = (side=='blue' and bw) or (side=='red' and not bw)
        t['w'] += 1 if won else 0
        t['l'] += 0 if won else 1
        if side=='blue':
            t['blue_n'] += 1
            t['blue_w'] += 1 if bw else 0
        else:
            t['red_n'] += 1
            t['red_w'] += 1 if not bw else 0
        if gd is not None:
            if side=='blue':
                t['gd15'].append(gd)
            else:
                t['gd15'].append(-gd)
for name,t in sorted(teams.items(), key=lambda x:-x[1]['w']):
    import statistics
    gd = t['gd15']
    print(f'{name}: W-L {t[\"w\"]}-{t[\"l\"]} ({t[\"w\"]/(t[\"w\"]+t[\"l\"]):.3f}), blue {t[\"blue_w\"]}/{t[\"blue_n\"]}, red {t[\"red_w\"]}/{t[\"red_n\"]}, gd15 mean {statistics.mean(gd):.0f} n={len(gd)}')
"
```

### 6. 命令结果

```
Karmine Corp: W-L 14-5 (0.737), blue 9/12, red 5/7, gd15 mean 1184 n=19
Invictus Gaming: W-L 11-7 (0.611), blue 4/9, red 7/9, gd15 mean 576 n=18
Top Esports: W-L 8-6 (0.571), blue 5/7, red 3/7, gd15 mean -78 n=14
Bilibili Gaming: W-L 8-3 (0.727), blue 5/6, red 3/5, gd15 mean 239 n=11
Gen.G: W-L 7-1 (0.875), blue 5/5, red 2/3, gd15 mean 498 n=8
MVK Esports: W-L 6-7 (0.462), blue 6/9, red 0/4, gd15 mean -222 n=13
LYON: W-L 6-8 (0.429), blue 3/6, red 3/8, gd15 mean -995 n=14
LØS: W-L 5-5 (0.500), blue 1/5, red 4/5, gd15 mean 210 n=10
T1: W-L 5-1 (0.833), blue 4/4, red 1/2, gd15 mean 1087 n=6
JD Gaming: W-L 4-4 (0.500), blue 2/5, red 2/3, gd15 mean 864 n=8
FURIA: W-L 4-7 (0.364), blue 2/3, red 2/8, gd15 mean -1512 n=11
Dplus Kia: W-L 4-3 (0.571), blue 3/5, red 1/2, gd15 mean -76 n=7
Cloud9: W-L 3-6 (0.333), blue 0/3, red 3/6, gd15 mean 135 n=9
Hanwha Life Esports: W-L 3-4 (0.429), blue 1/2, red 2/5, gd15 mean -299 n=7
Team Liquid: W-L 3-4 (0.429), blue 1/4, red 2/3, gd15 mean 111 n=7
Movistar KOI: W-L 2-6 (0.250), blue 2/3, red 0/5, gd15 mean -1581 n=8
Team WE: W-L 1-3 (0.250), blue 1/2, red 0/2, gd15 mean -1873 n=4
G2 Esports: W-L 1-4 (0.200), blue 0/1, red 1/4, gd15 mean 626 n=5
CTBC Flying Oyster: W-L 1-4 (0.200), blue 0/1, red 1/4, gd15 mean 531 n=5
Anyone's Legend: W-L 0-4 (0.000), blue 0/1, red 0/3, gd15 mean -1128 n=4
Team Secret Whales: W-L 0-4 (0.000), blue 0/3, red 0/1, gd15 mean -243 n=4
```

### 7. 终端命令

```
python3 -c "
import json
d = json.load(open('snapshot.json'))
h = d['history']
cur = d['current']
# find games in this series
for g in h:
    if g.get('series') == cur['series']:
        print('SERIES GAME', g['n'], 'blue', g['blue'], 'red', g['red'], 'blue_win', g.get('blue_win'), 'gd15', g.get('blue_gd15'), 'patch', g.get('patch'))
        if 'bp' in g:
            picks = [bp for bp in g['bp'] if bp['action']=='pick']
            bans = [bp for bp in g['bp'] if bp['action']=='ban']
            print('  blue picks:', [p['champion'] for p in picks if p['side']=='blue'])
            print('  red picks:', [p['champion'] for p in picks if p['side']=='red'])
            print('  blue bans:', [b['champion'] for b in bans if b['side']=='blue'])
            print('  red bans:', [b['champion'] for b in bans if b['side']=='red'])
"
```

### 8. 命令结果

```
SERIES GAME 1 blue T1 red Karmine Corp blue_win True gd15 -660 patch 26.20
  blue picks: ['Lulu', 'Jarvan IV', 'Yunara', 'Ornn', 'Viktor']
  red picks: ['Rumble', 'Ezreal', 'Leona', 'Syndra', 'Lee Sin']
  blue bans: ['Cassiopeia', 'Vi', 'Qiyana', 'Wukong', 'Pantheon']
  red bans: ['Nocturne', 'Renata Glasc', 'Galio', 'Locke', 'Orianna']
```

### 9. 终端命令

```
python3 -c "
import json
d = json.load(open('snapshot.json'))
h = d['history']
cur = d['current']
print('=== T1 games ===')
for g in h:
    if g['blue']=='T1' or g['red']=='T1':
        side = 'blue' if g['blue']=='T1' else 'red'
        opp = g['red'] if side=='blue' else g['blue']
        won = (side=='blue' and g.get('blue_win')) or (side=='red' and g.get('blue_win') is False)
        gd = g.get('blue_gd15')
        if side=='red': gd = -gd if gd is not None else None
        print(f'{g[\"event\"]} {g[\"series\"]} n{g[\"n\"]} patch{g[\"patch\"]} T1={side} vs {opp} won={won} gd15={gd}')
"
```

### 10. 命令结果

```
=== T1 games ===
worlds-2026-main-event worlds-2026-main-event-round-1-7 n1 patch26.20 T1=red vs LØS won=True gd15=2368
worlds-2026-main-event worlds-2026-main-event-round-2-7 n1 patch26.20 T1=red vs Dplus Kia won=False gd15=3024
worlds-2026-main-event worlds-2026-main-event-round-3-5 n1 patch26.20 T1=blue vs CTBC Flying Oyster won=True gd15=-1582
worlds-2026-main-event worlds-2026-main-event-round-4-1 n1 patch26.20 T1=blue vs Movistar KOI won=True gd15=-138
worlds-2026-main-event worlds-2026-main-event-round-4-1 n2 patch26.20 T1=blue vs Movistar KOI won=True gd15=3510
worlds-2026-main-event worlds-2026-main-event-quarterfinals-4 n1 patch26.20 T1=blue vs Karmine Corp won=True gd15=-660
```

### 11. 终端命令

```
python3 -c "
import json
d = json.load(open('snapshot.json'))
h = d['history']
cur = d['current']
print('=== KC games ===')
for g in h:
    if g['blue']=='Karmine Corp' or g['red']=='Karmine Corp':
        side = 'blue' if g['blue']=='Karmine Corp' else 'red'
        opp = g['red'] if side=='blue' else g['blue']
        won = (side=='blue' and g.get('blue_win')) or (side=='red' and g.get('blue_win') is False)
        gd = g.get('blue_gd15')
        if side=='red': gd = -gd if gd is not None else None
        print(f'{g[\"event\"]} {g[\"series\"]} n{g[\"n\"]} p{g[\"patch\"]} KC={side} vs {opp} won={won} gd15={gd}')
"
```

### 12. 命令结果

```
=== KC games ===
worlds-2026-play-in worlds-2026-play-in-round-1-1 n1 p26.20 KC=blue vs Cloud9 won=False gd15=-1525
worlds-2026-play-in worlds-2026-play-in-round-1-1 n2 p26.20 KC=red vs Cloud9 won=True gd15=-395
worlds-2026-play-in worlds-2026-play-in-round-1-1 n3 p26.20 KC=blue vs Cloud9 won=False gd15=-236
worlds-2026-play-in worlds-2026-play-in-round-1-1 n4 p26.20 KC=red vs Cloud9 won=True gd15=4476
worlds-2026-play-in worlds-2026-play-in-round-1-1 n5 p26.20 KC=blue vs Cloud9 won=True gd15=622
worlds-2026-play-in worlds-2026-play-in-round-2-1 n1 p26.20 KC=blue vs MVK Esports won=True gd15=3377
worlds-2026-play-in worlds-2026-play-in-round-2-1 n2 p26.20 KC=blue vs MVK Esports won=True gd15=-3003
worlds-2026-play-in worlds-2026-play-in-round-2-1 n3 p26.20 KC=red vs MVK Esports won=True gd15=2837
worlds-2026-play-in worlds-2026-play-in-round-3-1 n1 p26.20 KC=blue vs MVK Esports won=True gd15=3288
worlds-2026-play-in worlds-2026-play-in-round-3-1 n2 p26.20 KC=blue vs MVK Esports won=True gd15=6558
worlds-2026-play-in worlds-2026-play-in-round-3-1 n3 p26.20 KC=red vs MVK Esports won=True gd15=2294
worlds-2026-main-event worlds-2026-main-event-round-1-4 n1 p26.20 KC=blue vs Anyone's Legend won=True gd15=-461
worlds-2026-main-event worlds-2026-main-event-round-2-4 n1 p26.20 KC=blue vs LYON won=False gd15=2170
worlds-2026-main-event worlds-2026-main-event-round-3-6 n1 p26.20 KC=red vs Bilibili Gaming won=False gd15=-1055
worlds-2026-main-event worlds-2026-main-event-round-4-3 n1 p26.20 KC=blue vs CTBC Flying Oyster won=True gd15=1279
worlds-2026-main-event worlds-2026-main-event-round-4-3 n2 p26.20 KC=red vs CTBC Flying Oyster won=True gd15=-3870
worlds-2026-main-event worlds-2026-main-event-round-5-1 n1 p26.20 KC=blue vs Movistar KOI won=True gd15=1380
worlds-2026-main-event worlds-2026-main-event-round-5-1 n2 p26.20 KC=blue vs Movistar KOI won=True gd15=4093
worlds-2026-main-event worlds-2026-main-event-quarterfinals-4 n1 p26.20 KC=red vs T1 won=False gd15=660
```

### 13. 终端命令

```
python3 -c "
import json, statistics
d = json.load(open('snapshot.json'))
h = d['history']
cur = d['current']
# For KC: blue-side gd15 (blue_gd15 raw, positive=KC ahead)
kc_blue = []
kc_red = []
t1_red = []
t1_blue = []
for g in h:
    b, r = g['blue'], g['red']
    gd = g.get('blue_gd15')
    if gd is None: continue
    if b=='Karmine Corp':
        kc_blue.append(gd)  # KC ahead = +gd
    if r=='Karmine Corp':
        kc_red.append(-gd)  # KC ahead = -gd
    if r=='T1':
        t1_red.append(-gd)  # T1 ahead = -gd
    if b=='T1':
        t1_blue.append(gd)
def s(x):
    if not x: return 'n/a'
    return f'mean {statistics.mean(x):.0f} ahead15 {sum(1 for v in x if v>0)}/{len(x)}'
print('KC blue gd15 (KC ahead):', s(kc_blue), kc_blue)
print('KC red gd15 (KC ahead):', s(kc_red), kc_red)
print('T1 red gd15 (T1 ahead):', s(t1_red), t1_red)
print('T1 blue gd15 (T1 ahead):', s(t1_blue), t1_blue)
"
```

### 14. 命令结果

```
KC blue gd15 (KC ahead): mean 1462 ahead15 8/12 [-1525, -236, 622, 3377, -3003, 3288, 6558, -461, 2170, 1279, 1380, 4093]
KC red gd15 (KC ahead): mean 707 ahead15 4/7 [-395, 4476, 2837, 2294, -1055, -3870, 660]
T1 red gd15 (T1 ahead): mean 2696 ahead15 2/2 [2368, 3024]
T1 blue gd15 (T1 ahead): mean 282 ahead15 1/4 [-1582, -138, 3510, -660]
```

### 15. 终端命令

```
python3 -c "
import json
d = json.load(open('snapshot.json'))
h = d['history']
bw = [g['blue_win'] for g in h if g.get('blue_win') is not None]
print('overall blue win rate:', sum(bw)/len(bw), 'n=', len(bw))
gd = [g['blue_gd15'] for g in h if g.get('blue_gd15') is not None]
print('overall blue ahead15 rate:', sum(1 for x in gd if x>0)/len(gd), 'n=', len(gd))
"
```

### 16. 命令结果

```
overall blue win rate: 0.5625 n= 96
overall blue ahead15 rate: 0.5208333333333334 n= 96
```

### 17. 工具调用 · Write

```
{
  "file_path": "[ephemeral]/app/prediction.json",
  "content": "{\n  \"p_blue_win\": 0.40,\n  \"p_blue_ahead_15\": 0.58\n}\n"
}
```

### 18. 工具结果

```
File created successfully at: [ephemeral]/app/prediction.json (file state is current in your context — no need to Read it back)
```

### 19. 终端命令

```
python3 -c "import json; d=json.load(open('prediction.json')); print(d); assert set(d)=={'p_blue_win','p_blue_ahead_15'}; assert all(isinstance(v,(int,float)) and 0<=v<=1 for v in d.values()); print('valid')"
```

### 20. 命令结果

```
{'p_blue_win': 0.4, 'p_blue_ahead_15': 0.58}
valid
```

### 21. 模型消息

````
I've analyzed the snapshot and saved my forecast.

**Key evidence:**

- **Game 1 (this series):** T1 (blue) beat Karmine Corp, coming back from a −660 gold deficit at 15:00 — T1 won despite KC having the early lead.
- **T1:** 5–1 overall (0.833), beating LØS, CTBC, Movistar KOI ×2, and KC. Only loss was to Dplus Kia (after being +3k at 15). T1 was *behind* at 15 in 3 of 6 games — they're a late-game team.
- **KC:** 14–5 overall, but almost entirely against weak opponents (Cloud9, MVK, AL, LYON, CTBC, KOI). Their only games vs strong teams (BLG, T1) were both losses. KC's blue-side 9–3 record is inflated by the soft schedule.
- **Early-game:** KC was ahead at 15 in 8/12 blue-side games, and led T1 at 15 in the direct matchup. Baseline blue ahead-15 rate in the data is ~52%.

**Forecast reasoning:** T1 is the clearly stronger roster (5–1 with a win over KC already), so I discount KC's blue-side win well below the ~56% blue baseline. But KC's early-game edge plus blue side keeps them likely to lead at 15 — consistent with game 1 where they led early but lost late.

```json
{
  "p_blue_win": 0.40,
  "p_blue_ahead_15": 0.58
}
```

Both values are valid probabilities in `prediction.json`.
````
