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
    "p_blue_win": 0.64,
    "p_blue_ahead_15": 0.66
  },
  "observed_outcome": {
    "p_blue_win": 0,
    "p_blue_ahead_15": 1
  },
  "brier": {
    "p_blue_win": 0.4096,
    "p_blue_ahead_15": 0.11559999999999998
  },
  "reward": 0.7374
}
```

## CLI 报告的 token 用量

```
{
  "input_tokens": 14073,
  "cache_creation_input_tokens": 0,
  "cache_read_input_tokens": 89600,
  "output_tokens": 10422
}
```

## 执行轨迹

### 1. 终端命令

```
ls -la && cat snapshot.json | head -c 3000
```

### 2. 命令结果

```
total 408
drwxr-xr-x@ 3 [local-user]  [local-group]      96 Nov  9 02:05 .
drwx------@ 8 [local-user]  [local-group]     256 Nov  9 02:04 ..
-rw-r--r--@ 1 [local-user]  [local-group]  207367 Nov  9 02:04 snapshot.json
{"phase": "lobby", "series_time_utc": "2026-10-31T18:59:00+00:00", "current": {"event": "worlds-2026-main-event", "stage": "Round 5", "series": "worlds-2026-main-event-round-5-2", "n": 2, "patch": "26.20", "bo": 3, "blue": "LØS", "red": "LYON", "starters": {"blue": ["Ackerman", "Curse", "Duduhh", "Feisty", "Zest"], "red": ["Berserker", "Dhokla", "Inspired", "Isles", "Saint"]}, "draft_rule": "Fearless"}, "history": [{"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": true, "blue_gd15": -38, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Syndra"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Renekton"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Jayce"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yorick"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Yorick", "k": 2, "d": 1, "a": 6}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 1, "d": 5, "a": 5}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Syndra", "k": 3, "d": 1, "a": 7}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 5, "d": 5, "a": 4}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Lulu", "k": 0, "d": 0, "a": 10}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Jayce", "k": 1, "d": 1, "a": 5}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Cho'Gath", "k": 1, "d": 6, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Orianna", "k": 7, "d": 0, "a": 1}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Lucian", "k": 2, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion": "M
```

### 3. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
print('keys', list(d.keys()))
print('coverage', json.dumps(d['coverage'], indent=2))
print('current', json.dumps(d['current'], indent=2))
print('history len', len(d['history']))
"
```

### 4. 命令结果

```
keys ['phase', 'series_time_utc', 'current', 'history', 'coverage']
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
history len 79
```

### 5. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
h=d['history']
blue_starters=set(['Ackerman','Curse','Duduhh','Feisty','Zest'])
red_starters=set(['Berserker','Dhokla','Inspired','Isles','Saint'])
# find games by team name
for g in h:
    if g.get('blue') in ('LØS','LYON') or g.get('red') in ('LØS','LYON'):
        print(g['series'], 'n',g.get('n'), g['patch'], g['blue'],'vs',g['red'], 'win', g.get('blue_win'), 'gd15', g.get('blue_gd15'))
