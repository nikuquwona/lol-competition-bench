# LØS vs LYON · G2 · BP 前

worlds-2026-main-event · Round 5 · 26.20 · BO3

[实际题面](instruction.md) · [可查询的完整快照](snapshot.json) · [原始事件 JSONL](../../jobs/worlds-2026-main-event-round-5-2-g2-lobby/trajectory.jsonl) · [stderr](../../jobs/worlds-2026-main-event-round-5-2-g2-lobby/stderr.txt) · [交卷文件](../../jobs/worlds-2026-main-event-round-5-2-g2-lobby/prediction.json)

## 输入与可查询证据

蓝方首发为 Ackerman, Curse, Duduhh, Feisty, Zest。

红方首发为 Berserker, Dhokla, Inspired, Isles, Saint。

冻结时可查 79 个历史小局，10 名首发有历史出场记录。

本局可见 0 手禁选。

## 预测与赛后结算

```
{
  "status": "scored",
  "prediction": {
    "p_blue_win": 0.67,
    "p_blue_ahead_15": 0.66
  },
  "observed_outcome": {
    "p_blue_win": 0,
    "p_blue_ahead_15": 1
  },
  "brier": {
    "p_blue_win": 0.4489000000000001,
    "p_blue_ahead_15": 0.11559999999999998
  },
  "reward": 0.71775
}
```

## CLI 报告的 token 用量

```
{
  "input_tokens": 460201,
  "cached_input_tokens": 447488,
  "cache_write_input_tokens": 0,
  "output_tokens": 23522,
  "reasoning_output_tokens": 15379
}
```

## 执行轨迹

### 1. CLI 诊断

```
Model metadata for `deepseek-v4-pro` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
```

### 2. 模型消息

```
I'll start by examining the snapshot data, then make an early estimate.
```

### 3. 终端命令 · 退出码 0

```
/bin/zsh -c 'cat ./snapshot.json | head -c 4000'
```

### 4. 命令输出

```
{"phase": "lobby", "series_time_utc": "2026-10-31T18:59:00+00:00", "current": {"event": "worlds-2026-main-event", "stage": "Round 5", "series": "worlds-2026-main-event-round-5-2", "n": 2, "patch": "26.20", "bo": 3, "blue": "LØS", "red": "LYON", "starters": {"blue": ["Ackerman", "Curse", "Duduhh", "Feisty", "Zest"], "red": ["Berserker", "Dhokla", "Inspired", "Isles", "Saint"]}, "draft_rule": "Fearless"}, "history": [{"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": true, "blue_gd15": -38, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Syndra"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Renekton"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Jayce"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yorick"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Yorick", "k": 2, "d": 1, "a": 6}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 1, "d": 5, "a": 5}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Syndra", "k": 3, "d": 1, "a": 7}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 5, "d": 5, "a": 4}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Lulu", "k": 0, "d": 0, "a": 10}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Jayce", "k": 1, "d": 1, "a": 5}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Cho'Gath", "k": 1, "d": 6, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Orianna", "k": 7, "d": 0, "a": 1}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Lucian", "k": 2, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion": "Milio", "k": 1, "d": 2, "a": 10}]}, {"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 2, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": false, "blue_gd15": -1351, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Trundle"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Olaf"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Ashe"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Seraphine"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Ryze"}, {"turn": 11, "side": "red", "ac
```

### 5. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json
d=json.load(open('snapshot.json'))
print('keys', list(d.keys()))
print('current', json.dumps(d['current'], indent=1))
print('coverage', json.dumps(d['coverage'], indent=1))
print('history count', len(d['history']))
\""
```

### 6. 命令输出

```
keys ['phase', 'series_time_utc', 'current', 'history', 'coverage']
current {
 "event": "worlds-2026-main-event",
 "stage": "Round 5",
 "series": "worlds-2026-main-event-round-5-2",
 "n": 2,
 "patch": "26.20",
 "bo": 3,
 "blue": "L\u00d8S",
 "red": "LYON",
 "starters": {
  "blue": [
   "Ackerman",
   "Curse",
   "Duduhh",
   "Feisty",
   "Zest"
  ],
  "red": [
   "Berserker",
   "Dhokla",
   "Inspired",
   "Isles",
   "Saint"
  ]
 },
 "draft_rule": "Fearless"
}
coverage {
 "history_games": 79,
 "starters": [
  {
   "side": "blue",
   "name": "Ackerman",
   "games": 8,
   "same_patch_games": 8
  },
  {
   "side": "blue",
   "name": "Curse",
   "games": 8,
   "same_patch_games": 8
  },
  {
   "side": "blue",
   "name": "Duduhh",
   "games": 8,
   "same_patch_games": 8
  },
  {
   "side": "blue",
   "name": "Feisty",
   "games": 8,
   "same_patch_games": 8
  },
  {
   "side": "blue",
   "name": "Zest",
   "games": 8,
   "same_patch_games": 8
  },
  {
   "side": "red",
   "name": "Berserker",
   "games": 9,
   "same_patch_games": 9
  },
  {
   "side": "red",
   "name": "Dhokla",
   "games": 9,
   "same_patch_games": 9
  },
  {
   "side": "red",
   "name": "Inspired",
   "games": 9,
   "same_patch_games": 9
  },
  {
   "side": "red",
   "name": "Isles",
   "games": 9,
   "same_patch_games": 9
  },
  {
   "side": "red",
   "name": "Saint",
   "games": 9,
   "same_patch_games": 9
  }
 ],
 "starters_with_history": 10,
 "coverage_group": "all",
 "previous_series_games": [
  1
 ],
 "missing_previous_series_games": []
}
history count 79
```

### 7. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json
d=json.load(open('snapshot.json'))
blue='LØS'; red='LYON'
for g in d['history']:
    if g.get('blue')==blue or g.get('red')==blue or g.get('blue')==red or g.get('red')==red:
        print(g['series'], 'n=',g.get('n'), 'patch',g.get('patch'), g.get('blue'),'vs',g.get('red'), 'blue_win',g.get('blue_win'), 'gd15',g.get('blue_gd15'))
\""
```

