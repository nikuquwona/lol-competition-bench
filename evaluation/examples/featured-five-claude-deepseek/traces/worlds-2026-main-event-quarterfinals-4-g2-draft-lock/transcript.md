# Karmine Corp vs T1 · G2 · BP 锁定

worlds-2026-main-event · Quarterfinals · 26.20 · BO5

[实际题面](instruction.md) · [可查询的完整快照](snapshot.json) · [原始事件 JSONL](../../jobs/worlds-2026-main-event-quarterfinals-4-g2-draft-lock/trajectory.jsonl) · [stderr](../../jobs/worlds-2026-main-event-quarterfinals-4-g2-draft-lock/stderr.txt) · [交卷文件](../../jobs/worlds-2026-main-event-quarterfinals-4-g2-draft-lock/prediction.json)

## 输入与可查询证据

蓝方首发为 Busio, Caliste, Canna, Kyeahoo, Yike。

红方首发为 Doran, Faker, Keria, Oner, Peyz。

冻结时可查 96 个历史小局，10 名首发有历史出场记录。

本局可见 20 手禁选。

## 预测与赛后结算

```
{
  "status": "scored",
  "prediction": {
    "p_blue_win": 0.31,
    "p_blue_ahead_15": 0.58
  },
  "observed_outcome": {
    "p_blue_win": 0,
    "p_blue_ahead_15": 0
  },
  "brier": {
    "p_blue_win": 0.0961,
    "p_blue_ahead_15": 0.3364
  },
  "reward": 0.78375
}
```

## CLI 报告的 token 用量

```
{
  "input_tokens": 18136,
  "cache_creation_input_tokens": 0,
  "cache_read_input_tokens": 222464,
  "output_tokens": 15399
}
```

## 执行轨迹

### 1. 终端命令

```
cat [ephemeral]/app/snapshot.json | head -c 8000
```

### 2. 命令结果

```
{"phase": "draft-lock", "series_time_utc": "2026-11-06T22:00:00+00:00", "current": {"event": "worlds-2026-main-event", "stage": "Quarterfinals", "series": "worlds-2026-main-event-quarterfinals-4", "n": 2, "patch": "26.20", "bo": 5, "blue": "Karmine Corp", "red": "T1", "starters": {"blue": ["Busio", "Caliste", "Canna", "Kyeahoo", "Yike"], "red": ["Doran", "Faker", "Keria", "Oner", "Peyz"]}, "draft_rule": "Fearless", "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Locke"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Qiyana"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Renata Glasc"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Cassiopeia"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Orianna"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Pantheon"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Olaf"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Nautilus"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Ambessa"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Xin Zhao"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Alistar"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Wukong"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Xayah"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Rell"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Kai'Sa"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Trundle"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Tristana"}]}, "history": [{"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": true, "blue_gd15": -38, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Syndra"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Renekton"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Jayce"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yorick"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Yorick", "k": 2, "d": 1, "a": 6}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 1, "d": 5, "a": 5}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Syndra", "k": 3, "d": 1, "a": 7}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 5, "d": 5, "a": 4}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Lulu", "k": 0, "d": 0, "a": 10}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Jayce", "k": 1, "d": 1, "a": 5}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Cho'Gath", "k": 1, "d": 6, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Orianna", "k": 7, "d": 0, "a": 1}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Lucian", "k": 2, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion": "Milio", "k": 1, "d": 2, "a": 10}]}, {"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 2, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": false, "blue_gd15": -1351, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Trundle"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Olaf"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Ashe"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Seraphine"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Ryze"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Lee Sin"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Camille"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Nautilus"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Galio"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Renata Glasc"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Naafiri"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Maokai"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Ezreal"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Karma"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yone"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Camille", "k": 1, "d": 6, "a": 2}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Maokai", "k": 1, "d": 2, "a": 6}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Yone", "k": 1, "d": 2, "a": 4}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Ashe", "k": 4, "d": 3, "a": 1}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Seraphine", "k": 1, "d": 1, "a": 6}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Olaf", "k": 7, "d": 2, "a": 3}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Lee Sin", "k": 3, "d": 3, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Ryze", "k": 2, "d": 0, "a": 6}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Ezreal", "k": 1, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion": "Karma", "k": 1, "d": 1, "a": 8}]}, {"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 3, "patch": "26.17", "blue": "Top Esports", "red": "Invictus Gaming", "blue_win": true, "blue_gd15": 2775, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Ahri"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Vi"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Galio"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Viktor"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Qiyana"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Locke"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Jarvan IV"}, {"turn": 11, "sid
```