"
```

### 6. 命令结果

```
worlds-2026-main-event-round-1-7 n 1 26.20 LØS vs T1 win False gd15 -2368
worlds-2026-main-event-round-1-8 n 1 26.20 LYON vs Team Secret Whales win True gd15 -51
worlds-2026-main-event-round-2-3 n 1 26.20 LØS vs G2 Esports win False gd15 -753
worlds-2026-main-event-round-2-4 n 1 26.20 Karmine Corp vs LYON win False gd15 2170
worlds-2026-main-event-round-3-4 n 1 26.20 LYON vs Gen.G win True gd15 -1063
worlds-2026-main-event-round-3-4 n 2 26.20 Gen.G vs LYON win True gd15 1623
worlds-2026-main-event-round-3-4 n 3 26.20 Gen.G vs LYON win True gd15 -2221
worlds-2026-main-event-round-3-7 n 1 26.20 Team Secret Whales vs LØS win False gd15 1421
worlds-2026-main-event-round-3-7 n 2 26.20 Team Secret Whales vs LØS win False gd15 -1500
worlds-2026-main-event-round-4-2 n 1 26.20 LYON vs Invictus Gaming win False gd15 -1628
worlds-2026-main-event-round-4-2 n 2 26.20 Invictus Gaming vs LYON win False gd15 338
worlds-2026-main-event-round-4-2 n 3 26.20 LYON vs Invictus Gaming win False gd15 -4021
worlds-2026-main-event-round-4-5 n 1 26.20 LØS vs Team Liquid win True gd15 1483
worlds-2026-main-event-round-4-5 n 2 26.20 LØS vs Team Liquid win False gd15 -1870
worlds-2026-main-event-round-4-5 n 3 26.20 Team Liquid vs LØS win False gd15 -4667
worlds-2026-main-event-round-5-2 n 1 26.20 LYON vs LØS win False gd15 -1315
```

### 7. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
h=d['history']
for g in h:
    if g.get('blue') in ('LØS','LYON') or g.get('red') in ('LØS','LYON'):
        print('===', g['series'], 'n',g.get('n'), 'patch',g['patch'], g['blue'],'(B) vs',g['red'],'(R)')
        print('  blue_win', g.get('blue_win'), 'gd15', g.get('blue_gd15'))
        for p in g.get('players',[]):
            print('   ', p['side'], p['role'], p['name'], p['champion'], 'KDA', p['k'],p['d'],p['a'])
        # draft bans/picks
        bp=g.get('bp',[])
        picks=[(x['side'],x['action'],x['champion']) for x in bp if x['action']=='pick']
        bans=[(x['side'],x['champion']) for x in bp if x['action']=='ban']
        print('  picks', picks)
        print('  bans', bans)
"
```

### 8. 命令结果