### 8. 命令输出

```
worlds-2026-main-event-round-1-7 n= 1 patch 26.20 LØS vs T1 blue_win False gd15 -2368
worlds-2026-main-event-round-1-8 n= 1 patch 26.20 LYON vs Team Secret Whales blue_win True gd15 -51
worlds-2026-main-event-round-2-3 n= 1 patch 26.20 LØS vs G2 Esports blue_win False gd15 -753
worlds-2026-main-event-round-2-4 n= 1 patch 26.20 Karmine Corp vs LYON blue_win False gd15 2170
worlds-2026-main-event-round-3-4 n= 1 patch 26.20 LYON vs Gen.G blue_win True gd15 -1063
worlds-2026-main-event-round-3-4 n= 2 patch 26.20 Gen.G vs LYON blue_win True gd15 1623
worlds-2026-main-event-round-3-4 n= 3 patch 26.20 Gen.G vs LYON blue_win True gd15 -2221
worlds-2026-main-event-round-3-7 n= 1 patch 26.20 Team Secret Whales vs LØS blue_win False gd15 1421
worlds-2026-main-event-round-3-7 n= 2 patch 26.20 Team Secret Whales vs LØS blue_win False gd15 -1500
worlds-2026-main-event-round-4-2 n= 1 patch 26.20 LYON vs Invictus Gaming blue_win False gd15 -1628
worlds-2026-main-event-round-4-2 n= 2 patch 26.20 Invictus Gaming vs LYON blue_win False gd15 338
worlds-2026-main-event-round-4-2 n= 3 patch 26.20 LYON vs Invictus Gaming blue_win False gd15 -4021
worlds-2026-main-event-round-4-5 n= 1 patch 26.20 LØS vs Team Liquid blue_win True gd15 1483
worlds-2026-main-event-round-4-5 n= 2 patch 26.20 LØS vs Team Liquid blue_win False gd15 -1870
worlds-2026-main-event-round-4-5 n= 3 patch 26.20 Team Liquid vs LØS blue_win False gd15 -4667
worlds-2026-main-event-round-5-2 n= 1 patch 26.20 LYON vs LØS blue_win False gd15 -1315
```

### 9. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json
d=json.load(open('snapshot.json'))
for g in d['history']:
    if g.get('series')=='worlds-2026-main-event-round-5-2':
        print(json.dumps(g, indent=1))
\""
```

### 10. 命令输出

```
{
 "series": "worlds-2026-main-event-round-5-2",
 "series_time": "2026-10-31T18:59:00+00:00",
 "event": "worlds-2026-main-event",
 "n": 1,
 "patch": "26.20",
 "blue": "LYON",
 "red": "L\u00d8S",
 "blue_win": false,
 "blue_gd15": -1315,
 "bp": [
  {
   "turn": 1,
   "side": "blue",
   "action": "ban",
   "champion": "Renata Glasc"
  },
  {
   "turn": 2,
   "side": "red",
   "action": "ban",
   "champion": "Qiyana"
  },
  {
   "turn": 3,
   "side": "blue",
   "action": "ban",
   "champion": "Jarvan IV"
  },
  {
   "turn": 4,
   "side": "red",
   "action": "ban",
   "champion": "Nocturne"
  },
  {
   "turn": 5,
   "side": "blue",
   "action": "ban",
   "champion": "Trundle"
  },
  {
   "turn": 6,
   "side": "red",
   "action": "ban",
   "champion": "Olaf"
  },
  {
   "turn": 7,
   "side": "blue",
   "action": "pick",
   "champion": "Syndra"
  },
  {
   "turn": 8,
   "side": "red",
   "action": "pick",
   "champion": "Cassiopeia"
  },
  {
   "turn": 9,
   "side": "red",
   "action": "pick",
   "champion": "Vi"
  },
  {
   "turn": 10,
   "side": "blue",
   "action": "pick",
   "champion": "Ezreal"
  },
  {
   "turn": 11,
   "side": "blue",
   "action": "pick",
   "champion": "Pantheon"
  },
  {
   "turn": 12,
   "side": "red",
   "action": "pick",
   "champion": "Kai'Sa"
  },
  {
   "turn": 13,
   "side": "red",
   "action": "ban",
   "champion": "Karma"
  },
  {
   "turn": 14,
   "side": "blue",
   "action": "ban",
   "champion": "Ambessa"
  },
  {
   "turn": 15,
   "side": "red",
   "action": "ban",
   "champion": "Jayce"
  },
  {
   "turn": 16,
   "side": "blue",
   "action": "ban",
   "champion": "K'Sante"
  },
  {
   "turn": 17,
   "side": "red",
   "action": "pick",
   "champion": "Nautilus"
  },
  {
   "turn": 18,
   "side": "blue",
   "action": "pick",
   "champion": "Alistar"
  },
  {
   "turn": 19,
   "side": "blue",
   "action": "pick",
   "champion": "Rumble"
  },
  {
   "turn": 20,
   "side": "red",
   "action": "pick",
   "champion": "Aurora"
  }
 ],
 "players": [
  {
   "name": "Dhokla",
   "role": "Top",
   "side": "blue",
   "champion": "Rumble",
   "k": 3,
   "d": 1,
   "a": 2
  },
  {
   "name": "Inspired",
   "role": "Jungle",
   "side": "blue",
   "champion": "Pantheon",
   "k": 2,
   "d": 1,
   "a": 4
  },
  {
   "name": "Saint",
   "role": "Mid",
   "side": "blue",
   "champion": "Syndra",
   "k": 1,
   "d": 3,
   "a": 1
  },
  {
   "name": "Berserker",
   "role": "Bot",
   "side": "blue",
   "champion": "Ezreal",
   "k": 2,
   "d": 3,
   "a": 1
  },
  {
   "name": "Isles",
   "role": "Support",
   "side": "blue",
   "champion": "Alistar",
   "k": 0,
   "d": 3,
   "a": 4
  },
  {
   "name": "Zest",
   "role": "Top",
   "side": "red",
   "champion": "Aurora",
   "k": 1,
   "d": 1,
   "a": 2
  },
  {
   "name": "Curse",
   "role": "Jungle",
   "side": "red",
   "champion": "Vi",
   "k": 3,
   "d": 2,
   "a": 4
  },
  {
   "name": "Feisty",
   "role": "Mid",
   "side": "red",
   "champion": "Cassiopeia",
   "k": 2,
   "d": 3,
   "a": 5
  },
  {
   "name": "Duduhh",
   "role": "Bot",
   "side": "red",
   "champion": "Kai'Sa",
   "k": 4,
   "d": 1,
   "a": 2
  },
  {
   "name": "Ackerman",
   "role": "Support",
   "side": "red",
   "champion": "Nautilus",
   "k": 1,
   "d": 1,
   "a": 4
  }
 ]
}
```

### 11. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json
d=json.load(open('snapshot.json'))
blue='LØS'; red='LYON'
def team_side(g):
    if g.get('blue')==blue: return 'blue'
    if g.get('red')==blue: return 'red'
    return None
print('=== LØS games ===')
for g in d['history']:
    s=team_side(g)
    if s:
        w = g['blue_win'] if s=='blue' else (not g['blue_win'])
        gd = g['blue_gd15'] if s=='blue' else -g['blue_gd15'] if g.get('blue_gd15') is not None else None
        opp = g['red'] if s=='blue' else g['blue']
        print(g['series'],'n',g.get('n'),'side',s,'vs',opp,'W' if w else 'L','gd15',gd)
\""
```