### 3. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
print('keys', list(d.keys()))
print('coverage', json.dumps(d['coverage'], indent=2))
print('history len', len(d['history']))
# events in history
from collections import Counter
print(Counter([h.get('event') for h in d['history']]))
"
```

### 4. 命令结果

```
keys ['phase', 'series_time_utc', 'current', 'history', 'coverage']
coverage {
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
history len 96
Counter({'worlds-2026-main-event': 62, 'worlds-2026-play-in': 22, 'lpl-2026-regional-finals': 12})
```

### 5. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
for h in d['history']:
    if 'Karmine' in h['blue'] or 'Karmine' in h['red'] or 'T1' in h['blue'] or 'T1' in h['red']:
        print(h['series'], 'n',h['n'], h['patch'], h['blue'],'vs',h['red'], 'blue_win', h['blue_win'], 'gd15', h.get('blue_gd15'))
"
```

### 6. 命令结果

```
worlds-2026-play-in-round-1-1 n 1 26.20 Karmine Corp vs Cloud9 blue_win False gd15 -1525
worlds-2026-play-in-round-1-1 n 2 26.20 Cloud9 vs Karmine Corp blue_win False gd15 395
worlds-2026-play-in-round-1-1 n 3 26.20 Karmine Corp vs Cloud9 blue_win False gd15 -236
worlds-2026-play-in-round-1-1 n 4 26.20 Cloud9 vs Karmine Corp blue_win False gd15 -4476
worlds-2026-play-in-round-1-1 n 5 26.20 Karmine Corp vs Cloud9 blue_win True gd15 622
worlds-2026-play-in-round-2-1 n 1 26.20 Karmine Corp vs MVK Esports blue_win True gd15 3377
worlds-2026-play-in-round-2-1 n 2 26.20 Karmine Corp vs MVK Esports blue_win True gd15 -3003
worlds-2026-play-in-round-2-1 n 3 26.20 MVK Esports vs Karmine Corp blue_win False gd15 -2837
worlds-2026-play-in-round-3-1 n 1 26.20 Karmine Corp vs MVK Esports blue_win True gd15 3288
worlds-2026-play-in-round-3-1 n 2 26.20 Karmine Corp vs MVK Esports blue_win True gd15 6558
worlds-2026-play-in-round-3-1 n 3 26.20 MVK Esports vs Karmine Corp blue_win False gd15 -2294
worlds-2026-main-event-round-1-4 n 1 26.20 Karmine Corp vs Anyone's Legend blue_win True gd15 -461
worlds-2026-main-event-round-1-7 n 1 26.20 LØS vs T1 blue_win False gd15 -2368
worlds-2026-main-event-round-2-4 n 1 26.20 Karmine Corp vs LYON blue_win False gd15 2170
worlds-2026-main-event-round-2-7 n 1 26.20 Dplus Kia vs T1 blue_win True gd15 -3024
worlds-2026-main-event-round-3-5 n 1 26.20 T1 vs CTBC Flying Oyster blue_win True gd15 -1582
worlds-2026-main-event-round-3-6 n 1 26.20 Bilibili Gaming vs Karmine Corp blue_win True gd15 1055
worlds-2026-main-event-round-4-1 n 1 26.20 T1 vs Movistar KOI blue_win True gd15 -138
worlds-2026-main-event-round-4-1 n 2 26.20 T1 vs Movistar KOI blue_win True gd15 3510
worlds-2026-main-event-round-4-3 n 1 26.20 Karmine Corp vs CTBC Flying Oyster blue_win True gd15 1279
worlds-2026-main-event-round-4-3 n 2 26.20 CTBC Flying Oyster vs Karmine Corp blue_win False gd15 3870
worlds-2026-main-event-round-5-1 n 1 26.20 Karmine Corp vs Movistar KOI blue_win True gd15 1380
worlds-2026-main-event-round-5-1 n 2 26.20 Karmine Corp vs Movistar KOI blue_win True gd15 4093
worlds-2026-main-event-quarterfinals-4 n 1 26.20 T1 vs Karmine Corp blue_win True gd15 -660
```

### 7. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
for h in d['history']:
    if h['series']=='worlds-2026-main-event-quarterfinals-4':
        print(json.dumps(h, indent=2))
"
```

### 8. 命令结果

```
{
  "series": "worlds-2026-main-event-quarterfinals-4",
  "series_time": "2026-11-06T22:00:00+00:00",
  "event": "worlds-2026-main-event",
  "n": 1,
  "patch": "26.20",
  "blue": "T1",
  "red": "Karmine Corp",
  "blue_win": true,
  "blue_gd15": -660,
  "bp": [
    {
      "turn": 1,
      "side": "red",
      "action": "ban",
      "champion": "Nocturne"
    },
    {
      "turn": 2,
      "side": "blue",
      "action": "ban",
      "champion": "Cassiopeia"
    },
    {
      "turn": 3,
      "side": "red",
      "action": "ban",
      "champion": "Renata Glasc"
    },
    {
      "turn": 4,
      "side": "blue",
      "action": "ban",
      "champion": "Vi"
    },
    {
      "turn": 5,
      "side": "red",
      "action": "ban",
      "champion": "Galio"
    },
    {
      "turn": 6,
      "side": "blue",
      "action": "ban",
      "champion": "Qiyana"
    },
    {
      "turn": 7,
      "side": "red",
      "action": "pick",
      "champion": "Rumble"
    },
    {
      "turn": 8,
      "side": "blue",
      "action": "pick",
      "champion": "Lulu"
    },
    {
      "turn": 9,
      "side": "blue",
      "action": "pick",
      "champion": "Jarvan IV"
    },
    {
      "turn": 10,
      "side": "red",
      "action": "pick",
      "champion": "Ezreal"
    },
    {
      "turn": 11,
      "side": "red",
      "action": "pick",
      "champion": "Leona"
    },
    {
      "turn": 12,
      "side": "blue",
      "action": "pick",
      "champion": "Yunara"
    },
    {
      "turn": 13,
      "side": "blue",
      "action": "ban",
      "champion": "Wukong"
    },
    {
      "turn": 14,
      "side": "red",
      "action": "ban",
      "champion": "Locke"
    },
    {
      "turn": 15,
      "side": "blue",
      "action": "ban",
      "champion": "Pantheon"
    },
    {
      "turn": 16,
      "side": "red",
      "action": "ban",
      "champion": "Orianna"
    },
    {
      "turn": 17,
      "side": "blue",
      "action": "pick",
      "champion": "Ornn"
    },
    {
      "turn": 18,
      "side": "red",
      "action": "pick",
      "champion": "Syndra"
    },
    {
      "turn": 19,
      "side": "red",
      "action": "pick",
      "champion": "Lee Sin"
    },
    {
      "turn": 20,
      "side": "blue",
      "action": "pick",
      "champion": "Viktor"
    }
  ],
  "players": [
    {
      "name": "Doran",
      "role": "Top",
      "side": "blue",
      "champion": "Ornn",
      "k": 1,
      "d": 3,
      "a": 13
    },
    {
      "name": "Oner",
      "role": "Jungle",
      "side": "blue",
      "champion": "Jarvan IV",
      "k": 4,
      "d": 1,
      "a": 18
    },
    {
      "name": "Faker",
      "role": "Mid",
      "side": "blue",
      "champion": "Viktor",
      "k": 7,
      "d": 0,
      "a": 5
    },
    {
      "name": "Peyz",
      "role": "Bot",
      "side": "blue",
      "champion": "Yunara",
      "k": 11,
      "d": 1,
      "a": 6
    },
    {
      "name": "Keria",
      "role": "Support",
      "side": "blue",
      "champion": "Lulu",
      "k": 0,
      "d": 2,
      "a": 15
    },
    {
      "name": "Canna",
      "role": "Top",
      "side": "red",
      "champion": "Rumble",
      "k": 2,
      "d": 4,
      "a": 3
    },
    {
      "name": "Yike",
      "role": "Jungle",
      "side": "red",
      "champion": "Lee Sin",
      "k": 2,
      "d": 5,
      "a": 2
    },
    {
      "name": "Kyeahoo",
      "role": "Mid",
      "side": "red",
      "champion": "Syndra",
      "k": 2,
      "d": 5,
      "a": 2
    },
    {
      "name": "Caliste",
      "role": "Bot",
      "side": "red",
      "champion": "Ezreal",
      "k": 1,
      "d": 3,
      "a": 2
    },
    {
      "name": "Busio",
      "role": "Support",
      "side": "red",
      "champion": "Leona",
      "k": 0,
      "d": 6,
      "a": 4
    }
  ]
}
```

### 9. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
h=d['history']
n=len(h)
bw=sum(1 for x in h if x['blue_win'])
print('total', n, 'blue win', bw, 'blue winrate', bw/n)
gd=[x for x in h if x.get('blue_gd15') is not None]
print('with gd15', len(gd))
ahead=sum(1 for x in gd if x['blue_gd15']>0)
print('blue ahead15', ahead, 'rate', ahead/len(gd))
# among ahead at 15, win rate
aw=sum(1 for x in gd if x['blue_gd15']>0 and x['blue_win'])
bw2=sum(1 for x in gd if x['blue_gd15']<=0 and x['blue_win'])
print('ahead->win', aw, 'of', ahead)
behind=[x for x in gd if x['blue_gd15']<=0]
print('behind->win', bw2, 'of', len(behind))
"
```

### 10. 命令结果

```
total 96 blue win 54 blue winrate 0.5625
with gd15 96
blue ahead15 50 rate 0.5208333333333334
ahead->win 35 of 50
behind->win 19 of 46
```

### 11. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
h=[x for x in d['history'] if x['event']=='worlds-2026-main-event']
for x in sorted(h, key=lambda z:(z['series'],z['n'])):
    print(x['series'], 'n',x['n'], x['blue'],'vs',x['red'], 'blue_win' if x['blue_win'] else 'red_win', 'gd15', x['blue_gd15'])
"
```

### 12. 命令结果

```
worlds-2026-main-event-quarterfinals-1 n 1 Invictus Gaming vs Top Esports blue_win gd15 998
worlds-2026-main-event-quarterfinals-1 n 2 Invictus Gaming vs Top Esports red_win gd15 949
worlds-2026-main-event-quarterfinals-1 n 3 Top Esports vs Invictus Gaming red_win gd15 -2282
worlds-2026-main-event-quarterfinals-1 n 4 Invictus Gaming vs Top Esports blue_win gd15 942
worlds-2026-main-event-quarterfinals-2 n 1 Gen.G vs LYON blue_win gd15 841
worlds-2026-main-event-quarterfinals-2 n 2 Gen.G vs LYON blue_win gd15 3080
worlds-2026-main-event-quarterfinals-2 n 3 Gen.G vs LYON blue_win gd15 468
worlds-2026-main-event-quarterfinals-3 n 1 Bilibili Gaming vs Dplus Kia blue_win gd15 -416
worlds-2026-main-event-quarterfinals-3 n 2 Dplus Kia vs Bilibili Gaming red_win gd15 593
worlds-2026-main-event-quarterfinals-3 n 3 Dplus Kia vs Bilibili Gaming red_win gd15 -2537
worlds-2026-main-event-quarterfinals-4 n 1 T1 vs Karmine Corp blue_win gd15 -660
worlds-2026-main-event-round-1-1 n 1 Invictus Gaming vs Gen.G red_win gd15 1892
worlds-2026-main-event-round-1-2 n 1 Top Esports vs Hanwha Life Esports red_win gd15 -943
worlds-2026-main-event-round-1-3 n 1 Movistar KOI vs Bilibili Gaming blue_win gd15 1088
worlds-2026-main-event-round-1-4 n 1 Karmine Corp vs Anyone's Legend blue_win gd15 -461
worlds-2026-main-event-round-1-5 n 1 Dplus Kia vs G2 Esports blue_win gd15 -2185
worlds-2026-main-event-round-1-6 n 1 Team Liquid vs CTBC Flying Oyster red_win gd15 206
worlds-2026-main-event-round-1-7 n 1 LØS vs T1 red_win gd15 -2368
worlds-2026-main-event-round-1-8 n 1 LYON vs Team Secret Whales blue_win gd15 -51
worlds-2026-main-event-round-2-1 n 1 Top Esports vs Anyone's Legend blue_win gd15 417
worlds-2026-main-event-round-2-2 n 1 Movistar KOI vs CTBC Flying Oyster blue_win gd15 1314
worlds-2026-main-event-round-2-3 n 1 LØS vs G2 Esports red_win gd15 -753
worlds-2026-main-event-round-2-4 n 1 Karmine Corp vs LYON red_win gd15 2170
worlds-2026-main-event-round-2-5 n 1 Team Secret Whales vs Invictus Gaming red_win gd15 -944
worlds-2026-main-event-round-2-6 n 1 Hanwha Life Esports vs Gen.G red_win gd15 -1021
worlds-2026-main-event-round-2-7 n 1 Dplus Kia vs T1 blue_win gd15 -3024
worlds-2026-main-event-round-2-8 n 1 Team Liquid vs Bilibili Gaming red_win gd15 293
worlds-2026-main-event-round-3-1 n 1 Invictus Gaming vs Hanwha Life Esports blue_win gd15 856
worlds-2026-main-event-round-3-2 n 1 Top Esports vs G2 Esports blue_win gd15 -562
worlds-2026-main-event-round-3-3 n 1 Movistar KOI vs Dplus Kia red_win gd15 -767
worlds-2026-main-event-round-3-3 n 2 Dplus Kia vs Movistar KOI blue_win gd15 5439
worlds-2026-main-event-round-3-4 n 1 LYON vs Gen.G blue_win gd15 -1063
worlds-2026-main-event-round-3-4 n 2 Gen.G vs LYON blue_win gd15 1623
worlds-2026-main-event-round-3-4 n 3 Gen.G vs LYON blue_win gd15 -2221
worlds-2026-main-event-round-3-5 n 1 T1 vs CTBC Flying Oyster blue_win gd15 -1582
worlds-2026-main-event-round-3-6 n 1 Bilibili Gaming vs Karmine Corp blue_win gd15 1055
worlds-2026-main-event-round-3-7 n 1 Team Secret Whales vs LØS red_win gd15 1421
worlds-2026-main-event-round-3-7 n 2 Team Secret Whales vs LØS red_win gd15 -1500
worlds-2026-main-event-round-3-8 n 1 Anyone's Legend vs Team Liquid red_win gd15 -1385
worlds-2026-main-event-round-3-8 n 2 Team Liquid vs Anyone's Legend blue_win gd15 3170
worlds-2026-main-event-round-4-1 n 1 T1 vs Movistar KOI blue_win gd15 -138
worlds-2026-main-event-round-4-1 n 2 T1 vs Movistar KOI blue_win gd15 3510
worlds-2026-main-event-round-4-2 n 1 LYON vs Invictus Gaming red_win gd15 -1628
worlds-2026-main-event-round-4-2 n 2 Invictus Gaming vs LYON red_win gd15 338
worlds-2026-main-event-round-4-2 n 3 LYON vs Invictus Gaming red_win gd15 -4021
worlds-2026-main-event-round-4-3 n 1 Karmine Corp vs CTBC Flying Oyster blue_win gd15 1279
worlds-2026-main-event-round-4-3 n 2 CTBC Flying Oyster vs Karmine Corp red_win gd15 3870
worlds-2026-main-event-round-4-4 n 1 Bilibili Gaming vs Top Esports blue_win gd15 1957
worlds-2026-main-event-round-4-4 n 2 Bilibili Gaming vs Top Esports red_win gd15 923
worlds-2026-main-event-round-4-4 n 3 Top Esports vs Bilibili Gaming blue_win gd15 2986
worlds-2026-main-event-round-4-5 n 1 LØS vs Team Liquid blue_win gd15 1483
worlds-2026-main-event-round-4-5 n 2 LØS vs Team Liquid red_win gd15 -1870
worlds-2026-main-event-round-4-5 n 3 Team Liquid vs LØS red_win gd15 -4667
worlds-2026-main-event-round-4-6 n 1 G2 Esports vs Hanwha Life Esports red_win gd15 -495
worlds-2026-main-event-round-4-6 n 2 Hanwha Life Esports vs G2 Esports blue_win gd15 -126
worlds-2026-main-event-round-5-1 n 1 Karmine Corp vs Movistar KOI blue_win gd15 1380
worlds-2026-main-event-round-5-1 n 2 Karmine Corp vs Movistar KOI blue_win gd15 4093
worlds-2026-main-event-round-5-2 n 1 LYON vs LØS red_win gd15 -1315
worlds-2026-main-event-round-5-2 n 2 LØS vs LYON red_win gd15 962
worlds-2026-main-event-round-5-2 n 3 LYON vs LØS blue_win gd15 1412
worlds-2026-main-event-round-5-3 n 1 Bilibili Gaming vs Hanwha Life Esports blue_win gd15 197
worlds-2026-main-event-round-5-3 n 2 Bilibili Gaming vs Hanwha Life Esports blue_win gd15 1331
```

### 13. 工具调用 · Write

```
{
  "file_path": "[ephemeral]/app/prediction.json",
  "content": "{\"p_blue_win\": 0.26, \"p_blue_ahead_15\": 0.57}\n"
}
```

### 14. 工具结果

```
File created successfully at: [ephemeral]/app/prediction.json (file state is current in your context — no need to Read it back)
```

### 15. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
for x in d['history']:
    if x['event']=='worlds-2026-main-event' and ('T1' in x['blue'] or 'T1' in x['red']):
        print('===', x['series'], 'n',x['n'], x['blue'],'vs',x['red'], 'winner', 'blue' if x['blue_win'] else 'red', 'gd15', x['blue_gd15'])
        for p in x['players']:
            print('  ', p['side'], p['name'], p['role'], p['champion'], f\"{p['k']}/{p['d']}/{p['a']}\")
"
```

### 16. 命令结果

```
=== worlds-2026-main-event-round-1-7 n 1 LØS vs T1 winner red gd15 -2368
   blue Zest Top K'Sante 1/5/1
   blue Curse Jungle Pantheon 0/5/2
   blue Feisty Mid Syndra 2/3/1
   blue Duduhh Bot Tristana 0/3/2
   blue Ackerman Support Rakan 0/3/3
   red Doran Top Jayce 4/0/9
   red Oner Jungle Lee Sin 8/0/6
   red Faker Mid LeBlanc 6/0/7
   red Peyz Bot Jhin 1/1/9
   red Keria Support Alistar 0/2/15
=== worlds-2026-main-event-round-2-7 n 1 Dplus Kia vs T1 winner blue gd15 -3024
   blue Siwoo Top K'Sante 0/2/3
   blue Lucid Jungle Jarvan IV 2/3/6
   blue ShowMaker Mid Viktor 2/2/4
   blue Smash Bot Kalista 4/0/3
   blue Career Support Renata Glasc 2/1/6
   red Doran Top Jayce 1/3/1
   red Oner Jungle Vi 2/3/5
   red Faker Mid Anivia 1/2/4
   red Peyz Bot Caitlyn 4/1/2
   red Keria Support Neeko 0/1/5
=== worlds-2026-main-event-round-3-5 n 1 T1 vs CTBC Flying Oyster winner blue gd15 -1582
   blue Doran Top Ambessa 3/3/6
   blue Oner Jungle Vi 4/1/5
   blue Faker Mid Galio 2/1/8
   blue Peyz Bot Jhin 3/1/8
   blue Keria Support Rakan 2/0/10
   red Rest Top Rumble 0/3/1
   red Shad0w Jungle Qiyana 2/2/3
   red POUT Mid Ryze 0/2/2
   red Doggo Bot Kai'Sa 4/3/2
   red Kino Support Alistar 0/4/6
=== worlds-2026-main-event-round-4-1 n 1 T1 vs Movistar KOI winner blue gd15 -138
   blue Doran Top Ambessa 6/0/6
   blue Oner Jungle Lee Sin 6/3/9
   blue Faker Mid Syndra 5/2/8
   blue Peyz Bot Xayah 2/3/9
   blue Keria Support Nautilus 1/2/14
   red Myrwn Top Gnar 2/3/4
   red Elyoya Jungle Qiyana 3/6/5
   red Jojopyun Mid Akali 2/5/2
   red Supa Bot Kai'Sa 3/2/4
   red Alvaro Support Alistar 0/4/9
=== worlds-2026-main-event-round-4-1 n 2 T1 vs Movistar KOI winner blue gd15 3510
   blue Doran Top Gwen 4/0/7
   blue Oner Jungle Jarvan IV 2/3/13
   blue Faker Mid Orianna 5/2/10
   blue Peyz Bot Jhin 8/1/5
   blue Keria Support Karma 3/3/16
   red Myrwn Top Ornn 0/4/3
   red Elyoya Jungle Xin Zhao 2/3/4
   red Jojopyun Mid Viktor 2/5/3
   red Supa Bot Ezreal 3/3/1
   red Alvaro Support Seraphine 2/7/6
=== worlds-2026-main-event-quarterfinals-4 n 1 T1 vs Karmine Corp winner blue gd15 -660
   blue Doran Top Ornn 1/3/13
   blue Oner Jungle Jarvan IV 4/1/18
   blue Faker Mid Viktor 7/0/5
   blue Peyz Bot Yunara 11/1/6
   blue Keria Support Lulu 0/2/15
   red Canna Top Rumble 2/4/3
   red Yike Jungle Lee Sin 2/5/2
   red Kyeahoo Mid Syndra 2/5/2
   red Caliste Bot Ezreal 1/3/2
   red Busio Support Leona 0/6/4
```

### 17. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
for x in d['history']:
    if 'Karmine' in x['blue'] or 'Karmine' in x['red']:
        print('===', x['series'], 'n',x['n'], x['blue'],'vs',x['red'], 'winner', 'blue' if x['blue_win'] else 'red', 'gd15(blue)', x['blue_gd15'])
        for p in x['players']:
            print('  ', p['side'], p['name'], p['role'], p['champion'], f\"{p['k']}/{p['d']}/{p['a']}\")
"
```

### 18. 命令结果

```
=== worlds-2026-play-in-round-1-1 n 1 Karmine Corp vs Cloud9 winner red gd15(blue) -1525
   blue Canna Top Rumble 0/4/0
   blue Yike Jungle Lee Sin 0/1/1
   blue Kyeahoo Mid Syndra 1/3/0
   blue Caliste Bot Miss Fortune 0/6/1
   blue Busio Support Nautilus 0/6/1
   red Thanatos Top Gnar 1/0/5
   red Blaber Jungle Xin Zhao 4/0/10
   red Loki Mid Locke 11/0/3
   red Tactical Bot Ezreal 3/0/9
   red Vulcan Support Karma 1/1/16
=== worlds-2026-play-in-round-1-1 n 2 Cloud9 vs Karmine Corp winner red gd15(blue) 395
   blue Thanatos Top Camille 4/5/6
   blue Blaber Jungle Wukong 1/4/9
   blue Loki Mid Akali 5/2/1
   blue Tactical Bot Kalista 6/1/5
   blue Vulcan Support Renata Glasc 0/2/13
   red Canna Top Jayce 5/4/4
   red Yike Jungle Vi 1/4/11
   red Kyeahoo Mid Cassiopeia 2/4/5
   red Caliste Bot Varus 4/2/6
   red Busio Support Vel'Koz 2/2/6
=== worlds-2026-play-in-round-1-1 n 3 Karmine Corp vs Cloud9 winner red gd15(blue) -236
   blue Canna Top Kled 0/4/1
   blue Yike Jungle Naafiri 1/5/2
   blue Kyeahoo Mid Anivia 2/8/1
   blue Caliste Bot Lucian 2/2/3
   blue Busio Support Nami 0/3/5
   red Thanatos Top Olaf 5/1/3
   red Blaber Jungle Jarvan IV 7/0/14
   red Loki Mid Annie 1/2/14
   red Tactical Bot Jhin 7/1/7
   red Vulcan Support Alistar 2/1/12
=== worlds-2026-play-in-round-1-1 n 4 Cloud9 vs Karmine Corp winner red gd15(blue) -4476
   blue Thanatos Top Zaahen 2/1/1
   blue Blaber Jungle Sejuani 0/2/6
   blue Loki Mid Sylas 0/5/4
   blue Tactical Bot Yunara 3/4/2
   blue Vulcan Support Lulu 1/3/4
   red Canna Top Renekton 1/0/8
   red Yike Jungle Qiyana 1/2/6
   red Kyeahoo Mid Orianna 2/2/5
   red Caliste Bot Xayah 11/1/3
   red Busio Support Rakan 0/1/9
=== worlds-2026-play-in-round-1-1 n 5 Karmine Corp vs Cloud9 winner blue gd15(blue) 622
   blue Canna Top Ambessa 3/1/7
   blue Yike Jungle Trundle 5/1/10
   blue Kyeahoo Mid Ahri 6/1/8
   blue Caliste Bot Kai'Sa 3/1/10
   blue Busio Support Rell 0/4/14
   red Thanatos Top K'Sante 4/2/1
   red Blaber Jungle Lillia 0/4/3
   red Loki Mid Yone 1/4/3
   red Tactical Bot Ziggs 3/3/2
   red Vulcan Support Shen 0/4/6
=== worlds-2026-play-in-round-2-1 n 1 Karmine Corp vs MVK Esports winner blue gd15(blue) 3377
   blue Canna Top Jayce 2/1/3
   blue Yike Jungle Vi 1/1/4
   blue Kyeahoo Mid Syndra 3/0/1
   blue Caliste Bot Draven 3/1/4
   blue Busio Support Nautilus 0/1/7
   red Kratos Top Ambessa 0/1/1
   red Gury Jungle Maokai 0/3/3
   red Chika Mid K'Sante 1/1/1
   red Harky Bot Tristana 3/3/1
   red SiuLoong Support Lulu 0/1/3
=== worlds-2026-play-in-round-2-1 n 2 Karmine Corp vs MVK Esports winner blue gd15(blue) -3003
   blue Canna Top Galio 1/4/12
   blue Yike Jungle Lee Sin 5/1/8
   blue Kyeahoo Mid Ahri 6/1/6
   blue Caliste Bot Ashe 5/3/10
   blue Busio Support Seraphine 4/2/14
   red Kratos Top Twisted Fate 3/4/1
   red SanSan Jungle Qiyana 3/4/4
   red Chika Mid Rumble 2/6/2
   red Harky Bot Ezreal 2/3/3
   red SiuLoong Support Pyke 1/4/3
=== worlds-2026-play-in-round-2-1 n 3 MVK Esports vs Karmine Corp winner red gd15(blue) -2837
   blue Kratos Top Yorick 1/2/1
   blue SanSan Jungle Wukong 0/4/4
   blue Chika Mid Kog'Maw 3/6/1
   blue Harky Bot Lucian 2/0/2
   blue SiuLoong Support Milio 1/2/3
   red Canna Top Kennen 6/2/1
   red Yike Jungle Jarvan IV 5/1/5
   red Kyeahoo Mid Viktor 1/4/3
   red Caliste Bot Xayah 2/0/3
   red Busio Support Rakan 0/0/9
=== worlds-2026-play-in-round-3-1 n 1 Karmine Corp vs MVK Esports winner blue gd15(blue) 3288
   blue Canna Top Jayce 1/0/6
   blue Yike Jungle Lee Sin 2/0/5
   blue Kyeahoo Mid Cassiopeia 4/1/2
   blue Caliste Bot Zeri 6/1/1
   blue Busio Support Yuumi 0/0/10
   red Kratos Top Yorick 0/4/0
   red Gury Jungle Jarvan IV 1/2/0
   red Chika Mid Akali 0/4/0
   red Harky Bot Ashe 1/1/1
   red SiuLoong Support Seraphine 0/2/0
=== worlds-2026-play-in-round-3-1 n 2 Karmine Corp vs MVK Esports winner blue gd15(blue) 6558
   blue Canna Top Galio 0/2/7
   blue Yike Jungle Qiyana 9/2/2
   blue Kyeahoo Mid Ryze 5/1/4
   blue Caliste Bot Yunara 2/0/6
   blue Busio Support Lulu 1/1/5
   red Kratos Top Rumble 1/6/1
   red Gury Jungle Malphite 1/3/0
   red Chika Mid Hwei 1/5/0
   red Harky Bot Lucian 1/3/1
   red SiuLoong Support Milio 0/0/3
=== worlds-2026-play-in-round-3-1 n 3 MVK Esports vs Karmine Corp winner red gd15(blue) -2294
   blue Kratos Top Yone 2/4/4
   blue Gury Jungle Aatrox 2/5/6
   blue Chika Mid Locke 3/5/2
   blue Harky Bot Twitch 0/5/4
   blue SiuLoong Support Camille 5/6/3
   red Canna Top Zaahen 5/6/4
   red Yike Jungle Naafiri 6/3/6
   red Kyeahoo Mid Viktor 4/0/11
   red Caliste Bot Ezreal 9/1/3
   red Busio Support Leona 1/2/10
=== worlds-2026-main-event-round-1-4 n 1 Karmine Corp vs Anyone's Legend winner blue gd15(blue) -461
   blue Canna Top Jax 5/2/1
   blue Yike Jungle Jarvan IV 3/1/9
   blue Kyeahoo Mid Orianna 1/1/9
   blue Caliste Bot Kalista 3/0/6
   blue Busio Support Renata Glasc 0/0/11
   red Breathe Top Olaf 1/2/1
   red Tarzan Jungle Nocturne 0/2/3
   red Shanks Mid Akali 1/2/2
   red Hope Bot Miss Fortune 2/3/1
   red Kael Support Neeko 0/3/3
=== worlds-2026-main-event-round-2-4 n 1 Karmine Corp vs LYON winner red gd15(blue) 2170
   blue Canna Top Rumble 4/2/8
   blue Yike Jungle Lee Sin 3/4/4
   blue Kyeahoo Mid Cassiopeia 1/3/9
   blue Caliste Bot Kalista 6/4/8
   blue Busio Support Renata Glasc 1/2/14
   red Dhokla Top Galio 2/1/12
   red Inspired Jungle Wukong 2/3/11
   red Saint Mid Syndra 6/2/6
   red Berserker Bot Yunara 5/4/8
   red Isles Support Lulu 0/5/13
=== worlds-2026-main-event-round-3-6 n 1 Bilibili Gaming vs Karmine Corp winner blue gd15(blue) 1055
   blue Bin Top Ambessa 4/1/7
   blue Xun Jungle Jarvan IV 2/2/12
   blue Knight Mid Orianna 3/1/11
   blue Viper Bot Kai'Sa 5/1/6
   blue ON Support Nautilus 0/6/13
   red Canna Top Rumble 2/2/4
   red Yike Jungle Lee Sin 4/4/5
   red Kyeahoo Mid Viktor 1/4/8
   red Caliste Bot Jhin 4/1/4
   red Busio Support Alistar 0/3/9
=== worlds-2026-main-event-round-4-3 n 1 Karmine Corp vs CTBC Flying Oyster winner blue gd15(blue) 1279
   blue Canna Top Galio 2/0/10
   blue Yike Jungle Wukong 4/0/11
   blue Kyeahoo Mid Cassiopeia 6/1/8
   blue Caliste Bot Tristana 7/0/5
   blue Busio Support Nautilus 0/2/12
   red Rest Top Rumble 0/2/1
   red Shad0w Jungle Jarvan IV 0/6/3
   red POUT Mid Syndra 3/3/0
   red Doggo Bot Kai'Sa 0/3/0
   red Kino Support Alistar 0/5/2
=== worlds-2026-main-event-round-4-3 n 2 CTBC Flying Oyster vs Karmine Corp winner red gd15(blue) 3870
   blue Rest Top Ambessa 1/5/2
   blue Shad0w Jungle Lee Sin 5/3/4
   blue POUT Mid Ryze 3/3/3
   blue Doggo Bot Caitlyn 2/6/7
   blue Kino Support Karma 1/3/9
   red Canna Top Camille 5/3/4
   red Yike Jungle Pantheon 4/2/12
   red Kyeahoo Mid Viktor 6/0/11
   red Caliste Bot Yunara 4/4/12
   red Busio Support Lulu 1/3/17
=== worlds-2026-main-event-round-5-1 n 1 Karmine Corp vs Movistar KOI winner blue gd15(blue) 1380
   blue Canna Top Renekton 3/5/6
   blue Yike Jungle Wukong 2/2/9
   blue Kyeahoo Mid Syndra 3/2/6
   blue Caliste Bot Ashe 5/3/7
   blue Busio Support Seraphine 0/2/12
   red Myrwn Top Camille 4/4/6
   red Elyoya Jungle Sejuani 3/3/9
   red Jojopyun Mid Cassiopeia 5/2/5
   red Supa Bot Zeri 2/3/5
   red Alvaro Support Yuumi 0/1/12
=== worlds-2026-main-event-round-5-1 n 2 Karmine Corp vs Movistar KOI winner blue gd15(blue) 4093
   blue Canna Top Rumble 3/2/6
   blue Yike Jungle Pantheon 9/0/5
   blue Kyeahoo Mid Viktor 1/0/8
   blue Caliste Bot Sivir 5/1/7
   blue Busio Support Lulu 0/1/15
   red Myrwn Top Ornn 1/4/2
   red Elyoya Jungle Lee Sin 1/5/2
   red Jojopyun Mid Anivia 1/4/2
   red Supa Bot Ezreal 1/3/2
   red Alvaro Support Karma 0/2/4
=== worlds-2026-main-event-quarterfinals-4 n 1 T1 vs Karmine Corp winner blue gd15(blue) -660
   blue Doran Top Ornn 1/3/13
   blue Oner Jungle Jarvan IV 4/1/18
   blue Faker Mid Viktor 7/0/5
   blue Peyz Bot Yunara 11/1/6
   blue Keria Support Lulu 0/2/15
   red Canna Top Rumble 2/4/3
   red Yike Jungle Lee Sin 2/5/2
   red Kyeahoo Mid Syndra 2/5/2
   red Caliste Bot Ezreal 1/3/2
   red Busio Support Leona 0/6/4
```

### 19. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
me=[x for x in d['history'] if x['event']=='worlds-2026-main-event']
print('main event blue win', sum(1 for x in me if x['blue_win']), '/', len(me), sum(1 for x in me if x['blue_win'])/len(me))
# same-patch main event
me26=[x for x in me if x['patch']=='26.20']
print('main event 26.20 blue win', sum(1 for x in me26 if x['blue_win']), '/', len(me26), sum(1 for x in me26 if x['blue_win'])/len(me26))
# KC as blue winrate
kcb=[x for x in d['history'] if x['blue']=='Karmine Corp']
print('KC blue games', len(kcb), 'wins', sum(1 for x in kcb if x['blue_win']))
# T1 as red winrate
t1r=[x for x in d['history'] if x['red']=='T1']
print('T1 red games', len(t1r), 'T1 wins(red)', sum(1 for x in t1r if not x['blue_win']))
"
```

### 20. 命令结果

```
main event blue win 35 / 62 0.5645161290322581
main event 26.20 blue win 35 / 62 0.5645161290322581
KC blue games 12 wins 9
T1 red games 2 T1 wins(red) 1
```

### 21. 工具调用 · Write

```
{
  "file_path": "[ephemeral]/app/prediction.json",
  "content": "{\"p_blue_win\": 0.31, \"p_blue_ahead_15\": 0.58}\n"
}
```

### 22. 工具结果

```
The file [ephemeral]/app/prediction.json has been updated successfully. (file state is current in your context — no need to Read it back)
```

### 23. 终端命令

```
python3 -c "
import json
d=json.load(open('[ephemeral]/app/prediction.json'))
print(d)
assert set(d)=={'p_blue_win','p_blue_ahead_15'}
assert all(isinstance(v,(int,float)) and 0<=v<=1 for v in d.values())
print('valid')
"
```

### 24. 命令结果

```
{'p_blue_win': 0.31, 'p_blue_ahead_15': 0.58}
valid
```

### 25. 模型消息

```
I've written the forecast to `prediction.json`. Here's my reasoning:

**Context:** This is Worlds 2026 Quarterfinals, game 2 of a Fearless BO5. T1 (red) leads 1-0 after winning game 1 decisively (23-7 kills) despite being *behind* ~660g at 15:00 — a classic T1 slow-start, strong-finish pattern.

**Win probability — `p_blue_win = 0.31`:**
- T1 is the clear favorite: 5-1 in their recorded games, and they stomped KC in game 1. Their late-game macro is elite.
- But KC has real advantages here: they're on **blue side** (9-3 in their blue-side games this run, 75%), and their game 2 draft is a "comfort comp" — all five KC champions have prior wins this tournament:
  - Canna Ambessa (3/1/7), Yike Pantheon (4/2/12 and 9/0/5), Kyeahoo Orianna (2-0), Caliste Tristana (7/0/5), Busio Rell (0/4/14)
- T1 counter-drafted (Trundle into Ambessa, Cassiopeia's Miasma to ground Ambessa, Olaf to shrug off CC), which keeps them favored, so I settle near 0.31 rather than higher.

**15-minute gold — `p_blue_ahead_15 = 0.58`:**
- KC has been ahead at 15 in ~67% of their blue-side games and ~63% overall, and their Pantheon/Tristana/Rell comp is early-game oriented (bot lane should bully Kai'Sa/Nautilus early).
- T1 frequently concedes early leads (behind at 15 in game 1 vs KC, plus vs CFO and KOI), though their 2 red-side games show them ahead early — so I temper the estimate to 0.58 rather than ~0.65.

Final submission: `{"p_blue_win": 0.31, "p_blue_ahead_15": 0.58}` — validated as finite numbers in [0,1] with exactly the required fields.
```