```
=== worlds-2026-main-event-round-1-7 n 1 patch 26.20 LØS (B) vs T1 (R)
  blue_win False gd15 -2368
    blue Top Zest K'Sante KDA 1 5 1
    blue Jungle Curse Pantheon KDA 0 5 2
    blue Mid Feisty Syndra KDA 2 3 1
    blue Bot Duduhh Tristana KDA 0 3 2
    blue Support Ackerman Rakan KDA 0 3 3
    red Top Doran Jayce KDA 4 0 9
    red Jungle Oner Lee Sin KDA 8 0 6
    red Mid Faker LeBlanc KDA 6 0 7
    red Bot Peyz Jhin KDA 1 1 9
    red Support Keria Alistar KDA 0 2 15
  picks [('red', 'pick', 'Lee Sin'), ('blue', 'pick', 'Syndra'), ('blue', 'pick', 'Pantheon'), ('red', 'pick', 'Jhin'), ('red', 'pick', 'Jayce'), ('blue', 'pick', "K'Sante"), ('blue', 'pick', 'Tristana'), ('red', 'pick', 'Alistar'), ('red', 'pick', 'LeBlanc'), ('blue', 'pick', 'Rakan')]
  bans [('red', 'Nocturne'), ('blue', 'Bard'), ('red', 'Cassiopeia'), ('blue', 'Vi'), ('red', 'Poppy'), ('blue', 'Qiyana'), ('blue', 'Locke'), ('red', 'Kalista'), ('blue', 'Akali'), ('red', 'Nautilus')]
=== worlds-2026-main-event-round-1-8 n 1 patch 26.20 LYON (B) vs Team Secret Whales (R)
  blue_win True gd15 -51
    blue Top Dhokla K'Sante KDA 2 1 8
    blue Jungle Inspired Nocturne KDA 2 2 11
    blue Mid Saint Anivia KDA 2 0 11
    blue Bot Berserker Ezreal KDA 13 1 5
    blue Support Isles Alistar KDA 3 2 18
    red Top Pun Rumble KDA 0 5 2
    red Jungle Hizto Lee Sin KDA 0 4 3
    red Mid Dire Ryze KDA 4 2 1
    red Bot Eddie Kai'Sa KDA 2 4 3
    red Support Bie Nautilus KDA 0 7 3
  picks [('red', 'pick', 'Ryze'), ('blue', 'pick', 'Ezreal'), ('blue', 'pick', 'Nocturne'), ('red', 'pick', 'Lee Sin'), ('red', 'pick', 'Nautilus'), ('blue', 'pick', 'Alistar'), ('blue', 'pick', 'Anivia'), ('red', 'pick', "Kai'Sa"), ('red', 'pick', 'Rumble'), ('blue', 'pick', "K'Sante")]
  bans [('red', 'Syndra'), ('blue', 'Vi'), ('red', 'Renata Glasc'), ('blue', 'Qiyana'), ('red', 'Olaf'), ('blue', 'Cassiopeia'), ('blue', 'Jhin'), ('red', 'Orianna'), ('blue', 'Corki'), ('red', 'Galio')]
=== worlds-2026-main-event-round-2-3 n 1 patch 26.20 LØS (B) vs G2 Esports (R)
  blue_win False gd15 -753
    blue Top Zest Jayce KDA 3 3 2
    blue Jungle Curse Nocturne KDA 1 5 5
    blue Mid Feisty Orianna KDA 2 4 2
    blue Bot Duduhh Kalista KDA 3 5 3
    blue Support Ackerman Renata Glasc KDA 0 5 7
    red Top BrokenBlade K'Sante KDA 3 1 6
    red Jungle SkewMond Lee Sin KDA 10 1 8
    red Mid Caps Locke KDA 8 5 5
    red Bot Hans Sama Ezreal KDA 1 1 9
    red Support Labrov Karma KDA 0 1 16
  picks [('blue', 'pick', 'Nocturne'), ('red', 'pick', 'Ezreal'), ('red', 'pick', 'Karma'), ('blue', 'pick', 'Jayce'), ('blue', 'pick', 'Orianna'), ('red', 'pick', "K'Sante"), ('red', 'pick', 'Locke'), ('blue', 'pick', 'Kalista'), ('blue', 'pick', 'Renata Glasc'), ('red', 'pick', 'Lee Sin')]
  bans [('blue', 'Olaf'), ('red', 'Vi'), ('blue', 'Jarvan IV'), ('red', 'Seraphine'), ('blue', 'Galio'), ('red', 'Syndra'), ('red', 'Nautilus'), ('blue', 'Akali'), ('red', 'Sivir'), ('blue', 'LeBlanc')]
=== worlds-2026-main-event-round-2-4 n 1 patch 26.20 Karmine Corp (B) vs LYON (R)
  blue_win False gd15 2170
    blue Top Canna Rumble KDA 4 2 8
    blue Jungle Yike Lee Sin KDA 3 4 4
    blue Mid Kyeahoo Cassiopeia KDA 1 3 9
    blue Bot Caliste Kalista KDA 6 4 8
    blue Support Busio Renata Glasc KDA 1 2 14
    red Top Dhokla Galio KDA 2 1 12
    red Jungle Inspired Wukong KDA 2 3 11
    red Mid Saint Syndra KDA 6 2 6
    red Bot Berserker Yunara KDA 5 4 8
    red Support Isles Lulu KDA 0 5 13
  picks [('red', 'pick', 'Wukong'), ('blue', 'pick', 'Lee Sin'), ('blue', 'pick', 'Rumble'), ('red', 'pick', 'Galio'), ('red', 'pick', 'Syndra'), ('blue', 'pick', 'Cassiopeia'), ('blue', 'pick', 'Renata Glasc'), ('red', 'pick', 'Yunara'), ('red', 'pick', 'Lulu'), ('blue', 'pick', 'Kalista')]
  bans [('red', 'Jayce'), ('blue', 'Ezreal'), ('red', 'Vi'), ('blue', 'Nocturne'), ('red', 'Qiyana'), ('blue', "K'Sante"), ('blue', 'Seraphine'), ('red', 'Jhin'), ('blue', 'Caitlyn'), ('red', 'Olaf')]
=== worlds-2026-main-event-round-3-4 n 1 patch 26.20 LYON (B) vs Gen.G (R)
  blue_win True gd15 -1063
    blue Top Dhokla Olaf KDA 2 3 2
    blue Jungle Inspired Xin Zhao KDA 1 0 8
    blue Mid Saint Ahri KDA 3 0 6
    blue Bot Berserker Kalista KDA 4 0 4
    blue Support Isles Renata Glasc KDA 0 1 9
    red Top Kiin Rumble KDA 2 1 1
    red Jungle Canyon Qiyana KDA 0 1 3
    red Mid Chovy Anivia KDA 0 3 1
    red Bot Ruler Jhin KDA 1 2 2
    red Support Duro Alistar KDA 1 3 2
  picks [('red', 'pick', 'Qiyana'), ('blue', 'pick', 'Kalista'), ('blue', 'pick', 'Renata Glasc'), ('red', 'pick', 'Jhin'), ('red', 'pick', 'Alistar'), ('blue', 'pick', 'Olaf'), ('blue', 'pick', 'Xin Zhao'), ('red', 'pick', 'Anivia'), ('red', 'pick', 'Rumble'), ('blue', 'pick', 'Ahri')]
  bans [('red', 'Nocturne'), ('blue', 'Cassiopeia'), ('red', 'Ezreal'), ('blue', 'Akali'), ('red', 'Vi'), ('blue', 'Syndra'), ('blue', "K'Sante"), ('red', 'Lee Sin'), ('blue', 'Jax'), ('red', 'LeBlanc')]
=== worlds-2026-main-event-round-3-4 n 2 patch 26.20 Gen.G (B) vs LYON (R)
  blue_win True gd15 1623
    blue Top Kiin Ambessa KDA 5 2 6
    blue Jungle Canyon Nocturne KDA 1 1 12
    blue Mid Chovy Lissandra KDA 2 3 10
    blue Bot Ruler Ashe KDA 7 2 7
    blue Support Duro Seraphine KDA 1 1 12
    red Top Dhokla Shen KDA 1 3 5
    red Jungle Inspired Vi KDA 1 5 6
    red Mid Saint Akali KDA 5 3 3
    red Bot Berserker Yunara KDA 2 3 3
    red Support Isles Lulu KDA 0 2 7
  picks [('blue', 'pick', 'Nocturne'), ('red', 'pick', 'Vi'), ('red', 'pick', 'Lulu'), ('blue', 'pick', 'Ashe'), ('blue', 'pick', 'Seraphine'), ('red', 'pick', 'Yunara'), ('red', 'pick', 'Akali'), ('blue', 'pick', 'Ambessa'), ('blue', 'pick', 'Lissandra'), ('red', 'pick', 'Shen')]
  bans [('blue', 'Jarvan IV'), ('red', 'Cassiopeia'), ('blue', 'Ezreal'), ('red', 'Syndra'), ('blue', 'Wukong'), ('red', 'Orianna'), ('red', 'Galio'), ('blue', 'Sylas'), ('red', 'Twisted Fate'), ('blue', 'Renekton')]
=== worlds-2026-main-event-round-3-4 n 3 patch 26.20 Gen.G (B) vs LYON (R)
  blue_win True gd15 -2221
    blue Top Kiin Camille KDA 3 1 9
    blue Jungle Canyon Jayce KDA 3 1 11
    blue Mid Chovy Galio KDA 4 2 4
    blue Bot Ruler Ezreal KDA 5 2 7
    blue Support Duro Nautilus KDA 0 1 9
    red Top Dhokla K'Sante KDA 1 3 3
    red Jungle Inspired Maokai KDA 0 3 5
    red Mid Saint Tristana KDA 4 2 0
    red Bot Berserker Lucian KDA 1 4 2
    red Support Isles Milio KDA 1 3 6
  picks [('blue', 'pick', 'Ezreal'), ('red', 'pick', 'Lucian'), ('red', 'pick', 'Milio'), ('blue', 'pick', 'Jayce'), ('blue', 'pick', 'Nautilus'), ('red', 'pick', "K'Sante"), ('red', 'pick', 'Maokai'), ('blue', 'pick', 'Camille'), ('blue', 'pick', 'Galio'), ('red', 'pick', 'Tristana')]
  bans [('blue', 'Wukong'), ('red', 'Cassiopeia'), ('blue', 'Jarvan IV'), ('red', 'Syndra'), ('blue', 'Sivir'), ('red', 'Lee Sin'), ('red', 'Gnar'), ('blue', 'Pantheon'), ('red', 'Gwen'), ('blue', 'Trundle')]
=== worlds-2026-main-event-round-3-7 n 1 patch 26.20 Team Secret Whales (B) vs LØS (R)
  blue_win False gd15 1421
    blue Top Pun Shen KDA 1 3 5
    blue Jungle Hizto Lee Sin KDA 0 3 3
    blue Mid Dire Akali KDA 5 4 1
    blue Bot Eddie Caitlyn KDA 1 3 4
    blue Support Bie Elise KDA 2 1 3
    red Top Zest Gnar KDA 3 1 6
    red Jungle Curse Wukong KDA 1 2 9
    red Mid Feisty Orianna KDA 4 2 6
    red Bot Duduhh Kalista KDA 6 2 5
    red Support Ackerman Renata Glasc KDA 0 2 12
  picks [('blue', 'pick', 'Lee Sin'), ('red', 'pick', 'Kalista'), ('red', 'pick', 'Renata Glasc'), ('blue', 'pick', 'Caitlyn'), ('blue', 'pick', 'Elise'), ('red', 'pick', 'Orianna'), ('red', 'pick', 'Wukong'), ('blue', 'pick', 'Akali'), ('blue', 'pick', 'Shen'), ('red', 'pick', 'Gnar')]
  bans [('blue', 'Syndra'), ('red', 'Cassiopeia'), ('blue', 'Nocturne'), ('red', 'Qiyana'), ('blue', 'Jayce'), ('red', 'Vi'), ('red', 'Locke'), ('blue', 'Rumble'), ('red', 'Ryze'), ('blue', 'Jarvan IV')]
=== worlds-2026-main-event-round-3-7 n 2 patch 26.20 Team Secret Whales (B) vs LØS (R)
  blue_win False gd15 -1500
    blue Top Pun Jax KDA 0 5 6
    blue Jungle Hizto Vi KDA 2 4 6
    blue Mid Dire Locke KDA 5 3 2
    blue Bot Eddie Miss Fortune KDA 6 4 5
    blue Support Bie Nautilus KDA 0 6 9
    red Top Zest Kennen KDA 9 2 5
    red Jungle Curse Trundle KDA 5 2 14
    red Mid Feisty Galio KDA 2 3 15
    red Bot Duduhh Ashe KDA 5 3 9
    red Support Ackerman Seraphine KDA 1 3 17
  picks [('blue', 'pick', 'Vi'), ('red', 'pick', 'Ashe'), ('red', 'pick', 'Seraphine'), ('blue', 'pick', 'Locke'), ('blue', 'pick', 'Nautilus'), ('red', 'pick', 'Galio'), ('red', 'pick', 'Trundle'), ('blue', 'pick', 'Miss Fortune'), ('blue', 'pick', 'Jax'), ('red', 'pick', 'Kennen')]
  bans [('blue', 'Syndra'), ('red', 'Cassiopeia'), ('blue', 'Nocturne'), ('red', 'Qiyana'), ('blue', 'Jayce'), ('red', 'Olaf'), ('red', 'Jhin'), ('blue', 'Jarvan IV'), ('red', 'Rumble'), ('blue', "K'Sante")]
=== worlds-2026-main-event-round-4-2 n 1 patch 26.20 LYON (B) vs Invictus Gaming (R)
  blue_win False gd15 -1628
    blue Top Dhokla Rumble KDA 2 3 1
    blue Jungle Inspired Nocturne KDA 1 6 1
    blue Mid Saint Sylas KDA 1 2 2
    blue Bot Berserker Ezreal KDA 0 3 3
    blue Support Isles Karma KDA 0 5 3
    red Top TheShy Ornn KDA 2 0 5
    red Jungle Wei Vi KDA 3 2 11
    red Mid Rookie Aurora KDA 8 1 8
    red Bot JiaQi Yunara KDA 6 1 6
    red Support Meiko Lulu KDA 0 0 16
  picks [('red', 'pick', 'Lulu'), ('blue', 'pick', 'Ezreal'), ('blue', 'pick', 'Nocturne'), ('red', 'pick', 'Vi'), ('red', 'pick', 'Yunara'), ('blue', 'pick', 'Karma'), ('blue', 'pick', 'Rumble'), ('red', 'pick', 'Ornn'), ('red', 'pick', 'Aurora'), ('blue', 'pick', 'Sylas')]
  bans [('red', 'Wukong'), ('blue', 'Syndra'), ('red', 'Galio'), ('blue', 'Cassiopeia'), ('red', 'Renata Glasc'), ('blue', 'Orianna'), ('blue', 'Ambessa'), ('red', 'Ahri'), ('blue', "K'Sante"), ('red', 'Annie')]
=== worlds-2026-main-event-round-4-2 n 2 patch 26.20 Invictus Gaming (B) vs LYON (R)
  blue_win False gd15 338
    blue Top TheShy Zaahen KDA 0 4 3
    blue Jungle Wei Lee Sin KDA 3 3 4
    blue Mid Rookie Annie KDA 2 4 4
    blue Bot JiaQi Jhin KDA 3 3 3
    blue Support Meiko Nautilus KDA 0 4 4
    red Top Dhokla Olaf KDA 4 2 3
    red Jungle Inspired Qiyana KDA 4 1 5
    red Mid Saint Taliyah KDA 4 1 7
    red Bot Berserker Corki KDA 6 0 2
    red Support Isles Alistar KDA 0 4 12
  picks [('red', 'pick', 'Qiyana'), ('blue', 'pick', 'Jhin'), ('blue', 'pick', 'Lee Sin'), ('red', 'pick', 'Alistar'), ('red', 'pick', 'Corki'), ('blue', 'pick', 'Nautilus'), ('blue', 'pick', 'Annie'), ('red', 'pick', 'Olaf'), ('red', 'pick', 'Taliyah'), ('blue', 'pick', 'Zaahen')]
  bans [('red', 'Syndra'), ('blue', 'Renata Glasc'), ('red', 'Orianna'), ('blue', 'Cassiopeia'), ('red', 'Jayce'), ('blue', 'Wukong'), ('blue', 'Ahri'), ('red', 'Ambessa'), ('blue', 'Viktor'), ('red', 'Twisted Fate')]
=== worlds-2026-main-event-round-4-2 n 3 patch 26.20 LYON (B) vs Invictus Gaming (R)
  blue_win False gd15 -4021
    blue Top Dhokla K'Sante KDA 1 2 0
    blue Jungle Inspired Xin Zhao KDA 2 2 3
    blue Mid Saint LeBlanc KDA 0 1 1
    blue Bot Berserker Lucian KDA 1 2 1
    blue Support Isles Milio KDA 1 0 2
    red Top TheShy Jayce KDA 2 0 2
    red Jungle Wei Trundle KDA 0 0 3
    red Mid Rookie Orianna KDA 0 2 4
    red Bot JiaQi Caitlyn KDA 5 1 2
    red Support Meiko Lux KDA 0 2 7
  picks [('red', 'pick', 'Orianna'), ('blue', 'pick', 'Lucian'), ('blue', 'pick', 'Milio'), ('red', 'pick', 'Caitlyn'), ('red', 'pick', 'Lux'), ('blue', 'pick', 'LeBlanc'), ('blue', 'pick', 'Xin Zhao'), ('red', 'pick', 'Trundle'), ('red', 'pick', 'Jayce'), ('blue', 'pick', "K'Sante")]
  bans [('red', 'Akali'), ('blue', 'Syndra'), ('red', 'Locke'), ('blue', 'Cassiopeia'), ('red', 'Ryze'), ('blue', 'Renata Glasc'), ('blue', 'Naafiri'), ('red', 'Jarvan IV'), ('blue', 'Skarner'), ('red', 'Wukong')]
=== worlds-2026-main-event-round-4-5 n 1 patch 26.20 LØS (B) vs Team Liquid (R)
  blue_win True gd15 1483
    blue Top Zest Jayce KDA 2 2 6
    blue Jungle Curse Trundle KDA 7 0 6
    blue Mid Feisty Syndra KDA 2 2 6
    blue Bot Duduhh Ashe KDA 4 2 3
    blue Support Ackerman Seraphine KDA 0 1 11
    red Top Morgan Ambessa KDA 1 3 2
    red Jungle Josedeodo Nocturne KDA 3 3 2
    red Mid Quid Sylas KDA 2 4 3
    red Bot Yeon Ziggs KDA 1 3 3
    red Support CoreJJ Nautilus KDA 0 2 5
  picks [('red', 'pick', 'Nocturne'), ('blue', 'pick', 'Ashe'), ('blue', 'pick', 'Seraphine'), ('red', 'pick', 'Ziggs'), ('red', 'pick', 'Nautilus'), ('blue', 'pick', 'Syndra'), ('blue', 'pick', 'Trundle'), ('red', 'pick', 'Sylas'), ('red', 'pick', 'Ambessa'), ('blue', 'pick', 'Jayce')]
  bans [('red', 'Cassiopeia'), ('blue', 'Qiyana'), ('red', 'Vi'), ('blue', 'Lee Sin'), ('red', 'Renata Glasc'), ('blue', 'Orianna'), ('blue', 'Olaf'), ('red', 'Wukong'), ('blue', 'Camille'), ('red', 'Renekton')]
=== worlds-2026-main-event-round-4-5 n 2 patch 26.20 LØS (B) vs Team Liquid (R)
  blue_win False gd15 -1870
    blue Top Zest Rumble KDA 0 1 5
    blue Jungle Curse Jarvan IV KDA 0 5 5
    blue Mid Feisty Galio KDA 1 3 5
    blue Bot Duduhh Ezreal KDA 5 3 2
    blue Support Ackerman Karma KDA 2 3 6
    red Top Morgan Ornn KDA 1 2 8
    red Jungle Josedeodo Xin Zhao KDA 5 1 10
    red Mid Quid Orianna KDA 4 0 6
    red Bot Yeon Lucian KDA 4 4 8
    red Support CoreJJ Nami KDA 1 1 14
  picks [('blue', 'pick', 'Ezreal'), ('red', 'pick', 'Lucian'), ('red', 'pick', 'Nami'), ('blue', 'pick', 'Karma'), ('blue', 'pick', 'Jarvan IV'), ('red', 'pick', 'Orianna'), ('red', 'pick', 'Xin Zhao'), ('blue', 'pick', 'Rumble'), ('blue', 'pick', 'Galio'), ('red', 'pick', 'Ornn')]
  bans [('blue', 'Lee Sin'), ('red', 'Vi'), ('blue', 'Renata Glasc'), ('red', 'Cassiopeia'), ('blue', 'Locke'), ('red', 'Qiyana'), ('red', 'Viktor'), ('blue', 'Wukong'), ('red', 'Akali'), ('blue', 'Jax')]
=== worlds-2026-main-event-round-4-5 n 3 patch 26.20 Team Liquid (B) vs LØS (R)
  blue_win False gd15 -4667
    blue Top Morgan Gnar KDA 0 4 1
    blue Jungle Josedeodo Sejuani KDA 1 3 5
    blue Mid Quid Viktor KDA 0 5 5
    blue Bot Yeon Yunara KDA 4 3 0
    blue Support CoreJJ Lulu KDA 0 2 4
    red Top Zest Tristana KDA 10 1 3
    red Jungle Curse Pantheon KDA 4 0 7
    red Mid Feisty Taliyah KDA 0 1 12
    red Bot Duduhh Kalista KDA 2 1 7
    red Support Ackerman Renata Glasc KDA 1 2 11
  picks [('blue', 'pick', 'Viktor'), ('red', 'pick', 'Kalista'), ('red', 'pick', 'Renata Glasc'), ('blue', 'pick', 'Yunara'), ('blue', 'pick', 'Lulu'), ('red', 'pick', 'Pantheon'), ('red', 'pick', 'Taliyah'), ('blue', 'pick', 'Sejuani'), ('blue', 'pick', 'Gnar'), ('red', 'pick', 'Tristana')]
  bans [('blue', 'Cassiopeia'), ('red', 'Lee Sin'), ('blue', 'Vi'), ('red', 'Qiyana'), ('blue', 'Locke'), ('red', 'Olaf'), ('red', 'Wukong'), ('blue', 'Akali'), ('red', 'Skarner'), ('blue', 'Vayne')]
=== worlds-2026-main-event-round-5-2 n 1 patch 26.20 LYON (B) vs LØS (R)
  blue_win False gd15 -1315
    blue Top Dhokla Rumble KDA 3 1 2
    blue Jungle Inspired Pantheon KDA 2 1 4
    blue Mid Saint Syndra KDA 1 3 1
    blue Bot Berserker Ezreal KDA 2 3 1
    blue Support Isles Alistar KDA 0 3 4
    red Top Zest Aurora KDA 1 1 2
    red Jungle Curse Vi KDA 3 2 4
    red Mid Feisty Cassiopeia KDA 2 3 5
    red Bot Duduhh Kai'Sa KDA 4 1 2
    red Support Ackerman Nautilus KDA 1 1 4
  picks [('blue', 'pick', 'Syndra'), ('red', 'pick', 'Cassiopeia'), ('red', 'pick', 'Vi'), ('blue', 'pick', 'Ezreal'), ('blue', 'pick', 'Pantheon'), ('red', 'pick', "Kai'Sa"), ('red', 'pick', 'Nautilus'), ('blue', 'pick', 'Alistar'), ('blue', 'pick', 'Rumble'), ('red', 'pick', 'Aurora')]
  bans [('blue', 'Renata Glasc'), ('red', 'Qiyana'), ('blue', 'Jarvan IV'), ('red', 'Nocturne'), ('blue', 'Trundle'), ('red', 'Olaf'), ('red', 'Karma'), ('blue', 'Ambessa'), ('red', 'Jayce'), ('blue', "K'Sante")]
```