### 12. 命令输出

```
=== LØS games ===
worlds-2026-main-event-round-1-7 n 1 side blue vs T1 L gd15 -2368
worlds-2026-main-event-round-2-3 n 1 side blue vs G2 Esports L gd15 -753
worlds-2026-main-event-round-3-7 n 1 side red vs Team Secret Whales W gd15 -1421
worlds-2026-main-event-round-3-7 n 2 side red vs Team Secret Whales W gd15 1500
worlds-2026-main-event-round-4-5 n 1 side blue vs Team Liquid W gd15 1483
worlds-2026-main-event-round-4-5 n 2 side blue vs Team Liquid L gd15 -1870
worlds-2026-main-event-round-4-5 n 3 side red vs Team Liquid W gd15 4667
worlds-2026-main-event-round-5-2 n 1 side red vs LYON W gd15 1315
```

### 13. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json
d=json.load(open('snapshot.json'))
red='LYON'
print('=== LYON games ===')
for g in d['history']:
    s = 'blue' if g.get('blue')==red else ('red' if g.get('red')==red else None)
    if s:
        w = g['blue_win'] if s=='blue' else (not g['blue_win'])
        gd = g['blue_gd15'] if s=='blue' else (-g['blue_gd15'] if g.get('blue_gd15') is not None else None)
        opp = g['red'] if s=='blue' else g['blue']
        print(g['series'],'n',g.get('n'),'side',s,'vs',opp,'W' if w else 'L','gd15',gd)
\""
```

### 14. 命令输出

```
=== LYON games ===
worlds-2026-main-event-round-1-8 n 1 side blue vs Team Secret Whales W gd15 -51
worlds-2026-main-event-round-2-4 n 1 side red vs Karmine Corp W gd15 -2170
worlds-2026-main-event-round-3-4 n 1 side blue vs Gen.G W gd15 -1063
worlds-2026-main-event-round-3-4 n 2 side red vs Gen.G L gd15 -1623
worlds-2026-main-event-round-3-4 n 3 side red vs Gen.G L gd15 2221
worlds-2026-main-event-round-4-2 n 1 side blue vs Invictus Gaming L gd15 -1628
worlds-2026-main-event-round-4-2 n 2 side red vs Invictus Gaming W gd15 -338
worlds-2026-main-event-round-4-2 n 3 side blue vs Invictus Gaming L gd15 -4021
worlds-2026-main-event-round-5-2 n 1 side blue vs LØS L gd15 -1315
```

### 15. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json
d=json.load(open('snapshot.json'))
hist=d['history']
bw=0; n=0; ba=0; n15=0
for g in hist:
    n+=1
    if g.get('blue_win'): bw+=1
    if g.get('blue_gd15') is not None:
        n15+=1
        if g['blue_gd15']>0: ba+=1
print('total games',n,'blue win',bw, round(bw/n,3))
print('blue ahead15',ba,'/',n15, round(ba/n15,3))
# patch 26.20 only
sub=[g for g in hist if g.get('patch')=='26.20']
bw=sum(1 for g in sub if g.get('blue_win')); n=len(sub)
ba=sum(1 for g in sub if g.get('blue_gd15') is not None and g['blue_gd15']>0); n15=sum(1 for g in sub if g.get('blue_gd15') is not None)
print('patch26.20 games',n,'blue win',bw,round(bw/n,3),'blue ahead15',ba,'/',n15,round(ba/n15,3))
\""
```

### 16. 命令输出

```
total games 79 blue win 42 0.532
blue ahead15 37 / 79 0.468
patch26.20 games 67 blue win 36 0.537 blue ahead15 32 / 67 0.478
```