### 9. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
h=d['history']
n=len(h)
bw=sum(1 for g in h if g.get('blue_win') is True)
bw_k=sum(1 for g in h if 'blue_win' in g)
gd=sum(1 for g in h if g.get('blue_gd15') is not None)
ahead=sum(1 for g in h if g.get('blue_gd15') is not None and g['blue_gd15']>0)
ahead_won=sum(1 for g in h if g.get('blue_gd15') is not None and g['blue_gd15']>0 and g['blue_win'] is True)
behind_won=sum(1 for g in h if g.get('blue_gd15') is not None and g['blue_gd15']<0 and g['blue_win'] is True)
print('games', n, 'blue_win known', bw_k, 'blue wins', bw, 'blue win rate', bw/bw_k)
print('gd15 known', gd, 'blue ahead@15', ahead, 'rate', ahead/gd)
print('ahead->win', ahead_won, 'of', ahead, '=', ahead_won/ahead if ahead else None)
print('behind->win', behind_won, 'of', sum(1 for g in h if g.get('blue_gd15') is not None and g['blue_gd15']<0))
"
```

### 10. 命令结果

```
games 79 blue_win known 79 blue wins 42 blue win rate 0.5316455696202531
gd15 known 79 blue ahead@15 37 rate 0.46835443037974683
ahead->win 25 of 37 = 0.6756756756756757
behind->win 17 of 42
```

### 11. 工具调用 · Write

```
{
  "file_path": "[ephemeral]/app/prediction.json",
  "content": "{\"p_blue_win\": 0.64, \"p_blue_ahead_15\": 0.66}\n"
}
```

### 12. 工具结果

```
File created successfully at: [ephemeral]/app/prediction.json (file state is current in your context — no need to Read it back)
```

### 13. 终端命令

```
python3 -c "
import json
p=json.load(open('prediction.json'))
assert set(p)=={'p_blue_win','p_blue_ahead_15'}
for k,v in p.items():
    assert isinstance(v,(int,float)) and 0<=v<=1
print('valid', p)
"
```

### 14. 命令结果

```
valid {'p_blue_win': 0.64, 'p_blue_ahead_15': 0.66}
```

### 15. 模型消息

````
Forecast submitted to `prediction.json`:

```json
{"p_blue_win": 0.64, "p_blue_ahead_15": 0.66}
```

**Reasoning from the evidence:**

- **Head-to-head / series state:** LØS beat LYON in game 1 (as red side), winning with a +1315 gold lead at 15:00. LØS is now up 1-0 and on blue side for game 2.
- **Team strength:** LØS is 5-3 overall with quality wins (2× Team Liquid, 2× TSW), losing only to elite teams (T1, G2). LYON is 4-5, with its wins coming against weaker opponents (TSW, KC, one game vs Gen.G/IG).
- **Early-game signal for `p_blue_ahead_15`:** LYON was behind at 15:00 in 8 of their 9 games (including 3 of 4 on red side) — their style consistently concedes early gold and wins from behind. LØS was ahead at 15 in half their games and ahead +1315 in the direct matchup. Combined with a modest blue-side discount (blue was ahead at 15 in only ~47% of the dataset), I set this at 0.66.
- **`p_blue_win`:** Baseline blue win rate is ~53%, raised for the stronger team, the 1-0 head-to-head, and series momentum, but tempered by Fearless removing some LØS comfort picks (Kai'Sa, Vi, Aurora, Nautilus) and LYON's own (Ezreal, Syndra, Alistar, Rumble) → 0.64.
````