### 17. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json
d=json.load(open('snapshot.json'))
blue='LØS'; red='LYON'
players = {'Ackerman':'blue','Curse':'blue','Duduhh':'blue','Feisty':'blue','Zest':'blue','Berserker':'red','Dhokla':'red','Inspired':'red','Isles':'red','Saint':'red'}
for g in d['history']:
    for p in g.get('players',[]):
        if p['name'] in players:
            side = p['side']
            # team of player
            t = 'blue' if side=='blue' else 'red'
            team = g['blue'] if side=='blue' else g['red']
            # win from player's team perspective
            w = g['blue_win'] if side=='blue' else (not g['blue_win'])
            gd = g.get('blue_gd15')
            if gd is not None and side=='red': gd=-gd
            print(f\\\"{p['name']:10s} {p['role']:9s} {p['champion']:12s} {p['k']}/{p['d']}/{p['a']} {'W' if w else 'L'} gd15={gd} vs {g['red'] if side=='blue' else g['blue']} (series {g['series']}, n{g.get('n')})\\\")
\""
```

### 18. 命令输出

```
Zest       Top       K'Sante      1/5/1 L gd15=-2368 vs T1 (series worlds-2026-main-event-round-1-7, n1)
Curse      Jungle    Pantheon     0/5/2 L gd15=-2368 vs T1 (series worlds-2026-main-event-round-1-7, n1)
Feisty     Mid       Syndra       2/3/1 L gd15=-2368 vs T1 (series worlds-2026-main-event-round-1-7, n1)
Duduhh     Bot       Tristana     0/3/2 L gd15=-2368 vs T1 (series worlds-2026-main-event-round-1-7, n1)
Ackerman   Support   Rakan        0/3/3 L gd15=-2368 vs T1 (series worlds-2026-main-event-round-1-7, n1)
Dhokla     Top       K'Sante      2/1/8 W gd15=-51 vs Team Secret Whales (series worlds-2026-main-event-round-1-8, n1)
Inspired   Jungle    Nocturne     2/2/11 W gd15=-51 vs Team Secret Whales (series worlds-2026-main-event-round-1-8, n1)
Saint      Mid       Anivia       2/0/11 W gd15=-51 vs Team Secret Whales (series worlds-2026-main-event-round-1-8, n1)
Berserker  Bot       Ezreal       13/1/5 W gd15=-51 vs Team Secret Whales (series worlds-2026-main-event-round-1-8, n1)
Isles      Support   Alistar      3/2/18 W gd15=-51 vs Team Secret Whales (series worlds-2026-main-event-round-1-8, n1)
Zest       Top       Jayce        3/3/2 L gd15=-753 vs G2 Esports (series worlds-2026-main-event-round-2-3, n1)
Curse      Jungle    Nocturne     1/5/5 L gd15=-753 vs G2 Esports (series worlds-2026-main-event-round-2-3, n1)
Feisty     Mid       Orianna      2/4/2 L gd15=-753 vs G2 Esports (series worlds-2026-main-event-round-2-3, n1)
Duduhh     Bot       Kalista      3/5/3 L gd15=-753 vs G2 Esports (series worlds-2026-main-event-round-2-3, n1)
Ackerman   Support   Renata Glasc 0/5/7 L gd15=-753 vs G2 Esports (series worlds-2026-main-event-round-2-3, n1)
Dhokla     Top       Galio        2/1/12 W gd15=-2170 vs Karmine Corp (series worlds-2026-main-event-round-2-4, n1)
Inspired   Jungle    Wukong       2/3/11 W gd15=-2170 vs Karmine Corp (series worlds-2026-main-event-round-2-4, n1)
Saint      Mid       Syndra       6/2/6 W gd15=-2170 vs Karmine Corp (series worlds-2026-main-event-round-2-4, n1)
Berserker  Bot       Yunara       5/4/8 W gd15=-2170 vs Karmine Corp (series worlds-2026-main-event-round-2-4, n1)
Isles      Support   Lulu         0/5/13 W gd15=-2170 vs Karmine Corp (series worlds-2026-main-event-round-2-4, n1)
Dhokla     Top       Olaf         2/3/2 W gd15=-1063 vs Gen.G (series worlds-2026-main-event-round-3-4, n1)
Inspired   Jungle    Xin Zhao     1/0/8 W gd15=-1063 vs Gen.G (series worlds-2026-main-event-round-3-4, n1)
Saint      Mid       Ahri         3/0/6 W gd15=-1063 vs Gen.G (series worlds-2026-main-event-round-3-4, n1)
Berserker  Bot       Kalista      4/0/4 W gd15=-1063 vs Gen.G (series worlds-2026-main-event-round-3-4, n1)
Isles      Support   Renata Glasc 0/1/9 W gd15=-1063 vs Gen.G (series worlds-2026-main-event-round-3-4, n1)
Dhokla     Top       Shen         1/3/5 L gd15=-1623 vs Gen.G (series worlds-2026-main-event-round-3-4, n2)
Inspired   Jungle    Vi           1/5/6 L gd15=-1623 vs Gen.G (series worlds-2026-main-event-round-3-4, n2)
Saint      Mid       Akali        5/3/3 L gd15=-1623 vs Gen.G (series worlds-2026-main-event-round-3-4, n2)
Berserker  Bot       Yunara       2/3/3 L gd15=-1623 vs Gen.G (series worlds-2026-main-event-round-3-4, n2)
Isles      Support   Lulu         0/2/7 L gd15=-1623 vs Gen.G (series worlds-2026-main-event-round-3-4, n2)
Dhokla     Top       K'Sante      1/3/3 L gd15=2221 vs Gen.G (series worlds-2026-main-event-round-3-4, n3)
Inspired   Jungle    Maokai       0/3/5 L gd15=2221 vs Gen.G (series worlds-2026-main-event-round-3-4, n3)
Saint      Mid       Tristana     4/2/0 L gd15=2221 vs Gen.G (series worlds-2026-main-event-round-3-4, n3)
Berserker  Bot       Lucian       1/4/2 L gd15=2221 vs Gen.G (series worlds-2026-main-event-round-3-4, n3)
Isles      Support   Milio        1/3/6 L gd15=2221 vs Gen.G (series worlds-2026-main-event-round-3-4, n3)
Zest       Top       Gnar         3/1/6 W gd15=-1421 vs Team Secret Whales (series worlds-2026-main-event-round-3-7, n1)
Curse      Jungle    Wukong       1/2/9 W gd15=-1421 vs Team Secret Whales (series worlds-2026-main-event-round-3-7, n1)
Feisty     Mid       Orianna      4/2/6 W gd15=-1421 vs Team Secret Whales (series worlds-2026-main-event-round-3-7, n1)
Duduhh     Bot       Kalista      6/2/5 W gd15=-1421 vs Team Secret Whales (series worlds-2026-main-event-round-3-7, n1)
Ackerman   Support   Renata Glasc 0/2/12 W gd15=-1421 vs Team Secret Whales (series worlds-2026-main-event-round-3-7, n1)
Zest       Top       Kennen       9/2/5 W gd15=1500 vs Team Secret Whales (series worlds-2026-main-event-round-3-7, n2)
Curse      Jungle    Trundle      5/2/14 W gd15=1500 vs Team Secret Whales (series worlds-2026-main-event-round-3-7, n2)
Feisty     Mid       Galio        2/3/15 W gd15=1500 vs Team Secret Whales (series worlds-2026-main-event-round-3-7, n2)
Duduhh     Bot       Ashe         5/3/9 W gd15=1500 vs Team Secret Whales (series worlds-2026-main-event-round-3-7, n2)
Ackerman   Support   Seraphine    1/3/17 W gd15=1500 vs Team Secret Whales (series worlds-2026-main-event-round-3-7, n2)
Dhokla     Top       Rumble       2/3/1 L gd15=-1628 vs Invictus Gaming (series worlds-2026-main-event-round-4-2, n1)
Inspired   Jungle    Nocturne     1/6/1 L gd15=-1628 vs Invictus Gaming (series worlds-2026-main-event-round-4-2, n1)
Saint      Mid       Sylas        1/2/2 L gd15=-1628 vs Invictus Gaming (series worlds-2026-main-event-round-4-2, n1)
Berserker  Bot       Ezreal       0/3/3 L gd15=-1628 vs Invictus Gaming (series worlds-2026-main-event-round-4-2, n1)
Isles      Support   Karma        0/5/3 L gd15=-1628 vs Invictus Gaming (series worlds-2026-main-event-round-4-2, n1)
Dhokla     Top       Olaf         4/2/3 W gd15=-338 vs Invictus Gaming (series worlds-2026-main-event-round-4-2, n2)
Inspired   Jungle    Qiyana       4/1/5 W gd15=-338 vs Invictus Gaming (series worlds-2026-main-event-round-4-2, n2)
Saint      Mid       Taliyah      4/1/7 W gd15=-338 vs Invictus Gaming (series worlds-2026-main-event-round-4-2, n2)
Berserker  Bot       Corki        6/0/2 W gd15=-338 vs Invictus Gaming (series worlds-2026-main-event-round-4-2, n2)
Isles      Support   Alistar      0/4/12 W gd15=-338 vs Invictus Gaming (series worlds-2026-main-event-round-4-2, n2)
Dhokla     Top       K'Sante      1/2/0 L gd15=-4021 vs Invictus Gaming (series worlds-2026-main-event-round-4-2, n3)
Inspired   Jungle    Xin Zhao     2/2/3 L gd15=-4021 vs Invictus Gaming (series worlds-2026-main-event-round-4-2, n3)
Saint      Mid       LeBlanc      0/1/1 L gd15=-4021 vs Invictus Gaming (series worlds-2026-main-event-round-4-2, n3)
Berserker  Bot       Lucian       1/2/1 L gd15=-4021 vs Invictus Gaming (series worlds-2026-main-event-round-4-2, n3)
Isles      Support   Milio        1/0/2 L gd15=-4021 vs Invictus Gaming (series worlds-2026-main-event-round-4-2, n3)
Zest       Top       Jayce        2/2/6 W gd15=1483 vs Team Liquid (series worlds-2026-main-event-round-4-5, n1)
Curse      Jungle    Trundle      7/0/6 W gd15=1483 vs Team Liquid (series worlds-2026-main-event-round-4-5, n1)
Feisty     Mid       Syndra       2/2/6 W gd15=1483 vs Team Liquid (series worlds-2026-main-event-round-4-5, n1)
Duduhh     Bot       Ashe         4/2/3 W gd15=1483 vs Team Liquid (series worlds-2026-main-event-round-4-5, n1)
Ackerman   Support   Seraphine    0/1/11 W gd15=1483 vs Team Liquid (series worlds-2026-main-event-round-4-5, n1)
Zest       Top       Rumble       0/1/5 L gd15=-1870 vs Team Liquid (series worlds-2026-main-event-round-4-5, n2)
Curse      Jungle    Jarvan IV    0/5/5 L gd15=-1870 vs Team Liquid (series worlds-2026-main-event-round-4-5, n2)
Feisty     Mid       Galio        1/3/5 L gd15=-1870 vs Team Liquid (series worlds-2026-main-event-round-4-5, n2)
Duduhh     Bot       Ezreal       5/3/2 L gd15=-1870 vs Team Liquid (series worlds-2026-main-event-round-4-5, n2)
Ackerman   Support   Karma        2/3/6 L gd15=-1870 vs Team Liquid (series worlds-2026-main-event-round-4-5, n2)
Zest       Top       Tristana     10/1/3 W gd15=4667 vs Team Liquid (series worlds-2026-main-event-round-4-5, n3)
Curse      Jungle    Pantheon     4/0/7 W gd15=4667 vs Team Liquid (series worlds-2026-main-event-round-4-5, n3)
Feisty     Mid       Taliyah      0/1/12 W gd15=4667 vs Team Liquid (series worlds-2026-main-event-round-4-5, n3)
Duduhh     Bot       Kalista      2/1/7 W gd15=4667 vs Team Liquid (series worlds-2026-main-event-round-4-5, n3)
Ackerman   Support   Renata Glasc 1/2/11 W gd15=4667 vs Team Liquid (series worlds-2026-main-event-round-4-5, n3)
Dhokla     Top       Rumble       3/1/2 L gd15=-1315 vs LØS (series worlds-2026-main-event-round-5-2, n1)
Inspired   Jungle    Pantheon     2/1/4 L gd15=-1315 vs LØS (series worlds-2026-main-event-round-5-2, n1)
Saint      Mid       Syndra       1/3/1 L gd15=-1315 vs LØS (series worlds-2026-main-event-round-5-2, n1)
Berserker  Bot       Ezreal       2/3/1 L gd15=-1315 vs LØS (series worlds-2026-main-event-round-5-2, n1)
Isles      Support   Alistar      0/3/4 L gd15=-1315 vs LØS (series worlds-2026-main-event-round-5-2, n1)
Zest       Top       Aurora       1/1/2 W gd15=1315 vs LYON (series worlds-2026-main-event-round-5-2, n1)
Curse      Jungle    Vi           3/2/4 W gd15=1315 vs LYON (series worlds-2026-main-event-round-5-2, n1)
Feisty     Mid       Cassiopeia   2/3/5 W gd15=1315 vs LYON (series worlds-2026-main-event-round-5-2, n1)
Duduhh     Bot       Kai'Sa       4/1/2 W gd15=1315 vs LYON (series worlds-2026-main-event-round-5-2, n1)
Ackerman   Support   Nautilus     1/1/4 W gd15=1315 vs LYON (series worlds-2026-main-event-round-5-2, n1)
```

### 19. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json
d=json.load(open('snapshot.json'))
sub=[g for g in d['history'] if g.get('patch')=='26.20' and g.get('blue_gd15') is not None]
ahead=[g for g in sub if g['blue_gd15']>0]
behind=[g for g in sub if g['blue_gd15']<=0]
print('blue ahead games',len(ahead),'blue win when ahead',sum(1 for g in ahead if g['blue_win']),round(sum(1 for g in ahead if g['blue_win'])/len(ahead),3))
print('blue behind games',len(behind),'blue win when behind',sum(1 for g in behind if g['blue_win']),round(sum(1 for g in behind if g['blue_win'])/len(behind),3))
\""
```

### 20. 命令输出

```
blue ahead games 32 blue win when ahead 22 0.688
blue behind games 35 blue win when behind 14 0.4
```

### 21. 模型消息

```
I have a good picture of the matchup. Writing an initial estimate now, then I'll refine.
```

### 22. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json
pred={'p_blue_win':0.68,'p_blue_ahead_15':0.65}
json.dump(pred, open('prediction.json','w'))
print(open('prediction.json').read())
\""
```

### 23. 命令输出

```
{"p_blue_win": 0.68, "p_blue_ahead_15": 0.65}
```

### 24. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json
d=json.load(open('snapshot.json'))
sub=[g for g in d['history'] if g.get('patch')=='26.20']
from collections import defaultdict
stats=defaultdict(lambda:{'w':0,'l':0,'gd':[],'oppgd':[]})
for g in sub:
    b=g['blue']; r=g['red']
    if g.get('blue_win'):
        stats[b]['w']+=1; stats[r]['l']+=1
    else:
        stats[r]['w']+=1; stats[b]['l']+=1
    if g.get('blue_gd15') is not None:
        stats[b]['gd'].append(g['blue_gd15'])
        stats[r]['gd'].append(-g['blue_gd15'])
for t,s in sorted(stats.items()):
    n=s['w']+s['l']
    avg=sum(s['gd'])/len(s['gd']) if s['gd'] else None
    print(f\\\"{t:22s} W{s['w']}-{s['l']}L  n={n}  avg_gd15={avg:.0f}\\\" if avg is not None else f\\\"{t:22s} W{s['w']}-{s['l']}L n={n} avg_gd15=None\\\")
\""
```

### 25. 命令输出

```
Anyone's Legend        W0-4L  n=4  avg_gd15=-1128
Bilibili Gaming        W3-3L  n=6  avg_gd15=-72
CTBC Flying Oyster     W1-4L  n=5  avg_gd15=531
Cloud9                 W3-6L  n=9  avg_gd15=135
Dplus Kia              W4-0L  n=4  avg_gd15=249
FURIA                  W4-7L  n=11  avg_gd15=-1512
G2 Esports             W1-4L  n=5  avg_gd15=626
Gen.G                  W4-1L  n=5  avg_gd15=-81
Hanwha Life Esports    W3-2L  n=5  avg_gd15=-113
Invictus Gaming        W4-2L  n=6  avg_gd15=1613
Karmine Corp           W12-4L  n=16  avg_gd15=1022
LYON                   W4-5L  n=9  avg_gd15=-1110
LØS                    W5-3L  n=8  avg_gd15=319
MVK Esports            W6-7L  n=13  avg_gd15=-222
Movistar KOI           W2-4L  n=6  avg_gd15=-1196
T1                     W4-1L  n=5  avg_gd15=1436
Team Liquid            W3-4L  n=7  avg_gd15=111
Team Secret Whales     W0-4L  n=4  avg_gd15=-243
Top Esports            W4-2L  n=6  avg_gd15=-164
```

### 26. 终端命令 · 退出码 1

```
/bin/zsh -c "python3 -c \"
import json, math
d=json.load(open('snapshot.json'))
sub=[g for g in d['history'] if g.get('patch')=='26.20']
# Bradley-Terry with blue-side multiplier
teams=set()
rows=[]
for g in sub:
    b=g['blue']; r=g['red']
    teams.add(b); teams.add(r)
    y = 1 if g.get('blue_win') else 0
    rows.append((b,r,y))
teams=sorted(teams)
idx={t:i for i,t in enumerate(teams)}
n=len(teams)
# parameters: rating for each team, last is blue bonus (log)
import numpy as np
# use scipy? check
try:
    import scipy.optimize as opt
    HAS=True
except:
    HAS=False
print('scipy',HAS)
def negll(params):
    r=params[:n]
    blue=params[n]
    ll=0
    for b,rname,y in rows:
        # logit p = blue_bonus + r[b]-r[rname]
        z = blue + r[idx[b]] - r[idx[rname]]
        p = 1/(1+math.exp(-z))
        ll += y*math.log(p+1e-9)+(1-y)*math.log(1-p+1e-9)
    return -ll
if HAS:
    import scipy.optimize as opt
    x0=[0.0]*(n+1)
    res=opt.minimize(negll,x0,method='BFGS')
    r=res.x[:n]
    blue=res.x[n]
    # normalize
    r=r-r.mean()
    print('blue bonus log',blue,'odds',math.exp(blue))
    for t in teams:
        print(f'{t:22s} rating {r[idx[t]]:.3f}')
    # predict LØS blue vs LYON red
    z=blue + r[idx['LØS']]-r[idx['LYON']]
    p=1/(1+math.exp(-z))
    print('p_blue_win predicted',p)
else:
    print('no scipy; do manual')
\""
```

### 27. 命令输出

```
Traceback (most recent call last):
  File "<string>", line 17, in <module>
ModuleNotFoundError: No module named 'numpy'
```

### 28. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json, math
d=json.load(open('snapshot.json'))
sub=[g for g in d['history'] if g.get('patch')=='26.20']
teams=set()
rows=[]
for g in sub:
    b=g['blue']; r=g['red']
    teams.add(b); teams.add(r)
    y = 1 if g.get('blue_win') else 0
    rows.append((b,r,y))
teams=sorted(teams)
idx={t:i for i,t in enumerate(teams)}
n=len(teams)
# gradient descent on ratings + blue bonus
r=[0.0]*n
blue=0.0
lr=0.5
for it in range(20000):
    gradr=[0.0]*n
    gradblue=0.0
    ll=0
    for b,rname,y in rows:
        z=blue+r[idx[b]]-r[idx[rname]]
        # p = sigmoid(z)
        if z>0:
            s=math.exp(-z)
            p=1/(1+s)
            dp=s*p*p  # derivative sigmoid wrt z
        else:
            e=math.exp(z)
            p=e/(1+e)
            dp=e/((1+e)**2)
        # ll contribution
        ll += y*math.log(p+1e-12)+(1-y)*math.log(1-p+1e-12)
        # d ll / dz = y - p
        g = y - p
        gradblue += g
        gradr[idx[b]] += g
        gradr[idx[rname]] -= g
    # gradient ascent on ll = descent on -ll
    for i in range(n):
        r[i]+=lr*gradr[i]
    blue+=lr*gradblue
    if it%5000==0:
        print(it,'ll',ll,'blue',blue)
# normalize
mean=sum(r)/n
r=[x-mean for x in r]
print('blue bonus',blue,'odds',math.exp(blue))
for t in teams:
    print(f'{t:22s} {r[idx[t]]:.3f}')
z=blue+r[idx['LØS']]-r[idx['LYON']]
p=1/(1+math.exp(-z))
print('p_blue_win BT',round(p,3))
\""
```

### 29. 命令输出

```
0 ll -46.44086109738234 blue 1.25
5000 ll -41.29219897919138 blue 2.42880334352496
10000 ll -64.99768302359244 blue 3.2470907636057884
15000 ll -39.2293746354233 blue 1.4904875304082985
blue bonus -4.922338101908828 odds 0.007282084670636976
Anyone's Legend        -20.224
Bilibili Gaming        0.394
CTBC Flying Oyster     -6.737
Cloud9                 -8.199
Dplus Kia              34.859
FURIA                  -9.864
G2 Esports             -2.687
Gen.G                  5.695
Hanwha Life Esports    2.177
Invictus Gaming        3.471
Karmine Corp           -2.610
LYON                   0.584
LØS                    -3.287
MVK Esports            -7.010
Movistar KOI           11.457
T1                     23.257
Team Liquid            -7.522
Team Secret Whales     -15.493
Top Esports            1.738
p_blue_win BT 0.0
```

### 30. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json, math
d=json.load(open('snapshot.json'))
sub=[g for g in d['history'] if g.get('patch')=='26.20']
teams=set()
rows=[]
for g in sub:
    b=g['blue']; r=g['red']
    teams.add(b); teams.add(r)
    y = 1 if g.get('blue_win') else 0
    rows.append((b,r,y))
teams=sorted(teams)
idx={t:i for i,t in enumerate(teams)}
n=len(teams)
r=[0.0]*n
blue=0.0
lr=0.01
lam=0.05
for it in range(50000):
    gradr=[0.0]*n
    gradblue=0.0
    ll=0
    for b,rname,y in rows:
        z=blue+r[idx[b]]-r[idx[rname]]
        p=1/(1+math.exp(-z))
        ll += y*math.log(p+1e-12)+(1-y)*math.log(1-p+1e-12)
        g=y-p
        gradblue+=g
        gradr[idx[b]]+=g
        gradr[idx[rname]]-=g
    # ridge on ratings and blue
    for i in range(n):
        gradr[i]-=lam*r[i]
    gradblue-=lam*blue
    for i in range(n):
        r[i]+=lr*gradr[i]
    blue+=lr*gradblue
    if it%10000==0:
        print(it,'ll',round(ll,3),'blue',round(blue,3))
mean=sum(r)/n
r=[x-mean for x in r]
print('blue bonus',round(blue,3),'odds',round(math.exp(blue),3))
for t in teams:
    print(f'{t:22s} {r[idx[t]]:6.3f}')
z=blue+r[idx['LØS']]-r[idx['LYON']]
p=1/(1+math.exp(-z))
print('p_blue_win BT',round(p,3))
\""
```

### 31. 命令输出

```
0 ll -46.441 blue 0.025
10000 ll -28.013 blue -0.189
20000 ll -28.013 blue -0.189
30000 ll -28.013 blue -0.189
40000 ll -28.013 blue -0.189
blue bonus -0.189 odds 0.828
Anyone's Legend        -3.975
Bilibili Gaming         0.398
CTBC Flying Oyster     -1.438
Cloud9                 -1.828
Dplus Kia               4.840
FURIA                  -2.065
G2 Esports             -0.601
Gen.G                   2.226
Hanwha Life Esports     1.081
Invictus Gaming         1.535
Karmine Corp           -0.067
LYON                    0.787
LØS                    -0.311
MVK Esports            -1.244
Movistar KOI            1.240
T1                      3.152
Team Liquid            -1.550
Team Secret Whales     -2.957
Top Esports             0.778
p_blue_win BT 0.216
```

### 32. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json
d=json.load(open('snapshot.json'))
sub=[g for g in d['history'] if g.get('patch')=='26.20' and g.get('blue_gd15') is not None]
teams=set()
rows=[]
for g in sub:
    b=g['blue']; r=g['red']
    teams.add(b); teams.add(r)
    rows.append((b,r,g['blue_gd15']))
teams=sorted(teams)
idx={t:i for i,t in enumerate(teams)}
n=len(teams)
# least squares: gd15 = blue_bonus + rating[b] - rating[r]
# solve normal equations via gradient descent
r=[0.0]*n
blue=0.0
lr=0.001
lam=0.01
for it in range(200000):
    gradr=[0.0]*n
    gradblue=0.0
    for b,rn,g in rows:
        pred=blue+r[idx[b]]-r[idx[rn]]
        err=pred-g
        gradblue+=2*err
        gradr[idx[b]]+=2*err
        gradr[idx[rn]]-=2*err
    for i in range(n): gradr[i]+=2*lam*r[i]
    gradblue+=2*lam*blue
    for i in range(n): r[i]-=lr*gradr[i]
    blue-=lr*gradblue
    if it%50000==0:
        mse=sum((blue+r[idx[b]]-r[idx[rn]]-g)**2 for b,rn,g in rows)/len(rows)
        print(it,'mse',round(mse,0),'blue',round(blue,0))
mean=sum(r)/n
r=[x-mean for x in r]
print('blue bonus gd15',round(blue,0))
for t in teams:
    print(f'{t:22s} {r[idx[t]]:7.0f}')
diff=blue+r[idx['LØS']]-r[idx['LYON']]
print('expected gd15 LØS vs LYON',round(diff,0))
\""
```

### 33. 命令输出

```
0 mse 5342667.0 blue 28.0
50000 mse 3802826.0 blue 85.0
100000 mse 3802826.0 blue 85.0
150000 mse 3802826.0 blue 85.0
blue bonus gd15 85.0
Anyone's Legend          -1041
Bilibili Gaming           -136
CTBC Flying Oyster         859
Cloud9                   -1598
Dplus Kia                  968
FURIA                    -3523
G2 Esports                1361
Gen.G                      210
Hanwha Life Esports        810
Invictus Gaming           1678
Karmine Corp              -355
LYON                      -371
LØS                        918
MVK Esports              -2313
Movistar KOI              -113
T1                        1920
Team Liquid                297
Team Secret Whales         499
Top Esports                -71
expected gd15 LØS vs LYON 1374.0
```

### 34. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json, math
d=json.load(open('snapshot.json'))
sub=[g for g in d['history'] if g.get('patch')=='26.20' and g.get('blue_gd15') is not None and g.get('blue_win') is not None]
# logistic fit P(blue win) = sigmoid(a + b*blue_gd15)
a=0.0; b=0.0
lr=1e-7
for it in range(200000):
    ga=0; gb=0
    ll=0
    for g in sub:
        x=g['blue_gd15']; y=1 if g['blue_win'] else 0
        z=a+b*x
        p=1/(1+math.exp(-z))
        ll+=y*math.log(p+1e-12)+(1-y)*math.log(1-p+1e-12)
        e=y-p
        ga+=e
        gb+=e*x
    a+=lr*ga; b+=lr*gb
    if it%50000==0: print(it,round(ll,2),'a',round(a,4),'b',round(b,6))
print('final a',a,'b',b)
# predicted win at gd15=0
p0=1/(1+math.exp(-a))
print('P(blue win | gd15=0)',round(p0,3))
# if LØS ahead by gd15=1374, blue win prob
for gd in [0,1374,900]:
    p=1/(1+math.exp(-(a+b*gd)))
    print('gd',gd,'-> p win',round(p,3))
\""
```

### 35. 命令输出

```
0 -46.44 a 0.0 b 0.003199
50000 -208.17 a 0.0136 b 0.003968
100000 -115.64 a 0.0268 b 0.000877
150000 -76.56 a 0.0395 b -0.000332
final a 0.0516465056583871 b -0.0007067800687645877
P(blue win | gd15=0) 0.513
gd 0 -> p win 0.513
gd 1374 -> p win 0.285
gd 900 -> p win 0.358
```

### 36. 终端命令 · 退出码 0

```
/bin/zsh -c "python3 -c \"
import json
pred={'p_blue_win':0.67,'p_blue_ahead_15':0.66}
json.dump(pred, open('prediction.json','w'))
print(open('prediction.json').read())
\""
```

### 37. 命令输出

```
{"p_blue_win": 0.67, "p_blue_ahead_15": 0.66}
```

### 38. 模型消息

```
Forecast saved to `prediction.json`.

**Final Estimate**
- `p_blue_win`: 0.67
- `p_blue_ahead_15`: 0.66

**Reasoning**
- LØS beat LYON in game 1 as red side (+1315 gold at 15), and now gets blue side for game 2.
- LØS is on a strong run (won 5 of last 6), while LYON lost 4 of its last 5.
- LYON's early game is consistently weak: behind at 15 in 8 of 9 games, with most wins coming from behind. LØS's gold-diff profile is stronger, supporting the early-lead probability.
- Slight tempering for strength of schedule: LYON did take single games off KC, Gen.G, and Invictus Gaming, so the win probability isn't pushed higher.
```
